# Oversight Governance API

Acie i i

18 — Oversight / Governance Hub API

Repo: qrt~qh-oversight—governancé-api (aka. qrt-qh-platform-o ight=api) Stack: Java + Spring Boot, Spring Web (REST), Spring Data JPA. Spring Security, MapStruct, Spring Cache, springdoc
OpenAPI, PostgreSQL Your role: Contributor / exposure — this is a Java service, not part of your Python resume. (=

Ay Honesty note (read first)

This repo is Java/Spring Boot, not Python/FastAPI. Your resume is deliberately Python-focused, so: : =

* Ifyou did meaningful work here: Position it as "I also contributed to a Spring Boot platform service" — a credible full-stack/polyglot signal.

* Ifyou only had light exposure: don't Over-claim. Mention it as “our platform's governance API, which | integrated with / read from” rather than "I built it.” Interviewers catch inflated Java claims fast when the rest of your
story is Python.

Use this file to (a) understand the service so you can speak to it, and (b) show you can reason about backend design in a language you don't primarily use. : =

Snapshot

“A Spring Boot governa nce/oversight AP! for the QuantHub platform — it models the app portal (applications, categories, sections, tiles, navigation), tracks per-user usage, and manages user preferences and access. tsa
layered Spring service: REST controllers > services > Spring Data JPA entities on PostgreSQL, with MapStruct DTO mapping, Spring Security, caching, and OpenAPI docs.”
a) =

What it does (from the code structure)

* Controllers: ContentController, NavigationController, PortalControllé meSeriesController, UsageController, HealthController — REST endpoints f

portal content, navigation, usage, and time-series governance data. it “
* Entities (JPA): Application, Category, Group, Section, Tile, User references, UserUsage — mapped to PostgreSQL (db=seripts/ddll, sql. dmi/sqi).
* Config: SecurityConfig (Spring Security), CacheConf ig (Spring Cache), Mapper onfig + Co ter /ConverterImpl (MapStruct entity+DTO mapping), OpenAp:

* Cross-cutting: GlobalExceptionHandler for consistent error responses.

ntroller, T

Transferable talking points (backend design, language-agnostic)

* Layered architecture: Controller + Service > Repository/Entity is the same separation you use in FastAPI| (router — service — db layer). You can speak to why that layering matters regardless of language.

* DTO mapping (MapStruct) vs Pydantic: Spring uses MapStruct to convert JPA entities to API DTOs; in FastAPI you use Pydantic response models. Same principle — never expose your persistence model di
API. E :

* Spring Cache vs your Redis cache: CacheConfiig is the declarative-annotation equivalent of the Redis caching you hand-rolled in the Holding Analyzer (project 09). Wis

* Global exception handler vs FastAPI exception handlers: both centralise error-to-HTTP mapping so endpoints don't leak stack traces.

* springdoc OpenAPI vs FastAPI's built-in docs: both publish a machine-readable API contract.

: O ORA


ae than 4) Rett i " si
aa Ny fue _——— a EE lh ) ‘gira yt

Likely follow-up Q&A

Q: You mostly do Python — how comfortable are you in this Java service? A: |'m Python-first, but backend design transfers: this is a standard layered Spring Boot service — controllers, JPA entities on PostgreSQL, MapStruct
DTO mapping. Spring Security, and declarative caching. | can read it, reason about it, and map each piece to its FastAPI equivalent (router/Pydantic/dependency-injection/Redis). [Then be honest about your actual contribution
level.)

Q: How does Spring Data JPA differ from what you use (SQLAIchemy)? A: Both are ORMs Mapping classes to tables. JPA leans on fepository interfaces + annotations and a managed persistence context; SQLAIchemy is
more explicit about sessions and queries. Same goal — object-relational mapping with a unit-of-work/session boundary.

Q: Would you have built this in Python? A: Fora platform-standard, strongly-typed enterprise service in a Java estate, Spring Boot is a reasonable fit. My services are Python/FastAPI where async I/O and Pandas-heavy,
analytics dominate. The right tool depends on the team’s platform and the workload.



>


& DO =

99 — Cross-Cutting Themes (the rapid-fire tech screen)

These are the resume bullets and skills that span every repo — the questions you'll get in a tech screen regardless of which project comes up. Each theme has: the claim, the real evidence, the why, and the follow-ups,

1, Docker & AWS EKS deployment

Claim: "Containerised backend services with Docker and deployed on AWS EKS.”

Evidence: Every repo has hélm—chart/, codebuild/. and a multi-stage |Doeker file), Services run as EKS Deployments; batch jobs run as Kubernetes CronJobs; config via ConfigMaps; secrets via AWS Secrets Manager __
(SecretProviderClass).

Why multi-stage Docker? A builder stage compiles/installs dependencies; the runtime stage copies only what's needed — smaller, more secure images (no build tools, fewer CVEs). The firm uses Chainguard base images
which are distroless — so CMD must be exec form (L*python", "=m", . 11), not shell form, because there's no shell at runtime.

Follow-ups:

* Q: Deployment vs Cronlob — when each? Long-running services (APIs) = Deployment; scheduled batch (data pipelines, reports) = CronJob with retries and history.
© Q: How do secrets reach the pod? AWS Secrets Manager — SecretProviderClass (CSI) + mounted as env; never in the image or ConfigMap. Non-sensitive config (hosts, ports, flags) - ConfigMap/Helm values.
* Q: How do you roll back? Helm rollback / redeploy previous image tag; for data jobs, re-run the prior known-good (and | keep archived prior versions, e.g. the pre-Databricks cronjob). iy

2. CI/CD (AWS CodeBuild / CodePipeline, GitHub Actions)

Claim: “Built Cl/CD pipelines across 10+ apps/APls/cron jobs, enforcing quality gates."

Evidence: codebuild/buildspec_ x. ym1 per repo (build-develop, build-release, deploy-develop, deploy-prod); Prisma/Twistlock container scanning; SonatypelQ/Nexus dependency scanning.
Why quality gates? Block unstable/vulnerable code from prod automatically — security scans (Prisma for containers, Nexus IQ for dependencies), tests, and build success are gates, not suggestions.
Follow-ups:

* Q: Dev = Prod with no QA? Correct — this estate is Dev — Prod. So gates and tests carry more weight, and prod deploys are deliberate.
* Q: What triggers a build? Merge to the relevant branch (develop/release) triggers CodeBuild — image build + scan + deploy to the target EKS cluster.

3. PostgreSQL optimisation

Claim: “Optimised PostgreSQL queries, indexing, and schemas — ~40% faster API responses.” 4

Evidence / how to defend the 40%: Be ready to explain the mechanism: added indexes on columns used in WHERE / JOIN/ ORDER BY, avoided N+1 queries, selected only needed columns, and pushed aggregation into SQL |

instead of doing it in Pandas. Measured via before/after response times (the timing middleware in the Portfolio Metrics API logs durations).

Why these techniques?


