"""See COPYRIGHT.md for copyright information.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from arelle_test_engine.testcase_set import TestcaseSet


class TestcaseLoader(ABC):
    __test__ = False  # Tells pytest: Not a test class.

    @abstractmethod
    def is_loadable(self, index_file: Path) -> bool:
        """Is the given index file able to be loaded by this loader?
        :param index_file:
        :return:
        """

    @abstractmethod
    def load(self, index_file: Path) -> TestcaseSet:
        """Returns a testcase set generated based on the provided path.
        :param index_file:
        :return:
        """
