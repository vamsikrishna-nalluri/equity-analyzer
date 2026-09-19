# Python Coding Guidelines & Best Practices

This document outlines the coding standards, structural requirements, and stylistic conventions for this Python project. Adherence to these guidelines ensures readability, maintainability, and consistency across the codebase.

---

## 1. Code Style & Formatting

*   **PEP 8 Compliance:** All code must strictly follow [PEP 8](https://github.com/spacetelescope/style-guides/blob/master/guides/python.md) style recommendations.
*   **Line Length:** Limit all lines to a maximum of **80 characters** for code, and **72 characters** for comments and docstrings.
*   **Indentation:** Use exactly **4 spaces** per indentation level. Never use tabs.
*   **String Formatting:** Prefer **f-strings** over `.format()` or `%` formatting for readability and performance.
*   **Path Management:** Always use the built-in **`pathlib`** module. Do not use `os.path`.

---

## 2. Naming Conventions

*   **Variables & Functions:** Use `snake_case` (e.g., `calculate_total_price`).
*   **Classes:** Use `PascalCase` (e.g., `UserProfileManager`).
*   **Constants:** Use `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_ATTEMPTS`).
*   **Private Members:** Prefix with a single underscore for internal module/class use (e.g., `_internal_verify`).

---

## 3. Best Practices & Idiomatic Python

*   **Mutable Defaults:** **NEVER** use mutable default arguments (like `def append_to(element, to=[]):`). Use `None` and instantiate inside the function instead.
*   **Resource Management:** **MUST** use context managers (`with` statements) for opening files, sockets, or managing databases.
*   **Comparisons:** **MUST** use `is` or `is not` when evaluating singletons like `None`, `True`, or `False`. Never use `==`.
*   **Loop Counters:** Use `enumerate()` instead of maintaining manual counter variables.
*   **Comprehensions:** Use list, dictionary, and generator comprehensions where they improve readability, but avoid over-nesting them.

---

## 4. Error Handling

*   **EAFP Principle:** Follow "Easier to Ask for Forgiveness than Permission". Handle explicitly expected exceptions rather than aggressively checking state up front.
*   **Specific Exceptions:** Avoid catch-all `except Exception:` blocks. Always catch specific errors (e.g., `except KeyError:`).
*   **Clean Cleanup:** Rely on `finally` blocks or context managers to guarantee cleanup routines execute successfully.

---

## 5. Documentation & Type Hinting

*   **Type Hints:** Type-hint all public functions, methods, and their explicit return values.
*   **Docstring Format:** Document every public class, method, and function using **Google-style docstrings**.
*   **Module Placement:** Place module-level docstrings at the absolute top of the file, preceding any imports.

### Example Format:
```python
def fetch_user_record(user_id: int) -> dict:
    """Fetches a specific user record from the database.

    Args:
        user_id: The unique primary integer identifier for the user.

    Returns:
        A dictionary containing the parsed user record data.

    Raises:
        UserNotFoundError: If the user_id does not exist in the database.
    """
    ...
```

---

## 6. Imports Workflow

1.  **Group Order:** Structure imports at the top of the file in three distinct blocks, separated by a single blank line:
    1.  Standard library imports.
    2.  Related third-party imports.
    3.  Local application/library specific imports.
2.  **Absolute Imports:** Prefer absolute imports over relative imports.
3.  **No Wildcards:** Never use wildcard imports (`from module import *`).
