/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState } from "react";

const TodoContext = createContext(null);

export const TodoProvider = ({ children }) => {
  const [todos, setTodos] = useState([
    { id: 1, text: "Learn React useState hook", completed: true },
    { id: 2, text: "Build a premium Todo Application", completed: false },
    { id: 3, text: "Master Advanced Agentic Coding", completed: false },
  ]);

  const addTodo = (text) => {
    const newTodo = {
      id: Date.now(),
      text: text,
      completed: false,
    };
    setTodos((prevTodos) => [...prevTodos, newTodo]);
  };

  const toggleTodo = (id) => {
    setTodos((prevTodos) =>
      prevTodos.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo,
      ),
    );
  };

  const deleteTodo = (id) => {
    setTodos((prevTodos) => prevTodos.filter((todo) => todo.id !== id));
  };

  return (
    <TodoContext.Provider value={{ todos, addTodo, toggleTodo, deleteTodo }}>
      {children}
    </TodoContext.Provider>
  );
};

export const useTodo = () => {
  const context = useContext(TodoContext);
  if (!context) {
    throw new Error("useTodo must be used within a TodoProvider");
  }
  return context;
};
