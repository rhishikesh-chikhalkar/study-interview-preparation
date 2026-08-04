# Original implementation (without memory):
# from langchain_ollama import ChatOllama
# llm = ChatOllama(model="qwen3:1.7b", temperature=0)
# resp = llm.invoke([{"role": "user", "content": "Hello!"}])
# print(resp.content)

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from llm_factory import get_configured_llm

# Initialize the model using the centralized factory
llm = get_configured_llm()

# Setup a prompt that has a placeholder for chat history
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# Chain the prompt with the chat model
chain = prompt | llm

# Memory store to keep chat history per session_id
store = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


# Wrap the chain with RunnableWithMessageHistory
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Configure the session ID
config = {"configurable": {"session_id": "day_2_session"}}

# Turn 1: Introducing user name
print("--- Turn 1 ---")
input_1 = "Hello! My name is Rhishikesh."
print(f"User: {input_1}")
resp_1 = with_message_history.invoke({"input": input_1}, config=config)
print(f"Bot: {resp_1.content}\n")

# Turn 2: Querying memory of the user name
print("--- Turn 2 ---")
input_2 = "What is my name?"
print(f"User: {input_2}")
resp_2 = with_message_history.invoke({"input": input_2}, config=config)
print(f"Bot: {resp_2.content}\n")
