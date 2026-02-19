import argparse
import json
import sys
from pathlib import Path
from typing import Any

from arelle_test_engine.constraint import Constraint
from arelle_test_engine.error_level import ErrorLevel
from arelle_test_engine.test_engine import TestEngine
from arelle_test_engine.test_engine_options import TestEngineOptions


def _load_config(config_path: Path) -> dict[str, Any]:
    """
    Parses the JSON configuration file and converts types to match TestEngineOptions.
    """
    data: dict[str, Any]
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    try:
        with config_path.open("r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise RuntimeError("Failed to parse configuration file.") from e


def _parse(args: list[str]) -> TestEngineOptions:
    parser = argparse.ArgumentParser(
        description="Arelle Test Engine",
    )
    parser.add_argument(
        "index_file",
        type=Path,
        nargs="?",
        help="Path to the test index file (optional if provided in config).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a JSON configuration file.",
    )
    parser.add_argument(
        "--compare-formula-output",
        action="store_true",
        default=None,
        help="Treat 'instance' elements in expected testcase results as expected "
             "formula output rather than instance facts.",
    )
    parser.add_argument(
        "--filter",
        action="append",
        dest="filters",
        default=None,
        help="If any are provided, only testcases with an ID matching a filter will "
             "be executed.",
    )
    parser.add_argument(
        "--ignore-level",
        action="append",
        dest="ignore_levels",
        default=None,
        choices=[lvl.name.lower() for lvl in ErrorLevel],
        help="Errors with the specified level(s) will be ignored when evaluating "
             "testcase results.",
    )
    parser.add_argument(
        "--log-directory",
        type=Path,
        default=None,
        help="If provided, test logs will be written to files in this directory. "
             "Otherwise logs will be written to standard output.",
    )
    parser.add_argument(
        "--match", choices=["all", "any"],
        dest="match",
        default=None,
        help="Whether all constraints must be met for a testcase to pass (match-all), "
             "or if any single constraint being met is sufficient (match-any).",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="An optional name for this test run, used in logging and reporting.",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        dest="parallel",
        default=None,
        help="Whether to execute testcases in parallel (series execution is the default).",
    )
    parser.add_argument(
        "--series",
        action="store_false",
        dest="parallel",
        default=None,
        help="Whether to execute testcases in series.",
    )
    parser.add_argument(
        "--processes",
        type=int,
        default=None,
        help="The number of worker processes to use for parallel execution. If not "
             "provided, the number of available CPU cores will be used.",
    )
    parser.add_argument(
        "--report",
        action="append",
        type=Path,
        dest="reports",
        default=None,
        help="Generate report(s) in the following formats: CSV, HTML, JSON, XLSX, XML.",
    )

    parsed_args = parser.parse_args(args)

    # Load configuration from file
    config_values = _load_config(parsed_args.config) if parsed_args.config else {}

    # Extract CLI overrides
    cli_overrides = {k: v for k, v in vars(parsed_args).items() if v is not None}

    # Merge
    # TestEngineOptions defaults < Config file < CLI overrides
    merged = {
        **TestEngineOptions(Path()).__dict__,
        **_process_raw_options(config_values),
        **_process_raw_options(cli_overrides),
    }

    if not merged.get("index_file"):
        parser.error("the following arguments are required: index_file (via CLI or config)")

    return TestEngineOptions(
        index_file=merged["index_file"],
        additional_constraints=merged["additional_constraints"],
        compare_formula_output=merged["compare_formula_output"],
        custom_compare_patterns=merged["custom_compare_patterns"],
        disclosure_system_by_id=merged["disclosure_system_by_id"],
        filters=merged["filters"],
        ignore_levels=merged["ignore_levels"],
        log_directory=merged["log_directory"],
        match_all=merged["match_all"],
        name=merged["name"],
        options=merged["options"],
        plugins_by_id=merged["plugins_by_id"],
        parallel=merged["parallel"],
        processes=merged["processes"],
        reports=merged["reports"],
    )


def _process_raw_options(data: dict[str, Any]) -> dict[str, Any]:

    if data.get("index_file"):
        index_path = Path(data["index_file"])
        data["index_file"] = index_path
        if not data.get("name"):
            data["name"] = index_path.stem

    if data.get("log_directory"):
        data["log_directory"] = Path(data["log_directory"])

    if data.get("match") == "all":
        data["match_all"] = True
    elif data.get("match") == "any":
        data["match_all"] = False

    if "ignore_levels" in data:
        data["ignore_levels"] = frozenset(
            ErrorLevel[lvl.upper()] for lvl in data["ignore_levels"]
        )

    if "additional_constraints" in data:
        additional_constraints = []
        for testcase_id, values in data["additional_constraints"]:
            constraints = []
            for constraint in values:
                if "level" in constraint:
                    constraint["level"] = ErrorLevel[constraint["level"].upper()]
                constraints.append(Constraint(**constraint))
            additional_constraints.append((
                str(testcase_id),
                constraints,
            ))
        data["additional_constraints"] = additional_constraints

    if "custom_compare_patterns" in data:
        data["custom_compare_patterns"] = [
            (str(k), str(v)) for k, v in data["custom_compare_patterns"]
        ]

    if "disclosure_system_by_id" in data:
        data["disclosure_system_by_id"] = [
            (str(k), str(v)) for k, v in data["disclosure_system_by_id"]
        ]

    if "plugins_by_id" in data:
        data["plugins_by_id"] = [
            (str(k), frozenset(v)) for k, v in data["plugins_by_id"]
        ]

    return data


def _run(args: list[str]) -> None:
    """
    Entry point for engine execution.
    """
    options = _parse(args)
    test_engine = TestEngine(options)
    result = test_engine.run()
    if any(
            not r.passed and not r.skip
            for r in result.testcase_results
    ):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    _run(sys.argv[1:])
