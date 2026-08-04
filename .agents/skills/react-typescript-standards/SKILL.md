---
name: react-typescript-standards
description: Use when writing, reviewing, or refactoring React and TypeScript code. Covers feature-based architecture, component design, custom hooks, state management, JSDoc documentation, and FAANG-level anti-patterns.
---

# React & TypeScript Production Standards

Production-grade React/TypeScript standards for all projects.

---

## 1. Architecture & Project Structure (STRICT FEATURE-BASED)

Follow a domain-driven, feature-based structure for high modularity and clear boundaries.

### Folder Layout

```
src/
  app/            # Root component, global styles, providers
  features/       # Business domains (e.g., search, user, billing)
    <feature>/
      components/ # Feature-specific UI
      hooks/      # Feature-specific logic
      services/   # Feature-specific API interactions
      types.ts    # Feature-specific interfaces
      index.ts    # Public API for the feature (Entry point)
  components/     # Reusable, stateless UI (Shared)
  hooks/          # Global reusable logic (Shared)
  services/       # Global API clients and base configurations
  utils/          # Generic helpers (Shared)
  types/          # Global/shared type definitions
```

### Responsibility Rules

- Feature logic **MUST** stay inside the respective feature folder.
- Entry files (`index.ts`) must encapsulate internal feature details.
- Never mix feature-specific code into global shared folders.
- **Pattern**: `UI (Component) -> Hook (Logic) -> Service (API) -> Backend`

---

## 2. Component & Custom Hook Design

- **Functional Components**: Use functional components only (no class components). Use TypeScript for all props.
- **Keep it Slim**: Components should be < 200 lines. Move all business logic into custom hooks.
- **Hook Purpose**: Hooks must start with `use`, handle loading/error states, and return data/actions (never JSX).
- **Separation of Concerns**: UI components handle presentation only. Hooks manage state and side effects.

### Example: Service & Hook Pattern

```ts
// src/features/user/services/userService.ts
export const fetchUser = async (id: string) => apiClient.get(`/users/${id}`);

// src/features/user/hooks/useUser.ts
export const useUser = (id: string) => {
  const [data, setData] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setError(null);

    fetchUser(id)
      .then((res) => {
        if (isMounted) setData(res.data);
      })
      .catch((err) => {
        if (isMounted) setError(transformStandardError(err));
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => { isMounted = false; };
  }, [id]);

  return { data, loading, error };
};
```

---

## 3. React Hook Best Practices

- **State Initialization**: Prefer lazy state initializers (`useState(() => ...)`) when initializing from external sources like URL parameters or LocalStorage.
- **Effect Synchronization**: Avoid synchronous `setState` calls inside `useEffect` bodies. Use refs for internal coordination flags.
- **Dependency Integrity**: Strictly follow `exhaustive-deps`. Never ignore or suppress hook dependency warnings.

---

## 4. State, Performance & Error Management

- **State Locality**: Keep state as close to its usage as possible. Use global state (Zustand/Context) only for truly global data.
- **API Layer**: Never call APIs inside components. Use a centralized `apiClient` (Axios) in the service layer.
- **Performance**: Use `React.memo`, `useMemo`, and `useCallback` judiciously. Avoid storing derived data in state.
- **Standardized Errors**: Handle errors in the service layer. Return user-friendly messages for the UI.

---

## 5. Documentation & JSDoc Standards

### Mandatory Docstrings

- Every exported function, component, or hook **MUST** have a **single-line docstring** using `/** ... */`.
- EVERY file MUST have a module-level JSDoc at the top:

```ts
/**
 * <Module Name> Module
 *
 * Responsibilities:
 * - <Primary task 1>
 * - <Primary task 2>
 *
 * Boundaries:
 * - <What this module does NOT handle>
 */
```

### Rules

- Prefer single-line descriptions. Avoid repeating TypeScript types in comments.
- Ensure exactly one empty line follows the module-level JSDoc.

---

## 6. Strict Discipline & Anti-Patterns (FAANG-Level)

- **Stop Using `any`**: TypeScript safety is mandatory. No untyped code allowed.
- **No Inline Logic**: Do NOT put complex logic or mapping inside JSX. Extract into variables or hooks.
- **No Monoliths**: Break large components/hooks into smaller, focused modules immediately.
- **No Hardcoding**: Use constants or environment variables for all magic values and URLs.

---

## 7. Validation Commands

```bash
npm run lint
npx tsc --noEmit
```
