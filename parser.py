import string
import nodes
import symbols
from collections import deque

def parse(exp):
    d = deque(exp)
    return _parse(d)

def _parse(exp):
    if not exp:
        raise IOError, "Not a wff."
    char = exp.popleft()
    if char in string.ascii_lowercase:
        return nodes.AtomNode(char)
    elif char == "~":
        return nodes.NotNode("~", _parse(exp))
    elif char == "(":
        l = _parse(exp)
        op = exp.popleft()
        r = _parse(exp)
        return symbols.to_node(op)(l, r)
    else:
        raise IOError, "Not a wff."

if __name__ == "__main__":
    tree = parse("~(a&b)")
    tree.tree_print()
    #parse("((a%c)&~b)").treeprint()
