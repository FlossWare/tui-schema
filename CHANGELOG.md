# Changelog

## 1.0

Initial shared TUI contract.

### Contract hardening

- Type-discriminated widget shapes.
- `group` is a real widget container with `children`.
- Top-level menus are the sole menu model in 1.0; nested menus and menu widgets are excluded.
- Menu separators have an explicit schema shape.
- Themes use a portable registry name instead of implementation-specific color maps.
- Window menu-bar association, initial focus, and dialog default/cancel actions are defined.
- List items and selection are explicitly modeled.
- Layout coordinate and defaulting semantics are documented.
- Document-wide ID uniqueness and cross-object reference invariants are documented and tested outside JSON Schema.
- JSON Schema and all examples are intended to be validated in CI.
