import { useState } from "react";
import { useTodo } from "../context/TodoContext";

const TodoInput = () => {
  const [inputText, setInputText] = useState("");
  const { addTodo } = useTodo();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;
    addTodo(inputText.trim());
    setInputText("");
  };

  return (
    <form onSubmit={handleSubmit} className="todo-form">
      <input
        type="text"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Add a new task..."
        className="todo-input"
      />
      <button type="submit" className="todo-button">
        Add Task
      </button>
    </form>
  );
};

export default TodoInput;
