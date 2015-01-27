import string
import symbols
from nodes import AndNode, OrNode, NotNode, AtomNode

def parse(expression):
    """Return an expression tree, given a sentence."""

    # Check if it's an atom, 1-prefix or 2-infix expression,
    # then parse out the appropriate subexpressions or return the atom.

    # Atom case
    if expression[0] in symbols.ATOM:
        return AtomNode(expression[0])
    # NOT case
    elif expression[0] in symbols.NOT:
        return NotNode(parse(expression[1:]))


if __name__ == "__main__":
    assert type(parse("A")) == AtomNode
    assert type(parse("!A")) == NotNode
    assert type(parse("~A")) == NotNode
    assert type(parse("~A").l) == AtomNode
