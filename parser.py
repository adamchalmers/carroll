from nose.tools import assert_equals, assert_raises, assert_is_instance
import string
from nodes import AtomNode, NotNode, AndNode, OrNode
from symbols import meaning_of
import symbols
from collections import deque

def parse(exp):
    d = deque(exp)
    return _parse(d)

def _parse(exp):
    if not exp:
        raise IOError, "Not a wff."
    char = exp.popleft()
    if meaning_of(char) == AtomNode:
        return AtomNode(char)
    elif meaning_of(char) == NotNode:
        return NotNode(_parse(exp))
    elif char == "(":
        l = _parse(exp)
        op = exp.popleft()
        r = _parse(exp)
        return meaning_of(op)(l, r)
    else:
        raise IOError, "Not a wff."

def test_error_parse():
    assert_raises(IOError, parse, "")
    assert_raises(IOError, parse, "(")
    assert_raises(IOError, parse, "()")
    assert_raises(IOError, parse, "(~)")
    assert_raises(IOError, parse, "&")

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
