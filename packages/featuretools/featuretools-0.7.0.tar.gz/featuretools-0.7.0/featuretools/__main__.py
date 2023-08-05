import click
import pandas as pd

import featuretools
from featuretools.primitives.utils import get_featuretools_root


@click.group()
def cli():
    pass


@click.command()
def info():
    print("Featuretools version: %s" % featuretools.__version__)
    print("Featuretools installation directory: %s" % get_featuretools_root())


@click.command()
def list_primitives():
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', -1, 'display.width', 1000):
        print(featuretools.list_primitives())


cli.add_command(list_primitives)
cli.add_command(info)


if __name__ == "__main__":
    cli()
