#!/usr/bin/env python3

import os

from . import __version__
import click

# from hello import helloworld

def hello_world(first_name,last_name):
    """ Log hello world on cli """
    return "Hello "+first_name+" "+last_name


@click.version_option(__version__, message='%(version)s')
@click.group()
def cli():
    ''' Pravash python package example '''
    pass


@cli.command("hello")
@click.option("--firstname", help="Enter First Name")
@click.option("--lastname", help="Enter Last Name")
def list(firstname, lastname):
    """ Greet with first name and lastname """
    if bool(firstname) and bool(lastname):
        greeting = hello_world(firstname, lastname)
        click.echo("{}".format(greeting))
    else:
        click.echo("Please provide firstname and lastname")
        return

if __name__ == "__main__":
    cli()