import { Link } from "react-router-dom";
import "./Projects.css";

const Projects = () => {
  const projectsList = [
    {
      id: 1,
      title: "Todo Application",
      description: "A complete CRUD application built using React hooks (useState). Split into reusable modular subcomponents.",
      tech: ["React", "CSS3", "Vite"],
      path: "/projects/todo",
    },
    {
      id: 2,
      title: "Cat Facts Generator",
      description: "An asynchronous application utilizing the useEffect hook to fetch live cat trivia from a public API.",
      tech: ["React", "Fetch API", "Async/Await"],
      path: "/projects/cat-facts",
    },
    {
      id: 3,
      title: "Interactive Counter",
      description: "A component exhibiting state modifications, event handlers, and incremental step controls.",
      tech: ["React", "Hooks"],
      path: "/projects/counter",
    },
    {
      id: 4,
      title: "Search Filter",
      description: "A component that renders a list of items with a real-time input filter box.",
      tech: ["React", "State", "Filter"],
      path: "/projects/search-filter",
    },
    {
      id: 5,
      title: "AI Assistant",
      description: "Connect a React frontend with a Flask AI/RAG backend to search indexed PDF content and display responses.",
      tech: ["React", "Fetch API", "Flask", "RAG"],
      path: "/projects/ai-assistant",
    },
    {
      id: 6,
      title: "Responsive Navbar",
      description: "A responsive navigation bar with desktop links and a mobile hamburger menu built with Tailwind CSS.",
      tech: ["React", "Tailwind CSS", "Hooks"],
      path: "/projects/navbar",
    },
    {
      id: 7,
      title: "3-Service Architecture",
      description: "End-to-end microservices telemetry: React SPA -> Flask BFF API Gateway -> Go High-Performance Microservice.",
      tech: ["React", "Flask", "Go", "BFF Microservices"],
      path: "/projects/microservices",
    },
  ];

  return (
    <div className="projects-container">
      <h1 className="projects-title">
        Our Projects
      </h1>
      <p className="projects-description">
        Here is a list of features and learning modules developed as part of our React study roadmap:
      </p>

      <div className="projects-list">
        {projectsList.map((project) => (
          <Link key={project.id} to={project.path} className="project-card-link">
            <div className="project-card">
              <h3 className="project-card-title">
                {project.title}
              </h3>
              <p className="project-card-desc">
                {project.description}
              </p>
              <div className="project-tech-tags">
                {project.tech.map((techItem) => (
                  <span key={techItem} className="project-tech-tag">
                    {techItem}
                  </span>
                ))}
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Projects;
