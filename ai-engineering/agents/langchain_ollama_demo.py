from langchain_ollama import ChatOllama

chat = ChatOllama(model="qwen3:1.7b", temperature=0)

resp = chat.invoke([{"role": "user", "content": "Hello!"}])
print(resp.content)
