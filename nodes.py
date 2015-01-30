T = True
F = False

class Node(object):
    def __init__(self, l, r=None):
        self.l = l
        self.r = r
    def eval(self, model):
        raise NotImplementedError
    def tree_print(self, d=0):
        raise NotImplementedError



class AndNode(Node):
    def eval(self, model):
        return self.l.eval(model) and self.r.eval(model)
    def tree_print(self, d=0):
        print "  "*d, "&"
        self.l.tree_print(d+1)
        self.r.tree_print(d+1)

class OrNode(Node):
    def eval(self, model):
        return self.l.eval(model) or self.r.eval(model)
    def tree_print(self, d=0):
        print "  "*d, "v"
        self.l.tree_print(d+1)
        self.r.tree_print(d+1)

class NotNode(Node):
    def eval(self, model):
        return not self.l.eval(model)
    def tree_print(self, d=0):
        print "  "*d, "~"
        self.l.tree_print(d+1)

class AtomNode(Node):
    def eval(self, model):
        return model[self.l]
    def tree_print(self, d=0):
        print "  "*d, self.l

def test_single_node_eval():
    a = AtomNode("a")
    b = AtomNode("b")
    model = {"a": T, "b": F}
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

def test_compound_node_eval():
    a = AtomNode("a")
    b = AtomNode("b")
    model = {"a": T, "b": F}
    assert NotNode(NotNode(a)).eval(model)
    assert NotNode(AndNode(a, b)).eval(model)
    assert not NotNode(OrNode(a, b)).eval(model)
    assert OrNode(NotNode(AndNode(a,b)), NotNode(OrNode(a, b))).eval(model)
    assert NotNode(OrNode(b, b))
