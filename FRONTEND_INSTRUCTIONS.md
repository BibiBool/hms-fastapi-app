# Frontend Implementation Guide: Healthcare Appointment Service

## Project Context

We are building a lightweight frontend for a FastAPI backend using `fastapi-users`. 
- **Backend URL**: http://localhost:8000
- **Auth Provider**: fastapi-users (SQLAlchemy/SQLite)
- **Registration Endpoint**: POST `/auth/register`

## Frontend Requirements

The frontend consists of a simple registration flow using the existing files in `/static`.

### 1. Registration Page (index.html)

- Create a clean, professional healthcare-themed form.
- **Fields required by backend**:
  - `full_name` (String)
  - `email` (String)
  - `password` (String)
  - `is_active` (Boolean, default true)
  - `is_superuser` (Boolean, default false)
  - `is_verified` (Boolean, default false)

### 2. Logic (script.js)

- Intercept the form submission.
- Send a JSON payload to `http://localhost:8000/auth/register`.
- **Success Handling**: On a 201 Created response, hide the form and display a "You are registered" message.
- **Error Handling**: Display validation errors (e.g., 400 Bad Request if the user already exists).

### 3. Styling (style.css)

- Use a clean "Medical/Healthcare" color palette (Blues, Whites, Light Greys).
- Ensure the form is centered and responsive.
