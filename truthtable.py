from __future__ import print_function
import parser
import symbols
import string
from nose.tools import assert_items_equal, assert_equal

T = True
F = False

class Row():

    def __init__(self, model, value):
        self.model = model
        self.value = value

    def __str__(self):
        return truth_to_str(self.model) + " " + str(self.value)

    def __eq__(self, other):
        return isinstance(other, Row) and self.model == other.model and self.value == other.value


def print_truth_table(exp, verbose, output=True):
    """Outputs the truth table for an expression to stdout."""
    try:
        tree = parser.parse(exp)
        table = truth_table(exp)
    except IOError as e:
        print("Parse error: %s" % e)
        return
    for row in table:
        print(row)
    if verbose:
        print()
        table = truth_table(exp)
        print_sat_info(table)

def truth_table(exp):
    """Generates truth table rows from a proposition string."""
    tree = parser.parse(exp)
    atoms = find_atoms(exp)
    for truth in gen_truths(atoms):
        yield Row(truth, tree.eval(truth))

def find_atoms(exp):
    """Returns a list of atoms in a proposition string."""
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

def all_equal(iterable):
    iterable = iter(iterable)
    first = iterable.next()
    for element in iterable:
        if element != first:
            return False
    return True

def equivalent(exp1, exp2):
    table1, table2 = truth_table(exp1), truth_table(exp2)
    return all([row1 == row2 for row1, row2 in zip(table1, table2)])

def print_sat_info(table):
    satisfiable = False
    tautology = True
    for row in table:
        if row.value:
            satisfiable = True
        else:
            tautology = False

    print("Satisfiable:\t%s" % satisfiable)
    print("Tautology:\t%s" % tautology)

    return (satisfiable, tautology)

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
            Row({"A": T, "B": T}, T),
            Row({"A": T, "B": F}, F),
            Row({"A": F, "B": T}, F),
            Row({"A": F, "B": F}, F),
    ]
    actual_table = truth_table("(A&B)")
    assert_items_equal(expected_table, actual_table)

def test_truth_table_or():
    expected_table = [
            Row({"A": T, "B": T}, T),
            Row({"A": T, "B": F}, T),
            Row({"A": F, "B": T}, T),
            Row({"A": F, "B": F}, F),
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

def test_all_equal():
    assert all_equal([1,1,1])
    assert all_equal([True])
    assert all_equal([True, True, True])
    assert all_equal([False])
    assert all_equal([False, False, False])

def test_not_all_equal():
    assert not all_equal([1,2])
    assert not all_equal([True, False])
    assert not all_equal([True, 2])

def test_sat_info():
    assert print_sat_info(truth_table("(Av~A)")) == (T, T)
    assert print_sat_info(truth_table("A")) == (T, F)
    assert print_sat_info(truth_table("~A")) == (T, F)
    assert print_sat_info(truth_table("(A&~A)")) == (F, F)
