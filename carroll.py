import truthtable
import sys
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument("expression_1")
@click.argument("expression_2")
def equiv(expression_1, expression_2):
    print(truthtable.equivalent(expression_1, expression_2))

@cli.command()
@click.argument("expression")
def table(expression):
    truthtable.print_truth_table(expression)

if __name__ == "__main__":
    cli()
