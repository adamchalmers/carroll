import string
import nodes
from collections import defaultdict

NODE_TYPES = [(string.ascii_uppercase, nodes.AtomNode),
    ("&^", nodes.AndNode),
    ("|v", nodes.OrNode),
    ("!~", nodes.NotNode),
    ("x", nodes.XorNode),
    (">", nodes.IfNode),
    ("=", nodes.IffNode),
]

# Map every recognized character to its node type.
_symbols = defaultdict(lambda: None)
for symbols, node in NODE_TYPES:
    for symbol in symbols:
        _symbols[symbol] = node


def meaning_of(symbol):
    """Returns the type of node this symbol represents."""
    return _symbols[symbol]

def test_symbol_mapping():
    assert meaning_of("A") == nodes.AtomNode
    assert meaning_of("B") == nodes.AtomNode
    assert meaning_of("Y") == nodes.AtomNode
    assert meaning_of("&") == nodes.AndNode
    assert meaning_of("v") == nodes.OrNode
    assert meaning_of(")") == None
    assert meaning_of("(") == None
    assert meaning_of("d") == None

