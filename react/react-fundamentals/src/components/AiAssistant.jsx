import { useState, useRef, useEffect } from "react";

const API_BASE_URL = (
  import.meta.env.VITE_API_URL ||
  "https://flask-rag-api-191y.onrender.com"
).replace(/\/$/, "");

const SAMPLE_PROMPTS = [
  "What documents are indexed in the RAG system?",
  "Explain how retrieval augmented generation works.",
  "How are React and Flask connected securely?",
];

const AiAssistant = () => {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I am your RAG-powered AI Assistant." +
        " Ask me questions about the indexed documents.",
    },
  ]);
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [openSources, setOpenSources] = useState({});
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const sendQuery = async (userText) => {
    if (!userText.trim() || isLoading) return;

    const userMessage = { role: "user", content: userText.trim() };
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
          // Fallback if response is not JSON
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
      const isNetwork =
        err.message.includes("fetch") ||
        err.message.includes("Failed to fetch") ||
        err.message.includes("NetworkError");
      const errorMsg = isNetwork
        ? "Unable to connect to the Flask AI server."
        : `AI Backend Error: ${err.message}`;

      setIsError(true);
      setErrorMessage(errorMsg);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: isNetwork
            ? "Network error communicating with AI backend. Verify server."
            : `AI backend error: ${err.message}`,
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    await sendQuery(query);
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
    setOpenSources({});
  };

  const toggleSources = (idx) => {
    setOpenSources((prev) => ({
      ...prev,
      [idx]: !prev[idx],
    }));
  };

  const containerClasses = [
    "max-w-3xl",
    "w-[94%]",
    "my-8",
    "mx-auto",
    "bg-slate-900/80",
    "border",
    "border-slate-800",
    "rounded-2xl",
    "shadow-2xl",
    "backdrop-blur-xl",
    "flex",
    "flex-col",
    "h-[650px]",
    "overflow-hidden",
    "text-left",
  ].join(" ");

  const headerClasses = [
    "px-6",
    "py-4",
    "bg-slate-900/90",
    "border-b",
    "border-slate-800",
    "flex",
    "justify-between",
    "items-center",
    "backdrop-blur-md",
    "sticky",
    "top-0",
    "z-10",
  ].join(" ");

  const badgeClasses = [
    "flex",
    "items-center",
    "gap-1.5",
    "px-3",
    "py-1",
    "bg-gradient-to-r",
    "from-indigo-500/10",
    "via-purple-500/10",
    "to-pink-500/10",
    "border",
    "border-indigo-500/30",
    "rounded-full",
    "text-indigo-300",
    "text-xs",
    "font-semibold",
    "shadow-sm",
  ].join(" ");

  const clearBtnClasses = [
    "px-3",
    "py-1.5",
    "text-xs",
    "font-semibold",
    "text-rose-400",
    "hover:text-rose-300",
    "border",
    "border-rose-500/30",
    "hover:border-rose-500/60",
    "bg-rose-500/10",
    "hover:bg-rose-500/20",
    "rounded-lg",
    "transition-all",
    "cursor-pointer",
    "flex",
    "items-center",
    "gap-1.5",
  ].join(" ");

  const userBubbleStyle = [
    "bg-gradient-to-r",
    "from-indigo-600",
    "to-violet-600",
    "text-white",
    "rounded-br-xs",
    "shadow-md",
    "shadow-indigo-500/10",
  ].join(" ");

  const assistantBubbleStyle = [
    "bg-slate-800/90",
    "text-slate-100",
    "border",
    "border-slate-700/50",
    "rounded-bl-xs",
    "shadow-sm",
  ].join(" ");

  const inputClasses = [
    "flex-1",
    "px-4",
    "py-3",
    "bg-slate-950/90",
    "border",
    "border-slate-800",
    "rounded-xl",
    "text-slate-100",
    "placeholder-slate-500",
    "text-sm",
    "focus:outline-none",
    "focus:ring-2",
    "focus:ring-indigo-500/50",
    "focus:border-indigo-500",
    "transition-all",
    "disabled:opacity-50",
  ].join(" ");

  const submitBtnClasses = [
    "px-5",
    "py-3",
    "bg-indigo-600",
    "hover:bg-indigo-500",
    "disabled:opacity-40",
    "disabled:cursor-not-allowed",
    "text-white",
    "font-semibold",
    "text-sm",
    "rounded-xl",
    "flex",
    "items-center",
    "justify-center",
    "transition-all",
    "shadow-md",
    "shadow-indigo-600/20",
    "cursor-pointer",
    "gap-2",
  ].join(" ");

  return (
    <div className={containerClasses}>
      {/* Top Header */}
      <div className={headerClasses}>
        <div className="flex items-center gap-3">
          <div
            className={
              "flex items-center justify-center w-9 h-9 rounded-xl " +
              "bg-indigo-600/20 border border-indigo-500/30 text-indigo-400"
            }
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d={
                  "M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2" +
                  "V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                }
              />
            </svg>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-bold text-slate-100 m-0">
                Portfolio AI Assistant
              </h2>
              <span className="relative flex h-2 w-2">
                <span
                  className={
                    "animate-ping absolute inline-flex h-full w-full " +
                    "rounded-full bg-emerald-400 opacity-75"
                  }
                ></span>
                <span
                  className={
                    "relative inline-flex rounded-full h-2 w-2 " +
                    "bg-emerald-500"
                  }
                ></span>
              </span>
            </div>
            <p className="text-xs text-slate-400 m-0">
              Retrieval-Augmented Generation Engine
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Powered by AI Badge */}
          <div className={badgeClasses}>
            <svg
              className="w-3.5 h-3.5 text-indigo-400 animate-pulse"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                d={
                  "M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 " +
                  "0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 " +
                  "1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 " +
                  "1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838" +
                  "-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 " +
                  "8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69" +
                  "l1.07-3.292z"
                }
              />
            </svg>
            <span>Powered by AI</span>
          </div>

          <button
            onClick={handleClear}
            className={clearBtnClasses}
            title="Clear Conversation"
          >
            <svg
              className="w-3.5 h-3.5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d={
                  "M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995" +
                  "-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 " +
                  "0 00-1 1v3M4 7h16"
                }
              />
            </svg>
            <span>Clear</span>
          </button>
        </div>
      </div>

      {/* Chat Feed */}
      <div className="flex-1 p-6 overflow-y-auto flex flex-col gap-4 bg-slate-950/50 chat-scroll">
        {messages.map((msg, idx) => {
          const isUser = msg.role === "user";
          const hasSources = msg.sources && msg.sources.length > 0;
          const isSourceOpen = !!openSources[idx];

          const bubbleStyle = msg.isError
            ? "bg-rose-950/40 border border-rose-500/30 text-rose-200"
            : isUser
            ? userBubbleStyle
            : assistantBubbleStyle;

          return (
            <div
              key={idx}
              className={
                "flex w-full animate-message-appear " +
                (isUser ? "justify-end" : "justify-start")
              }
            >
              <div
                className={
                  "max-w-[82%] px-4 py-3 rounded-2xl text-sm leading-relaxed " +
                  bubbleStyle
                }
              >
                <div>{msg.content}</div>

                {/* Collapsible Retrieved Sources */}
                {hasSources && (
                  <div className="mt-3 pt-3 border-t border-slate-700/40 text-xs">
                    <button
                      onClick={() => toggleSources(idx)}
                      className={
                        "flex items-center gap-1.5 font-semibold text-indigo-400 " +
                        "hover:text-indigo-300 transition-colors cursor-pointer"
                      }
                    >
                      <svg
                        className={
                          "w-3.5 h-3.5 transform transition-transform " +
                          (isSourceOpen ? "rotate-90" : "")
                        }
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="2"
                          d="M9 5l7 7-7 7"
                        />
                      </svg>
                      <span>
                        {isSourceOpen ? "Hide" : "View"} Context Chunks (
                        {msg.sources.length})
                      </span>
                    </button>

                    {isSourceOpen && (
                      <div className="mt-2 flex flex-col gap-2">
                        {msg.sources.map((src, sIdx) => (
                          <div
                            key={sIdx}
                            className={
                              "bg-slate-900/90 p-2.5 rounded-lg border " +
                              "border-slate-800 text-left"
                            }
                          >
                            <span
                              className={
                                "inline-block font-medium text-sky-400 " +
                                "text-[11px] mb-1 bg-sky-950/50 px-2 py-0.5 " +
                                "rounded border border-sky-800/40"
                              }
                            >
                              {src.metadata?.source || "Doc"} (Page{" "}
                              {src.metadata?.page || 1})
                            </span>
                            <p className="m-0 text-slate-400 italic leading-snug">
                              &quot;
                              {src.text ? src.text.slice(0, 140) : ""}
                              ...&quot;
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Quick Sample Prompts */}
        {messages.length <= 1 && (
          <div className="my-2 p-4 bg-slate-900/40 border border-slate-800/60 rounded-xl text-left">
            <p className="text-xs font-semibold text-slate-400 mb-2">
              Suggested Questions:
            </p>
            <div className="flex flex-wrap gap-2">
              {SAMPLE_PROMPTS.map((promptText, pIdx) => (
                <button
                  key={pIdx}
                  onClick={() => sendQuery(promptText)}
                  className={
                    "px-3 py-1.5 bg-slate-800/80 hover:bg-indigo-600/30 " +
                    "border border-slate-700/60 hover:border-indigo-500/50 " +
                    "text-slate-300 hover:text-indigo-200 text-xs rounded-lg " +
                    "transition-all cursor-pointer text-left"
                  }
                >
                  {promptText}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Loading State Indicator */}
        {isLoading && (
          <div className="flex w-full justify-start animate-message-appear">
            <div
              className={
                "flex items-center gap-3 px-4 py-3 bg-slate-800/90 text-slate-300 " +
                "border border-slate-700/50 rounded-2xl rounded-bl-xs shadow-sm text-sm"
              }
            >
              <div
                className={
                  "animate-spin h-4 w-4 border-2 border-indigo-400 " +
                  "border-t-transparent rounded-full"
                }
              ></div>
              <span>AI is searching vectors &amp; generating response...</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Error Banner */}
      {isError && (
        <div
          className={
            "bg-rose-950/50 border-t border-rose-800/50 text-rose-300 " +
            "px-6 py-3 text-xs flex justify-between items-center gap-4"
          }
        >
          <span>{errorMessage}</span>
          <button
            className={
              "text-rose-300 hover:text-white transition-colors cursor-pointer " +
              "text-sm font-bold px-1"
            }
            onClick={() => setIsError(false)}
            title="Dismiss Error"
          >
            ✕
          </button>
        </div>
      )}

      {/* Bottom Input Form */}
      <form
        onSubmit={handleSend}
        className="p-4 bg-slate-900/90 border-t border-slate-800 flex gap-3 backdrop-blur-md"
      >
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about indexed documents..."
          className={inputClasses}
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className={submitBtnClasses}
        >
          {isLoading ? (
            <div className="flex items-center gap-2">
              <div
                className={
                  "animate-spin h-4 w-4 border-2 border-white " +
                  "border-t-transparent rounded-full"
                }
              ></div>
              <span>Thinking...</span>
            </div>
          ) : (
            <>
              <span>Send</span>
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default AiAssistant;
