# Carroll
Carroll is a **C**ommand-line **A**pp for **R**apidly **R**emoving **O**bstacles to **L**earning **L**ogic.

<h2>Usage</h2>
Example: using Carroll to get a truth table for an expression.
```
$ python carroll.py table "((A&B) v (~A&~B))" --verbose
 A  B  True
~A  B  False
 A ~B  False
~A ~B  True

Satisfiable: True
Tautology: False
```
Example: using Carroll to check the validity of modus ponens.
```
$ python carroll.py proof
 > (A>B)
 > A
 > B
 >
Valid
```

<h3>Connectives/operators:</h3>
- **AND:** & or ^
- **OR:** \| or v
- **NOT:** ~ or !
- **IF:** >
- **IFF:** =
- **XOR:** x

<h3>Dependencies</h3> 
Carroll uses Nose and Click.


<h2>Commands</h2>

 - ```table```: Prints a truth table for an expression. Optionally checks satisfiability and tautology too.
 - ```equiv```: Checks two expressions for logical equivalence (i.e. whether they compute the same boolean function)
 - ```cnf``` and ```dnf```: Converts an expression to its equivalent in conjunctive or disjunctive normal form.
 - ```proof```: Accepts propositions from stdin until an empty proposition is entered. Checks if the last proposition (conclusion) is implied by the previous propositions (premises).

<h2>Planned features:</h2>

 - Check any number of propositions for equivalence, mutual satisfiability, etc
 - Simplify expressions
 - Use user-defined connectives?
