"""See COPYRIGHT.md for copyright information.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from arelle_test_engine.constraint_set import ConstraintSet


@dataclass(frozen=True)
class Testcase:
    __test__ = False  # Tells pytest: Not a test class.

    base: Path
    blocked_code_pattern: str
    calc_mode: str | None
    compare_instance_uri: Path | None
    description: str
    expected_instance_count: int | None
    full_id: str
    inline_target: str | None
    local_id: str
    name: str
    parameters: str
    read_first_uris: list[str]
    reference: str | None
    constraint_set: ConstraintSet
