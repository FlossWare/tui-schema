# FlossWare TUI Schema

Language-neutral, versioned JSON contract for describing terminal user interfaces used across FlossWare projects.

## Purpose

`tui-schema` defines the **meaning and structure** of a TUI. It does not define rendering code, curses APIs, Java classes, or application business logic.

Implementations interpret the same declarative document in their native language.

## Canonical format

**JSON is the canonical interchange format.** YAML and XML are intentionally not part of the contract.

The schema uses JSON Schema Draft 2020-12 and is versioned independently from implementation libraries.

## Version 1.0

The 1.0 contract describes:

- top-level menu bars with action items and separators
- semantic actions and portable alphanumeric accelerators
- windows, dialogs, popups, and panels
- movable/resizable behavior and absolute cell-based layout
- typed widgets: labels, text inputs, checkboxes, lists, buttons, separators, and groups
- focus, initial focus, visibility, and enabled state
- dialog default/cancel actions
- named implementation themes

Widget objects are type-discriminated and reject properties that do not belong to their selected type. Groups are real containers with nested widgets. Menu widgets and nested menus are intentionally excluded from 1.0 to keep the grammar unambiguous.

Application actions remain application-owned. For example, `"action": "profiles"` identifies an event; it does not embed executable code in the schema.

Document-wide ID uniqueness and cross-object reference validity are semantic invariants checked by the repository test suite because JSON Schema cannot compare arbitrary nested `id` fields as a single global set.

## Repository layout

```text
schema/
  tui-1.0.schema.json
examples/
  menu.json
  dialog.json
  form.json
  list.json
  group.json
docs/
  GRAMMAR.md
  VERSIONING.md
CHANGELOG.md
tests/
  validate.py
  invalid/
.github/workflows/
  validate.yml
```

Run the local validation suite with:

```bash
python -m pip install jsonschema
python tests/validate.py
```

Implementations validate documents against the schema version they support. Schema versions are independent of implementation package versions.
