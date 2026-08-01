import { useTodo } from "../context/TodoContext";

const TodoList = () => {
  const { todos, toggleTodo, deleteTodo } = useTodo();

  return (
    <>
      {todos.length === 0 ? (
        <div className="todo-empty">
          <p>No tasks left! 🎉 Enjoy your day.</p>
        </div>
      ) : (
        <ul className="todo-list">
          {todos.map((todo) => (
            <li
              key={todo.id}
              className={`todo-item ${todo.completed ? "completed" : ""}`}
            >
              <div
                className="todo-item-content"
                onClick={() => toggleTodo(todo.id)}
              >
                <div
                  className={`todo-checkbox ${todo.completed ? "checked" : ""}`}
                >
                  {todo.completed && (
                    <svg
                      className="todo-check-icon"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="3"
                        d="M5 13l4 4L19 7"
                      ></path>
                    </svg>
                  )}
                </div>
                <span className="todo-text">{todo.text}</span>
              </div>
              <button
                onClick={() => deleteTodo(todo.id)}
                className="todo-delete-btn"
                aria-label="Delete todo"
              >
                <svg
                  className="todo-trash-icon"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  ></path>
                </svg>
              </button>
            </li>
          ))}
        </ul>
      )}
    </>
  );
};

export default TodoList;
