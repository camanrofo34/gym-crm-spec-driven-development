IA utilizada: GPT-5.3

# Prompt - Frontend Generation Sprint (Spec Driven Development)

You are a senior frontend engineer specialized in React, TypeScript, dashboard systems, API integrations, and scalable UI architecture.

Your task is to generate a complete frontend application that consumes an already existing backend API previously generated through Spec Driven Development.

This is NOT a backend refinement task.

This is a second product iteration focused on building the client layer on top of an already functional REST API.

---

# Development Context

The backend already exists and includes:

- Authentication endpoints
- User management
- Trainer assignment
- Activity logging
- Analytics endpoints

You MUST reuse the existing product specifications and backend contract.

You MUST NOT redesign the backend.

You MUST consume the existing API as source of truth.

---

# Input Files

Use these files as context:

1. `specs/product.spec.md`
2. `specs/requirements.spec.json`

Use them to understand:

- domain entities
- business flows
- analytics meaning
- user roles
- expected data structures

Additionally, assume backend endpoints are already implemented exactly as specified.

---

# Technical Stack

Generate frontend using:

- React
- TypeScript
- Vite
- Axios
- React Router
- Recharts (for charts)
- CSS Modules or clean modular CSS

---

# Output Project Structure

Generate a professional structure:

frontend/
src/
- main.tsx
- App.tsx
- router/
- pages/
- components/
- layouts/
- services/
- hooks/
- types/
- styles/

---

# Required Screens

## 1. Authentication

### Login Page
- email
- password
- login button

### Register Page
- email
- password
- role selector:
  - TRAINEE
  - TRAINER

---

## 2. Dashboard (Main Value)

Create a professional analytics dashboard consuming backend endpoints.

Include:

### KPI Cards

- Total Users
- Total Activities
- Average Duration
- Active Trainers

### Charts

#### Trainer Ranking
Bar chart using:

GET /analytics/trainer-ranking

#### Weekly Trainer Load
Line or bar chart using:

GET /analytics/trainer-load

#### User Activity Summary
Pie chart or table using:

GET /analytics/user-summary

---

## 3. Users Page

- list users
- status badge (active/inactive)
- role badge
- search by email

Use:

GET /users

---

## 4. Activities Page

- create activity form
- list activity history
- filters by type/date

Use:

POST /activities
GET /activities

Fields:

- user_id
- duration_minutes
- activity_type
- date

---

## 5. Assignments Page

- assign trainer to trainee
- list assignments

Use:

POST /assignments
GET /assignments

---

# UI/UX Requirements

The UI must be modern and clean.

Use:

- sidebar navigation
- top navbar
- responsive cards
- spacing consistency
- professional admin dashboard style

Avoid generic ugly UI.

---

# State Management

Use:

- React hooks
- Context only if needed
- local state preferred

---

# API Layer

Create reusable API client:

src/services/api.ts

Must include:

- baseURL config
- axios instance
- reusable methods

---

# Type Safety

Create TypeScript interfaces for:

- User
- Activity
- TrainerLoad
- RankingItem
- UserSummary

---

# Error Handling

Implement:

- loading states
- empty states
- error messages
- form validation

---

# Constraints

- Do NOT modify backend assumptions
- Do NOT generate backend code
- Do NOT use mock data unless necessary fallback
- Do NOT skip charts
- Do NOT skip routing
- Do NOT skip the responsive layout

---

# Quality Expectations

Code must be:

- production-style
- modular
- readable
- reusable
- ready to run

---

# Final Deliverables

Generate:

1. Full React project structure
2. All pages
3. Components
4. API integration layer
5. Charts dashboard
6. Routing
7. Styling
8. Instructions to run

---

# Final Instruction

Generate the COMPLETE frontend application integrated with the existing backend API.

This frontend must transform the backend into a usable product with strong analytical visualization value.