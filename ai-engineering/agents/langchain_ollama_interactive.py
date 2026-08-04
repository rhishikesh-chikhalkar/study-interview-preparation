from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from llm_factory import get_configured_llm


def main():
    print("Initializing LLM model using model factory...")
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
    config = {"configurable": {"session_id": "terminal_chat_session"}}

    print("\n==================================================")
    print("Interactive Chatbot Started!")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("==================================================\n")

    while True:
        try:
            # Capture user input
            user_input = input("You: ")

            # Check for exit commands
            if user_input.strip().lower() in ["exit", "quit"]:
                print("Bot: Goodbye!")
                break

            # Skip empty inputs
            if not user_input.strip():
                continue

            # Invoke the model with message history
            response = with_message_history.invoke({"input": user_input}, config=config)

            # Print response
            print(f"Bot: {response.content}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Goodbye!")
            break


if __name__ == "__main__":
    main()
