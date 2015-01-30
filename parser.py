import string
import symbols
from collections import deque
from nose.tools import assert_equals, assert_raises, assert_is_instance
from symbols import meaning_of
from nodes import AtomNode, NotNode, AndNode, OrNode

def parse(exp):
    """Starts parsing a logical expression (supplied as a string). Returns a tree of Nodes."""
    exp = exp.replace(" ", "")
    d = deque(exp)
    tree = _parse(d)
    if d:
        raise IOError("Unconsumed tokens %s" % "".join(d))
    else:
        return tree

def _parse(exp):
    """Recursive-descent parsing algorithm for logic expressions. Returns a tree of Nodes."""
    if not exp:
        raise IOError("Empty string is not a wff.")
    char = exp.popleft()
    if meaning_of(char) == AtomNode:
        return AtomNode(char)
    elif meaning_of(char) == NotNode:
        return NotNode(_parse(exp))
    elif char == "(":
        l = _parse(exp)
        op = exp.popleft()
        r = _parse(exp)
        if not exp or exp.popleft() != ")":
            raise IOError("Missing )")
        return meaning_of(op)(l, r)
    else:
        raise IOError("%s can't start a wff." % char)

def test_error_parse():
    assert_raises(IOError, parse, "")
    assert_raises(IOError, parse, "(")
    assert_raises(IOError, parse, "()")
    assert_raises(IOError, parse, "(~)")
    assert_raises(IOError, parse, "&")
    assert_raises(IOError, parse, "BvC")
    assert_raises(IOError, parse, "A&A")
    assert_raises(IOError, parse, "(A&BC")
    assert_raises(IOError, parse, "(A&B")

def test_spaces_parse():
    parse("(A & B)")
    parse("(A& ~ B)")

def test_atom_parse():
    assert_is_instance(parse("A"), AtomNode)
    assert_is_instance(parse("D"), AtomNode)
    assert_is_instance(parse("Q"), AtomNode)

def test_not_parse():
    n = parse("~~A")
    assert_is_instance(n, NotNode)
    assert_is_instance(n.l, NotNode)
    assert_is_instance(n.l.l, AtomNode)

def test_simple_and_parse():
    n = parse("(A&B)")
    assert_is_instance(n, AndNode)
    assert_is_instance(n.l, AtomNode)
    assert_is_instance(n.r, AtomNode)

def test_complex_and_parse():
    n = parse("(~A&B)")
    assert_is_instance(n, AndNode)
    assert_is_instance(n.l, NotNode)
    assert_is_instance(n.l.l, AtomNode)
    assert_is_instance(n.r, AtomNode)

def test_multiple_and_parse():
    n = parse("(A&(B&C))")
    assert_is_instance(n, AndNode)
    assert_is_instance(n.r, AndNode)

def test_simple_or_parse():
    n = parse("(AvB)")
    assert_is_instance(n, OrNode)
    assert_is_instance(n.l, AtomNode)
    assert_is_instance(n.r, AtomNode)

def test_complex_or_parse():
    n = parse("(~A|B)")
    assert_is_instance(n, OrNode)
    assert_is_instance(n.l, NotNode)
    assert_is_instance(n.l.l, AtomNode)

def test_multiple_or_parse():
    n = parse("(Av(B|C))")
    assert_is_instance(n, OrNode)
    assert_is_instance(n.r, OrNode)

def test_complex_parse():
    n = parse("((~A|B)v(B&~C))")
    assert_is_instance(n, OrNode)
    assert_is_instance(n.l, OrNode)
    assert_is_instance(n.l.r, AtomNode)
    assert_is_instance(n.l.l, NotNode)
    assert_is_instance(n.l.l.l, AtomNode)
    assert_is_instance(n.r, AndNode)
    assert_is_instance(n.r.l, AtomNode)
    assert_is_instance(n.r.r, NotNode)
    assert_is_instance(n.r.r.l, AtomNode)

if __name__ == "__main__":
    n = parse("((~A|B)v(B&~C))")
    n.tree_print()
