"""See COPYRIGHT.md for copyright information.
"""
from __future__ import annotations

from dataclasses import dataclass

from arelle_test_engine.error_level import ErrorLevel


@dataclass(frozen=True)
class ActualError:
    code: str
    level: ErrorLevel

    def __str__(self) -> str:
        code = "(any)" if self.code == "*" else self.code
        if self.level:
            return f"{code} [{self.level}]"
        return code
