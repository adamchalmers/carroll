# Carroll
Carroll is a **C**ommand-line **A**pp for **R**apidly **R**emoving **O**bstacles to **L**earning **L**ogic.

<h2>Usage</h2>
```
$ python carroll.py table "((A&B) v (~A&~B))"
 A  B  True
~A  B  False
 A ~B  False
~A ~B  True
```
To find out which characters Carroll interprets as connectives (and to define your own), see `symbols.py`.

**Commands:**

 - ```table```: Prints a truth table for an expression.
 - ```equiv```: Checks two expressions for logical equivalence (i.e. whether they compute the same boolean function)
 - ```cnf``` and ```dnf```: Converts an expression to its equivalent in conjunctive or disjunctive normal form.

**Dependencies:** Carroll uses Nose and Click.

<h2>Current features:</h2>

 - Parse classical logic strings
 - Display truth tables
 - Check two propositions for equivalences

<h2>Planned features:</h2>

 - Check any number of propositions for equivalence, mutual satisfiability, etc
 - Simplify expressions
 - Use user-defined connectives?
