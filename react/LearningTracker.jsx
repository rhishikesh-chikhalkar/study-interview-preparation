import { useState, useEffect } from "react";

const TRACKS = [
  { id: "dsa", label: "DSA / System Design", emoji: "🧠", color: "#FF6B35" },
  { id: "react", label: "React", emoji: "⚛️", color: "#61DAFB" },
  { id: "java", label: "Java", emoji: "☕", color: "#F89820" },
  { id: "go", label: "Go", emoji: "🐹", color: "#00ADD8" },
  { id: "flutter", label: "Dart / Flutter", emoji: "🎯", color: "#54C5F8" },
  { id: "cloud", label: "AWS / Azure / GCP", emoji: "☁️", color: "#A78BFA" },
  { id: "devops", label: "DevOps", emoji: "⚙️", color: "#4ADE80" },
  { id: "db", label: "DB (SQL + NoSQL)", emoji: "🗄️", color: "#FB923C" },
  { id: "python", label: "Python Advanced", emoji: "🐍", color: "#FFD43B" },
];

// Thematic daily curriculum — grouped by unifying concept/pattern
const CURRICULUM = [
  {
    day: 1,
    theme: "The Basics of Everything",
    pattern: "Every technology has a runtime, a type system, and a way to store data. Day 1 shows you each one's foundation.",
    concepts: {
      dsa: { title: "Big O Notation", desc: "Time & space complexity — the lens through which all algorithms are judged." },
      react: { title: "JSX & Components", desc: "The atom of React: a function that returns UI." },
      java: { title: "JVM & Data Types", desc: "How Java code compiles and runs; primitives vs objects." },
      go: { title: "Go Toolchain & Packages", desc: "go run, go build, go mod — Go's opinionated project structure." },
      flutter: { title: "Dart Variables & Types", desc: "Strong typing, var, final, const — Dart's type system." },
      cloud: { title: "Cloud Regions & Availability Zones", desc: "AWS/Azure/GCP global infrastructure — where your code lives." },
      devops: { title: "What is DevOps?", desc: "Culture + automation pipeline: Dev → Build → Test → Deploy → Monitor." },
      db: { title: "SQL vs NoSQL — When to Use What", desc: "Relational tables vs document/key-value stores. The foundational tradeoff." },
      python: { title: "Python Internals: GIL & CPython", desc: "Why Python has the Global Interpreter Lock and what it means." },
    },
  },
  {
    day: 2,
    theme: "Collections & Data Structures",
    pattern: "Every language has arrays, maps, and sets. Learning them in parallel reveals how each language thinks about memory.",
    concepts: {
      dsa: { title: "Arrays & Hash Maps", desc: "Contiguous memory vs key-value lookup. O(1) read vs O(1) average insert." },
      react: { title: "useState & Lists", desc: "Managing arrays in state; rendering lists with .map() and keys." },
      java: { title: "ArrayList, HashMap, HashSet", desc: "Java Collections Framework — the workhorses of Java code." },
      go: { title: "Slices & Maps", desc: "Go's built-in dynamic array (slice) and hash map (map) with make()." },
      flutter: { title: "List, Map, Set in Dart", desc: "Dart's core collections — growable vs fixed, typed generics." },
      cloud: { title: "S3 / Blob Storage / GCS", desc: "Object storage across the big 3: buckets, blobs, objects — same idea, different names." },
      devops: { title: "Git Branching Strategy", desc: "Trunk-based dev vs GitFlow — how teams version control at scale." },
      db: { title: "Indexes in SQL & NoSQL", desc: "B-tree indexes (SQL) vs compound indexes (MongoDB) — speed up reads, slow down writes." },
      python: { title: "List Comprehensions & Generators", desc: "Pythonic iteration: lazy generators vs eager comprehensions, memory implications." },
    },
  },
  {
    day: 3,
    theme: "Functions, Closures & Scope",
    pattern: "How each language treats functions as values — the foundation of async, callbacks, and functional patterns.",
    concepts: {
      dsa: { title: "Recursion & Call Stack", desc: "How functions call themselves; stack frames, base cases, tail recursion." },
      react: { title: "useEffect & Closures", desc: "Why stale closures bite you in useEffect; the dependency array explained." },
      java: { title: "Lambdas & Functional Interfaces", desc: "Java 8+ lambdas, Function<T,R>, Predicate, Consumer — functional Java." },
      go: { title: "First-Class Functions & Closures", desc: "Functions as values, higher-order functions, closure over variables." },
      flutter: { title: "Functions & Arrow Syntax in Dart", desc: "Named, optional, positional params; => shorthand; closures in Dart." },
      cloud: { title: "AWS Lambda / Azure Functions / Cloud Run", desc: "Serverless functions — same concept, 3 implementations." },
      devops: { title: "CI/CD Pipelines", desc: "GitHub Actions / Jenkins / GitLab CI — automate test + deploy on every push." },
      db: { title: "Stored Procedures & Aggregation Pipelines", desc: "SQL stored procs vs MongoDB aggregation — logic inside the DB." },
      python: { title: "Decorators & Closures", desc: "How @decorator works under the hood; wrapping functions with functions." },
    },
  },
  {
    day: 4,
    theme: "Concurrency & Parallelism",
    pattern: "Doing multiple things at once is the hardest problem in computing. Each ecosystem solves it differently.",
    concepts: {
      dsa: { title: "Concurrency Patterns: Producer-Consumer", desc: "Queue-based decoupling; bounded buffers, semaphores." },
      react: { title: "Async in React: Suspense & Transitions", desc: "React 18 concurrent rendering — non-blocking UI updates." },
      java: { title: "Threads, ExecutorService & CompletableFuture", desc: "Java's concurrency stack: raw threads → thread pools → async futures." },
      go: { title: "Goroutines & Channels", desc: "Go's killer feature: lightweight goroutines + CSP-style channel communication." },
      flutter: { title: "Dart Isolates & async/await", desc: "Dart's single-threaded event loop; Isolates for true parallelism." },
      cloud: { title: "SQS / Service Bus / Pub-Sub", desc: "Message queues in AWS/Azure/GCP — async decoupling at cloud scale." },
      devops: { title: "Docker & Containers", desc: "Packaging apps with all dependencies — images, containers, Dockerfile basics." },
      db: { title: "Transactions & ACID", desc: "Atomicity, Consistency, Isolation, Durability — what makes DBs reliable." },
      python: { title: "asyncio, Threading vs Multiprocessing", desc: "When to use each: I/O-bound vs CPU-bound workloads; event loop internals." },
    },
  },
  {
    day: 5,
    theme: "Error Handling & Resilience",
    pattern: "Production systems fail. How each language/tool forces you to think about failure is its design philosophy.",
    concepts: {
      dsa: { title: "Retry, Backoff & Circuit Breaker", desc: "System design patterns for resilience — don't hammer a failing service." },
      react: { title: "Error Boundaries", desc: "Catching render-time errors in React; fallback UI patterns." },
      java: { title: "Checked vs Unchecked Exceptions", desc: "Java's controversial mandatory exception handling and when to use each." },
      go: { title: "Errors as Values", desc: "Go's explicit error returns; errors.Is, errors.As, wrapping with %w." },
      flutter: { title: "Try/Catch & Result Patterns in Dart", desc: "Exception handling in Dart; Either/Result pattern for typed errors." },
      cloud: { title: "Health Checks & Auto Scaling Groups", desc: "AWS ALB / Azure VMSS / GCP MIG — automatic failure recovery." },
      devops: { title: "Monitoring & Alerting: Prometheus + Grafana", desc: "Metrics collection, dashboards, and alerting thresholds." },
      db: { title: "DB Replication & Failover", desc: "Primary-replica setups; automatic failover in RDS / Atlas / Cloud SQL." },
      python: { title: "Context Managers & Exception Chains", desc: "__enter__/__exit__, with statement; raise X from Y — chaining exceptions." },
    },
  },
  {
    day: 6,
    theme: "APIs & Communication",
    pattern: "Services talk to each other. REST, gRPC, WebSockets — same problem, different tradeoffs.",
    concepts: {
      dsa: { title: "API Design: REST vs gRPC vs GraphQL", desc: "Tradeoffs in interface design — typed contracts vs flexible queries." },
      react: { title: "Fetching Data: fetch, Axios, React Query", desc: "HTTP in React — loading states, caching, refetching patterns." },
      java: { title: "Spring Boot REST Controllers", desc: "@RestController, @GetMapping — building APIs the Java way." },
      go: { title: "net/http & Building REST APIs", desc: "Go's stdlib HTTP server; JSON encoding/decoding; routing with mux." },
      flutter: { title: "http Package & Dio in Flutter", desc: "Making HTTP requests in Flutter; JSON parsing with jsonDecode." },
      cloud: { title: "API Gateway (AWS / APIM / Cloud Endpoints)", desc: "Managed API layer — rate limiting, auth, routing across all 3 clouds." },
      devops: { title: "Nginx & Reverse Proxies", desc: "Routing traffic, SSL termination, load balancing at the edge." },
      db: { title: "ORM vs Raw Queries", desc: "Hibernate (Java) / GORM (Go) / Prisma vs writing SQL — tradeoffs." },
      python: { title: "FastAPI & Pydantic", desc: "Modern async Python APIs; Pydantic models for validation and serialization." },
    },
  },
  {
    day: 7,
    theme: "State Management & Caching",
    pattern: "State is everywhere — in UI, in servers, in databases. Caching is just temporary state.",
    concepts: {
      dsa: { title: "LRU Cache Implementation", desc: "HashMap + Doubly Linked List — the classic caching interview problem." },
      react: { title: "Context API vs Redux vs Zustand", desc: "Global state in React — when to lift state vs use a store." },
      java: { title: "Spring Cache & Caffeine", desc: "@Cacheable, @CacheEvict — declarative in-process caching in Spring." },
      go: { title: "sync.Map & In-Memory Caching", desc: "Thread-safe maps; building a simple TTL cache in Go." },
      flutter: { title: "Provider & Riverpod", desc: "Flutter's state management landscape — why Provider isn't enough at scale." },
      cloud: { title: "ElastiCache / Azure Cache / Memorystore (Redis)", desc: "Managed Redis across clouds — same OSS, different wrappers." },
      devops: { title: "Kubernetes Basics", desc: "Pods, Deployments, Services — the 3 core K8s objects you need first." },
      db: { title: "Redis Data Structures", desc: "Strings, Lists, Sets, Sorted Sets, Hashes — Redis as a multi-tool." },
      python: { title: "functools.lru_cache & memoization", desc: "@lru_cache, @cache — built-in memoization; implementing your own." },
    },
  },
  {
    day: 8,
    theme: "Authentication & Security",
    pattern: "Every app needs auth. JWT, OAuth, and IAM roles are the same concept at different abstraction levels.",
    concepts: {
      dsa: { title: "Hashing & Cryptographic Basics", desc: "SHA-256, bcrypt, rainbow tables — why password hashing is a computer science problem." },
      react: { title: "JWT Auth Flow in React", desc: "Storing tokens, protected routes, interceptors — frontend auth end to end." },
      java: { title: "Spring Security & JWT", desc: "Filters, SecurityContext, stateless JWT validation in Spring Boot." },
      go: { title: "Middleware & JWT in Go", desc: "HTTP middleware chains; validating JWTs with golang-jwt." },
      flutter: { title: "Secure Storage & OAuth in Flutter", desc: "flutter_secure_storage; Google/Apple sign-in flows." },
      cloud: { title: "IAM Roles, Policies & Least Privilege", desc: "AWS IAM / Azure RBAC / GCP IAM — same model: who can do what to what." },
      devops: { title: "Secrets Management: Vault & AWS Secrets Manager", desc: "Never hardcode secrets; rotation, injection at runtime." },
      db: { title: "Row-Level Security & DB Users", desc: "PostgreSQL RLS, MongoDB RBAC — security inside the database." },
      python: { title: "Python Security: OWASP Basics", desc: "SQLi, CSRF, XSS in Python apps — using parameterized queries and CSP." },
    },
  },
  {
    day: 9,
    theme: "Testing",
    pattern: "The discipline of automated testing is language-agnostic. The tools differ; the philosophy doesn't.",
    concepts: {
      dsa: { title: "Testing Algorithmic Code", desc: "Edge cases, boundary values, property-based testing — test like an interviewer." },
      react: { title: "React Testing Library & Jest", desc: "Test behavior, not implementation — render, query, act, assert." },
      java: { title: "JUnit 5 & Mockito", desc: "@Test, @Mock, @InjectMocks — unit testing with mocking in Java." },
      go: { title: "Go testing Package & Table Tests", desc: "go test, t.Run() for subtests; table-driven tests as Go idiom." },
      flutter: { title: "Widget & Unit Tests in Flutter", desc: "testWidgets(), WidgetTester — testing Flutter UI components." },
      cloud: { title: "Testing Cloud Infra with LocalStack / Azurite", desc: "Run AWS/Azure services locally for integration tests without bills." },
      devops: { title: "Test Stages in CI: Unit → Integration → E2E", desc: "The test pyramid in a CI pipeline — fast feedback, confident deploys." },
      db: { title: "DB Testing: Migrations & Seeding", desc: "Flyway/Liquibase for migrations; test data seeding patterns." },
      python: { title: "pytest: Fixtures, Parametrize & Mocking", desc: "@pytest.fixture, @pytest.mark.parametrize, unittest.mock — Python testing mastery." },
    },
  },
  {
    day: 10,
    theme: "Scaling & Distributed Systems",
    pattern: "When one machine isn't enough — horizontal scaling, load balancing, and distributed data are universal problems.",
    concepts: {
      dsa: { title: "Consistent Hashing", desc: "Distributing data across nodes such that adding/removing nodes minimally reshuffles keys." },
      react: { title: "Code Splitting & Lazy Loading", desc: "React.lazy, Suspense — don't ship all JS upfront; scale frontend performance." },
      java: { title: "Spring Boot Microservices Basics", desc: "Service discovery, Feign clients, why you split a monolith." },
      go: { title: "Building a Load Balancer in Go", desc: "Round-robin proxying with net/http — understand load balancing by building one." },
      flutter: { title: "Pagination & Infinite Scroll in Flutter", desc: "Efficiently loading large datasets in mobile UI." },
      cloud: { title: "Auto Scaling + Load Balancers: ALB / AGW / GLB", desc: "Horizontal scaling automation across AWS/Azure/GCP." },
      devops: { title: "Kubernetes: HPA & Resource Limits", desc: "Horizontal Pod Autoscaler — K8s scaling based on CPU/memory metrics." },
      db: { title: "DB Sharding & Partitioning", desc: "Horizontal DB scaling — range, hash, and directory-based partitioning." },
      python: { title: "Celery & Distributed Task Queues", desc: "Offloading work to background workers; Redis/RabbitMQ as brokers." },
    },
  },
];

const PHASE_INFO = [
  { days: "1–30", label: "Phase 1", title: "Foundations", color: "#FF6B35", desc: "Core syntax, data structures, basic tooling across all 9 tracks." },
  { days: "31–90", label: "Phase 2", title: "Patterns", color: "#A78BFA", desc: "Design patterns, system design fundamentals, intermediate concepts." },
  { days: "91–180", label: "Phase 3", title: "Architecture", color: "#4ADE80", desc: "Distributed systems, advanced cloud, performance optimization." },
  { days: "181–365", label: "Phase 4", title: "Mastery", color: "#61DAFB", desc: "Interview prep, real projects, competitive programming, portfolio." },
];

export default function LearningTracker() {
  const [selectedDay, setSelectedDay] = useState(1);
  const [completedConcepts, setCompletedConcepts] = useState({});
  const [activeTrack, setActiveTrack] = useState(null);
  const [showPhases, setShowPhases] = useState(false);

  const dayData = CURRICULUM.find((d) => d.day === selectedDay) || CURRICULUM[0];

  const toggleConcept = (day, trackId) => {
    const key = `${day}-${trackId}`;
    setCompletedConcepts((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const isDone = (day, trackId) => !!completedConcepts[`${day}-${trackId}`];

  const dayProgress = TRACKS.filter((t) => isDone(selectedDay, t.id)).length;
  const totalProgress = Object.values(completedConcepts).filter(Boolean).length;

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0A0A0F",
      color: "#E8E8F0",
      fontFamily: "'DM Mono', 'Fira Mono', monospace",
      padding: "0",
    }}>
      {/* Header */}
      <div style={{
        borderBottom: "1px solid #1E1E2E",
        padding: "24px 32px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        background: "#0D0D15",
      }}>
        <div>
          <div style={{ fontSize: "10px", letterSpacing: "0.2em", color: "#6B6B8A", marginBottom: "4px" }}>DEEP LEARNING CURRICULUM</div>
          <div style={{ fontSize: "22px", fontWeight: "700", letterSpacing: "-0.02em", color: "#F0F0FF" }}>
            9 Tracks · Daily Concept Map
          </div>
        </div>
        <div style={{ display: "flex", gap: "24px", alignItems: "center" }}>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: "10px", color: "#6B6B8A", letterSpacing: "0.15em" }}>TOTAL DONE</div>
            <div style={{ fontSize: "28px", fontWeight: "700", color: "#A78BFA" }}>{totalProgress}</div>
          </div>
          <button
            onClick={() => setShowPhases(!showPhases)}
            style={{
              background: showPhases ? "#1E1E3A" : "transparent",
              border: "1px solid #2E2E4A",
              color: "#A78BFA",
              padding: "8px 16px",
              borderRadius: "6px",
              cursor: "pointer",
              fontSize: "11px",
              letterSpacing: "0.1em",
            }}
          >
            {showPhases ? "HIDE" : "ROADMAP"}
          </button>
        </div>
      </div>

      {/* Phase Roadmap */}
      {showPhases && (
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: "1px",
          background: "#1E1E2E",
          borderBottom: "1px solid #1E1E2E",
        }}>
          {PHASE_INFO.map((p) => (
            <div key={p.label} style={{ background: "#0D0D15", padding: "20px 24px" }}>
              <div style={{ fontSize: "9px", letterSpacing: "0.2em", color: p.color, marginBottom: "6px" }}>{p.label} · DAYS {p.days}</div>
              <div style={{ fontSize: "16px", fontWeight: "700", color: "#F0F0FF", marginBottom: "6px" }}>{p.title}</div>
              <div style={{ fontSize: "12px", color: "#6B6B8A", lineHeight: "1.5" }}>{p.desc}</div>
            </div>
          ))}
        </div>
      )}

      <div style={{ display: "flex", height: "calc(100vh - 81px)" }}>
        {/* Day Selector */}
        <div style={{
          width: "80px",
          borderRight: "1px solid #1E1E2E",
          background: "#0D0D15",
          overflowY: "auto",
          flexShrink: 0,
        }}>
          {CURRICULUM.map((d) => {
            const done = TRACKS.filter((t) => isDone(d.day, t.id)).length;
            const isActive = d.day === selectedDay;
            return (
              <button
                key={d.day}
                onClick={() => setSelectedDay(d.day)}
                style={{
                  width: "100%",
                  padding: "14px 0",
                  background: isActive ? "#1A1A2E" : "transparent",
                  border: "none",
                  borderLeft: isActive ? "2px solid #A78BFA" : "2px solid transparent",
                  cursor: "pointer",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: "4px",
                }}
              >
                <div style={{ fontSize: "10px", color: isActive ? "#A78BFA" : "#4A4A6A", letterSpacing: "0.1em" }}>DAY</div>
                <div style={{ fontSize: "18px", fontWeight: "700", color: isActive ? "#F0F0FF" : "#4A4A6A" }}>{d.day}</div>
                {done > 0 && (
                  <div style={{
                    width: "20px",
                    height: "3px",
                    background: "#4ADE80",
                    borderRadius: "2px",
                    opacity: done / 9,
                  }} />
                )}
              </button>
            );
          })}
          <div style={{ padding: "14px 0", textAlign: "center" }}>
            <div style={{ fontSize: "10px", color: "#2E2E4A" }}>···</div>
            <div style={{ fontSize: "9px", color: "#2E2E4A", marginTop: "4px" }}>365</div>
          </div>
        </div>

        {/* Main Content */}
        <div style={{ flex: 1, overflowY: "auto", padding: "28px 32px" }}>
          {/* Day Header */}
          <div style={{ marginBottom: "28px" }}>
            <div style={{ display: "flex", alignItems: "baseline", gap: "16px", marginBottom: "8px" }}>
              <div style={{ fontSize: "11px", color: "#A78BFA", letterSpacing: "0.2em" }}>DAY {selectedDay}</div>
              <div style={{ fontSize: "11px", color: "#2E2E4A" }}>·</div>
              <div style={{ fontSize: "11px", color: "#6B6B8A", letterSpacing: "0.1em" }}>THEME</div>
            </div>
            <div style={{ fontSize: "26px", fontWeight: "700", color: "#F0F0FF", letterSpacing: "-0.02em", marginBottom: "8px" }}>
              {dayData.theme}
            </div>
            <div style={{
              background: "#0D0D1A",
              border: "1px solid #1E1E3A",
              borderLeft: "3px solid #A78BFA",
              padding: "12px 16px",
              borderRadius: "0 6px 6px 0",
              fontSize: "13px",
              color: "#8A8AB0",
              lineHeight: "1.6",
              maxWidth: "680px",
            }}>
              💡 {dayData.pattern}
            </div>
          </div>

          {/* Progress Bar */}
          <div style={{ marginBottom: "28px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
              <div style={{ fontSize: "10px", color: "#6B6B8A", letterSpacing: "0.15em" }}>TODAY'S PROGRESS</div>
              <div style={{ fontSize: "10px", color: "#4ADE80" }}>{dayProgress} / {TRACKS.length} concepts</div>
            </div>
            <div style={{ height: "4px", background: "#1E1E2E", borderRadius: "2px" }}>
              <div style={{
                height: "100%",
                width: `${(dayProgress / TRACKS.length) * 100}%`,
                background: "linear-gradient(90deg, #A78BFA, #4ADE80)",
                borderRadius: "2px",
                transition: "width 0.3s ease",
              }} />
            </div>
          </div>

          {/* Track Filter */}
          <div style={{ display: "flex", gap: "8px", marginBottom: "20px", flexWrap: "wrap" }}>
            <button
              onClick={() => setActiveTrack(null)}
              style={{
                padding: "5px 12px",
                background: !activeTrack ? "#1E1E3A" : "transparent",
                border: "1px solid",
                borderColor: !activeTrack ? "#A78BFA" : "#2E2E4A",
                color: !activeTrack ? "#A78BFA" : "#4A4A6A",
                borderRadius: "20px",
                cursor: "pointer",
                fontSize: "10px",
                letterSpacing: "0.1em",
              }}
            >ALL</button>
            {TRACKS.map((t) => (
              <button
                key={t.id}
                onClick={() => setActiveTrack(activeTrack === t.id ? null : t.id)}
                style={{
                  padding: "5px 12px",
                  background: activeTrack === t.id ? "#1A1A2E" : "transparent",
                  border: "1px solid",
                  borderColor: activeTrack === t.id ? t.color : "#2E2E4A",
                  color: activeTrack === t.id ? t.color : "#4A4A6A",
                  borderRadius: "20px",
                  cursor: "pointer",
                  fontSize: "10px",
                  letterSpacing: "0.1em",
                }}
              >{t.emoji} {t.label.split(" ")[0]}</button>
            ))}
          </div>

          {/* Concept Cards */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "12px" }}>
            {TRACKS.filter((t) => !activeTrack || t.id === activeTrack).map((track) => {
              const concept = dayData.concepts[track.id];
              const done = isDone(selectedDay, track.id);
              return (
                <div
                  key={track.id}
                  onClick={() => toggleConcept(selectedDay, track.id)}
                  style={{
                    background: done ? "#0D1A12" : "#0D0D15",
                    border: "1px solid",
                    borderColor: done ? "#1A3A22" : "#1E1E2E",
                    borderRadius: "8px",
                    padding: "18px 20px",
                    cursor: "pointer",
                    transition: "all 0.2s ease",
                    position: "relative",
                    overflow: "hidden",
                  }}
                >
                  {/* Color accent bar */}
                  <div style={{
                    position: "absolute",
                    top: 0,
                    left: 0,
                    width: "3px",
                    height: "100%",
                    background: done ? "#4ADE80" : track.color,
                    opacity: done ? 1 : 0.6,
                  }} />
                  <div style={{ paddingLeft: "4px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
                      <div>
                        <div style={{ fontSize: "9px", letterSpacing: "0.2em", color: done ? "#4ADE80" : track.color, marginBottom: "3px" }}>
                          {track.emoji} {track.label.toUpperCase()}
                        </div>
                        <div style={{ fontSize: "15px", fontWeight: "600", color: done ? "#6B8A72" : "#E8E8F0", letterSpacing: "-0.01em" }}>
                          {concept.title}
                        </div>
                      </div>
                      <div style={{
                        width: "20px",
                        height: "20px",
                        borderRadius: "50%",
                        border: "1.5px solid",
                        borderColor: done ? "#4ADE80" : "#2E2E4A",
                        background: done ? "#4ADE80" : "transparent",
                        flexShrink: 0,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: "10px",
                        marginTop: "2px",
                      }}>
                        {done && "✓"}
                      </div>
                    </div>
                    <div style={{ fontSize: "12px", color: done ? "#3A5A42" : "#6B6B8A", lineHeight: "1.5" }}>
                      {concept.desc}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
