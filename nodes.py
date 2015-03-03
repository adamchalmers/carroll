from nose.tools import assert_raises, with_setup
import string

T = True
F = False

class LogicError(Exception):
    pass

class Node(object):
    """Base class for logic nodes.

    A node forms an expression tree for a sentence of symbolic logic."""

    def __init__(self, *children):
        self.check_valid(children)
        self.children = children

    def eval(self, model):
        """Evaluates the logic tree rooted at this node against a supplied model.

        Model is an assignment of truth values to atoms (dict of string -> bool)."""
        raise NotImplementedError

    def check_valid(self, children):
        """Ensures the children nodes are valid. Raises LogicError if they're not."""
        if len(children) == 0:
            raise LogicError("%s can't have 0 children!", type(self))
        self.check_valid_specific(children)

    def check_valid_specific(self, children):
        """Overridden by children nodes to implement custom child-checking logic.
        Should raise LogicError if children are invalid."""
        pass

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

class OrNode(Node):
    def eval(self, model):
        return any([n.eval(model) for n in self.children])

class NotNode(Node):
    def eval(self, model):
        if len(self.children) != 1:
            raise LogicError("NOT is undefined for multiple children.")
        return not self.l.eval(model)

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
    def check_valid_specific(self, children):
        if len(children) != 1:
            raise LogicError("Can't have multiple atomic propositions in one atom %s" % str(children))
        if children[0] not in string.uppercase:
            raise LogicError("Atoms must be capital letters (your atom is %s)" % str(children[0]))
        pass


def setup_tf_nodes():
    global a
    global b
    global model
    a = AtomNode("A")
    b = AtomNode("B")
    model = {"A": T, "B": F}

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
    a = AtomNode("A")
    b = AtomNode("B")
    c = AtomNode("C")
    model = {"A": T, "B": F, "C": F}
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
    a = AtomNode("A")
    b = AtomNode("B")
    c = AtomNode("C")
    model = {"A": T, "B": F, "C": F}
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

@with_setup(setup_tf_nodes, teardown)
def test_single_atom():
    assert_raises(LogicError, AtomNode, *(a,b))

def test_atoms_uppercase():
    assert_raises(LogicError, AtomNode, "a")

def test_check_valid():
    assert_raises(LogicError, AtomNode)

