import { NavLink } from "react-router-dom";
import "./Navigation.css";

const Navigation = () => {
  return (
    <nav className="navigation-bar">
      <NavLink to="/" className="navigation-logo">
        🚀 ReactRouterStudy
      </NavLink>
      <div className="navigation-links">
        <NavLink to="/" className="nav-link">
          Home
        </NavLink>
        <NavLink to="/about" className="nav-link">
          About
        </NavLink>
        <NavLink to="/projects" className="nav-link">
          Projects
        </NavLink>
      </div>
    </nav>
  );
};

export default Navigation;
