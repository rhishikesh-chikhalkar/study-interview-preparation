import { useState } from "react";
import { useTodo } from "../context/TodoContext";

const TodoInput = () => {
  const [inputText, setInputText] = useState("");
  const [priority, setPriority] = useState("medium");
  const { addTodo } = useTodo();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    addTodo(inputText.trim(), priority);
    setInputText("");
  };

  const priorityOptions = [
    {
      id: "low",
      label: "Low",
      activeBg: "bg-emerald-500 text-white shadow-emerald-500/20",
      idleBg: "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200",
    },
    {
      id: "medium",
      label: "Medium",
      activeBg: "bg-amber-500 text-white shadow-amber-500/20",
      idleBg: "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200",
    },
    {
      id: "high",
      label: "High",
      activeBg: "bg-rose-500 text-white shadow-rose-500/20",
      idleBg: "bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200",
    },
  ];

  return (
    <form onSubmit={handleSubmit} className="mb-6 space-y-3">
      <div className="flex flex-col sm:flex-row gap-2">
        <div className="relative flex-1">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Add a new task..."
            className="w-full px-4 py-3 text-sm bg-slate-50 dark:bg-slate-800/80 border 
                     border-slate-200 dark:border-slate-700/80 rounded-xl text-slate-900 
                     dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 
                     focus:ring-indigo-500/20 focus:border-indigo-500 transition-all 
                     duration-200"
          />
        </div>
        <button
          type="submit"
          className="inline-flex items-center justify-center px-5 py-3 text-sm font-semibold 
                   text-white bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 
                   hover:to-violet-500 active:scale-95 rounded-xl shadow-md 
                   shadow-indigo-500/20 hover:shadow-indigo-500/30 transition-all duration-200 
                   cursor-pointer shrink-0 gap-2"
        >
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2.5"
              d="M12 4.5v15m7.5-7.5h-15"
            />
          </svg>
          <span>Add Task</span>
        </button>
      </div>

      <div className="flex items-center gap-2 pt-1">
        <span className="text-xs font-medium text-slate-500 dark:text-slate-400">
          Priority:
        </span>
        <div className="flex gap-1.5">
          {priorityOptions.map((opt) => (
            <button
              key={opt.id}
              type="button"
              onClick={() => setPriority(opt.id)}
              className={`px-2.5 py-1 text-xs font-medium rounded-lg transition-all 
                       duration-200 cursor-pointer ${
                         priority === opt.id
                           ? `${opt.activeBg} shadow-sm font-semibold`
                           : opt.idleBg
                       }`}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>
    </form>
  );
};

export default TodoInput;
