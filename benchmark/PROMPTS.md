# Benchmark Prompts (fixed verbatim — pre-registered)

Used exactly as written in every model and condition.
- **Condition B (grounded)** prepends the full `CurbCut.md`, then the line: *"Follow the accessibility rules in CurbCut.md strictly."*
- **Condition C (enforced)** is B, then each output file is run through `curbcut-guard.py` (block mode); the hook's stderr is returned to the model with *"Fix every reported issue, then re-output the file."* — up to 2 rounds.

The prompts deliberately never mention accessibility.

## Task 1 — Signup form
```
Create a signup page in plain HTML, CSS and JavaScript with fields for full name, email and password. Validate the fields inline and show error messages when submission fails. Show a success message when it succeeds.
```

## Task 2 — Destructive-confirmation modal
```
Create a page in plain HTML, CSS and JavaScript showing a list of 5 saved documents. Each document has a Delete button. Clicking Delete opens a confirmation dialog asking "Delete this document?" with Cancel and Delete options. Deleting removes the item from the list.
```

## Task 3 — Sortable data table
```
Create a page in plain HTML, CSS and JavaScript with a table of 10 employees (name, role, salary). The columns can be sorted by clicking their headers, and each row has a "View details" button that shows that employee's information.
```
