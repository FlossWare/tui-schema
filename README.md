# FlossWare TUI Schema

Language-neutral, versioned JSON contract for describing terminal user interfaces used across FlossWare projects.

## Purpose

`tui-schema` defines the **meaning and structure** of a TUI. It does not define rendering code, curses APIs, Java classes, or application business logic.

Implementations interpret the same declarative document in their native language.

## Canonical format

**JSON is the canonical interchange format.** YAML and XML are intentionally not part of the contract.

The schema uses JSON Schema Draft 2020-12 and is versioned independently from implementation libraries.

## Version 1.0

The 1.0 contract describes menus, semantic actions, keyboard accelerators, windows/dialogs/popups/panels, movable/resizable behavior, layout and geometry constraints, common widgets, focus/visibility/enabled state, and themes.

Application actions remain application-owned. For example, `"action": "profiles"` identifies an event; it does not embed executable code in the schema.

## Repository layout

```text
schema/
  tui-1.0.schema.json
examples/
  menu.json
docs/
  VERSIONING.md
```

Implementations validate documents against the schema version they support. Schema versions are independent of implementation package versions.
