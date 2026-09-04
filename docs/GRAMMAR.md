# TUI Grammar

The schema is a declarative description of a terminal UI. It describes portable structure and semantic interaction, not implementation.

## Core model

A TUI document contains:

1. **Document metadata**: schema version, identifier, and title.
2. **Menus**: top-level menu-bar definitions containing actions and separators.
3. **Windows**: windows, dialogs, popups, and panels with geometry and interaction properties.
4. **Widgets**: typed controls with type-specific data and behavior.
5. **Theme**: a named implementation theme.

The 1.0 grammar intentionally does not define nested menus, arbitrary theme key/value maps, or executable callbacks.

## Semantic actions

Interactive elements expose an `action` identifier such as:

```json
{
  "id": "configure",
  "type": "button",
  "label": "Configure",
  "action": "configure"
}
```

An action is an event name. The consuming application maps it to application behavior. The schema MUST NOT contain executable code or language-specific callback names.

`defaultAction` and `cancelAction` on a window are semantic action identifiers. They do not imply that the action exists on a particular widget; applications decide how those actions are bound.

## Widgets

Widgets are type-discriminated. Each type has a defined shape:

- `label`: static single text label; never focusable.
- `text-input`: string value, optional label/action, focusable by default.
- `checkbox`: boolean value, optional label/action, focusable by default.
- `list`: one or more structured items, optional selected item and action, focusable by default.
- `button`: required label and action, focusable by default.
- `separator`: non-interactive visual separator.
- `group`: a non-focusable container with one or more child widgets.

The 1.0 schema rejects properties not allowed by the selected widget type. `menu` is deliberately a top-level construct rather than a widget type so the contract has one unambiguous menu model.

List selection is represented by the `selected` item identifier. The identifier MUST refer to an item in that list. Implementations should reject an invalid reference.

## Menus

`menus` defines top-level menu bars. A window may associate one menu bar with `menuBar`, which contains that menu's identifier.

Menu items are either action items or separators. Nested menus are not part of 1.0.

Within one menu scope, accelerators SHOULD be unique among visible, enabled action items. Implementations MUST reject ambiguous accelerator definitions when they cannot provide deterministic dispatch.

## Accelerators

An accelerator is a single ASCII alphanumeric key. This narrow form is intentional for 1.0 portability. Function keys, modifier combinations, and other terminal-specific key encodings are future schema work.

## Interaction semantics

The schema describes semantic capabilities without prescribing curses constants or another terminal API. Implementations should provide consistent semantics for:

- focus movement
- activation
- selection
- cancellation
- primary pointer activation
- moving windows when `movable` is true
- resizing windows when `resizable` is true

`initialFocus`, when present, identifies the widget that should receive initial focus. It MUST identify a focusable widget within the window. If omitted, the implementation chooses the first eligible focusable widget according to its documented traversal rules.

For dialogs, `modal` SHOULD be true when the application intends to block interaction with other windows. The schema does not force this because modality is an application interaction choice.

## Layout

Layout coordinates are integer **terminal cells**.

- The coordinate origin `(0, 0)` is the top-left cell of the implementation's terminal or containing window.
- `x` increases to the right and `y` increases downward.
- `width` and `height` are cell counts and include the complete window/widget rectangle represented by the implementation.
- `minWidth` / `minHeight` and `maxWidth` / `maxHeight` constrain resizing. Implementations MUST reject or clamp configurations that make the constraints impossible.
- `anchor` selects the corresponding point of the containing terminal/window as the reference point for placement.
- If `anchor` is omitted, `top-left` is used.
- If `layout` is omitted, the implementation applies its documented native default placement and sizing for that object kind. A consumer MUST NOT assume a particular default geometry from an omitted layout.

Absolute geometry is intentional for 1.0. Relative/fill sizing, padding, and richer alignment are future schema features.

## Theme

A 1.0 theme contains only a `name`. The name is a portable semantic reference to a theme registered by the implementation. Color encodings, curses color-pair numbers, RGB values, and attribute constants do not cross the language boundary.

This avoids creating two incompatible theme languages while allowing `curses-themes` and a future Java implementation to map the same semantic theme name to their native rendering systems.

## Identity and references

Every `id` in a document is a semantic identity and MUST be unique across the entire document, including nested widgets and list items. JSON Schema's `uniqueItems` is not used as an ID uniqueness mechanism because it compares complete JSON values rather than selected fields.

Cross-object references such as `menuBar`, `initialFocus`, and `selected` are semantic references. JSON Schema validates their syntax; implementations and contract tests validate that referenced IDs exist and have the required meaning.

## Scope boundary

`tui-schema` owns the contract. It does not own:

- rendering engines
- terminal libraries
- application state
- persistence
- provider/model configuration
- business workflows
- executable callbacks

This boundary keeps the contract usable by Python, Java, and future implementations without forcing them to share runtime dependencies.
