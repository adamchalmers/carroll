import string
import symbols
from collections import deque
from nose.tools import assert_equals, assert_raises, assert_is_instance
from symbols import meaning_of
from nodes import AtomNode, NotNode, AndNode, OrNode, XorNode, IfNode, IffNode

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

    # Atom node case
    if meaning_of(char) == AtomNode:
        return AtomNode(char)

    # Single-operand node case (i.e. NOT node)
    elif meaning_of(char) == NotNode:
        return NotNode(_parse(exp))

    # Multiple-operand node case (e.g. AND, NOT)
    elif char == "(":
        l = _parse(exp)
        _op = exp[0]
        more = []
        while exp and exp[0] == _op:
            op = exp.popleft()
            more.append(_parse(exp))
        if not exp or exp.popleft() != ")":
            raise IOError("Missing )")
        return meaning_of(op)(l, *more)
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

def test_multiple_operand_parse():
    n = parse("(A&A&A)")
    assert_is_instance(n, AndNode)
    for child in n.children:
        assert_is_instance(child, AtomNode)

def test_dnf_parse():
    exp = "((A & B & C) v (A & B & ~C) v (A & ~B & C))"
    n = parse(exp)
    assert_is_instance(n, OrNode)

def test_multiple_operand_fail():
    assert_raises(IOError, parse, "(A|A&A)")

def test_parse_if():
    n = parse("(A>B)")
    assert_is_instance(n, IfNode)
    assert_is_instance(n.l, AtomNode)
    assert_is_instance(n.r, AtomNode)

def test_parse_iff():
    n = parse("(A=B)")
    assert_is_instance(n, IffNode)
    assert_is_instance(n.l, AtomNode)
    assert_is_instance(n.r, AtomNode)

def test_parse_xor():
    n = parse("(AxB)")
    assert_is_instance(n, XorNode)
    assert_is_instance(n.l, AtomNode)
    assert_is_instance(n.r, AtomNode)