import { useState } from "react";
import { useTodo } from "../context/TodoContext";

const TodoList = () => {
  const { todos, toggleTodo, deleteTodo, clearCompleted } = useTodo();
  const [filter, setFilter] = useState("all");

  const filteredTodos = todos.filter((todo) => {
    if (filter === "active") return !todo.completed;
    if (filter === "completed") return todo.completed;
    return true;
  });

  const counts = {
    all: todos.length,
    active: todos.filter((t) => !t.completed).length,
    completed: todos.filter((t) => t.completed).length,
  };

  const getPriorityBadge = (priority) => {
    switch (priority) {
      case "high":
        return (
          <span className="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider 
                         bg-rose-500/10 text-rose-600 dark:text-rose-400 
                         border border-rose-500/20 rounded-md">
            High
          </span>
        );
      case "medium":
        return (
          <span className="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider 
                         bg-amber-500/10 text-amber-600 dark:text-amber-400 
                         border border-amber-500/20 rounded-md">
            Med
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider 
                         bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 
                         border border-emerald-500/20 rounded-md">
            Low
          </span>
        );
    }
  };

  return (
    <div className="space-y-4">
      {/* Filter Tabs Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-2 
                    border-b border-slate-100 dark:border-slate-800">
        <div className="flex bg-slate-100 dark:bg-slate-800/60 p-1 rounded-xl gap-1">
          {["all", "active", "completed"].map((tab) => (
            <button
              key={tab}
              onClick={() => setFilter(tab)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg capitalize 
                        transition-all duration-200 cursor-pointer flex items-center gap-1.5 ${
                          filter === tab
                            ? "bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-400 shadow-sm"
                            : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                        }`}
            >
              <span>{tab}</span>
              <span
                className={`px-1.5 py-0.2 text-[10px] rounded-full font-medium ${
                  filter === tab
                    ? "bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300"
                    : "bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-400"
                }`}
              >
                {counts[tab]}
              </span>
            </button>
          ))}
        </div>

        {counts.completed > 0 && (
          <button
            onClick={clearCompleted}
            className="text-xs font-medium text-slate-500 hover:text-rose-600 
                     dark:hover:text-rose-400 transition-colors cursor-pointer"
          >
            Clear completed
          </button>
        )}
      </div>

      {/* Task List items */}
      {filteredTodos.length === 0 ? (
        <div className="py-12 text-center rounded-2xl border-2 border-dashed 
                      border-slate-200 dark:border-slate-800 bg-slate-50/50 
                      dark:bg-slate-800/30">
          <div className="w-12 h-12 mx-auto mb-3 text-slate-300 dark:text-slate-600 
                        flex items-center justify-center bg-slate-100 
                        dark:bg-slate-800 rounded-full">
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="1.5"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>
          <p className="text-sm font-medium text-slate-600 dark:text-slate-400">
            {filter === "completed"
              ? "No completed tasks yet."
              : filter === "active"
              ? "No pending tasks! All caught up 🎉"
              : "Your task list is empty. Add a task above!"}
          </p>
        </div>
      ) : (
        <ul className="space-y-2.5">
          {filteredTodos.map((todo) => (
            <li
              key={todo.id}
              className={`group flex items-center justify-between p-3.5 
                       bg-white dark:bg-slate-800/90 border border-slate-200/80 
                       dark:border-slate-700/80 rounded-xl shadow-xs 
                       hover:border-indigo-300 dark:hover:border-indigo-600/60 
                       hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 ${
                         todo.completed ? "bg-slate-50/50 dark:bg-slate-800/40" : ""
                       }`}
            >
              <div
                className="flex items-center gap-3 flex-1 min-w-0 cursor-pointer"
                onClick={() => toggleTodo(todo.id)}
              >
                {/* Custom Styled Checkbox */}
                <div
                  className={`w-5 h-5 rounded-lg border flex items-center 
                           justify-center shrink-0 transition-all duration-200 ${
                             todo.completed
                               ? "bg-indigo-600 border-indigo-600 text-white shadow-xs scale-105"
                               : "border-slate-300 dark:border-slate-600 group-hover:border-indigo-400"
                           }`}
                >
                  {todo.completed && (
                    <svg
                      className="w-3.5 h-3.5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="3"
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  )}
                </div>

                {/* Todo Text */}
                <span
                  className={`text-sm font-medium transition-all duration-200 truncate ${
                    todo.completed
                      ? "line-through text-slate-400 dark:text-slate-500 opacity-75"
                      : "text-slate-800 dark:text-slate-100"
                  }`}
                >
                  {todo.text}
                </span>

                {/* Priority Badge */}
                {getPriorityBadge(todo.priority)}
              </div>

              {/* Action Buttons */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  deleteTodo(todo.id);
                }}
                className="p-1.5 ml-2 text-slate-400 hover:text-rose-600 
                         dark:hover:text-rose-400 hover:bg-rose-50 
                         dark:hover:bg-rose-950/40 rounded-lg transition-colors 
                         cursor-pointer opacity-70 group-hover:opacity-100"
                aria-label="Delete task"
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
                    strokeWidth="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TodoList;
