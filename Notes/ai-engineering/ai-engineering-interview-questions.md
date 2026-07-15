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
