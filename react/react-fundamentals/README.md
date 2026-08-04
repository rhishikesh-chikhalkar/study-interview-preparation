# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Features and Components

- **Responsive Navbar**: A navigation component built with React state management (`useState`)
  and Tailwind CSS (`hidden md:flex`, `md:hidden`), featuring a mobile hamburger toggle button,
  accessible ARIA attributes (`aria-expanded`, `aria-label`), and auto-closing mobile dropdown.
- **Todo Application**: State management and CRUD workflows.
- **Cat Facts Generator**: Asynchronous data fetching with `useEffect`.
- **Search Filter**: Real-time item filtering component.
- **AI Assistant**: RAG PDF search integration interface.

