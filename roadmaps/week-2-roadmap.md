# Week 2 Study Roadmap

**20 July to 26 July 2026**

---

## Monday 20 July

| Time | Task |
|------|------|
| 4:00–5:00 | React — Learn React Router. Set up a multi-page app with 3 pages: Home, About, Projects. Navigate between them. |
| 5:00–6:00 | AI — Learn what embeddings are. Use OpenAI embeddings API in Python to convert a sentence into a vector. Print it, understand what it represents. |
| 6:00–6:45 | Go — Learn Go interfaces. Write a simple interface `Shape` with an `Area()` method. Implement it for a circle and rectangle. |

---

## Tuesday 21 July

| Time | Task |
|------|------|
| 4:00–5:00 | React — Learn `useContext`. Remove prop drilling from your todo app by using a context for todo state. |
| 5:00–6:00 | AI — Learn what a vector database is (concept only). Set up ChromaDB locally (`pip install chromadb`). Store 5 sentences and retrieve the most similar one. |
| 6:00–6:45 | Go — Learn goroutines properly. Write a program that runs 3 tasks concurrently and prints their results. |

---

## Wednesday 22 July

| Time | Task |
|------|------|
| 4:00–5:00 | React — Build a simple search filter. Render a list of 10 items, add an input box that filters the list in real time as you type. |
| 5:00–6:00 | AI — Build a proper RAG pipeline. Load a PDF → chunk it → store in ChromaDB → retrieve relevant chunks → send to OpenAI → get answer. |
| 6:00–6:45 | Go — Learn Go channels. Write a producer-consumer program using channels. |

---

## Thursday 23 July

| Time | Task |
|------|------|
| 4:00–5:00 | React — Call your Flask AI API from React using `fetch`. Display the AI response on screen. This is your first full-stack AI feature. |
| 5:00–6:00 | AI — Wrap your RAG pipeline in a Flask API with a `/ask` POST endpoint that takes a question and returns an answer. Test it with Postman or curl. |
| 6:00–6:45 | Go — Build a Go REST API with two routes: `GET /ping` and `POST /echo` that returns whatever JSON you send it. |

---

## Friday 24 July

| Time | Task |
|------|------|
| 4:00–5:00 | React — Add a loading spinner and error message to your AI call. Practice conditional rendering (`isLoading`, `isError` states). |
| 5:00–6:00 | AI — Add conversation history to your RAG app. It should remember the last 3 exchanges and use them as context. |
| 6:00–6:45 | Go — Add basic middleware to your Go server that logs every incoming request with timestamp and method. |

---

## Saturday 25 July

| Time | Task |
|------|------|
| 4:00–5:30 | React + AI — Start building your mini portfolio project: A React frontend with a chat interface (input box + message thread UI) that talks to your Flask RAG backend. Style it cleanly with basic CSS. |
| 5:30–6:45 | Go — Build a small Go service that your Flask app can call — takes a string and returns word count and character count. Connect the two via HTTP. |

---

## Sunday 26 July

| Time | Task |
|------|------|
| 4:00–5:00 | Polish — Clean up your chat UI project. Make sure React → Flask → ChromaDB → OpenAI full flow works end to end. |
| 5:00–6:00 | GitHub — Push everything. Write a proper `README.md` for your RAG chatbot project. Describe what it does, tech stack, how to run it. |
| 6:00–6:45 | Reflect — Write down 3 things that clicked this week and 2 things still unclear. These become Week 3 priorities. |

---

## Deliverables by end of Week 2 (26 July)
- A full React + Flask + AI chat app working end to end
- A RAG pipeline with ChromaDB storing and retrieving real documents
- A Go microservice connected to your Python backend
- 2 clean GitHub repos with READMEs

---

**Week 3 starts Monday 27 July** — Tailwind CSS, deploying to Vercel + Render, and LangChain agents. You'll go from "works locally" to "live link I can share with anyone."
