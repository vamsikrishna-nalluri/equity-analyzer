# To-Do App — Week 4 Specs
Specs covering: Add Task, Edit Task, Delete Task

---

# Spec: Add Task
**ID:** TODO-SPEC-001
**Status:** Draft

## User Story
As a user of the to-do app, I want to add a new task to my list, so that I can track things I need to do.

## Scope
- In scope: creating a new task via the "Add Task" UI flow, validation of task detail, success/failure/cancel behavior.
- Out of scope: task priority, due dates, categories (covered in separate specs).

## Business Rules
- **BR-1:** Task detail shall be between 1 and 200 characters (inclusive). Empty or whitespace-only task details are not permitted.
- **BR-2:** Task detail shall not contain the special characters `<` or `>`.

## Scenarios

### Scenario 1: Successfully adding a task
```
GIVEN the to-do list contains 0 or more tasks
WHEN the user clicks the "Add Task" button
THEN a new task window shall open, displaying a task detail field, a Submit button, and a Cancel button

GIVEN the new task window is open
WHEN the user enters "Buy groceries" in the task detail field and clicks Submit
THEN the task window shall close
AND the task "Buy groceries" shall appear in the to-do list
```

### Scenario 2: Validation failure — task detail exceeds 200 characters
```
GIVEN the new task window is open
WHEN the user enters a task detail longer than 200 characters and clicks Submit
THEN the task window shall remain open
AND the system shall display "Failed to add task: task detail cannot exceed 200 characters."
AND no task shall be added to the list
```

### Scenario 3: Validation failure — task detail is empty
```
GIVEN the new task window is open
WHEN the user leaves the task detail field empty (or whitespace-only) and clicks Submit
THEN the task window shall remain open
AND the system shall display "Failed to add task: task detail cannot be empty."
AND no task shall be added to the list
```

### Scenario 4: Validation failure — task detail contains special characters
```
GIVEN the new task window is open
WHEN the user enters a task detail containing "<" or ">" and clicks Submit
THEN the task window shall remain open
AND the system shall display "Failed to add task: task detail cannot contain special characters (<, >)."
AND no task shall be added to the list
```

### Scenario 5: Failure due to network/server error
```
GIVEN the new task window is open with a valid task detail entered
AND the server is unreachable
WHEN the user clicks Submit
THEN the task window shall remain open
AND the system shall display "Failed to add task: unable to reach the server. Please try again."
AND no task shall be added to the list
```

### Scenario 6: User cancels task creation
```
GIVEN the new task window is open
WHEN the user clicks Cancel
THEN the task window shall close
AND no task shall be added to the list
```

## Non-Functional Requirements
- **NFR-1 (Performance):** Task creation, from Submit click to task appearing in the list, shall complete within 300ms on a standard broadband connection (>10 Mbps).

## Edge Cases
- **EC-1:** Task detail is exactly 200 characters (boundary) — shall be accepted.
- **EC-2:** Task detail is exactly 1 character — shall be accepted.
- **EC-3:** Task detail is empty or whitespace-only — shall be rejected (see Scenario 3).

---

# Spec: Edit Task
**ID:** TODO-SPEC-002
**Status:** Draft

## User Story
As a user of the to-do app, I want to edit an existing task, so that I can correct or update its details.

## Scope
- In scope: editing an existing task's detail via the "Edit Task" UI flow, validation, success/failure/cancel behavior.
- Out of scope: editing task priority, due dates, categories (covered in separate specs).

## Business Rules
- **BR-1:** Task detail shall be between 1 and 200 characters (inclusive). Empty or whitespace-only task details are not permitted.
- **BR-2:** Task detail shall not contain the special characters `<` or `>`.

## Scenarios

### Scenario 1: Successfully editing a task
```
GIVEN a task titled "Buy groceries" exists in the to-do list
WHEN the user clicks the "Edit" button next to the task
THEN an edit task window shall open, pre-filled with "Buy groceries" in the task detail field, an Update button, and a Cancel button

GIVEN the edit task window is open with "Buy groceries" in the task detail field
WHEN the user changes the text to "Buy groceries and milk" and clicks Update
THEN the edit task window shall close
AND the task shall display as "Buy groceries and milk" in the to-do list
```

### Scenario 2: Validation failure — task detail exceeds 200 characters
```
GIVEN the edit task window is open for an existing task
WHEN the user enters a task detail longer than 200 characters and clicks Update
THEN the edit task window shall remain open
AND the system shall display "Failed to update task: task detail cannot exceed 200 characters."
AND the task in the list shall remain unchanged
```

### Scenario 3: Validation failure — task detail is empty
```
GIVEN the edit task window is open for an existing task
WHEN the user clears the task detail field (or leaves it whitespace-only) and clicks Update
THEN the edit task window shall remain open
AND the system shall display "Failed to update task: task detail cannot be empty."
AND the task in the list shall remain unchanged
```

### Scenario 4: Validation failure — task detail contains special characters
```
GIVEN the edit task window is open for an existing task
WHEN the user enters a task detail containing "<" or ">" and clicks Update
THEN the edit task window shall remain open
AND the system shall display "Failed to update task: task detail cannot contain special characters (<, >)."
AND the task in the list shall remain unchanged
```

### Scenario 5: Failure due to network/server error
```
GIVEN the edit task window is open with a valid task detail entered
AND the server is unreachable
WHEN the user clicks Update
THEN the edit task window shall remain open
AND the system shall display "Failed to update task: unable to reach the server. Please try again."
AND the task in the list shall remain unchanged
```

### Scenario 6: Failure due to stale data — task no longer exists
```
GIVEN the edit task window is open for a task that was deleted (e.g., in another session) before Update is clicked
WHEN the user clicks Update
THEN the edit task window shall remain open
AND the system shall display "Failed to update task: task is not available in the list. Please refresh and check the to-do list."
AND no task shall be added or changed in the list
```

### Scenario 7: User cancels task edit
```
GIVEN the edit task window is open for an existing task
WHEN the user clicks Cancel
THEN the edit task window shall close
AND the task in the list shall remain unchanged
```

## Non-Functional Requirements
- **NFR-1 (Performance):** Task update, from Update click to the change appearing in the list, shall complete within 300ms on a standard broadband connection (>10 Mbps).

## Edge Cases
- **EC-1:** Task detail is edited to exactly 200 characters (boundary) — shall be accepted.
- **EC-2:** Task detail is edited to exactly 1 character — shall be accepted.
- **EC-3:** Task is deleted by another session while the edit window is open — shall be rejected with the stale-data message (see Scenario 6).

---

# Spec: Delete Task
**ID:** TODO-SPEC-003
**Status:** Draft

## User Story
As a user of the to-do app, I want to delete a task from my list, so that I can remove items I no longer need to track.

## Scope
- In scope: deleting an existing task via the "Delete Task" UI flow (with confirmation), success/failure/cancel behavior.
- Out of scope: soft-delete/recovery ("Trash" or "Recently Deleted") behavior — see Open Questions.

## Scenarios

### Scenario 1: Successfully deleting a task
```
GIVEN a task titled "Pick kid from school" exists in the to-do list
WHEN the user clicks the "Delete" button next to the task
THEN a delete confirmation window shall open, displaying the task detail "Pick kid from school" as a label, a Delete button, and a Cancel button

GIVEN the delete confirmation window is open for "Pick kid from school"
WHEN the user clicks Delete
THEN the delete confirmation window shall close
AND the task "Pick kid from school" shall no longer appear in the to-do list
```

### Scenario 2: Failure due to network/server error
```
GIVEN the delete confirmation window is open for an existing task
AND the server is unreachable
WHEN the user clicks Delete
THEN the delete confirmation window shall remain open
AND the system shall display "Failed to delete task: unable to reach the server. Please try again."
AND the task shall remain in the list
```

### Scenario 3: Failure due to stale data — task no longer exists
```
GIVEN the delete confirmation window is open for a task that was already deleted (e.g., in another session) before Delete is clicked
WHEN the user clicks Delete
THEN the delete confirmation window shall remain open
AND the system shall display "Failed to delete task: task is not available in the list. Please refresh and check the to-do list."
AND no further change shall occur in the list
```

### Scenario 4: User cancels task deletion
```
GIVEN the delete confirmation window is open for an existing task
WHEN the user clicks Cancel
THEN the delete confirmation window shall close
AND the task shall remain, unchanged, in the list
```

## Non-Functional Requirements
- **NFR-1 (Availability):** The delete action shall succeed 99.9% of the time under normal network conditions.

## Edge Cases
- **EC-1:** Deleting the last remaining task in the list — the list shall display an empty state after deletion.
- **EC-2:** Task is deleted by another session before this session's delete is confirmed — shall be rejected with the stale-data message (see Scenario 3).

## Open Questions
- Is deletion a **soft delete** (recoverable, e.g., moved to a "Recently Deleted" view for N days) or a **hard delete** (immediate, permanent)? This affects whether related requirements (e.g., "editing a deleted task") are applicable. Recommend resolving before implementation.