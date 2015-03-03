from nose.tools import with_setup
import nodes

"""
This class contains methods for transforming a logic node (expression).
Main use is for finding simpler representations of an expression.
e.g. [n for n in all_transforms(exp)]
"""

def all_transforms(node):
    """Returns all valid transformations of this node.
    Runs through each transform function.
    """
    pass

def commutative(node):
    if type(node) in [nodes.OrNode, nodes.AndNode, nodes.IffNode]:
        return type(node)(*node.children[::-1])
    return None

def idempotent(node):
    if type(node) in [nodes.AndNode, nodes.OrNode]:
        if set([type(child) for child in node.children]) == set([nodes.AtomNode]):
            if len(set([child.l for child in node.children])) == 1:
                return nodes.AtomNode(node.children[0].l)
    return None


def setup_tf_nodes():
    global a
    global b
    global model
    a = nodes.AtomNode("A")
    b = nodes.AtomNode("B")

def teardown():
    pass

@with_setup(setup_tf_nodes, teardown)
def test_commutative():
    n = nodes.AndNode(a, b)
    reversed_n = commutative(n)
    assert n.l.l == "A"
    assert n.r.l == "B"
    n = nodes.OrNode(a, b)
    reversed_n = commutative(n)
    assert n.l.l == "A"
    assert n.r.l == "B"
    n = nodes.IffNode(a, b)
    reversed_n = commutative(n)
    assert n.l.l == "A"
    assert n.r.l == "B"

@with_setup(setup_tf_nodes, teardown)
def test_not_commutative():
    n = nodes.XorNode(a, b)
    assert commutative(n) is None

@with_setup(setup_tf_nodes, teardown)
def test_idempotent():
    n = nodes.AndNode(a, a)
    m = idempotent(n)
    assert type(m) == nodes.AtomNode
    assert m.l == "A"
    n = nodes.OrNode(a, a)
    m = idempotent(n)
    assert type(m) == nodes.AtomNode
    assert m.l == "A"


@with_setup(setup_tf_nodes, teardown)
def test_not_idempotent():
    n = nodes.AndNode(a, b)
    assert idempotent(n) is None