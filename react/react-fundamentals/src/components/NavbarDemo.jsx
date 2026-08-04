import ResponsiveNavbar from "./ResponsiveNavbar";

const NavbarDemo = () => {
  return (
    <div className="w-full min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8">
      <div className="max-w-5xl mx-auto space-y-6">
        <header className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-white tracking-tight">
            Responsive Navbar Demo
          </h1>
          <p className="text-slate-400 max-w-2xl mx-auto">
            Built with React, Tailwind CSS, and accessibility best practices.
            Resize your window or test mobile viewports to inspect responsive behavior.
          </p>
        </header>

        <section className="bg-slate-900 border border-slate-800 rounded-xl shadow-2xl">
          <div className="bg-slate-800 px-4 py-2 text-xs font-mono text-slate-400 border-b">
            Interactive Navbar Component Preview
          </div>
          <ResponsiveNavbar />
        </section>

        <section className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <h2 className="text-xl font-semibold text-purple-400">
            Key Architecture and Technical Features
          </h2>
          <ul className="list-disc list-inside text-slate-300 space-y-2 text-sm">
            <li>
              <strong>Desktop Viewport:</strong> Displays full navigation links and primary
              action button using Tailwind utility classes <code>hidden md:flex</code>.
            </li>
            <li>
              <strong>Mobile Viewport:</strong> Displays animated SVG hamburger button using
              <code>md:hidden</code> that toggles state.
            </li>
            <li>
              <strong>State Management:</strong> Uses React <code>useState</code> hook for
              toggle state with automatic dropdown auto-close on link navigation.
            </li>
            <li>
              <strong>Accessibility (a11y):</strong> Enforces <code>aria-expanded</code> and
              <code>aria-label</code> attributes for assistive screen readers.
            </li>
          </ul>
        </section>
      </div>
    </div>
  );
};

export default NavbarDemo;
