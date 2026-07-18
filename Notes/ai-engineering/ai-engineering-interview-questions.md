# AI Engineering Interview Questions (5 YOE Level)

This document contains typical technical interview questions, deep conceptual breakdowns, and production considerations for AI engineering concepts based on local model execution and orchestration.

---

## 1. invoke() vs stream() in Web Applications

### Question
Why should we prefer using `stream()` over `invoke()` when building user-facing LLM applications in production, and how do they differ under the hood?

### Answer
- **Latency Mitigation**: `invoke()` blocks the entire backend thread/connection until the model has generated the final token, creating a high Time-to-First-Token (TTFT) experience for the user. `stream()` utilizes HTTP Server-Sent Events (SSE) or WebSockets to return chunks of text as they are computed, drastically improving the perceived latency.
- **Under the Hood**:
  - `invoke()` aggregates all tokens in the model’s internal output loop, formats them into a final response envelope, and returns it.
  - `stream()` exposes a generator object. In LangChain, this hooks into the underlying inference engine's event/streaming callbacks (e.g., Ollama's stream parameter or OpenAI's stream chunks), yielding token-by-token tokens formatted as `AIMessageChunk`.

---

## 2. Temperature Math & Determinism

### Question
What mathematical transformation occurs when you configure `temperature = 0` in an LLM, and is the output guaranteed to be 100% deterministic?

### Answer
- **The Math**: An LLM outputs log-probabilities (logits) for each token in its vocabulary. To generate a probability distribution, the Softmax function is applied:
  
  Probability(x_i) = exp(z_i / T) / Sum(exp(z_j / T))
  
  where `T` is the temperature. As `T` approaches `0` (or at exactly `0`), the distribution collapses into a delta function focusing all probability on the single token with the highest logit score. This is called **Greedy Decoding** or **Argmax Selection**.
- **Determinism**: No, it is not 100% deterministic on GPUs. Due to the parallel execution of matrix operations on high-performance accelerators, floating-point calculations (especially atomic additions) are non-associative. The order of execution can vary slightly depending on thread scheduling, leading to minute differences (e.g., 10^-7). At critical transition words, these tiny differences can cause the model to select an alternate token, leading to an entirely different path of text generation.

---

## 3. Local Hardware Sizing for LLM Inference

### Question
How do you estimate the memory (VRAM/RAM) requirements for serving a quantized local model (e.g., Qwen 1.7B vs Llama 8B) in production?

### Answer
- **Estimation Formula**:
  
  Memory (GB) ≈ (Parameters (in Billions) * Bits per weight / 8) * 1.2 (for overhead)
  
- **Examples**:
  - **Qwen 1.7B (4-bit quantized)**:
    `Memory = (1.7 * 4 / 8) * 1.2 ≈ 1.02 GB`. With runtime buffers and a small context window, this requires about 1.5–2 GB of RAM/VRAM.
  - **Llama 8B (4-bit quantized)**:
    `Memory = (8 * 4 / 8) * 1.2 ≈ 4.8 GB`. With runtime buffers, this requires at least 6–8 GB of dedicated VRAM.
- **Overhead Factors**: The `1.2` factor accounts for memory occupied by the KV-Cache (key-value states of prior tokens in the conversation context window), context processing buffers, and general execution framework footprints.

---

## 4. Scaling Concurrent Queries & Batching

### Question
If you have to process 1,000 queries using a local LLM runner, how would you optimize the script execution to prevent performance bottlenecks?

### Answer
- **Avoid Sequential Loops**: Running a standard loop with synchronous `invoke()` processes one query at a time, resulting in very low throughput.
- **Use Async Batching**: Use LangChain's `.abatch()` interface to trigger concurrent requests:
  
  ```python
  inputs = [{"role": "user", "content": q} for q in queries]
  responses = await chat.abatch(inputs, config={"max_concurrency": 20})
  ```
- **Engine Optimization**: Utilizing `abatch` allows modern inference engines (like vLLM or Ollama) to use **Continuous Batching** and **PagedAttention**. This groups active requests together, processing them in a single forward pass on the GPU, maximizing throughput and hardware utilization.

---

## 5. Production Resiliency & Failovers

### Question
How do you handle transient local inference service failures (like Ollama crashes) in a production AI pipeline without degrading the user experience?

### Answer
- **LangChain Fallbacks**: Implement the `.with_fallbacks()` mechanism to automatically route traffic to a secondary model (e.g., hosted cloud API) if the primary local engine fails.
  
  ```python
  from langchain_ollama import ChatOllama
  from langchain_openai import ChatOpenAI

  primary = ChatOllama(model="qwen3:1.7b")
  fallback = ChatOpenAI(model="gpt-3.5-turbo")

  resilient_chain = primary.with_fallbacks([fallback])
  ```
- **Retries with Jitter**: Configure retry wrappers with exponential backoff and jitter to absorb temporary connection timeouts or startup latency from the local runner.

---

## 6. Meaning of 'role' and 'content' in invoke() Message Payloads

### Question
When calling `chat.invoke([{"role": "user", "content": "Hello!"}])`, what do the `role` and `content` keys represent under the hood, and what are the standard roles available in LLM chat APIs?

### Answer
In modern chat model APIs (such as OpenAI, Anthropic, or Ollama/LangChain), conversation history is structured as a list of messages. Each message is an object containing `role` and `content` keys:

- **`role`**: Defines the source/persona of the message. This dictates how the inference engine packages the prompt structure into the model's specific chat template format (e.g., ChatML, Llama-style templates). The standard roles are:
  - **`system`**: Sets the behavior, tone, instructions, and guardrails for the assistant (e.g., `"You are a helpful assistant"`). Typically placed at the very beginning of the context.
  - **`user`** (or `human`): Represents input sent directly by the human interacting with the model.
  - **`assistant`** (or `ai`): Represents responses generated by the LLM. Keeping track of assistant messages is necessary for multi-turn conversations/memory.
  - **`tool`** (or `function`): Contains the execution output of external tools/functions that the model decided to call.
- **`content`**: The actual payload of the message. While historically restricted to string text (e.g., `"Hello!"`), modern models support multimodal content arrays (e.g., lists containing text, image URLs, or document blobs).

---

## 7. Stateful Conversations & Memory Management in LangChain

### Question
How do you implement stateful conversations (memory) with an LLM in LangChain? Explain the roles of `RunnableWithMessageHistory`, `MessagesPlaceholder`, and session history stores.

### Answer
- **`MessagesPlaceholder`**: Acts as a dynamic injection point in the prompt template (e.g., `MessagesPlaceholder(variable_name="history")`). During execution, LangChain dynamically replaces this placeholder with a sequence of past chat messages fetched from the history store.
- **Session History Store**: A mapping (usually a dictionary or database index) that maps a unique `session_id` to its corresponding message history (e.g., `InMemoryChatMessageHistory` or persistent databases like Redis/PostgreSQL). This allows a single application instance to manage separate conversational sessions for different users concurrently.
- **`RunnableWithMessageHistory`**: A wrapper that intercepts incoming requests to the chain/model, retrieves the correct chat history using a session helper (e.g., `get_session_history(session_id)`), injects it into the prompt (replacing the placeholder), sends the complete context to the model, and then automatically appends both the user's prompt and the model's response back to the session history.
- **Deprecation Note**: In modern LangChain applications, `RunnableWithMessageHistory` is deprecated in favor of **LangGraph's** built-in persistence layers, which provide more robust state saving, checkpointing, and human-in-the-loop support.

---

## 8. Deep Dive: MessagesPlaceholder in ChatPromptTemplates

### Question
What is `MessagesPlaceholder` in LangChain, why is it used instead of basic string formatting, and how does it render messages under the hood?

### Answer
- **The Concept**: Unlike simple text templates where inputs are formatted as strings (e.g., `{input}`), chat models require a list of structured message objects (e.g., `SystemMessage`, `HumanMessage`, `AIMessage`). `MessagesPlaceholder` is a placeholder element within a `ChatPromptTemplate` that reserves a spot for a dynamic list of these message objects.
- **Why String Formatting Fails**: If you try to format a list of chat history messages into a normal string placeholder like `{history}`, Python/LangChain will serialize the list as a raw string representation (e.g., `"[HumanMessage(content='hi'), AIMessage(content='hello')]"`), which ruins the chat template structure. `MessagesPlaceholder` directly inserts/unpacks the actual message objects into the prompt list at runtime.
- **Under the Hood Rendering**:
  - **Template Definition**:
    ```python
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    ```
  - **Runtime Execution**: When invoking the chain with `{"input": "What is my name?", "history": [HumanMessage(content="My name is Rhishi."), AIMessage(content="Nice to meet you, Rhishi!")]}`, LangChain renders the final list of messages by unpacking the `history` list directly into the middle:
    1. `SystemMessage(content="You are a helpful assistant.")`
    2. `HumanMessage(content="My name is Rhishi.")` *(Unpacked from placeholder)*
    3. `AIMessage(content="Nice to meet you, Rhishi!")` *(Unpacked from placeholder)*
    4. `HumanMessage(content="What is my name?")`

---

## 9. Implementation Mechanics of `RunnableWithMessageHistory`

### Question
Walk through the implementation mechanics of memory in your local interactive chatbot script. How do `InMemoryChatMessageHistory`, the session history callback, `RunnableWithMessageHistory` configuration keys, and the invocation config tie together?

### Answer
To implement multi-turn conversations, the code coordinates four key components:

1. **The In-Memory Store (`store = {}`)**:
   A simple dictionary acting as a database. Keys are session IDs (strings) and values are `InMemoryChatMessageHistory` objects containing lists of messages. In production, this would be backed by Redis or PostgreSQL.

2. **The Session Callback (`get_session_history`)**:
   ```python
   def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
       if session_id not in store:
           store[session_id] = InMemoryChatMessageHistory()
       return store[session_id]
   ```
   A function passed to the message history wrapper. It ensures that whenever a query comes in with a specific `session_id`, the correct chat history is either retrieved or initialized.

3. **The Wrapper Configuration (`RunnableWithMessageHistory`)**:
   ```python
   with_message_history = RunnableWithMessageHistory(
       chain,
       get_session_history,
       input_messages_key="input",
       history_messages_key="history",
   )
   ```
   - **`chain`**: The underlying runnable pipeline (`prompt | llm`).
   - **`get_session_history`**: The callback function to call.
   - **`input_messages_key="input"`**: Tells LangChain which key in the input dictionary (e.g. `{"input": user_input}`) represents the new human message.
   - **`history_messages_key="history"`**: Map this key to the prompt template's `MessagesPlaceholder(variable_name="history")` so LangChain knows where to inject the retrieved history.

4. **Dynamic Session Execution (`config`)**:
   ```python
   config = {"configurable": {"session_id": "terminal_chat_session"}}
   response = with_message_history.invoke({"input": user_input}, config=config)
   ```
   When `invoke` is executed, LangChain looks at `config["configurable"]` to find the `session_id`. It passes this ID to `get_session_history()`, retrieves the list of messages, inserts it into the prompt, invokes the model, and then automatically saves both the new input message and the resulting AI response back to the history store.

---

## 10. Text Embeddings in Semantic Search & RAG

### Question
What are text embeddings, how do they capture semantic meaning, and how are they utilized within a Retrieval-Augmented Generation (RAG) pipeline?

### Answer
- **Definition & Representation**: A text embedding is a vector representation (a list of floating-point numbers) of a text segment (word, sentence, or chunk) generated by an embedding model (e.g., `nomic-embed-text` or `text-embedding-3-small`).
- **Capturing Semantic Meaning**: The model projects the text into a high-dimensional vector space. Through training on large datasets, the model learns to place semantically similar or contextually related text blocks closer together in this geometric space, measuring relationship strength via distance metrics (like Cosine Similarity or Dot Product).
- **RAG Execution Role**:
  1. **Ingestion**: Document pages are split into chunks. Each chunk is passed through the embedding model to generate a vector, which is indexed in a vector store.
  2. **Retrieval**: The incoming user query is embedded using the *same* model. A vector database computes similarity scores against the stored document embeddings to fetch the top `k` most similar chunks.
  3. **Generation**: The retrieved text chunks are injected into the prompt context for the LLM to generate an accurate, grounded response.

---

## 11. FAISS (Facebook AI Similarity Search) & Vector Indices

### Question
What is FAISS, and why do we prefer it over traditional relational or document databases when searching through high-dimensional embeddings?

### Answer
- **What is FAISS**: FAISS is a library developed by Meta's Fundamental AI Research (FAIR) team, optimized for fast similarity search and clustering of dense vectors. It is implemented in C++ with optional GPU support and wrapped in Python.
- **Why Traditional Databases Fail**: Traditional databases are designed to index scalar values (numbers, strings) using structures like B-Trees or Hash tables. They do not support high-dimensional distance math (like L2 Euclidean Distance or Inner Product) at scale. Performing a brute-force scan over millions of 768-dimension vectors for every user query would cause massive CPU bottlenecks and scale poorly.
- **FAISS Capabilities & Optimizations**:
  - **In-Memory & Lightweight**: It can run entirely in-memory local to the application, eliminating database roundtrip latencies for smaller apps.
  - **Approximate Nearest Neighbor (ANN) Search**: FAISS achieves sub-millisecond search times by clustering vectors (e.g., via IndexIVFFlat) or building graph-based indices (e.g., HNSW). Instead of scanning every vector, it narrows down the search space to the most promising cluster/neighborhood.
