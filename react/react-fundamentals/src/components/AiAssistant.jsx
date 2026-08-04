import { useState, useRef, useEffect } from "react";

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
    <div className="max-w-3xl w-[92%] my-8 mx-auto bg-slate-900/60 border border-slate-800 rounded-2xl shadow-2xl backdrop-blur-xl flex flex-col h-[600px] overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 bg-slate-900/80 border-b border-slate-800/80 flex justify-between items-center backdrop-blur-md sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          <h2 className="text-lg font-bold text-slate-100 m-0">AI Assistant</h2>
        </div>
        <button
          onClick={handleClear}
          className="px-3 py-1.5 text-xs font-semibold text-rose-400 hover:text-rose-300 border border-rose-500/30 hover:border-rose-500/60 bg-rose-500/10 hover:bg-rose-500/20 rounded-lg transition-all cursor-pointer"
          title="Clear Conversation"
        >
          Clear History
        </button>
      </div>

      {/* Chat Messages Feed */}
      <div className="flex-1 p-6 overflow-y-auto flex flex-col gap-4 bg-slate-950/40">
        {messages.map((msg, idx) => {
          const isUser = msg.role === "user";
          return (
            <div
              key={idx}
              className={`flex w-full ${isUser ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                  msg.isError
                    ? "bg-rose-950/40 border border-rose-500/30 text-rose-200"
                    : isUser
                    ? "bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-br-xs shadow-md shadow-indigo-500/10"
                    : "bg-slate-800/90 text-slate-100 border border-slate-700/50 rounded-bl-xs shadow-sm"
                }`}
              >
                <div>{msg.content}</div>

                {/* Retrieved Sources Section */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-slate-700/40 text-xs">
                    <div className="font-semibold text-indigo-400 mb-2">Retrieved Chunks:</div>
                    {msg.sources.map((src, sIdx) => (
                      <div key={sIdx} className="bg-slate-900/80 p-2.5 rounded-lg mb-2 border border-slate-800">
                        <span className="inline-block font-medium text-sky-400 text-[11px] mb-1 bg-sky-950/50 px-2 py-0.5 rounded border border-sky-800/40">
                          {src.metadata.source} (Page {src.metadata.page})
                        </span>
                        <p className="m-0 text-slate-400 italic leading-snug">
                          &quot;{src.text.slice(0, 150)}...&quot;
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex w-full justify-start">
            <div className="flex items-center gap-3 px-4 py-3 bg-slate-800/90 text-slate-300 border border-slate-700/50 rounded-2xl rounded-bl-xs shadow-sm text-sm">
              <div className="animate-spin h-4 w-4 border-2 border-indigo-400 border-t-transparent rounded-full"></div>
              <span>AI is thinking...</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Error Banner */}
      {isError && (
        <div className="bg-rose-950/50 border-t border-rose-800/50 text-rose-300 px-6 py-3 text-xs flex justify-between items-center gap-4">
          <span>{errorMessage}</span>
          <button
            className="text-rose-300 hover:text-white transition-colors cursor-pointer text-sm font-bold px-1"
            onClick={() => setIsError(false)}
            title="Dismiss Error"
          >
            ✕
          </button>
        </div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSend} className="p-4 bg-slate-900/80 border-t border-slate-800/80 flex gap-3 backdrop-blur-md">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about the indexed PDF..."
          className="flex-1 px-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all disabled:opacity-50"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="px-5 py-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold text-sm rounded-xl flex items-center justify-center transition-all shadow-md shadow-indigo-600/20 cursor-pointer"
        >
          {isLoading ? (
            <div className="flex items-center gap-2">
              <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
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

