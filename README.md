# Carroll
Carroll is a **C**ommand-line **A**pp for **R**apidly **R**emoving **O**bstacles to **L**earning **L**ogic.

<h2>Usage</h2>
```
$ python carroll.py "((A&B) v (~A&~B))"
 A  B  True
~A  B  False
 A ~B  False
~A ~B  True
```
To find out which characters Carroll interprets as connectives (and to define your own), see `symbols.py`.

<h2>Current features:</h2>

 - Parse classical logic strings
 - Display truth tables

<h2>Planned features:</h2>

 - Check propositions for equivalences
 - Simplify expressions
 - Use user-defined connectives
