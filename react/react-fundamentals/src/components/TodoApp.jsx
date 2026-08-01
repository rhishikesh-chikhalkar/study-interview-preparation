import { TodoProvider, useTodo } from "../context/TodoContext";
import TodoInput from "./TodoInput";
import TodoList from "./TodoList";
import "./TodoApp.css";

const TodoAppContent = () => {
  const { todos } = useTodo();

  return (
    <div className="todo-container">
      <h2 className="todo-title">Task Manager</h2>
      <p className="todo-subtitle">Keep track of your daily goals</p>

      <TodoInput />

      <TodoList />

      <div className="todo-footer">
        <span>
          {todos.filter((t) => !t.completed).length} pending of {todos.length}{" "}
          total
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
