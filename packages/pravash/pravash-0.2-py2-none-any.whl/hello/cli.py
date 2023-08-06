#!/usr/bin/env python3

import os

import click

from hello import helloworld

def hello_world(first_name,last_name):
    """ Log hello world on cli """
    return "Hello "+first_name+" "+last_name


@click.group()
def cli():
    pass


@cli.command("hello")
@click.option("-firstname", help="Enter First Name")
@click.option("-lastname", help="Enter Last Name")
def list(firstname, lastname):
    """ Greet with first name and lastname """
    greeting = hello_world(first_name, last_name)
    click.echo("{}".format(greeting))

if __name__ == "__main__":
    cli()