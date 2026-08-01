import { useState, useRef, useEffect } from "react";
import "./AiAssistant.css";

const API_BASE_URL = "http://localhost:5001";

const AiAssistant = () => {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I am your RAG-powered AI Assistant. Ask me questions about the indexed documents, and I'll generate responses based on that context.",
    },
  ]);
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    const userMessage = { role: "user", content: query.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");
    setIsLoading(true);
    setIsError(false);
    setErrorMessage("");

    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userMessage.content }),
      });

      if (!response.ok) {
        let errMsg = `Server returned status: ${response.status}`;
        try {
          const errData = await response.json();
          if (errData && errData.error) {
            errMsg = errData.error;
          }
        } catch {
          // Fallback if not JSON
        }
        throw new Error(errMsg);
      }

      const data = await response.json();
      
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.retrieved_chunks || [],
        },
      ]);
    } catch (err) {
      console.error(err);
      const isNetworkError = err.message.includes("fetch") || err.message.includes("Failed to fetch") || err.message.includes("NetworkError");
      const errorMsg = isNetworkError
        ? "Unable to connect to the Flask AI server. Please make sure the backend is running on port 5001."
        : `AI Backend Error: ${err.message}`;
      
      setIsError(true);
      setErrorMessage(errorMsg);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: isNetworkError
            ? "Sorry, I encountered a network error communicating with the AI backend. Please verify that the Flask server is running locally on port 5001."
            : `Sorry, the AI backend encountered an error: ${err.message}`,
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = async () => {
    try {
      await fetch(`${API_BASE_URL}/clear_history`, { method: "POST" });
    } catch (err) {
      console.error("Failed to clear server history:", err);
    }
    setMessages([
      {
        role: "assistant",
        content: "Conversation history cleared. How can I help you today?",
      },
    ]);
    setIsError(false);
    setErrorMessage("");
  };

  return (
    <div className="ai-container">
      <div className="ai-header">
        <div className="ai-header-title">
          <span className="ai-status-dot"></span>
          <h2>AI Assistant</h2>
        </div>
        <button onClick={handleClear} className="ai-clear-btn" title="Clear Conversation">
          Clear History
        </button>
      </div>

      <div className="ai-chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`ai-message-row ${msg.role}`}>
            <div className={`ai-message-bubble ${msg.isError ? "error" : ""}`}>
              <div className="ai-message-content">{msg.content}</div>
              
              {msg.sources && msg.sources.length > 0 && (
                <div className="ai-message-sources">
                  <div className="ai-sources-title">Retrieved Chunks:</div>
                  {msg.sources.map((src, sIdx) => (
                    <div key={sIdx} className="ai-source-item">
                      <span className="ai-source-badge">
                        {src.metadata.source} (Page {src.metadata.page})
                      </span>
                      <p className="ai-source-text">&quot;{src.text.slice(0, 150)}...&quot;</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="ai-message-row assistant">
            <div className="ai-message-bubble loading-container">
              <div className="ai-spinner"></div>
              <span>AI is thinking...</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {isError && (
        <div className="ai-error-banner">
          <span>{errorMessage}</span>
          <button className="ai-error-dismiss" onClick={() => setIsError(false)} title="Dismiss Error">✕</button>
        </div>
      )}

      <form onSubmit={handleSend} className="ai-input-form">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about the indexed PDF..."
          className="ai-input-field"
          disabled={isLoading}
        />
        <button type="submit" className="ai-send-btn" disabled={isLoading || !query.trim()}>
          {isLoading ? (
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <div className="ai-spinner-small"></div>
              <span>Thinking...</span>
            </div>
          ) : (
            "Send"
          )}
        </button>
      </form>
    </div>
  );
};

export default AiAssistant;
