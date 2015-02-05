import truthtable
import sys
import click

@click.command()
@click.argument("expression")
def table(expression):
    truthtable.print_truth_table(expression)

if __name__ == "__main__":
    table()
