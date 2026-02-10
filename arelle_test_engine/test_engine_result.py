"""See COPYRIGHT.md for copyright information.
"""
from __future__ import annotations

from dataclasses import dataclass

from arelle_test_engine.testcase_result import TestcaseResult
from arelle_test_engine.testcase_set import TestcaseSet


@dataclass(frozen=True)
class TestEngineResult:
    __test__ = False  # Tells pytest: Not a test class.

    testcase_results: list[TestcaseResult]
    testcase_set: TestcaseSet
