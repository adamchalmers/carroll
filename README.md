# Carroll
Carroll is a **C**ommand-line **A**pp for **R**apidly **R**emoving **O**bstacles to **L**earning **L**ogic.

<h2>Usage</h2>
```
$ python carroll.py "((A&B)v(~A&~B))"
 A  B  True
~A  B  False
 A ~B  False
~A ~B  True
```

<h2>Current features:</h2>

 - Parse classical logic strings
 - Display truth tables

<h2>Planned features:</h2>

 - Evaluate propositions against a model
 - Check propositions for equivalences
 - Simplify expressions
 - Use user-defined connectives
