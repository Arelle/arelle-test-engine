"""See COPYRIGHT.md for copyright information.
"""
from __future__ import annotations

from dataclasses import dataclass

from arelle_test_engine.testcase import Testcase


@dataclass(frozen=True)
class TestcaseSet:
    __test__ = False  # Tells pytest: Not a test class.

    load_errors: list[str]
    skipped_testcases: list[Testcase]
    testcases: list[Testcase]
