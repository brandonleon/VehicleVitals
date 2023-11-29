"""
Commands to get config values from the database.
"""
import sqlite3
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from VehicleVitals.database_utilities import get_db_location

app = typer.Typer()


@app.command()
def fuel_types(
    name: Annotated[str, typer.Option(help="Name of fuel type")] = None,
    octane_level: Annotated[int, typer.Option(help="Octane level")] = None,
    cetane_level: Annotated[int, typer.Option(help="Cetane level")] = None,
):
    """
    Returns a list of fuel types fetched from the database.
    """

    # If no parameters are passed in, return all fuel types
    with sqlite3.connect(get_db_location()) as conn:
        console = Console()
        cursor = conn.cursor()
        query = "SELECT name, octane_level, cetane_level FROM fuel_types"
        cursor.execute(query)
        fuel_types = cursor.fetchall()

        table = Table("Fuel Type", "Octane/Cetane")

    for fuel_type in fuel_types:
        table.add_row(
            f"{fuel_type[0]}",
            f"{fuel_type[1] if fuel_type[1] is not None else ''}"
            f"{fuel_type[2] if fuel_type[2] is not None else ''}",
        )

    console.print(table)
