# Schema Versioning

`tui-schema` is a shared contract. Its version describes the contract, not the implementation package that consumes it.

## Version identifier

Every document declares a schema identifier using `major.minor` form:

```json
{
  "schema": "flossware.tui/1.0"
}
```

The schema file is stored as `schema/tui-1.0.schema.json`.

## Compatibility rules

- Patch-level clarifications that do not change validation semantics may be documented without creating a new schema release.
- Backward-compatible additions should increment the minor version when they require consumers to understand new fields or behavior.
- Breaking changes require a new major version.
- Consumers must explicitly declare which schema versions they support.
- Implementations must not silently reinterpret an unsupported schema version.

## Semantic stability

Field names and values describe portable concepts. They must not expose implementation details such as Python classes, Java classes, curses constants, or framework-specific objects.

Actions are semantic identifiers. The application that consumes a document owns the behavior associated with an action.

## Implementations

A language implementation may have its own release cycle. For example, a Python TUI library can release independently from `tui-schema` while supporting `flossware.tui/1.0`.
