# 18 — Oversight / Governance Hub API

- **Repo**: `qrt-qh-oversight-governance-api` (aka `qrt-qh-platform-oversight-api`)
- **Stack**: Java + Spring Boot, Spring Web (REST), Spring Data JPA, Spring Security, MapStruct, Spring Cache, springdoc OpenAPI, PostgreSQL
- **Your Role**: Contributor / exposure — this is a Java service, not part of your Python resume.

> **Honesty note (read first)**
>
> This repo is Java/Spring Boot, not Python/FastAPI. Your resume is deliberately Python-focused, so:
>
> - **If you did meaningful work here**: Position it as "I also contributed to a Spring Boot platform service" — a credible full-stack/polyglot signal.
> - **If you only had light exposure**: don't over-claim. Mention it as "our platform's governance API, which I integrated with / read from" rather than "I built it." Interviewers catch inflated Java claims fast when the rest of your story is Python.
>
> Use this file to (a) understand the service so you can speak to it, and (b) show you can reason about backend design in a language you don't primarily use.

## Snapshot (30-second pitch)
"A Spring Boot governance/oversight API for the QuantHub platform — it models the app portal (applications, categories, sections, tiles, navigation), tracks per-user usage, and manages user preferences and access. It's a layered Spring service: REST controllers → services → Spring Data JPA entities on PostgreSQL, with MapStruct DTO mapping, Spring Security, caching, and OpenAPI docs."

---

## What it does (from the code structure)

- **Controllers**: `ContentController`, `NavigationController`, `PortalController`, `TimeSeriesController`, `UsageController`, `HealthController` — REST endpoints for portal content, navigation, usage, and time-series governance data.
- **Entities (JPA)**: `Application`, `Category`, `Group`, `Section`, `Tile`, `UserPreferences`, `UserUsage` — mapped to PostgreSQL (`db-scripts/ddl.sql`, `dml.sql`).
- **Config**: `SecurityConfig` (Spring Security), `CacheConfig` (Spring Cache), `MapperConfig` + `ConverterImpl` (MapStruct entity↔DTO mapping), OpenAPI config.
- **Cross-cutting**: `GlobalExceptionHandler` for consistent error responses.

---

## Transferable talking points (backend design, language-agnostic)

- **Layered architecture**: Controller → Service → Repository/Entity is the same separation you use in FastAPI (router → service → db layer). You can speak to why that layering matters regardless of language.
- **DTO mapping (MapStruct) vs Pydantic**: Spring uses MapStruct to convert JPA entities to API DTOs; in FastAPI you use Pydantic response models. Same principle — never expose your persistence model directly in the API.
- **Spring Cache vs your Redis cache**: `CacheConfig` is the declarative-annotation equivalent of the Redis caching you hand-rolled in the Holding Analyzer (project 09).
- **Global exception handler vs FastAPI exception handlers**: Both centralise error-to-HTTP mapping so endpoints don't leak stack traces.
- **springdoc OpenAPI vs FastAPI's built-in docs**: Both publish a machine-readable API contract.

---

## Likely Follow-up Q&A

- **Q: You mostly do Python — how comfortable are you in this Java service?**
  - **A**: I'm Python-first, but backend design transfers: this is a standard layered Spring Boot service — controllers, JPA entities on PostgreSQL, MapStruct DTO mapping, Spring Security, and declarative caching. I can read it, reason about it, and map each piece to its FastAPI equivalent (router/Pydantic/dependency-injection/Redis). *(Then be honest about your actual contribution level.)*

- **Q: How does Spring Data JPA differ from what you use (SQLAlchemy)?**
  - **A**: Both are ORMs mapping classes to tables. JPA leans on repository interfaces + annotations and a managed persistence context; SQLAlchemy is more explicit about sessions and queries. Same goal — object-relational mapping with a unit-of-work/session boundary.

- **Q: Would you have built this in Python?**
  - **A**: For a platform-standard, strongly-typed enterprise service in a Java estate, Spring Boot is a reasonable fit. My services are Python/FastAPI where async I/O and Pandas-heavy analytics dominate. The right tool depends on the team's platform and the workload.
