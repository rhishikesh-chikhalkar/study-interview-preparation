import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navigation from "./components/Navigation";
import Home from "./pages/Home";
import About from "./pages/About";
import Projects from "./pages/Projects";
import TodoApp from "./components/TodoApp";
import CatFact from "./components/CatFact";
import Counter from "./components/Counter";
import SearchFilter from "./components/SearchFilter";
import AiAssistant from "./components/AiAssistant";

const App = () => {
  return (
    <Router>
      <div style={{ display: "flex", flexDirection: "column", minHeight: "100svh" }}>
        <Navigation />
        
        <main style={{ flex: 1, display: "flex", flexDirection: "column" }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/projects/todo" element={<TodoApp />} />
            <Route path="/projects/cat-facts" element={<CatFact />} />
            <Route path="/projects/counter" element={<Counter />} />
            <Route path="/projects/search-filter" element={<SearchFilter />} />
            <Route path="/projects/ai-assistant" element={<AiAssistant />} />
          </Routes>
        </main>

        <footer style={{ 
          padding: "20px", 
          borderTop: "1px solid var(--border)", 
          fontSize: "0.9rem", 
          color: "var(--text)",
          textAlign: "center"
        }}>
          Built with React Router v6 • Study Portal
        </footer>
      </div>
    </Router>
  );
};

export default App;
