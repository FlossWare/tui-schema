#!/usr/bin/env python3
"""Validate the 1.0 schema, examples, and semantic identity/reference invariants."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "tui-1.0.schema.json"
EXAMPLES_DIR = ROOT / "examples"
INVALID_DIR = ROOT / "tests" / "invalid"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_widgets(widgets: list[dict[str, Any]]):
    for widget in widgets:
        yield widget
        if widget.get("type") == "group":
            yield from iter_widgets(widget.get("children", []))


def collect_ids(document: dict[str, Any]) -> set[str]:
    ids: list[str] = [document["id"]]
    for menu in document.get("menus", []):
        ids.append(menu["id"])
        for item in menu["items"]:
            ids.append(item["id"])
    for window in document["windows"]:
        ids.append(window["id"])
        for widget in iter_widgets(window["content"]):
            ids.append(widget["id"])
            if widget.get("type") == "list":
                ids.extend(item["id"] for item in widget["items"])
    return ids


def check_semantics(document: dict[str, Any], path: Path) -> list[str]:
    errors: list[str] = []
    ids = collect_ids(document)
    if len(ids) != len(set(ids)):
        errors.append(f"duplicate id in {path}")

    menu_ids = {menu["id"] for menu in document.get("menus", [])}
    action_ids = set()
    for menu in document.get("menus", []):
        accelerators: set[str] = set()
        for item in menu["items"]:
            if item.get("type") == "separator":
                continue
            action_ids.add(item["action"])
            accelerator = item.get("accelerator")
            if accelerator and item.get("visible", True) and item.get("enabled", True):
                if accelerator.lower() in {a.lower() for a in accelerators}:
                    errors.append(f"duplicate menu accelerator in {path}: {accelerator}")
                accelerators.add(accelerator)

    for window in document["windows"]:
        if "menuBar" in window and window["menuBar"] not in menu_ids:
            errors.append(f"unknown menuBar reference in {path}: {window['menuBar']}")
        widget_ids = {widget["id"] for widget in iter_widgets(window["content"])}
        if "initialFocus" in window and window["initialFocus"] not in widget_ids:
            errors.append(f"unknown initialFocus reference in {path}: {window['initialFocus']}")
        for widget in iter_widgets(window["content"]):
            if widget.get("type") == "list" and "selected" in widget:
                item_ids = {item["id"] for item in widget["items"]}
                if widget["selected"] not in item_ids:
                    errors.append(f"unknown list selection in {path}: {widget['selected']}")
            if widget.get("type") in {"text-input", "checkbox", "button", "list"} and widget.get("action"):
                action_ids.add(widget["action"])
    return errors


def main() -> int:
    schema = load(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    failures: list[str] = []
    examples = sorted(EXAMPLES_DIR.glob("*.json"))
    if not examples:
        failures.append("no examples found")

    for path in examples:
        document = load(path)
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        failures.extend(f"{path}: {error.message}" for error in errors)
        if not errors:
            failures.extend(check_semantics(document, path))

    for path in sorted(INVALID_DIR.glob("*.json")):
        document = load(path)
        if not list(validator.iter_errors(document)):
            failures.append(f"invalid fixture unexpectedly validates: {path}")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1

    print(f"Validated schema and {len(examples)} examples; all invalid fixtures rejected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
