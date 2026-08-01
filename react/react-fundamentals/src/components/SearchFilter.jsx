import { useState } from "react";
import "./SearchFilter.css";

const ITEMS = [
  { id: 1, name: "React", category: "Frontend", desc: "A JavaScript library for building user interfaces with component-based architecture." },
  { id: 2, name: "TypeScript", category: "Languages", desc: "A typed superset of JavaScript that compiles to plain JavaScript." },
  { id: 3, name: "Tailwind CSS", category: "Styling", desc: "A utility-first CSS framework for rapid and modern UI development." },
  { id: 4, name: "Next.js", category: "Fullstack", desc: "The React framework for production with SSR, static generation, and routing." },
  { id: 5, name: "GraphQL", category: "API", desc: "A query language for APIs and runtime for fulfilling those queries with existing data." },
  { id: 6, name: "Node.js", category: "Backend", desc: "A JavaScript runtime built on Chrome's V8 JavaScript engine." },
  { id: 7, name: "PostgreSQL", category: "Database", desc: "A powerful, open-source object-relational database system." },
  { id: 8, name: "Docker", category: "DevOps", desc: "A platform designed to help developers build, share, and run modern applications." },
  { id: 9, name: "Vite", category: "Build Tools", desc: "A frontend build tool that is extremely fast, leveraging native ES modules." },
  { id: 10, name: "Web3.js", category: "Blockchain", desc: "A collection of libraries that allow you to interact with a local or remote ethereum node." },
];

const SearchFilter = () => {
  const [query, setQuery] = useState("");

  const filteredItems = ITEMS.filter(
    (item) =>
      item.name.toLowerCase().includes(query.toLowerCase()) ||
      item.category.toLowerCase().includes(query.toLowerCase()) ||
      item.desc.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="search-container">
      <div className="search-header">
        <h2 className="search-title">Tech Directory</h2>
        <p className="search-subtitle">Search and filter programming tools in real-time</p>
      </div>

      <div className="search-input-wrapper">
        <svg
          className="search-icon"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          ></path>
        </svg>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name, category or description..."
          className="search-input"
        />
        {query && (
          <button className="search-clear-btn" onClick={() => setQuery("")} aria-label="Clear search">
            ✕
          </button>
        )}
      </div>

      <div className="search-results-info">
        {query && (
          <span>
            Found {filteredItems.length} match{filteredItems.length !== 1 ? "es" : ""} for &quot;{query}&quot;
          </span>
        )}
      </div>

      <div className="search-list">
        {filteredItems.length > 0 ? (
          filteredItems.map((item) => (
            <div key={item.id} className="search-item-card">
              <div className="search-item-meta">
                <span className="search-item-category">{item.category}</span>
                <span className="search-item-id">#{item.id}</span>
              </div>
              <h3 className="search-item-name">{item.name}</h3>
              <p className="search-item-desc">{item.desc}</p>
            </div>
          ))
        ) : (
          <div className="search-empty-state">
            <svg
              className="search-empty-icon"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="1.5"
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
            <p className="search-empty-title">No matching tech found</p>
            <p className="search-empty-desc">Try searching for something else or clearing your query.</p>
            <button className="search-reset-btn" onClick={() => setQuery("")}>
              Clear Search
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchFilter;
