import { useState } from "react";
import { NavLink } from "react-router-dom";

const ResponsiveNavbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen((prev) => !prev);
  };

  const closeMenu = () => {
    setIsOpen(false);
  };

  const navLinks = [
    { name: "Home", path: "/" },
    { name: "About", path: "/about" },
    { name: "Projects", path: "/projects" },
    { name: "Responsive Navbar", path: "/projects/navbar" },
  ];

  return (
    <nav className="bg-slate-900 text-slate-100 shadow-lg border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <NavLink
              to="/"
              className="text-xl font-bold text-purple-400 hover:text-purple-300 transition"
            >
              DevPortal
            </NavLink>
          </div>

          <div className="hidden md:flex items-center space-x-6">
            {navLinks.map((link) => (
              <NavLink
                key={link.path}
                to={link.path}
                className={({ isActive }) =>
                  `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-slate-800 text-purple-400"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }`
                }
              >
                {link.name}
              </NavLink>
            ))}
            <button
              type="button"
              className="ml-4 px-4 py-2 text-sm font-semibold text-white bg-purple-600 "
              style={{ borderRadius: "0.375rem" }}
            >
              Get Started
            </button>
          </div>

          <div className="md:hidden flex items-center">
            <button
              type="button"
              onClick={toggleMenu}
              aria-expanded={isOpen}
              aria-label="Toggle navigation menu"
              className="p-2 rounded-md text-slate-400 hover:text-white hover:bg-slate-800"
            >
              {isOpen ? (
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              ) : (
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="md:hidden bg-slate-900 border-t border-slate-800 px-4 pt-2 pb-4 space-y-2">
          {navLinks.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
              onClick={closeMenu}
              className={({ isActive }) =>
                `block px-3 py-2 rounded-md text-base font-medium transition-colors ${
                  isActive
                    ? "bg-slate-800 text-purple-400"
                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                }`
              }
            >
              {link.name}
            </NavLink>
          ))}
          <div className="pt-2">
            <button
              type="button"
              onClick={closeMenu}
              className="w-full text-center px-4 py-2 text-base font-semibold text-white"
              style={{ backgroundColor: "#9333ea", borderRadius: "0.375rem" }}
            >
              Get Started
            </button>
          </div>
        </div>
      )}
    </nav>
  );
};

export default ResponsiveNavbar;
