import { TodoProvider, useTodo } from "../context/TodoContext";
import TodoInput from "./TodoInput";
import TodoList from "./TodoList";

const TodoAppContent = () => {
  const { todos } = useTodo();

  const total = todos.length;
  const completed = todos.filter((t) => t.completed).length;
  const pending = total - completed;
  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="w-full max-w-xl mx-auto my-8 p-6 sm:p-8 bg-white/90 
                  dark:bg-slate-900/90 border border-slate-200/80 
                  dark:border-slate-800 rounded-3xl shadow-xl 
                  backdrop-blur-xl transition-all duration-300">
      {/* Header Section */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr 
                          from-indigo-600 to-violet-500 flex items-center 
                          justify-center text-white shadow-md 
                          shadow-indigo-500/20">
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2.5"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div>
              <h2 className="text-xl sm:text-2xl font-bold text-slate-900 
                           dark:text-white tracking-tight">
                Task Flow
              </h2>
              <p className="text-xs sm:text-sm font-medium text-slate-500 
                          dark:text-slate-400">
                Organize your goals efficiently
              </p>
            </div>
          </div>

          <div className="text-right">
            <span className="text-xs font-semibold px-2.5 py-1 rounded-full 
                           bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 
                           dark:text-indigo-400 border border-indigo-200/50 
                           dark:border-indigo-800/50">
              {percentage}% Done
            </span>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mt-4">
          <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 
                        rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 
                       rounded-full transition-all duration-500 ease-out"
              style={{ width: `${percentage}%` }}
            />
          </div>
        </div>
      </div>

      {/* Input Form */}
      <TodoInput />

      {/* Todo List */}
      <TodoList />

      {/* Footer Stats */}
      <div className="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800 
                    flex items-center justify-between text-xs text-slate-500 
                    dark:text-slate-400 font-medium">
        <span>
          {pending} pending task{pending === 1 ? "" : "s"}
        </span>
        <span>
          {completed} of {total} completed
        </span>
      </div>
    </div>
  );
};

const TodoApp = () => {
  return (
    <TodoProvider>
      <TodoAppContent />
    </TodoProvider>
  );
};

export default TodoApp;
