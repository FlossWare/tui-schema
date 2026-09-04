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
- Consumers MUST explicitly declare which schema versions they support.
- Consumers MUST reject unsupported major versions.
- Consumers MUST reject unsupported minor versions rather than silently guessing at new semantics.
- Within a supported schema version, unknown fields are rejected by the 1.0 contract because structured objects use `additionalProperties: false` or `unevaluatedProperties: false`.

## Semantic stability

Field names and values describe portable concepts. They must not expose implementation details such as Python classes, Java classes, curses constants, or framework-specific objects.

Actions are semantic identifiers. The application that consumes a document owns the behavior associated with an action.

## Patch policy

A patch release is documentation-only when the clarification does not alter the set of documents accepted by the schema or the required interpretation of an existing field. Such clarifications belong in `CHANGELOG.md` and the versioned grammar documentation.

If a clarification changes validation, defaults, required fields, allowed values, or interpretation in a way that can affect consumers, it is a contract change and MUST use the appropriate minor or major schema version.

## Implementations

A language implementation may have its own release cycle. For example, a Python TUI library can release independently from `tui-schema` while supporting `flossware.tui/1.0`.
