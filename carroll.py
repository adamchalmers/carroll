import truthtable
import sys
import click

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

if __name__ == "__main__":
    cli()
