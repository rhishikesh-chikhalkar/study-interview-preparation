# Full FastAPI + LangChain customer support bot

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import Tool
from langchain_classic.agents import initialize_agent, AgentType
from langchain_classic.memory import ConversationBufferMemory
import jwt

# ─────────────────────────────────────────────
# 1. DATABASE SETUP
# ─────────────────────────────────────────────
engine = create_engine("postgresql://user:password@localhost/ecommerce")

def get_order_details(user_id: int) -> str:
    """Tool function — fetches live order data for a specific user."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT order_id, status, item, delivery_date FROM orders WHERE user_id = :uid"),
            {"uid": user_id}
        )
        rows = result.fetchall()
        if not rows:
            return "No orders found for this user."
        # Convert rows to readable string for the LLM
        return "\n".join(
            f"Order #{r.order_id}: {r.item} — Status: {r.status}, Delivery: {r.delivery_date}"
            for r in rows
        )

# ─────────────────────────────────────────────
# 2. VECTOR STORE SETUP (runs once at startup)
# ─────────────────────────────────────────────
def build_vectorstore() -> FAISS:
    """Load the PDF, chunk it, embed it, store it."""
    loader = PyPDFLoader("return_policy.pdf")
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # 500 chars per chunk
        chunk_overlap=50     # overlap so context isn't lost at boundaries
    )
    chunks = splitter.split_documents(pages)

    vectorstore = FAISS.from_documents(chunks, OpenAIEmbeddings())
    return vectorstore

vectorstore = build_vectorstore()  # loaded once, reused across requests

# ─────────────────────────────────────────────
# 3. AUTH — extract user_id from JWT token
# ─────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "your-secret-key"

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Decode JWT and return user_id. Never trust the user to tell you who they are."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return int(payload["user_id"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# ─────────────────────────────────────────────
# 4. BUILD AGENT (per request — memory is per session)
# ─────────────────────────────────────────────
def build_agent(user_id: int):
    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Tool 1 — Structured live data (SQL)
    # We close over user_id here so the agent can't be tricked into
    # fetching another user's orders
    order_tool = Tool(
        name="get_order_details",
        func=lambda _: get_order_details(user_id),  # user_id locked in
        description="Use this to answer questions about the user's orders, "
                    "delivery status, or order history. No input needed."
    )

    # Tool 2 — Unstructured static data (Vector search over PDF)
    def search_return_policy(query: str) -> str:
        docs = vectorstore.similarity_search(query, k=3)  # top 3 relevant chunks
        return "\n\n".join(d.page_content for d in docs)

    policy_tool = Tool(
        name="search_return_policy",
        func=search_return_policy,
        description="Use this to answer questions about return policies, "
                    "refunds, warranties, or exchange rules."
    )

    # Memory — remembers conversation history within this session
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    agent = initialize_agent(
        tools=[order_tool, policy_tool],
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        memory=memory,
        verbose=True  # logs which tool the agent picks — remove in prod
    )

    return agent

# ─────────────────────────────────────────────
# 5. FASTAPI ENDPOINT
# ─────────────────────────────────────────────
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id)  # auth resolves identity
):
    agent = build_agent(user_id)

    response = agent.invoke({
        "input": request.message
        # No need to inject user_id into the message —
        # the order_tool already has it locked in via closure
    })

    return {"reply": response["output"]}