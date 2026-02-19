"""See COPYRIGHT.md for copyright information.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from arelle_test_engine.constraint import Constraint
from arelle_test_engine.error_level import ErrorLevel


@dataclass(frozen=True)
class TestEngineOptions:
    __test__ = False  # Tells pytest: Not a test class.

    index_file: Path
    additional_constraints: list[tuple[str, list[Constraint]]] = field(default_factory=list)
    compare_formula_output: bool = False
    custom_compare_patterns: list[tuple[str, str]] = field(default_factory=list)
    disclosure_system_by_id: list[tuple[str, str]] = field(default_factory=list)
    filters: list[str] = field(default_factory=list)
    ignore_levels: frozenset[ErrorLevel] = field(default_factory=lambda: frozenset({ErrorLevel.OK}))
    log_directory: Path | None = None
    match_all: bool = True
    name: str | None = None
    options: dict[str, Any] = field(default_factory=dict)
    plugins_by_id: list[tuple[str, frozenset[str]]] = field(default_factory=list)
    parallel: bool = False
    processes: int | None = None
    reports: list[Path] = field(default_factory=list)
