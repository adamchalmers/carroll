from __future__ import print_function
import sys

import click

import truthtable
import transforms

@click.group()
def cli():
    """Carroll is a command line tool for analysing propositional logic (also known as boolean functions or expressions).
    """
    pass

@cli.command()
@click.argument("expression_1")
@click.argument("expression_2")
def equiv(expression_1, expression_2):
    """Checks whether two expressions are logically equivalent."""
    print(truthtable.equivalent(expression_1, expression_2))

@cli.command()
@click.argument("expression")
def table(expression):
    """Outputs a truth table for a logical expression."""
    truthtable.print_truth_table(expression)

@cli.command()
@click.argument("expression")
def dnf(expression):
    """Converts an expression to disjunctive normal form."""
    print(transforms.to_dnf(expression))

@cli.command()
@click.argument("expression")
def cnf(expression):
    """Converts an expression to conjunctive normal form."""
    print(transforms.to_cnf(expression))

if __name__ == "__main__":
    cli()
