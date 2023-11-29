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
    show_id: Annotated[bool, typer.Option(help="Show the ID of the fuel type")] = False,
):
    """
    Returns a list of fuel types fetched from the database.
    """
    with sqlite3.connect(get_db_location()) as conn:
        conn.row_factory = sqlite3.Row  # Set Row factory
        console = Console()
        cursor = conn.cursor()
        if show_id:
            query = "SELECT id, name, octane_level, cetane_level FROM fuel_types"
        else:
            query = "SELECT name, octane_level, cetane_level FROM fuel_types"
        cursor.execute(query)
        types = cursor.fetchall()

        if show_id:
            table = Table("ID", "Name", "Octane/Cetane Level")
        else:
            table = Table("Name", "Octane/Cetane Level")

        for fuel_type in types:
            if show_id:
                table.add_row(
                    f"{fuel_type['id']}",
                    f"{fuel_type['name']}",
                    f"{fuel_type['octane_level'] if fuel_type['octane_level'] is not None else ''}"
                    f"{fuel_type['cetane_level'] if fuel_type['cetane_level'] is not None else ''}",
                )
            else:
                table.add_row(
                    f"{fuel_type['name']}",
                    f"{fuel_type['octane_level'] if fuel_type['octane_level'] is not None else ''}"
                    f"{fuel_type['cetane_level'] if fuel_type['cetane_level'] is not None else ''}",
                )

        console.print(table)


@app.command()
def service_types(
    show_id: Annotated[
        bool, typer.Option(help="Show the ID of the service type")
    ] = False,
):
    """
    Returns a list of service types fetched from the database.
    """
    with sqlite3.connect(get_db_location()) as conn:
        conn.row_factory = sqlite3.Row  # Set Row factory
        console = Console()
        cursor = conn.cursor()
        if show_id:
            query = "SELECT id, name, description, interval_days, interval_miles FROM service_types"
        else:
            query = "SELECT name, description, interval_days, interval_miles FROM service_types"
        cursor.execute(query)
        types = cursor.fetchall()

        if show_id:
            table = Table(
                "ID", "Name", "Description", "Interval (Days)", "Interval (Miles)"
            )
        else:
            table = Table("Name", "Description", "Interval (Days)", "Interval (Miles)")

        for service_type in types:
            if show_id:
                table.add_row(
                    f"{service_type['id']}",
                    f"{service_type['name']}",
                    f"{service_type['description']}",
                    f"{service_type['interval_days']}",
                    f"{service_type['interval_miles']}",
                )
            else:
                table.add_row(
                    f"{service_type['name']}",
                    f"{service_type['description']}",
                    f"{service_type['interval_days']}",
                    f"{service_type['interval_miles']}",
                )

        console.print(table)
