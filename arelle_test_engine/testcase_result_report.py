"""
See COPYRIGHT.md for copyright information.
"""
from pathlib import Path

from arelle.ViewFile import View

from arelle_test_engine.test_engine_result import TestEngineResult
from arelle_test_engine.testcase_result import TestcaseResult


def save_report(
        test_engine_result: TestEngineResult,
        outfile: Path,
        columns: list[str] | None = None,
) -> None:
    view = TestcaseResultReport(str(outfile), columns)
    view.view_test_engine_result(test_engine_result)
    view.close()


COLUMN_WIDTHS = {
    "Id": 50,
    "Name": 50,
    "Description": 50,
    "Reference": 20,
    "ReadMeFirst": 20,
    "Status": 8,
    "Expected": 20,
    "Actual": 100,
}


class TestcaseResultReport(View):  # type: ignore[misc]
    def __init__(self, outfile: str, columns: list[str] | None):
        super().__init__(None, outfile, "Tests")
        self.columns = columns or []
        self.errors: list[str] = []

    def view_test_engine_result(self, test_engine_result: TestEngineResult) -> None:
        if self.columns:
            unrecognized_columns = []
            for column in self.columns:
                if column not in COLUMN_WIDTHS:
                    unrecognized_columns.append(column)
            if unrecognized_columns:
                self.errors.append("Unrecognized columns: " + ",".join(unrecognized_columns))
        else:
            self.columns = [
                "Id",
                "Name",
                "Description",
                "Reference",
                "ReadMeFirst",
                "Status",
                "Expected",
                "Actual",
            ]

        self.setColWidths([COLUMN_WIDTHS.get(col, 8) for col in self.columns])
        self.addRow(self.columns, asHeader=True)

        for testcase_result in test_engine_result.testcase_results:
            self.view_testcase_result(testcase_result)

    def view_testcase_result(self, testcase_result: TestcaseResult) -> None:
        testcase = testcase_result.testcase
        cols = []
        for col in self.columns:
            if col == "Id":
                cols.append(testcase.full_id)
            elif col == "Name":
                cols.append(testcase.name)
            elif col == "Description":
                cols.append(testcase.description)
            elif col == "Reference":
                cols.append(testcase.reference or "")
            elif col == "ReadMeFirst":
                cols.append(" ".join(str(uri) for uri in testcase.read_first_uris))
            elif col == "Status":
                cols.append(testcase_result.status)
            elif col == "Expected":
                expected = ", ".join(
                    str(constraint)
                    for constraint in testcase_result.applied_constraint_set.constraints
                )
                cols.append(expected)
            elif col == "Actual":
                actual = ", ".join(
                    str(actual_error)
                    for actual_error in testcase_result.actual_errors
                )
                cols.append(actual)
            else:
                cols.append("")
        self.addRow(cols, xmlRowElementName="testcase")
