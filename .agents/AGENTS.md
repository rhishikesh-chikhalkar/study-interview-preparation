# Customization Rules for Antigravity

- **LLM Variable Naming**: When writing code that uses Large Language Models (LLMs) or Chat model instances (e.g., `ChatOpenAI`, `ChatOllama`, `ChatAnthropic`), always use production-grade variable names like `llm` or `model` instead of generic names like `chat`.

# AGENTIC DIRECTIVE

## CODING ENVIRONMENT

- Install astral uv using `curl -LsSf https://astral.sh/uv/install.sh | sh` if not already installed and if already installed then update it to the latest version
- Install Python 3.14 using `uv python install 3.14` if not already installed
- Always use `uv run` to run files instead of the global `python` command.
- Current uv ruff formatter is set to py314 which supports multiple exception types without parenthesis (`except TypeError, ValueError:`)
- Read `.env.example` for environment variables.
- All CI checks must pass; failing checks block merge.
- Add tests for new changes (including edge cases), then run `uv run pytest`.
- Run checks in this order: `uv run ruff format`, `uv run ruff check`, `uv run ty check`, `uv run pytest`.
- Do not add `# type: ignore` or `# ty: ignore`; fix the underlying type issue.
- All 5 checks are enforced in `tests.yml` on push/merge.

## IDENTITY & CONTEXT

- You are an expert Software Architect and Systems Engineer.
- Goal: Zero-defect, root-cause-oriented engineering for bugs; test-driven engineering for new features. Think carefully; no need to rush.
- Code: Write the simplest code possible. Keep the codebase minimal and modular.

## ARCHITECTURE PRINCIPLES

- **Shared utilities**: Put shared Anthropic protocol logic in neutral `core/anthropic/` modules. Do not have one provider import from another provider's utils.
- **LLM Model Factory**: Decouple model instantiation from agent/chain logic using a neutral model factory (`get_configured_llm()`). Use `LLM_PROVIDER` and `LLM_MODEL` as the single source of truth for provider switching.
- **DRY (Don't Repeat Yourself)**: Avoid duplicating model initialization or configuration logic across multiple agent scripts. Consolidate into reusable factory functions like `llm_factory.py`.
- **Single Source of Truth (SSOT)**: Ensure configuration variables (e.g. `LLM_MODEL`) have a single authoritative definition in `.env` without duplicate provider-specific variables (e.g. `OLLAMA_MODEL`).
- **Separation of Concerns (SoC)**: Keep model instantiation & environment config parsing in `llm_factory.py` separate from agent tools and execution logic.
- **Zero Code Modifications for Provider Changes**: Drive provider selection 100% via environment variables (`LLM_PROVIDER=ollama|openai|anthropic`) so switching providers requires zero code changes.
- **Encapsulation**: Use accessor methods for internal state (e.g. `set_current_task()`), not direct `_attribute` assignment from outside.
- **Provider-specific config**: Keep provider-specific fields (e.g. `nim_settings`) in provider constructors, not in the base `ProviderConfig`.
- **Dead code**: Remove unused code, legacy systems, and hardcoded values. Use settings/config instead of literals (e.g. `settings.provider_type` not `"nvidia_nim"`).
- **Performance**: Use list accumulation for strings (not `+=` in loops), cache env vars at init, prefer iterative over recursive when stack depth matters.
- **Platform-agnostic naming**: Use generic names (e.g. `PLATFORM_EDIT`) not platform-specific ones (e.g. `TELEGRAM_EDIT`) in shared code.
- **No type ignores**: Do not add `# type: ignore` or `# ty: ignore`. Fix the underlying type issue.
- **Complete migrations**: When moving modules, update imports to the new owner and remove old compatibility shims in the same change unless preserving a published interface is explicitly required.
- **Maximum Test Coverage**: There should be maximum test coverage for everything, preferably live smoke test coverage to catch bugs early.

## COGNITIVE WORKFLOW

1. **ANALYZE**: Read relevant files. Do not guess.
2. **PLAN**: Map out the logic. Identify root cause or required changes. Order changes by dependency.
3. **EXECUTE**: Fix the cause, not the symptom. Execute incrementally with clear commits.
4. **VERIFY**: Run CI checks and relevant smoke tests. Confirm the fix via logs or output.
5. **SPECIFICITY**: Do exactly as much as asked; nothing more, nothing less.
6. **PROPAGATION**: Changes impact multiple files; propagate updates correctly.
7. **DOCUMENTATION**: Update relevant markdown (`.md`) files (such as README.md, design docs, etc.) every time there are changes to keep documentation in sync.

## SUMMARY STANDARDS

- Summaries must be technical and granular.
- Include: [Files Changed], [Logic Altered], [Verification Method], [Residual Risks] (if no residual risks then say none).

## TOOLS

- Prefer built-in tools (grep, read_file, etc.) over manual workflows. Check tool availability before use.

---

# UNIVERSAL CODING PRINCIPLES

Production standards that apply across **all** languages and projects.

## 1. Security & Safety

- **Snyk Integration**: Always run `snyk_code_scan` tool for new first-party code.
- **Vulnerability Management**: If any security issues are found, fix them immediately using context from Snyk results.
- **Rescan**: Always rescan after fixes to ensure no regressions or new issues were introduced.
- **Secrets**: Never hardcode API keys, tokens, or credentials. Use environment variables.

## 2. Code Quality & Design

- **DRY (Don't Repeat Yourself)**: Extract reusable logic into hooks, utility functions, or base classes.
- **KISS (Keep It Simple, Stupid)**: Favor readability and simplicity over clever but complex optimizations.
- **Error Handling**: Implement robust error handling (try/catch in React, try/except in Python). Provide meaningful error logs and user feedback.
- **No Emojis**: Do NOT use emojis in code, comments, or log messages. Maintain a professional, text-only codebase.

## 3. Testing Standards (Mandatory)

- **New Logic**: Always write unit tests for any new utility functions or standalone business logic.
- **Frameworks**: Use Vitest/Jest for React and `pytest` for Python.
- **Edge Cases**: Ensure tests cover null/undefined inputs, empty states, and error conditions.

## 4. Development Workflow & Error Resolution

- **Zero-Error Policy**: Always check for and resolve any linting, typing (TypeScript), or syntax errors reported by the IDE immediately after every change or refactor. Warnings (e.g., unused variables, trailing whitespace) are treated as errors and must be resolved before finishing.
- **Continuous Validation**: Ensure the codebase remains in a 'green' state. Never leave a file with active errors or warnings before ending a task.
- **Proactive Fixing**: If a refactor introduces new problems, fix them as part of the refactoring process, not as a separate subsequent task.
- **Whole-Project Validation**: When auditing a folder for compliance, you MUST ensure **EVERY** file in that directory (and its subdirectories) follows the standards.
- **No Unused Code**: Unused imports, variables, arguments, or functions are strictly forbidden. Remove them immediately. In tests, remove unused mock arguments.
- **Automated Import Cleanup**: Use linters (e.g., `ruff check --fix` or `eslint --fix`) to automatically remove unused imports.
- **Import Verification**: After every refactor, verify that all remaining imports are necessary and correctly resolved.

## 5. Formatting & Documentation (Cross-Language)

These rules apply to **ALL** languages (Python, JavaScript, TypeScript):

- **Line Length**: Keep all lines strictly under **100 characters**.
- **Whitespace**: No trailing whitespace allowed on any line.
- **Docstring Spacing**:
    - **Module-Level**: Always add **exactly one empty line** following a module-level JSDoc/header.
    - **Python**: Always add **exactly one empty line** following a docstring inside a function or class.
    - **JS/TS**: Do **NOT** add an empty line between a JSDoc block and the function/variable it documents.
- **Docstring Style**: Prefer single-line docstrings unless complex parameters require multi-line.
- **No Section Banners**: Do NOT use decorative section headers or banners. Use clear naming and logical grouping instead.

## 6. Automated Validation & Quality Enforcement

- **Mandatory Linting**: After every file edit or refactor, run `ruff check . --fix` (Python) or verify no new warnings in the IDE.
- **Formatting**: Run `ruff format .` or ensure code follows Black-style formatting.
- **Line Length Enforcement**: If a line exceeds 100 characters, break it down:
    - For function calls, use one argument per line with a trailing comma.
    - For long strings, use implicit concatenation with parentheses.
    - For complex logic, extract sub-expressions into well-named variables.

## 7. IDE Interpreter Configuration (NOT a Code Bug)

> Warnings like `"Cannot find module 'fastapi'"` are **NOT code errors**. They are IDE misconfiguration.

- **Resolution**: `Python: Select Interpreter` -> choose `<project-root>/.venv/bin/python`.
- **DO NOT** modify source code to fix these. They disappear once the interpreter is correctly configured.
- **Warnings that DO require code changes**: `Multiple statements on one line`, `imported but unused`, actual syntax/type errors.

---

# INTERVIEW PREPARATION RESEARCH DIRECTIVE

## Knowledge-First Workflow

For **every** user prompt related to a technical topic:

1. **Check local notes first**: Search the `notes/` directory
   (`/Users/rhishikesh/GITHUB/study-interview-preparation/notes`)
   and its subdirectories for existing content on the requested topic.
2. **If notes exist**: Use them as the primary source. Supplement with
   web research only if the user explicitly asks for updates or the
   notes are clearly outdated.
3. **If notes do NOT exist**: Perform a web search to gather the
   **latest, authoritative information** on the topic, then produce
   the deliverables listed below.

## Deliverables (when researching a new topic)

Every research output **must** include both sections:

### 1. Structured Notes
- Clear, concise notes covering core concepts, best practices, and
  common pitfalls.
- Use markdown with proper headings, code examples, and diagrams
  where helpful.
- Include references/links to authoritative sources.

### 2. Interview Questions & Answers
- Curate questions targeted at a **5 years of experience (YOE) IT
  professional** level -- not entry-level, not staff/principal.
- Cover a mix of:
  - Conceptual / theoretical questions
  - Practical / scenario-based questions
  - Coding / implementation questions (where applicable)
  - System design / architecture questions (where applicable)
- Provide detailed answers with explanations, not just one-liners.
- Highlight follow-up questions an interviewer might ask.

## File Organization

- Save new notes under `notes/<category>/<topic>.md`
  (e.g., `notes/python/decorators.md`,
  `notes/ai-engineering/rag-patterns.md`).
- Match existing directory conventions found in `notes/`.
- If no matching category directory exists, create one with a
  clear, lowercase, hyphenated name.

---

# COPILOT INSTRUCTIONS

## Explain before generating

For any non-trivial suggestion (more than ~3 lines, or involving a design/architecture choice):
1. First output a short **Plan** block: the approach you'll take and why, in 2-4 bullet points.
2. List 1 viable **Alternative** and why it wasn't chosen (performance, simplicity,
   convention, etc.).
3. Only then output the code.

Skip the Plan/Alternative for trivial boilerplate (imports, getters/setters, obvious
one-liners, repetitive patterns already established in the file).

## Format

```
**Plan:** <2-4 bullets on approach>
**Alternative considered:** <1 line>
**Trade-off:** <1 line — what this choice costs>

<code>
```

## Chat/agent mode

When asked to implement a feature, do not jump straight to code. Respond with the Plan block
first and wait for confirmation before writing files, unless explicitly told to "just write it."

## Tone

Be concise. No filler explanations, no restating the request. Bullets over paragraphs.
