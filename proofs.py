from parser import parse, find_atoms_in_tree
import truthtable
from nodes import AndNode, IfNode, AtomNode
from nose.tools import assert_is_instance

def serialize_argument_trees(expressions):
    """
    Takes in a list of parse tree expressions [A, B, C, ... Z].
    Outputs one parse tree ((A&B&C&...) -> Z).
    Last expression is the conclusion, all others are premises.
    """
    premises = AndNode(*expressions[:-1])
    argument = IfNode(premises, expressions[-1])
    return argument

def valid_proof(expressions):
    """
    Takes in a list of parse tree expressions [A, B, C, ... Z].
    Outputs one parse tree ((A&B&C&...) -> Z).
    Last expression is the conclusion, all others are premises.
    """
    trees = [parse(e) for e in expressions]
    argument = serialize_argument_trees(trees)
    find_atoms_in_tree(argument)
    return all([row.value for row in truthtable.from_tree(argument)])

def test_serialize_argtree_simple():
    expressions = ["A", "(A>B)", "B"]
    trees = [parse(e) for e in expressions]
    argument = serialize_argument_trees(trees)
    assert_is_instance(argument, IfNode)
    assert_is_instance(argument.l, AndNode)
    assert_is_instance(argument.r, AtomNode)
    assert_is_instance(argument.l.l, AtomNode)
    assert_is_instance(argument.l.r, IfNode)
    assert_is_instance(argument.l.r.l, AtomNode)
    assert_is_instance(argument.l.r.r, AtomNode)

def test_valid_proof():
    expressions = ["A", "(A>B)", "B"]
    assert valid_proof(expressions)

def test_invalid_proof():
    expressions = ["A", "(AxB)", "B"]
    assert not valid_proof(expressions)
