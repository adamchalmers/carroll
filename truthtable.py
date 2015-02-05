from __future__ import print_function
import parser
import symbols
import string
from nose.tools import assert_items_equal, assert_equal

T = True
F = False

def print_truth_table(exp, output=True):
    """Outputs the truth table for an expression to stdout."""
    _table = []
    try:
        tree = parser.parse(exp)
    except IOError as e:
        print("Parse error: %s" % e)
        return
    for row in truth_table(exp):
        print(row_to_str(row))

def truth_table(exp):
    tree = parser.parse(exp)
    atoms = find_atoms(exp)
    for truth in gen_truths(atoms):
        yield (truth, tree.eval(truth))

def find_atoms(exp):
    return list(set([char for char in exp if char in string.ascii_uppercase]))

def gen_truths(atoms):
    """Yields all possible maps of variables to truth values."""
    if len(atoms) == 1:
        yield {atoms[0]: T}
        yield {atoms[0]: F}
    else:
        for truth in gen_truths(atoms[1:]):
            yield dict([(atoms[0], T)] + truth.items())
            yield dict([(atoms[0], F)] + truth.items())

def truth_to_str(truth):
    """Produce a nice-formatted string of a truth assignment, e.g. " A ~B  C"."""
    prefix = {True: " ", False: "~"}
    items = truth.items()
    items.sort()
    return "".join([prefix[value] + var + " " for var, value in items])

def row_to_str(row):
    truth_assignment, value = row
    return truth_to_str(truth_assignment) + " " + str(value)

def equivalent(exp1, exp2):
    table1, table2 = truth_table(exp1), truth_table(exp2)
    for row1, row2 in zip(table1, table2):
        if row1 != row2:
            return False
    return True


# Tests

def test_gen_truths_base():
    expected = [{"A": True}, {"A": False}]
    assert_items_equal(expected, [truth for truth in gen_truths(["A"])])

def test_gen_truths_recursive():
    expected = [
            {"A": T, "B": T},
            {"A": T, "B": F},
            {"A": F, "B": T},
            {"A": F, "B": F},
    ]
    actual = [truth for truth in gen_truths(["A", "B"])]
    assert_items_equal(expected, actual)

def test_gen_truths_recursive_long():
    expected = [
            {"A": T, "B": T, "C": T},
            {"A": T, "B": T, "C": F},
            {"A": T, "B": F, "C": T},
            {"A": T, "B": F, "C": F},
            {"A": F, "B": T, "C": T},
            {"A": F, "B": T, "C": F},
            {"A": F, "B": F, "C": T},
            {"A": F, "B": F, "C": F},
    ]
    actual = [truth for truth in gen_truths(["A", "B", "C"])]
    assert_items_equal(expected, actual)

def test_find_atoms():
    assert_items_equal(find_atoms("ABC"), list("ABC"))
    assert_items_equal(find_atoms("A B C"), list("ABC"))
    assert_items_equal(find_atoms("Av   B&C"), list("ABC"))
    assert_items_equal(find_atoms("ABC"), list("ABC"))

def test_truth_table_and():
    expected_table = [
            ({"A": T, "B": T}, T),
            ({"A": T, "B": F}, F),
            ({"A": F, "B": T}, F),
            ({"A": F, "B": F}, F),
    ]
    actual_table = truth_table("(A&B)")
    assert_items_equal(expected_table, actual_table)

def test_truth_table_or():
    expected_table = [
            ({"A": T, "B": T}, T),
            ({"A": T, "B": F}, T),
            ({"A": F, "B": T}, T),
            ({"A": F, "B": F}, F),
    ]
    actual_table = truth_table("(AvB)")
    assert_items_equal(expected_table, actual_table)

def test_equiv_simple():
    assert equivalent("A", "A")
    assert equivalent("A", "~~A")

def test_not_equiv_simple():
    assert not equivalent("A", "B")
    assert not equivalent("A", "~A")
    assert not equivalent("A", "(A&B)")

def test_equiv_complex():
    assert equivalent("(A&~B)", "(~B&(AvB))")
    assert equivalent("(AvB)", "!(!A&!B)")

def test_not_equiv_complex():
    assert not equivalent("(AvB)", "(!A&!B)")
