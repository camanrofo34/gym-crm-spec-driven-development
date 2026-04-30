# Product Specification - Gym Analytics Management API

## 1. Overview
This system provides a REST API for managing gym users (trainees and trainers), tracking physical activities, and generating analytical metrics based on user performance and trainer workload.

The system is designed following a Spec Driven Development (SDD) approach, where all functionalities must strictly comply with the defined requirements.

---

## 2. Actors

### 2.1 Trainee
- Registers in the system
- Logs activities
- Can be assigned to one or more trainers
- Views personal activity history

### 2.2 Trainer
- Registers in the system
- Monitors trainee activities
- Has performance metrics calculated based on trainee activity

---

## 3. Core Features

### 3.1 Authentication
- Users must register before accessing the system
- Login is required for all protected endpoints

---

### 3.2 User Management
- Create user (trainee or trainer)
- Activate/deactivate user
- Update profile information

---

### 3.3 Trainer Assignment
- A trainee can be assigned to multiple trainers
- A trainer can have multiple trainees

---

### 3.4 Activity Logging
- Users can log activities with:
  - duration (minutes)
  - date
  - type (cardio, strength, etc.)
- Activities must belong to a valid user

---

### 3.5 Activity Visualization
- Users can retrieve their activity history
- Trainers can view activities of assigned trainees

---

## 4. Analytics Features

### 4.1 Weekly Trainer Load
- Total duration of activities associated with a trainer per week

### 4.2 User Activity Summary
- Total number of activities per user
- Average duration per activity

### 4.3 Trainer Ranking
- Trainers ranked by total weekly activity duration

---

## 5. Business Rules

- Users must have unique email addresses
- Inactive users cannot log activities
- Activities cannot have negative duration
- Activity dates cannot be in the future
- A trainee must exist before assigning a trainer
- Metrics must be calculated dynamically from stored data

---

## 6. Non-Functional Requirements

- The system must expose a REST API
- The system must validate all inputs
- The system must include automated tests
- The system must be deployable locally
- The system must provide API documentation (OpenAPI)

---

## 7. Expected Endpoints (High-Level)

### Auth
- POST /auth/register
- POST /auth/login

### Users
- GET /users
- PUT /users/{id}
- PATCH /users/{id}/activate

### Activities
- POST /activities
- GET /activities

### Analytics
- GET /analytics/trainer-load
- GET /analytics/user-summary
- GET /analytics/trainer-ranking