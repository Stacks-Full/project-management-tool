# Project Management Tool  - Stacks Full


## 1. Project Goal
To build a collaborative, real-time project management web application (an MVP) for a small
team (4-5 users), focusing on core features: To-Do List, Collaborative Notes, and Progress Tracking.

---

## 2. Minimum Viable Product (MVP) Feature Breakdown

| Module | Core Features | Focus |
| --------------- | --------------- | --------------- |
| 1. User & Auth | User registration, login, and simple profile management. | Authentication/Authorization. Ensure users can only access projects they belong to.|
| 2. Project and management | CRUD a project Title, Description, start/end dates, collaborator assigned | Core Django Model Design and API/View Implementation.|
| 3. To Do List | CRUD tasks, set a due date, status | Backend Logic and APIs and ensure efficient data retrieval and updates. |
| 4. Notes/ Documents | Simple text editor to create project notes. | Full-Stack Feature Integration. Handle the model and the frontend form/display logic for creating and showing notes. |
| 5. Dashboard | A single page showing project progress, task assigned, summary | Data Aggregation and Frontend Presentation |




### Module 1: User & Authentication Profiles (Security Focus)
* **Must-Have:** User Registration, Login, Logout
* **Must-Have:** Simple User Profile page.
* **Key Security Task:** Enforce permissions for Project/Task access.

### Module 2: Project Management
* **Must-Have:** CRUD (Create, Read, Update, Delete) functionality for Projects.
* **Data Fields:** Title, Description, Start/Due Date, Status.
* **Association:** Ability to assign multiple **Team Members (Users)** to a Project.

### Module 3: To-Do List
* **Must-Have:** CRUD functionality for individual Tasks, linked to a Project.
* **Data Fields:** Task Title, Description, Due Date, Priority.
* **Workflow:** Task Status field (`Todo`, `In Progress`, `Done`).
* **Assignment:** Ability to assign a Task to a single **User**.

### Module 4: Notes/Documents
* **Must-Have:** Simple form to create markdown/text-based **Notes** attached to a Project.
* **Feature:** Display all Notes on the Project Detail view.

### Module 5: Dashboard & Progress Tracking
* **Must-Have:** A landing page that displays critical, aggregated data for the user.
* **Data Display:**
    1.  List of all Projects the user is a member of.
    2.  List of **Tasks assigned to the current user** that are overdue.
    3.  Simple progress metric (X out of Y tasks completed).

---




## 3.  Role Allocation

### 1. The Architect (for full stack)
### 2. The Database & Backend Programmer
### 3. The Frontend 
### 4. The Dashboard & Data Visualizer
### 5. The Tester/DevOps
