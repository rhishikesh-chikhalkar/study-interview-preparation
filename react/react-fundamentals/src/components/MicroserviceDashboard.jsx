import { useState, useEffect, useCallback } from "react";

const API_BASE_URL = (
  import.meta.env.VITE_API_URL ||
  "https://flask-rag-api-191y.onrender.com"
).replace(/\/$/, "");

const MicroserviceDashboard = () => {
  const [flaskStatus, setFlaskStatus] = useState("checking");
  const [goStatus, setGoStatus] = useState("checking");
  const [goUrl, setGoUrl] = useState("");
  const [inputText, setInputText] = useState(
    "React SPA calling Flask Gateway which delegates to Go microservice."
  );
  const [analysisResult, setAnalysisResult] = useState(null);
  const [latency, setLatency] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [newTaskTitle, setNewTaskTitle] = useState("");

  const performHealthCheck = useCallback(async () => {
    setFlaskStatus("checking");
    setGoStatus("checking");
    setError(null);

    try {
      const flaskRes = await fetch(`${API_BASE_URL}/health`);
      setFlaskStatus(flaskRes.ok ? "online" : "degraded");

      const goRes = await fetch(`${API_BASE_URL}/go-health`);
      if (goRes.ok) {
        const goData = await goRes.json();
        setGoStatus(goData.status === "healthy" ? "online" : "degraded");
        setGoUrl(goData.go_service_url || "");
      } else {
        setGoStatus("offline");
      }
    } catch (err) {
      setFlaskStatus("offline");
      setGoStatus("offline");
      setError(`Network error connecting to Flask Gateway: ${err.message}`);
    }
  }, []);

  // Run initial health check on mount
  useEffect(() => {
    let ignore = false;

    const initHealth = async () => {
      try {
        const flaskRes = await fetch(`${API_BASE_URL}/health`);
        if (!ignore) {
          setFlaskStatus(flaskRes.ok ? "online" : "degraded");
        }

        const goRes = await fetch(`${API_BASE_URL}/go-health`);
        if (!ignore) {
          if (goRes.ok) {
            const goData = await goRes.json();
            setGoStatus(goData.status === "healthy" ? "online" : "degraded");
            setGoUrl(goData.go_service_url || "");
          } else {
            setGoStatus("offline");
          }
        }
      } catch (err) {
        if (!ignore) {
          setFlaskStatus("offline");
          setGoStatus("offline");
          setError(`Network error connecting to Flask Gateway: ${err.message}`);
        }
      }
    };

    initHealth();

    return () => {
      ignore = true;
    };
  }, []);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);

    const startTime = performance.now();

    try {
      const res = await fetch(`${API_BASE_URL}/go-analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText }),
      });

      const endTime = performance.now();
      setLatency(Math.round(endTime - startTime));

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.error || `HTTP Status ${res.status}`);
      }

      const data = await res.json();
      setAnalysisResult(data);
    } catch (err) {
      setError(`Failed 3-service analysis request: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchTasks = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/go-tasks`);
      if (res.ok) {
        const data = await res.json();
        setTasks(Array.isArray(data) ? data : []);
      }
    } catch (err) {
      console.error("Failed to fetch Go tasks:", err);
    }
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      const res = await fetch(`${API_BASE_URL}/go-tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: newTaskTitle,
          description: "Created from React SPA via Flask -> Go Pipeline",
        }),
      });

      if (res.ok) {
        setNewTaskTitle("");
        fetchTasks();
      }
    } catch (err) {
      setError(`Failed to create task in Go microservice: ${err.message}`);
    }
  };

  return (
    <div className="max-w-4xl w-[94%] my-8 mx-auto p-6 bg-slate-900/90 border border-slate-800 rounded-2xl shadow-2xl backdrop-blur-xl text-slate-100 text-left">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-slate-100 m-0">
              3-Service Microservice Dashboard
            </h2>
            <span className="px-2.5 py-0.5 bg-indigo-500/20 border border-indigo-500/40 rounded-full text-indigo-300 text-xs font-semibold">
              React → Flask → Go
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1 m-0">
            Live telemetry, inter-service proxying &amp; text analytics pipeline
          </p>
        </div>

        <button
          onClick={performHealthCheck}
          className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl text-xs font-semibold transition-all cursor-pointer flex items-center gap-2"
        >
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh Health</span>
        </button>
      </div>

      {/* Service Telemetry Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-6">
        {/* React Tier */}
        <div className="p-4 bg-slate-950/80 border border-slate-800 rounded-xl">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              1. React SPA
            </span>
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          </div>
          <p className="text-sm font-semibold text-slate-200 m-0">Frontend UI</p>
          <p className="text-[11px] text-slate-500 m-0 mt-1">
            Host: {window.location.host}
          </p>
        </div>

        {/* Flask Tier */}
        <div className="p-4 bg-slate-950/80 border border-slate-800 rounded-xl">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              2. Flask Gateway
            </span>
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                flaskStatus === "online"
                  ? "bg-emerald-500"
                  : flaskStatus === "degraded"
                  ? "bg-amber-500"
                  : "bg-rose-500"
              }`}
            ></span>
          </div>
          <p className="text-sm font-semibold text-slate-200 m-0">
            Python Backend BFF
          </p>
          <p className="text-[11px] text-slate-400 m-0 mt-1 truncate">
            <a
              href={API_BASE_URL}
              target="_blank"
              rel="noreferrer"
              className="underline hover:text-emerald-400 transition-colors"
            >
              {API_BASE_URL}
            </a>
          </p>
        </div>

        {/* Go Tier */}
        <div className="p-4 bg-slate-950/80 border border-slate-800 rounded-xl">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              3. Go Microservice
            </span>
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                goStatus === "online"
                  ? "bg-emerald-500"
                  : goStatus === "degraded"
                  ? "bg-amber-500"
                  : "bg-rose-500"
              }`}
            ></span>
          </div>
          <p className="text-sm font-semibold text-slate-200 m-0">
            High-Perf Engine
          </p>
          <p className="text-[11px] text-slate-400 m-0 mt-1 truncate">
            <a
              href={goUrl || "https://render-go-service-txtm.onrender.com"}
              target="_blank"
              rel="noreferrer"
              className="underline hover:text-sky-400 transition-colors"
            >
              {goUrl || "https://render-go-service-txtm.onrender.com"}
            </a>
          </p>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="mb-6 p-4 bg-rose-950/50 border border-rose-800/50 rounded-xl text-rose-300 text-xs flex justify-between items-center">
          <span>{error}</span>
          <button
            onClick={() => setError(null)}
            className="text-rose-300 font-bold hover:text-white"
          >
            ✕
          </button>
        </div>
      )}

      {/* Text Analytics Section */}
      <div className="mb-8 p-5 bg-slate-950/60 border border-slate-800/80 rounded-xl">
        <h3 className="text-sm font-bold text-slate-200 mb-3 m-0">
          Live 3-Service Text Analysis (React → Flask → Go)
        </h3>
        <form onSubmit={handleAnalyze} className="flex flex-col gap-3">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={3}
            className="w-full p-3 bg-slate-900 border border-slate-700 rounded-xl text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
            placeholder="Type text to process through Go microservice..."
          />
          <div className="flex justify-between items-center">
            <button
              type="submit"
              disabled={isLoading || !inputText.trim()}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white font-semibold text-xs rounded-xl transition-all cursor-pointer flex items-center gap-2"
            >
              {isLoading ? "Processing..." : "Analyze Text via Go"}
            </button>
            {latency !== null && (
              <span className="text-xs font-mono text-emerald-400">
                End-to-End Latency: {latency} ms
              </span>
            )}
          </div>
        </form>

        {analysisResult && (
          <div className="mt-4 p-4 bg-slate-900 border border-indigo-500/30 rounded-xl text-xs">
            <div className="flex justify-between items-center mb-3 pb-2 border-b border-slate-800">
              <span className="font-bold text-indigo-300">
                Analysis Response:
              </span>
              <span className="text-[11px] text-slate-400 font-mono">
                Gateway: {analysisResult.gateway}
              </span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-center">
              <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                <p className="text-slate-400 text-[10px] uppercase">Words</p>
                <p className="text-base font-bold text-indigo-400 m-0">
                  {analysisResult.word_count}
                </p>
              </div>
              <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                <p className="text-slate-400 text-[10px] uppercase">
                  Characters
                </p>
                <p className="text-base font-bold text-sky-400 m-0">
                  {analysisResult.character_count}
                </p>
              </div>
              <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                <p className="text-slate-400 text-[10px] uppercase">Lines</p>
                <p className="text-base font-bold text-purple-400 m-0">
                  {analysisResult.line_count}
                </p>
              </div>
              <div className="p-2 bg-slate-950 rounded-lg border border-slate-800">
                <p className="text-slate-400 text-[10px] uppercase">Bytes</p>
                <p className="text-base font-bold text-emerald-400 m-0">
                  {analysisResult.byte_size} B
                </p>
              </div>
            </div>
            <p className="mt-3 m-0 text-[11px] text-slate-400 text-left italic">
              Computed by: {analysisResult.service} at{" "}
              {new Date(analysisResult.processed_at).toLocaleTimeString()}
            </p>
          </div>
        )}
      </div>

      {/* Go Microservice Tasks Section */}
      <div className="p-5 bg-slate-950/60 border border-slate-800/80 rounded-xl">
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-sm font-bold text-slate-200 m-0">
            Go Microservice Task Management
          </h3>
          <button
            onClick={fetchTasks}
            className="text-xs text-indigo-400 hover:text-indigo-300 cursor-pointer"
          >
            Fetch Tasks
          </button>
        </div>

        <form onSubmit={handleCreateTask} className="flex gap-2 mb-4">
          <input
            type="text"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="New microservice task title..."
            className="flex-1 px-3 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-slate-100 placeholder-slate-500 focus:outline-none"
          />
          <button
            type="submit"
            disabled={!newTaskTitle.trim()}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-200 font-semibold text-xs rounded-xl cursor-pointer"
          >
            Add Task
          </button>
        </form>

        {tasks.length > 0 ? (
          <div className="flex flex-col gap-2">
            {tasks.map((t) => (
              <div
                key={t.id}
                className="p-3 bg-slate-900 border border-slate-800 rounded-xl flex justify-between items-center text-xs"
              >
                <div>
                  <p className="font-semibold text-slate-200 m-0">{t.title}</p>
                  <p className="text-[11px] text-slate-500 m-0">{t.description}</p>
                </div>
                <span className="px-2 py-0.5 bg-emerald-950 border border-emerald-800 text-emerald-300 text-[10px] rounded font-mono">
                  {t.status || "pending"}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 m-0 italic text-center py-2">
            No tasks loaded from Go microservice yet. Click &quot;Fetch Tasks&quot; or add a new task.
          </p>
        )}
      </div>
    </div>
  );
};

export default MicroserviceDashboard;
