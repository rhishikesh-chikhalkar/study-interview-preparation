---
name: interview-preparation
description: Use when documenting engineering challenges, solutions, and decisions for interview preparation. Covers the Shadow Logger protocol, senior-level narrative writing, and schema/metadata tracking.
---

# Interview Preparation & Documentation Protocol

---

## 1. The "Shadow Logger" Rule

Every time a significant bug is fixed or a complex feature is completed, you **MUST** prompt the user:

> *"Would you like me to document this in CHALLENGES_AND_SOLUTIONS.md for your interview prep?"*

---

## 2. Constraint Enforcement (Senior-Level Narrative)

When documenting in `CHALLENGES_AND_SOLUTIONS.md`, use high-level engineering terminology and professional narrative structures:

- **Terminology**: Use terms like "Asynchronous I/O," "Horizontal scaling," "State persistence," "Atomic transactions," "Lazy loading," "Middleware," and "Protocol-level compliance."
- **Focus**: Focus on the "Why" and the architectural impact, not just the code syntax. Highlight decision-making and trade-offs.

---

## 3. Metadata & Schema Tracking

Ensure that new features are explicitly linked to their corresponding database schema changes or infrastructure modifications in the documentation. Mention specific SQLAlchemy models or migration impacts when relevant.
