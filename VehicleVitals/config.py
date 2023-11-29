"""
This module contains the commands to configure the application.
"""
import sqlite3

import typer

from .database_utilities import get_db_location

# Create the Typer app
app = typer.Typer()


@app.command()
def fuel_types():
    """
    Returns a list of fuel types fetched from the database.
    """

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = "SELECT name, octane_level, cetane_level FROM fuel_types"
        cursor.execute(query)
        fuel_types = cursor.fetchall()

    for fuel_type in fuel_types:
        typer.echo(f"{fuel_type[0]}: {fuel_type[1]} octane, {fuel_type[2]} cetane")
