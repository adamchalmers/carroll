import string
from collections import deque

class Node():

    def __init__(self, op, l, r=None):
        self.op = op
        self.l = l
        self.r = r

    def __str__(self):
        if self.op == "atom": return self.l
        if self.r:
            r = ", %s" % self.r
        else:
            r = ""
        return "{%s: %s%s}" % (self.op, str(self.l), r)

    def treeprint(self, depth=0):
        space = "  "*depth
        if self.op == "atom":
            print space + self.l
        elif self.op == "~":
            print space + self.op + " {"
            self.l.treeprint(depth+1)
            print space + "}"
        else:
            print space + self.op + " {"
            self.l.treeprint(depth+1)
            self.r.treeprint(depth+1)
            print space + "}"

def parse(exp):
    d = deque(exp)
    return _parse(d)

def _parse(exp):
    if not exp:
        raise IOError, "Not a wff."
    char = exp.popleft()
    if char in string.ascii_lowercase:
        return Node("atom", char)
    elif char == "~":
        return Node("~", _parse(exp))
    elif char == "(":
        l = _parse(exp)
        op = exp.popleft()
        r = _parse(exp)
        return Node(op, l, r)
    else:
        raise IOError, "Not a wff."

if __name__ == "__main__":
    tree = parse("~(a&b)")
    tree.treeprint()
    #parse("((a%c)&~b)").treeprint()
