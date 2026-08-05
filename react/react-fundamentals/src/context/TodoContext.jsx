/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, useEffect } from "react";

const TodoContext = createContext(null);

const DEFAULT_TODOS = [
  {
    id: 1,
    text: "Master React & Tailwind CSS styling",
    priority: "high",
    completed: true,
  },
  {
    id: 2,
    text: "Build portfolio-worthy web applications",
    priority: "medium",
    completed: false,
  },
  {
    id: 3,
    text: "Review state management & context API",
    priority: "low",
    completed: false,
  },
];

export const TodoProvider = ({ children }) => {
  const [todos, setTodos] = useState(() => {
    const saved = localStorage.getItem("react_todos_v2");
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return DEFAULT_TODOS;
      }
    }
    return DEFAULT_TODOS;
  });

  useEffect(() => {
    localStorage.setItem("react_todos_v2", JSON.stringify(todos));
  }, [todos]);

  const addTodo = (text, priority = "medium") => {
    const newTodo = {
      id: Date.now(),
      text,
      priority,
      completed: false,
    };
    setTodos((prev) => [newTodo, ...prev]);
  };

  const toggleTodo = (id) => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  const deleteTodo = (id) => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  const clearCompleted = () => {
    setTodos((prev) => prev.filter((todo) => !todo.completed));
  };

  return (
    <TodoContext.Provider
      value={{ todos, addTodo, toggleTodo, deleteTodo, clearCompleted }}
    >
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
