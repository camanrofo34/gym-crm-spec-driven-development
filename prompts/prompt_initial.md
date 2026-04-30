IA utilizada: GPT-5.3

# Prompt Inicial - Spec Driven Development

You are a senior software engineer specialized in backend development, software architecture, and test-driven development.

Your task is to generate a complete, production-ready backend application based strictly on the provided specifications.

---

## Context

You are working under a Spec Driven Development (SDD) approach.

This means:
- ALL code must be derived from the specification files
- You MUST NOT invent features outside the spec
- You MUST implement ALL requirements explicitly defined
- You MUST ensure the implementation satisfies the business rules and validations

---

## Input Files

You will be provided with:

1. `specs/product.spec.md`
2. `specs/requirements.spec.json`

You must:
- Parse both files
- Extract entities, relationships, endpoints, constraints, and analytics requirements
- Use them as the ONLY source of truth

---

## Technical Requirements

Generate a backend application with the following stack:

- Language: Python
- Framework: FastAPI
- ORM: SQLAlchemy
- Database: SQLite
- Validation: Pydantic
- Testing: pytest

---

## Architecture Constraints

You MUST follow this modular architecture:

src/
- main.py
- api/
  - routes/
  - controllers/
- models/
- schemas/
- services/
- analytics/
- db/

Separation of concerns is REQUIRED:
- routes → HTTP layer only
- controllers → request/response orchestration
- services → business logic
- models → database structure
- schemas → validation (Pydantic)
- analytics → aggregation logic

---

## Functional Requirements

You MUST implement ALL features defined in the spec:

- Authentication (register, login)
- User management
- Trainer assignment
- Activity logging
- Analytics endpoints

Each endpoint must:
- Exist exactly as defined
- Validate inputs
- Return proper HTTP status codes
- Return JSON responses

---

## Business Rules Enforcement

You MUST strictly enforce:

- Unique email constraint
- Role validation (TRAINEE / TRAINER)
- No activity logging for inactive users
- No future dates for activities
- Activity duration must be > 0
- Valid trainer-trainee relationships

---

## Analytics Implementation

You MUST implement:

- Weekly trainer load (aggregation)
- User activity summary (count + average)
- Trainer ranking (sorted descending)

Analytics must:
- Be computed dynamically from stored data
- Use efficient queries (SQLAlchemy)

---

## Testing Requirements

You MUST generate:

- Unit tests
- Integration tests

Tests MUST cover:

- Success cases
- Validation failures
- Business rule violations
- Analytics correctness

Minimum coverage target: 80%

---

## Output Requirements

You MUST generate:

1. Complete project structure
2. All source code files
3. Database models
4. API routes
5. Validation schemas
6. Business logic (services)
7. Analytics module
8. Test suite (pytest)
9. Requirements file (requirements.txt)
10. Instructions to run the project

---

## Constraints

- Do NOT leave TODOs
- Do NOT generate pseudo-code
- Do NOT omit tests
- Do NOT skip validations
- Do NOT simplify analytics logic

---

## Quality Expectations

The code must be:

- Clean and modular
- Runnable without modification
- Consistent with the spec
- Properly structured
- Ready for local deployment

---

## Final Instruction

Generate the FULL backend project.

Ensure that:
- All requirements are implemented
- All endpoints are functional
- All tests pass conceptually
- The system is aligned with the provided specifications

Do not provide explanations outside the code unless necessary.