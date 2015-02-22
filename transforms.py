import truthtable
import parser
from nose.tools import assert_equals, assert_items_equal

def to_dnf(expression):
    """Converts a proposition string into a DNF string."""
    table = truthtable.truth_table(expression)
    output = "("
    for row in table:
        if row.value:
            output += "(%s) v " % model_to_and_clause(row.model)
    output = output[:-3] + ")"
    return output

def to_cnf(expression):
    table = truthtable.truth_table(expression)
    output = "("
    for row in table:
        if not row.value:
            output += "(%s) & " % model_to_cnf_clause(row.model)
    output = output[:-3] + ")"
    return output

def model_to_and_clause(model):
    l = []
    for atom, truth in model.items():
        if truth:
            l.append((atom, atom))
        else:
            l.append((atom, "~"+atom))
    l.sort()
    return " & ".join([elem[1] for elem in l])

def model_to_cnf_clause(model):
    l = []
    for atom, truth in model.items():
        if truth:
            l.append((atom, "~"+atom))
        else:
            l.append((atom, atom))
    l.sort()
    return " v ".join([elem[1] for elem in l])

def test_basic_dnf():
    expression = "(A & (B | C))"
    expected = "((A & B & C) v (A & B & ~C) v (A & ~B & C))"
    actual = to_dnf(expression)
    assert_equals(expected, actual)

def test_longer_dnf():
    expression_cnf = "((~A v ~B v ~C) & (~A v B v ~C) & (~A v B v C) & (A v ~B v ~C) & (A v ~B v C))"
    actual = to_dnf(expression_cnf)
    expected_dnf = "((A & B & ~C) v (~A & ~B & C) v (~A & ~B & ~C))"
    assert_equals(expected_dnf, actual)

def test_basic_cnf():
    expression = "(~A & (B v C))"
    expected = "((~A v ~B v ~C) & (~A v ~B v C) & (~A v B v ~C) & (~A v B v C) & (A v B v C))"
    actual = to_cnf(expression)
    assert_equals(expected, actual)

def test_longer_cnf():
    expression_dnf = "((A & B & ~C) v (~A & ~B & C) v (~A & ~B & ~C))"
    actual = to_cnf(expression_dnf)
    expected_cnf = "((~A v ~B v ~C) & (~A v B v ~C) & (~A v B v C) & (A v ~B v ~C) & (A v ~B v C))"

    # We strip out the opening/closing brackets, and compare the clauses
    # so the strangely-ordered CNF conversion doesn't ruin our test.
    assert_items_equal(expected_cnf[1:-1].split(" & "), actual[1:-1].split(" & "))
