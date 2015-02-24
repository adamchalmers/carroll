from itertools import chain
from nose.tools import assert_raises, with_setup

T = True
F = False

class LogicError(Exception):
    pass

class Node(object):
    """Base class for logic nodes.

    A node forms an expression tree for a sentence of symbolic logic."""

    def __init__(self, *children):
        self.children = children

    def eval(self, model):
        """Evaluates the logic tree rooted at this node against a supplied model.

        Model is an assignment of truth values to atoms (dict of string -> bool)."""
        raise NotImplementedError

    def tree_print(self, d=0):
        """Recursively prints the logic tree to stdout."""
        raise NotImplementedError

    @property
    def l(self):
        return self.children[0]

    @property
    def r(self):
        try:
            return self.children[1]
        except IndexError:
            return None

class AndNode(Node):
    def eval(self, model):
        return all([n.eval(model) for n in self.children])
    def tree_print(self, d=0):
        print("  "*d + "&")
        self.l.tree_print(d+1)
        self.r.tree_print(d+1)

class OrNode(Node):
    def eval(self, model):
        return any([n.eval(model) for n in self.children])
    def tree_print(self, d=0):
        print("  "*d + "v")
        self.l.tree_print(d+1)
        self.r.tree_print(d+1)

class NotNode(Node):
    def eval(self, model):
        if len(self.children) != 1:
            raise LogicError("NOT is undefined for multiple children.")
        return not self.l.eval(model)
    def tree_print(self, d=0):
        print("  "*d +"~")
        self.l.tree_print(d+1)

class IfNode(Node):
    def eval(self, model):
        if len(self.children) != 2:
            raise LogicError("IF is only defined for exactly two children.")
        return not self.children[0].eval(model) or self.children[1].eval(model)

class XorNode(Node):
    def eval(self, model):
        children_values = [n.eval(model) for n in self.children]
        return any(children_values) and not all(children_values)

class IffNode(Node):
    def eval(self, model):
        children_values = [n.eval(model) for n in self.children]
        return not any(children_values) or all(children_values)


class AtomNode(Node):
    """These nodes will always form the leaves of a logic tree.

    They are the only node whose children are strings, not other nodes."""
    def eval(self, model):
        return model[self.l]
    def tree_print(self, d=0):
        print("  "*d + self.l)


def setup_tf_nodes():
    global a
    global b
    global model
    a = AtomNode("a")
    b = AtomNode("b")
    model = {"a": T, "b": F}

def teardown():
    pass

@with_setup(setup_tf_nodes, teardown)
def test_single_node_eval():
    assert a.eval(model)
    assert not b.eval(model)
    assert OrNode(a, a).eval(model)
    assert OrNode(a, b).eval(model)
    assert OrNode(b, a).eval(model)
    assert not OrNode(b, b).eval(model)
    assert AndNode(a, a).eval(model)
    assert not AndNode(a, b).eval(model)
    assert not AndNode(b, a).eval(model)
    assert not AndNode(b, b).eval(model)
    assert not NotNode(a).eval(model)
    assert NotNode(b).eval(model)

@with_setup(setup_tf_nodes, teardown)
def test_if_nodes():
    assert IfNode(a, a).eval(model)
    assert not IfNode(a, b).eval(model)
    assert IfNode(b, a).eval(model)
    assert IfNode(b, b).eval(model)

@with_setup(setup_tf_nodes, teardown)
def test_xor_nodes():
    assert not XorNode(a, a).eval(model)
    assert XorNode(a, b).eval(model)
    assert XorNode(b, a).eval(model)
    assert not XorNode(b, b).eval(model)

def test_multiple_xor_nodes():
    a = AtomNode("a")
    b = AtomNode("b")
    c = AtomNode("c")
    model = {"a": T, "b": F, "c": F}
    assert XorNode(a, b, c).eval(model)
    assert XorNode(a, a, c).eval(model)
    assert XorNode(b, a, a).eval(model)
    assert not XorNode(a, a, a).eval(model)
    assert not XorNode(b, c, b).eval(model)
    assert not XorNode(b, b, b).eval(model)


@with_setup(setup_tf_nodes, teardown)
def test_iff_nodes():
    assert IffNode(a, a).eval(model)
    assert not IffNode(a, b).eval(model)
    assert not IffNode(b, a).eval(model)
    assert IffNode(b, b).eval(model)

def test_multiple_iff_nodes():
    a = AtomNode("a")
    b = AtomNode("b")
    c = AtomNode("c")
    model = {"a": T, "b": F, "c": F}
    assert not IffNode(a, b, c).eval(model)
    assert not IffNode(a, a, c).eval(model)
    assert not IffNode(b, a, a).eval(model)
    assert IffNode(a, a, a).eval(model)
    assert IffNode(b, c, b).eval(model)
    assert IffNode(b, b, b).eval(model)

@with_setup(setup_tf_nodes, teardown)
def test_compound_node_eval():
    assert NotNode(NotNode(a)).eval(model)
    assert NotNode(AndNode(a, b)).eval(model)
    assert not NotNode(OrNode(a, b)).eval(model)
    assert OrNode(NotNode(AndNode(a,b)), NotNode(OrNode(a, b))).eval(model)
    assert NotNode(OrNode(b, b))

@with_setup(setup_tf_nodes, teardown)
def test_many_ands():
    assert AndNode(a, a, a).eval(model)
    assert AndNode(a, a, a, a).eval(model)
    assert not AndNode(a, a, b).eval(model)
    assert not AndNode(a, b, a).eval(model)
    assert not AndNode(b, a, a).eval(model)


@with_setup(setup_tf_nodes, teardown)
def test_many_ors():
    assert OrNode(b, b, a).eval(model)
    assert OrNode(b, a, a).eval(model)
    assert OrNode(a, b, a).eval(model)
    assert OrNode(a, a, b).eval(model)
    assert not OrNode(b, b, b).eval(model)

def test_single_not():
    n = NotNode(AtomNode("A"), AtomNode("B"))
    model = {"A": True, "B": True}
    assert_raises(LogicError, n.eval, model)

