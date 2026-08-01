import "./About.css";

const About = () => {
  return (
    <div className="about-container">
      <h1 className="about-title">
        About Us
      </h1>
      <p className="about-description">
        This application was designed to help developers master client-side routing concepts using React Router. By structuring pages as individual route elements, React Router intercepts browser link clicks, preventing typical round-trip server request delays.
      </p>

      <div className="about-box">
        <h3 className="about-box-title">💡 Routing Core Concepts</h3>
        <ul className="about-list">
          <li><strong>BrowserRouter:</strong> Wraps your application to sync rendering with the current browser URL state.</li>
          <li><strong>Routes:</strong> Acts as a container for all the defined route components.</li>
          <li><strong>Route:</strong> Declares a mapping between a specific URL path and the React component to render.</li>
          <li><strong>NavLink / Link:</strong> Renders accessible anchor tags that interact with the router navigation system.</li>
        </ul>
      </div>
    </div>
  );
};

export default About;
