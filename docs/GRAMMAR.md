# TUI Grammar

The schema is a declarative description of a terminal UI. It describes structure and semantic interaction, not implementation.

## Core model

A TUI document contains:

1. **Document metadata**: schema version, identifier, and title.
2. **Menus**: navigable commands with optional keyboard accelerators.
3. **Windows**: windows, dialogs, popups, and panels with layout and interaction properties.
4. **Widgets**: controls such as labels, inputs, checkboxes, lists, menus, buttons, separators, and groups.
5. **Theme**: semantic colors and attributes.

## Semantic actions

Interactive elements can expose an `action` identifier such as:

```json
{
  "id": "configure",
  "label": "Configure",
  "accelerator": "c",
  "action": "configure"
}
```

The identifier is an event name. The consuming application maps it to application behavior. The schema MUST NOT contain executable code or language-specific callback names.

## Accelerators

An accelerator is a single alphanumeric key associated with a semantic action. Implementations are responsible for deciding how the key is presented and normalized for their terminal environment.

Within a single menu scope, accelerators SHOULD be unique among visible, enabled items. Implementations MAY reject ambiguous accelerator definitions.

## Keyboard and mouse behavior

The schema describes interaction capabilities but does not prescribe terminal-specific key constants.

Implementations should provide consistent semantics for:

- focus movement
- selection
- activation
- cancellation
- primary pointer activation
- moving windows
- resizing windows

The Python `curses-themes` implementation is one implementation of these semantics. A future Java implementation can provide the same semantics independently.

## Layout

Layout uses portable geometry concepts such as `x`, `y`, `width`, `height`, minimum and maximum dimensions, and semantic anchors. Implementations translate these into their native windowing primitives.

## Scope boundary

`tui-schema` owns the contract. It does not own:

- rendering engines
- terminal libraries
- application state
- persistence
- provider/model configuration
- business workflows
- executable callbacks

This boundary keeps the contract usable by Python, Java, and future implementations without forcing those implementations to share runtime dependencies.
