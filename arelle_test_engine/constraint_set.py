"""See COPYRIGHT.md for copyright information.
"""
from __future__ import annotations

from dataclasses import dataclass

from arelle_test_engine.constraint import Constraint


@dataclass(frozen=True)
class ConstraintSet:
    constraints: list[Constraint]
    match_all: bool | None
