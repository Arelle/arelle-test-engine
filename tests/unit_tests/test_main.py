"""See COPYRIGHT.md for copyright information.
"""

from pathlib import Path

import pytest
from arelle.ModelValue import QName

from arelle_test_engine.__main__ import _parse
from arelle_test_engine.constraint import Constraint
from arelle_test_engine.error_level import ErrorLevel

CONFORMANCE_URI = "http://xbrl.org/2005/conformance"
TEST_URI = "http://xbrl.org/2005/test"


def _qname(localName: str, namespaceURI: str = CONFORMANCE_URI) -> QName:
    return QName(None, namespaceURI=namespaceURI, localName=localName)


class TestMain:

    def test_parse_config_only(self) -> None:
        options = _parse([
            "--config", str(Path("tests/unit_tests/resources/configs/test_config_all.json")),
        ])
        assert options.index_file == Path("tests/unit_tests/resources/test_suite/index.xml")
        assert options.filters == ["filter1", "filter2"]
        assert options.additional_constraints == [
            ("testcase1", [
                Constraint(count=1, pattern="*"),
                Constraint(count=2, level=ErrorLevel.WARNING, pattern="1.2.3"),
            ]),
            ("testcase2", [
                Constraint(count=3, pattern="1.2.3"),
            ]),
        ]
        assert options.compare_formula_output is True
        assert options.custom_compare_patterns == [
            ("pattern1", "replacement1"),
            ("pattern2", "replacement2"),
        ]
        assert options.disclosure_system_by_id == [
            ("ds1", "http://example.com/ds1"),
            ("ds2", "http://example.com/ds2"),
        ]
        assert options.ignore_levels == frozenset({ErrorLevel.OK, ErrorLevel.SATISFIED, ErrorLevel.WARNING})
        assert options.plugins_by_id == [
            ("testcase1", frozenset({"plugin1", "plugin2"})),
            ("testcase2", frozenset({"plugin3"})),
        ]
        assert options.log_directory == Path(".test_engine/all")
        assert options.match_all is False
        assert options.name == "All"
        assert options.parallel is True
        assert options.processes == 8
        assert options.options == {
            "option1": "value1",
            "option2": 2,
            "option3": True,
            "option4": [1, 2, 3],
        }

    def test_parse_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError) as _:
            _ = _parse([
                "--config", str(Path("tests/unit_tests/resources/configs/not_found.json")),
            ])

    def test_parse_index_only(self) -> None:
        index_path = Path("tests/unit_tests/resources/test_suite/index.xml")
        options = _parse([
            str(index_path),
        ])
        assert options.index_file == index_path
        assert options.filters == []
        assert options.additional_constraints == []
        assert options.compare_formula_output is False
        assert options.custom_compare_patterns == []
        assert options.disclosure_system_by_id == []
        assert options.ignore_levels == frozenset({ErrorLevel.OK})
        assert options.plugins_by_id == []
        assert options.log_directory is None
        assert options.match_all is True
        assert options.name == "index"
        assert options.parallel is False
        assert options.processes is None
        assert options.options == {}

    def test_parse_file_invalid(self) -> None:
        with pytest.raises(RuntimeError) as _:
            _ = _parse([
                "--config", str(Path("tests/unit_tests/resources/configs/test_config_invalid.json")),
            ])

    def test_parse_overrides(self) -> None:
        index_path = Path("tests/unit_tests/resources/test_suite/index.xml")
        options = _parse([
            str(index_path),
            "--filter", "override",
            "--ignore-level", "warning",
            "--log-directory", ".override/all",
            "--match", "all",
            "--name", "override",
            "--series",
            "--config", str(Path("tests/unit_tests/resources/configs/test_config_all.json")),
        ])
        assert options.index_file == index_path
        assert options.filters == ["override"]
        assert options.additional_constraints == [
            ("testcase1", [
                Constraint(count=1, pattern="*"),
                Constraint(count=2, level=ErrorLevel.WARNING, pattern="1.2.3"),
            ]),
            ("testcase2", [
                Constraint(count=3, pattern="1.2.3"),
            ]),
        ]
        assert options.compare_formula_output is True
        assert options.custom_compare_patterns == [
            ("pattern1", "replacement1"),
            ("pattern2", "replacement2"),
        ]
        assert options.disclosure_system_by_id == [
            ("ds1", "http://example.com/ds1"),
            ("ds2", "http://example.com/ds2"),
        ]
        assert options.ignore_levels == frozenset({ErrorLevel.WARNING})
        assert options.plugins_by_id == [
            ("testcase1", frozenset({"plugin1", "plugin2"})),
            ("testcase2", frozenset({"plugin3"})),
        ]
        assert options.log_directory == Path(".override/all")
        assert options.match_all is True
        assert options.name == "override"
        assert options.parallel is False
        assert options.processes == 8
        assert options.options == {
            "option1": "value1",
            "option2": 2,
            "option3": True,
            "option4": [1, 2, 3],
        }

    def test_parse_overrides2(self) -> None:
        index_path = Path("tests/unit_tests/resources/test_suite/index.xml")
        options = _parse([
            str(index_path),
            "--compare-formula-output",
            "--filter", "override",
            "--ignore-level", "warning",
            "--log-directory", ".override/all",
            "--match", "any",
            "--name", "override",
            "--parallel",
            "--processes", "4",
            "--config", str(Path("tests/unit_tests/resources/configs/test_config_override.json")),
        ])
        assert options.index_file == index_path
        assert options.filters == ["override"]
        assert options.additional_constraints == [
            ("testcase1", [
                Constraint(count=1, pattern="*"),
                Constraint(count=2, level=ErrorLevel.WARNING, pattern="1.2.3"),
            ]),
            ("testcase2", [
                Constraint(count=3, pattern="1.2.3"),
            ]),
        ]
        assert options.compare_formula_output is True
        assert options.custom_compare_patterns == [
            ("pattern1", "replacement1"),
            ("pattern2", "replacement2"),
        ]
        assert options.disclosure_system_by_id == [
            ("ds1", "http://example.com/ds1"),
            ("ds2", "http://example.com/ds2"),
        ]
        assert options.ignore_levels == frozenset({ErrorLevel.WARNING})
        assert options.plugins_by_id == [
            ("testcase1", frozenset({"plugin1", "plugin2"})),
            ("testcase2", frozenset({"plugin3"})),
        ]
        assert options.log_directory == Path(".override/all")
        assert options.match_all is False
        assert options.name == "override"
        assert options.parallel is True
        assert options.processes == 4
        assert options.options == {
            "option1": "value1",
            "option2": 2,
            "option3": True,
            "option4": [1, 2, 3],
        }
