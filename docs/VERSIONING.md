# Schema Versioning

`tui-schema` is a shared contract. Its version describes the contract, not the implementation package that consumes it.

## Version identifier

Every document declares a schema identifier:

```json
{
  "schema": "flossware.tui/v1"
}
```

The schema file is stored as `schema/tui-v1.schema.json`.

## Compatibility rules

- Patch-level clarifications that do not change validation semantics may be documented without creating a new major schema version.
- Backward-compatible additions should use a minor schema version when they require consumers to opt into new fields or behavior.
- Breaking changes require a new major schema version.
- Consumers must explicitly declare which schema versions they support.
- Implementations must not silently reinterpret an unsupported schema version.

## Semantic stability

Field names and values describe portable concepts. They must not expose implementation details such as Python classes, Java classes, curses constants, or framework-specific objects.

Actions are semantic identifiers. The application that consumes a document owns the behavior associated with an action.

## Implementations

A language implementation may have its own release cycle. For example, a Python TUI library can release independently from `tui-schema` while supporting `flossware.tui/v1`.
