from __future__ import print_function
import parser
import symbols
import string
from nose.tools import assert_items_equal

T = True
F = False

def print_truth_table(exp):
    try:
        tree = parser.parse(exp)
        atoms = list(set([char for char in exp if char in string.ascii_uppercase]))
        for truth in gen_truths(atoms):
            print(truth_to_str(truth), tree.eval(truth))
    except IOError as e:
        print("Parse error: %s" % e)

def gen_truths(atoms):
    if len(atoms) == 1:
        yield {atoms[0]: T}
        yield {atoms[0]: F}
    else:
        for truth in gen_truths(atoms[1:]):
            yield dict([(atoms[0], T)] + truth.items())
            yield dict([(atoms[0], F)] + truth.items())

def truth_to_str(truth):
    s = ""
    prefix = {True: " ", False: "~"}
    items = truth.items()
    items.sort()
    for var, value in items:
        s += prefix[value] + var + " "
    return s

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

