# Project Management Tool: Real-Time Collaborative Platform

## 1. Project Goal & Overview

The objective of this project is to build a modern, real-time Minimum Viable Product (MVP)
for a collaborative project management tool. Our focus is on delivering a robust, performant
API backend and a dynamic, responsive frontend.

---

## 2. Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend API** | **FastAPI (Python)** | High performance, rapid development, and Python ecosystem. |
| **Frontend UI** | **SvelteKit** | Modern framework for performance and ease of development. |
| **Database** | **MySQL** | Reliable, robust relational database for structured project data. |
| **Real-time** | **WebSockets** | For instant task/progress updates across all user sessions. |
| **Dashboard** | **chart.js** | Used for advanced, potentially experimental 3D data visualization. |
| **Containerization** | **Docker** | Ensures consistent development environments for the entire team. |

---

## 3. Core MVP Feature Breakdown

Our initial focus is on five key modules:

1.  **User & Auth:** Registration, Login, Profile.
2.  **Project Management:** CRUD for Project entities.
3.  **To-Do List:** CRUD for Task entities, due dates, priority, assignment.
4.  **Notes/Documents:** Simple markdown/text notes linked to a Project.
5.  **Dashboard:** Personalized view of aggregated data (overdue tasks, progress).

---

## 4. Mandatory Developer Rules & Guidelines (MUST READ)

These rules are non-negotiable and apply to everyone, regardless of experience.

### 4.1. Code Quality & Formatting
* **Use Linters & Formatters:** Every developer **must** install and use **Black** (for Python)
    and **Prettier** (for JavaScript/SvelteKit). Code must be formatted before every commit.
* **No Unused Imports:** Remove all unused variables, functions, and imported libraries before committing.
* **Principle of Least Privilege:** APIs that read data should **only** allow GET requests. APIs
    that create/update/delete should be protected with appropriate permissions/authentication.

### 4.2. Contribution Rules (Branching & Merging)
* **Main Branch Protection:** The `main` branch is protected and contains only stable, production-ready
    code. **NO DIRECT PUSHES TO `main` ARE ALLOWED.**
* **Separate Branches:** All work must be done on a new feature or fix branch.
    * **Naming Convention:** Use `feature/<short-description>` (e.g., `feature/task-crud`)
        or `fix/<issue-number>-<short-fix-name>` (e.g., `fix/15-login-bug`).
* **Pull Requests (PRs):**
    1.  Always create a Pull Request from your feature branch back into `main`.
    2.  The PR **must** pass all automated tests (if implemented).
    3.  A PR is **not** merged until all requested changes are resolved and approved.

### 4.3. Commit Message & Tagging Convention
We will use clear **lowercase tags** in our commit messages and GitHub Issues.

| Tag/Label | Purpose | Example |
| :--- | :--- | :--- |
| **(imp)** | **improvement:** Refactoring, cleanup, or non-feature-breaking changes. | `[imp] refactor database connection in utils.py` |
| **(feat)** | **feature:** A new user-facing functionality (e.g., Project Creation). | `[feat] add POST endpoint for creating new projects` |
| **(fix)** | **bug fix:** A correction to broken, unintended, or incorrect behavior. | `[fix] resolve 404 error on /tasks/ list endpoint` |
| **(docs)** | **documentation:** Changes related to README, contributing guide, or API documentation. | `[docs] update local setup instructions in README` |
| **risk** | **High-Risk/Complex:** Used as a **GitHub Issue Label** for tasks involving complex logic, security, or core infrastructure. These require mandatory review. | *Issue Label: risk* |

### 4.4. Commenting Guidelines
* **What to Comment:** Focus comments on the **WHY** and **HOW** of complex logic. Do not
    comment on the obvious.
    * **Good Comment:** `# Check if the task is overdue based on server time, not client time, to prevent drift.`
    * **Bad Comment:** `# Define a new function (Obvious)`
* **Docstrings:** Every function, class, and method **must** have a docstring that explains
    its purpose, arguments, and return type.

---

## 5. Team Roles and Responsibilities

This project uses a layered approach to development. Each team member is expected to focus
on their primary role but also assist others when necessary.

| Role | Responsibility Focus | Technical Ownership |
| :--- | :--- | :--- |
| **The Architect / Technical Lead** | Final say on API design, overall structure, and code review gatekeeper. | Docker Setup, CI/CD, Core API Security/Permissions. |
| **Database & Backend Programmer** | Data Model integrity, efficient query design (MySQL), and internal logic. | FastAPI Routers for Project and Task CRUD, Pydantic Schema Definitions. |
| **The Frontend Developer** | User experience (UX) and User Interface (UI) implementation. | SvelteKit Components, Routing, State Management, API Integration (fetch calls). |
| **Dashboard & Data Visualizer** | Advanced frontend visualization and data aggregation logic. | Chart.js implementation, API endpoints for aggregated progress data. |
| **The Tester/DevOps** | Ensure quality and consistent environments. | Writing automated tests (e.g., pytest), maintaining the Docker setup. |

---

## 6. Development Utilities & Environment

### A. Prerequisite
- **Python 3.11**
- **Docker**
- **Git**
- **Node.js 20**

### B. Environment Setup
1.  **Clone the Repository:**
    ```bash
    git clone git@github.com:Stacks-Full/project-management-tool.git
    ```
2.  **Configure Environment:** Create a `.env` file by copying `env.example`.
    **DO NOT** commit `.env` to Git.
    ```bash
    cp env.example .env
    ```
3.  **Use Docker (The Standard Environment):** We use Docker Compose.

    * **First-Time Setup (Build & Run):**
        ```bash
        docker compose up --build -d
        ```
    * **Check Container Status:**
    ```bash
        docker compose ps
    ```
    * **Subsequent Runs (Start/Stop):**
        ```bash
        docker compose start
        docker compose stop
        ```

4.  **Access the Application:**
    * **Frontend:** `http://localhost:5173`
    * **Backend API:** `http://localhost:8000`
    * **API Docs (Swagger):** `http://localhost:8000/docs`


### C. Testing & Documentation
* **Testing:** We will use **Pytest** for backend testing. Always write tests for new complex logic.
* **API Documentation:** FastAPI provides automatic API documentation (Swagger UI/ReDoc).
    Access it via `/docs` or `/redoc` when the server is running. Ensure your Pydantic schemas and
    docstrings are clear to make this documentation valuable.

---

## 7. Critical Team Policies

### 7.1. ("Ask First" Rules )
To protect the core architecture, the following changes **MUST** be discussed and approved before any code is written:

1.  **Changing a Database Model:** Adding, removing, or changing a field in our core data models (e.g., `Project`, `Task`, `User`).
2.  **Adding a New Library:** Installing any new Python, Node, or Svelte library/dependency.
3.  **Authentication/Permission Logic:** Any changes to how users log in, how tokens are managed, or how permissions are checked.

### 7.2. Definition of Done (DoD) for a Pull Request
A Pull Request **is not ready for review** (and definitely not ready to merge) until **ALL** of the following are true:

1.  The code runs successfully in the developer's local Docker environment.
2.  All automated tests (Pytest/other) related to the change pass.
3.  The feature/fix has been manually tested and works as described in the original GitHub Issue.
4.  There are **no unused imports, code is formatted (Black/Prettier),** and all functions have proper docstrings.
5.  All **Git conflicts** have been resolved by the author of the PR.

### 7.3. Handling Conflict (Code or otherwise)
* **Merge Conflicts:** If Git reports a conflict when trying to push or merge, **DO NOT** force push. Ask for help. Resolving conflicts is a key learning point.
* **Task Conflicts:** If two people start working on the same feature, immediately stop, notify the team, and decide how to **split the task** (e.g., one writes the schema, the other writes the view). Never work on the same file simultaneously without a clear plan.

---

## **Note to the Team**

> "Welcome to the project! This is a great opportunity to learn modern full-stack development.
> We are here to help each other. If you get stuck, don't waste more than 30 minutes. Post your
> question in our group chat, and include your code, the full traceback, and what you have
> already tried. **Ask before you code if you are unsure of the API contract.** We will win as a team."



