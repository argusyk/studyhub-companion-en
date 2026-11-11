# StudyHub architecture (a starting description for Lab 4)

> This is only a draft of context. In Lab 4 you will turn it into `docs/taxonomy.md`
> (a glossary of components and an architecture map).

StudyHub is a service for tracking a department's lab assignments: a student submits work, the instructor
checks it and assigns a score, and sees group statistics.

## Backend layers (apps/api)
`routers` (HTTP, prefix `/api/v1`) -> `services` (business logic) -> SQLAlchemy `Session`.
There is no separate `repositories` layer: queries are written in the services.

## Entities
Student, Lab, Submission. Grade (Chapter 8) and GradeAudit will appear later.

## Data and time
All points in time are stored in UTC. The instructor enters a deadline in department time
(Europe/Kyiv); the conversion happens at the API boundary.

## Frontend (apps/web)
Next.js 15 + TypeScript. Types are shared with `packages/shared`.
