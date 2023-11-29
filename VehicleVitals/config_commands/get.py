"""
Commands to get config values from the database.
"""
import sqlite3

import typer
from rich.console import Console
from rich.table import Table

from VehicleVitals.database_utilities import get_db_location

app = typer.Typer()


@app.command()
def fuel_types():
    """
    Returns a list of fuel types fetched from the database.
    """
    with sqlite3.connect(get_db_location()) as conn:
        console = Console()
        cursor = conn.cursor()
        query = "SELECT name, octane_level, cetane_level FROM fuel_types"
        cursor.execute(query)
        types = cursor.fetchall()

        table = Table("Fuel Type", "Octane/Cetane")

    for fuel_type in types:
        table.add_row(
            f"{fuel_type[0]}",
            f"{fuel_type[1] if fuel_type[1] is not None else ''}"
            f"{fuel_type[2] if fuel_type[2] is not None else ''}",
        )

    console.print(table)


@app.command()
def service_types():
    """
    Returns a list of service types fetched from the database.
    """
    with sqlite3.connect(get_db_location()) as conn:
        console = Console()
        cursor = conn.cursor()
        query = (
            "SELECT name, description, interval_days, interval_miles FROM service_types"
        )
        cursor.execute(query)
        types = cursor.fetchall()

        table = Table("Name", "Description", "Interval (Days)", "Interval (Miles)")

        for service_type in types:
            table.add_row(
                f"{service_type[0]}",
                f"{service_type[1]}",
                f"{service_type[2]}",
                f"{service_type[3]}",
            )

        console.print(table)
