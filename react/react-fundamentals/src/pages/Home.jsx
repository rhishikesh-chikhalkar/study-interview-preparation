import "./Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <h1 className="home-title">
        Welcome Home
      </h1>
      <p className="home-description">
        This is a beautiful, single-page application demonstrating <strong>React Router</strong> navigation. 
        Explore the different pages to see how client-side routing enables smooth, instant page transitions without full-page reloads.
      </p>

      <div className="home-grid">
        <div className="home-card">
          <h3 className="home-card-title">⚡ Client-Side Routing</h3>
          <p className="home-card-desc">
            Navigate between pages instantly. React Router updates the browser URL and swaps components dynamically.
          </p>
        </div>
        <div className="home-card">
          <h3 className="home-card-title">🎨 Elegant Design</h3>
          <p className="home-card-desc">
            Built using modern typography, glassmorphism-inspired layout patterns, and responsive CSS grids.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
