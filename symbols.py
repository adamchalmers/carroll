import string
import nodes
from collections import defaultdict

symbols = defaultdict(lambda: None)
for letter in string.ascii_uppercase:
    symbols[letter] = nodes.AtomNode
symbols["!"] = nodes.NotNode
symbols["~"] = nodes.NotNode
symbols["&"] = nodes.AndNode
symbols["^"] = nodes.AndNode
symbols["|"] = nodes.OrNode
symbols["v"] = nodes.OrNode

def to_node(symbol):
    return symbols[symbol]

if __name__ == "__main__":
    assert to_node("A") == nodes.AtomNode
    assert to_node("&") == nodes.AndNode
    assert to_node("v") == nodes.OrNode
    assert to_node(")") == None
