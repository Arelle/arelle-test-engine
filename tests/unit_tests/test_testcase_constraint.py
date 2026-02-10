"""See COPYRIGHT.md for copyright information.
"""

from arelle.ModelValue import qname

from arelle_test_engine.constraint import Constraint


class TestConstraint:
    def test_normalize_constraints(self) -> None:
        source_constraints = [
            Constraint(count=1, pattern="A"),
            Constraint(count=2, qname=qname("B")),
            Constraint(count=2, pattern="C"),
            Constraint(count=1, pattern="A"),
            Constraint(count=1, qname=qname("B")),
        ]
        expected_constraints = [
            Constraint(count=2, pattern="A"),
            Constraint(count=3, qname=qname("B")),
            Constraint(count=2, pattern="C"),
        ]
        actual_constraints = Constraint.normalize_constraints(source_constraints)
        assert actual_constraints == expected_constraints
