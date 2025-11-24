# API Specification Contract (v1)
This document defines the complete API contract for the Project Management Tool MVP.

## Global API Standards

### Base Path
Example: POST to `/api/v1/auth/register`
all endpoints will be prefixed with `/api/v1`.


### HTTP Status Codes

| Code | Status | Description |
| :--- | :--- | :--- |
| **200** | OK | Success request(`GET`, `PUT`, `DELETE`) |
| **201** | Created | Resource successfully created (`POST`) |
| **204** | No Content | Successful request, but no body returned (eg: Logout) |
| **400** | Bad Request | The server cannot or will not process the request due to Client-side input validation error |
| **401** | Unauthorized | Authentication token is missing or invalid |
| **403** | Forbidden | User is authenticated but lacks permission to access the resource |
| **404** | Not Found | Requested resource does not exist |
| **500** | Internal Server Error | Server side unexpected error |



### Standard Error Response Structure
All non-success responses (4xx, 5xx) should return a JSON body with the following
structure for consistency:

- **Example of a 403 Forbidden error response:**
```json
{
  "status": "error",
  "code": 403,
  "message": "Permission denied. You must be a collaborator or owner to perform this action.",
  "details": null // Optional: for showing specific validation errors (eg: missing fields)
}
```

---

<br>

## 1. Authentication Module

This module handles user registration, login, and session management.

### 1.1. Register User

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/auth/register` |
| **Method** | `POST` |
| **Authentication** | None  |
| **Permissions** | Any user can register |

#### Request Body Schema

Based on the `users` table ( `full_name`,`username`, `email`, `hashed_password`):

```json
{
  "full_name": "string (max 30 chars)",
  "username": "string (unique)",
  "email": "string(email format)" 
  "password": "string (min 8 chars)"
}
```

#### Successful Response (201 Created)

Returns the newly created user's profile (excluding the password hash).

```json
{
  "user_id": 1,
  "full_name": "Test User Name",
  "username": "testuser",
  "email": "testuser@email.com" 
  "created_at": "2025-11-24T14:30:00Z"
}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **400** | Bad Request| Missing required fields (username, password) or password too short |
| **400** | Bad Request| Username already exists |




### 1.2. Login User

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/auth/login` |
| **Method** | `POST` |
| **Authentication** | None  |
| **Permissions** | Any user can attempt to log in|


#### Request Body Schema

```json
{
  "username": "string",
  "password": "string"
}
```


#### Successful Response

Returns an access token required for all subsequent authenticated requests.

```json
{
  "status": "success",
  "token_type": "bearer",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MzQ0OTg0MDB9.EXAMPLE_JWT_TOKEN"
}
```

#### Error Response

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Invalid username or password combination|
| **400** | Bad Request| Missing required fields(`username` or `email`, `password`)|




### 1.3. Get Current User Profile 

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/auth/me` |
| **Method** | `GET` |
| **Authentication** | Required (Bearer Token)|
| **Permissions** | Must be logged in|



#### Successful Response

Returns the profile of the user associated with the provided access token.

```json
{
  "user_id": 1,
  "full_name": "Test User Name",
  "username": "testuser",
  "email": "testuser@email.com",
  "created_at": "2025-11-24T14:30:00Z"
}
```

#### Error Response

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or expired access token|






### 1.4. Logout User 

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/auth/logout` |
| **Method** | `POST` |
| **Authentication** | Required (Bearer Token)|
| **Permissions** | Must be logged in|



#### Successful Response

No response body is returned upon successful logout/token invalidation or,

```json
// Optional message(alert)
{
    "message": "Successfully logged out"
}
```

#### Error Response

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or expired access token|



---

<br>

## 2. Projects Module

This module handles the creation, retrieval, updating, and deletion of projects, and
management of project members.

### 2.1. Create a New Project

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/projects/` |
| **Method** | `POST` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | Any authenticated user can create a project. The creator is automatically set as the `project_owner`. |

#### Request Body Schema

Based on the `projects` table:

```json
{
  "project_name": "string (max 30 chars)",
  "description": "string (optional)",
  "start_date": "datetime (YYYY-MM-DD)",
  "end_date": "datetime (YYYY-MM-DD)",
  "status": "string (eg: 'Planning', 'In Progress', 'Completed')"
}
```

#### Successful Response (201 Created)

Returns the created project details. The backend must also automatically insert a record
into the `project_roles` table, setting the current user as the owner.

```json
{
  "project_id": 5,
  "project_name": "My New Project",
  "project_owner": 1, // The ID of the user who created it
  "status": "Planning",
  "start_date": "2025-12-01",
  "end_date": "2026-03-01"
  // ... other fields
}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **400** | Bad Request| Missing required fields (eg: project_name) or invalid dates|



### 2.2. List User's Project

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/projects/` |
| **Method** | `GET` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be associated with the project via `project_roles`|


#### Successful Response (200 OK)

Returns an array of projects the user is associated with.

```json
[
  {
    "project_id": 5,
    "project_name": "New Project Alpha",
    "project_owner": 1,
    "user_role": "owner", // Added field to show the user's role in this project
    "status": "Planning"
    // ... other project fields
  },
  {
    "project_id": 8,
    "project_name": "Beta Feature Development",
    "project_owner": 3,
    "user_role": "collaborator",
    "status": "In Progress"
  }
]
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|




### 2.3. Get Project Details

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/projects/{project_id}` |
| **Method** | `GET` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be associated with the project via `project_roles` (owner, collaborator, or viewer)|


#### Successful Response (200 OK)

Returns a single project object, including the current user's role.

```json
{
  "project_id": 5,
  "project_name": "My New Project ",
  "project_owner": 1,
  "user_role": "owner",
  "status": "Planning",
  "start_date": "2025-12-01",

  // Optional: List of users in the project
  "team_members": [     
    {"user_id": 1, "username": "owneruser", "role": "owner"},
    {"user_id": 2, "username": "collabuser", "role": "collaborator"}
  ]
}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User is authenticated but is **not** a member of the project|
| **404** | Not Found| Project with `project_id` does not exist|




### 2.4. Update Project Details

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/projects/{project_id}` |
| **Method** | `PUT` or `PATCH` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be an owner or a collaborator in the project's `project_roles` table. Viewers are Forbidden (`403`).|


#### Request Body Schema (Partial update is allowed)

```json
{
  "project_name": "string (max 25-30 chars, optional)",
  "status": "string (optional, eg: 'Completed')"
}
```

#### Successful Response (200 OK)

Returns the updated project object(or All details).

```json
{
  "project_id": 5,
  "project_name": "Updated My New Project ",
  "project_owner": 1,
  "user_role": "owner",
  "status": "Planning",
  "start_date": "2025-12-01",

  // Optional: List of users in the project
  "team_members": [     
    {"user_id": 1, "username": "owneruser", "role": "owner"},
    {"user_id": 2, "username": "collabuser", "role": "collaborator"}
  ]
}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User is a member but only has the viewer role or no role|
| **404** | Not Found| Project with `project_id` does not exist|





### 2.5. Delete Project

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/projects/{project_id}` |
| **Method** | `DELETE` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be the `project_owner`. Collaborators/Viewers are Forbidden (`403`).|



#### Successful Response (204 No Content)

Or, Returns the message/alert

```json
{
    "message": "Project Successfully Deleted."
}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User is a member but is not the owner|
| **404** | Not Found| Project with `project_id` does not exist|




### 2.6. Assing/Update User Role on a Project

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/projects/{project_id}/members` |
| **Method** | `POSt`(for adding) or `PUT`(for updating) |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be the `project_owner`. Collaborators/Viewers are Forbidden (`403`).|


#### Request Body Schema

```json
{
  "user_id": 2,
  "role": "collaborator" // owner, collaborator, or, viewer
}
```

#### Successful Response (200 Ok)

 Returns the message/alert

```json
{
  "message": "User role successfully updated to collaborator in Project 5."
}
```



#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **403** | Forbidden| User is a member but is not the owner|
| **404** | Not Found| Target `user_id` or `project_id` does not exist|
| **400** | Bad Request| Invalid role provided|


---


<br>

## 3. Tasks Module

This module handles the creation and management of individual tasks within a project.
Tasks are directly linked to a Project and can be assigned to a User.

### 3.1. Create a New Task

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/projects/{project_id}/tasks/` |
| **Method** | `POST` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be a **`collaborator`** or **`owner`** of the project in `project_roles` table |

#### Request Body Schema

Based on the `todo_list` table:

```json
{
  "task_name": "string (max 50 chars)",
  "due_date": "datetime (YYYY-MM-DD)",
  "description": "string (optional)",
  "priority": "string (eg: 'High', 'Medium', 'Low')",
  "user_assigned": "integer (id of a user to assign the task to, must be a member of the project)"
}
```
#### Successful Response (201 Created)

Returns the created task details.

```json
{
  "task_id": 101,
  "project_id": 5,
  "task_name": "Design the Auth Flow",
  "due_date": "2025-12-15",
  "status": "Todo", // Default status
  "user_assigned": {
    "user_id": 2,
    "username": "collaboratoruser"
  }
}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User lacks `collaborator/owner` role in the project|
| **404** | Not Found| Project with `project_id` does not exist|
| **400** | Bad Request| `user_assigned` is not a member of the project, or missing required fields|




### 3.2. List Tasks by Project 

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/projects/{project_id}/tasks/` |
| **Method** | `GET` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be associated with the project  |


#### Successful Response (200 OK)

Returns an array of tasks for the specified project.

```json
[
  {
    "task_id": 101,
    "task_name": "Design the Auth Flow",
    "status": "In Progress",
    "priority": "High",
    "assigned_user": {"user_id": 2, "username": "collabuser"}
  },
  {
    "task_id": 102,
    "task_name": "Setup Docker Compose",
    "status": "Done",
    "priority": "Medium",
    "assigned_user": {"user_id": 1, "username": "owneruser"}
  }
]
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User is authenticated but **not** a member|
| **404** | Not Found| Project with `project_id` does not exist|





### 3.3. Get Single Task Details

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/tasks/{task_id}` |
| **Method** | `GET` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be associated with the task's parent project(any role)  |


#### Successful Response (200 OK)

Returns the single task object.

```json
{
  "task_id": 101,
  "project_id": 5,
  "task_name": "Design the Auth Flow",
  "description": "Details about the task",
  "status": "In Progress",
  "assigned_user": {"user_id": 2, "username": "collaboratoruser"},
  "due_date": "2025-11-24"
}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User is not a member of the task's project|
| **404** | Not Found| Task with `task_id` does not exist|




### 3.4. Update Task Details

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/tasks/{task_id}` |
| **Method** | `PUT` or `PATCH` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be Owner or collaborator  |


#### Request Body Schema (Partial Update)
```json
{
  "task_name": "string",
  "status": "string (eg: 'Done')",
  "assigned_user_id": "integer (must be a project member)"
}
```

#### Successful Response (200 OK)

Returns the updated task object, or

```json
{
    "message": "Successfully Updated Task"
}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User lacks role|
| **404** | Not Found| Task with `task_id` does not exist|





### 3.5. Delete Task 

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/tasks/{task_id}` |
| **Method** | `DELETE` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be Owner of the parent project|



#### Successful Response (204 No Content)

Returns the updated task object, or (200 OK)

```json
{
    "message": "Successfully Deleted Task"
}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User is not the project owner|
| **404** | Not Found| Task with `task_id` does not exist|


---


<br>


## 4. Notes Module

This module handles the creation, listing, and deletion of text based notes associated
with a specific project.

### 4.1. Create a New Note

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/projects/{project_id}/notes/` |
| **Method** | `POST` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be a **`collaborator`** or **`owner`** of the project. Viewers can typically read but not create. |


#### Request Body Schema

Based on the `notes` table:

```json
{
  "content": "string (markdown/plain text body)",
  "author_id": "integer (optional, defaults to the current authenticated user)",
}
```

#### Successful Response(201 Created)

Returns the created note details.

```json
{
  "note_id": 15,
  "project_id": 5,
  "title": "Initial Backend Setup Thoughts",
  "created_by": 1, // id of the creator
  "created_at": "2025-11-24T16:00:00Z"
}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User lacks the role in the project|
| **404** | Not Found| Project with `project_id` does not exist|



### 4.2. List Notes by Project 

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/projects/{project_id}/notes/` |
| **Method** | `GET` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be associated with the project(any role) |



#### Successful Response(201 OK)

Returns an array of notes for the specified project, sorted by creation date.

```json
[
  {
    "note_id": 205,
    "content": "Initial Backend Setup Thoughts",
    "user_id": 1,
    "project_id": 15,
    "created_time": "2025-11-24T16:00:00Z",
    "content_snippet": "First few lines of the note"
  },
  {
    "note_id": 206,
    "content": "Frontend Component Checklist",
    "user_id": 2,
    "project_id": 15,
    "created_time": "2025-11-24T17:00:00Z",
    "content_snippet": "Needs buttons, input forms, etc."
  }
]
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User is authenticated but not a member of the project|
| **404** | Not Found| Project with `project_id` does not exist|




### 4.3. Delete Note

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/notes/{notes_id}` |
| **Method** | `DELETE` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | User must be the project_owner or the note_creator |



#### Successful Response(204 No Content)

Or, send a feedback message

```json
{"message": "Note successfully Deleted"}
```

#### Error Responses

| Code | Status | Description |
| :--- | :--- | :--- |
| **401** | Unauthorized| Missing or invalid access token|
| **403** | Forbidden| User is not the owner of the project AND not the creator of the note|
| **404** | Not Found| Note with `note_id` does not exist|


---



<br>



> [!NOTE]
> Below section is a proposal for Dashboard

## 5. Dashboard Module(Visualization)

summarizing Data status across all users associated projects.

### 5.1. Get User Dashboard Summary

| Detail | Description |
| :--- | :--- |
| **Path** | `/api/v1/dashboard/summary` |
| **Method** | `GET` |
| **Authentication** | Required (Bearer Token) |
| **Permissions** | Must be logged in |

#### Successful Response (200 OK)

Returns aggregated metrics and data necessary for the landing page.

```json
{
  "total_projects": 5,
  "active_projects": 3,
  "overdue_tasks_count": 2,
  "tasks_assigned_to_me": {
    "total": 15,
    "in_progress": 8,
    "done": 7
  },
  "overdue_tasks_list": [ 
    {
      "task_id": 105,
      "task_name": "Fix DB connection issue",
      "due_date": "2025-11-20",
      "project_name": "New Project Alpha"
    },
        //.. other items
  ],
  "recent_projects": [ 
    {
      "project_id": 5,
      "project_name": "New Project Alpha",
      "progress_percent": 60 
    }
  ]
}
