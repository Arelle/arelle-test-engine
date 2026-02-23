from pathlib import Path, PurePath

from tests.integration_tests.validation.conformance_suite_config import (
    CiConfig,
    ConformanceSuiteAssetConfig,
    ConformanceSuiteConfig,
)

config = ConformanceSuiteConfig(
    assets=[
        ConformanceSuiteAssetConfig.local_conformance_suite(
            Path("test_suite"),
            entry_point=Path("index.xml"),
        ),
    ],
    ci_config=CiConfig(fast=True),
    expected_failure_ids=frozenset(f"tests/{s}" for s in {
        "001_valid/testcase.xml:fail-code",
        "001_valid/testcase.xml:fail-invalid",
        "002_invalid/testcase.xml:fail-code-mismatch",
        "002_invalid/testcase.xml:fail-valid",
    }),
    info_url="https://github.com/Arelle/arelle-test-engine",
    name=PurePath(__file__).stem,
    test_case_result_options='match-any',
)
