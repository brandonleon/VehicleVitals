"""
Commands to create config values in the database.
"""
import sqlite3
from typing import Annotated
from uuid import uuid4

import typer
from rich.console import Console
from rich.table import Table

from VehicleVitals.database_utilities import get_db_location

app = typer.Typer()


@app.command()
def fuel_type(
    name: Annotated[str, typer.Option(help="Name of the fuel type")],
    octane: Annotated[int, typer.Option(help="Octane level of the fuel type")] = None,
    cetane: Annotated[int, typer.Option(help="Cetane level of the fuel type")] = None,
):
    """
    Add a new fuel type to the database.
    """

    # Validate one of either octane_level or cetane_level provided
    if octane is None and cetane is None:
        raise typer.BadParameter(
            "Either octane_level or cetane_level must be provided."
        )

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = f"INSERT INTO fuel_types (id, name, octane_level, cetane_level) VALUES ('{str(uuid4())}', ?, ?, ?)"
        params = [name, octane, cetane]
        cursor.execute(query, params)
        conn.commit()

    typer.echo(f"Added fuel type {name} to the database.")


@app.command()
def service_type(
    name: Annotated[str, typer.Option(help="Name of the service type")],
    interval_days: Annotated[
        int, typer.Option(help="Interval in days of the service type")
    ],
    interval_miles: Annotated[
        int, typer.Option(help="Interval in miles of the service type")
    ],
    description: Annotated[
        str, typer.Option(help="Description of the service type")
    ] = None,
):
    """
    Add a new service type to the database.
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = (
            f"INSERT INTO service_types (id, name, description, interval_days, interval_miles)"
            f"VALUES ('{str(uuid4())}', ?, ?, ?, ?)"
        )
        params = [name, description, interval_days, interval_miles]
        cursor.execute(query, params)
        conn.commit()

    typer.echo(f"Added service type {name} to the database.")


@app.command()
def part(
    name: Annotated[str, typer.Option(help="Name of the part")],
    cost: Annotated[float, typer.Option(help="Cost of the part")],
    description: Annotated[str, typer.Option(help="Description of the part")] = None,
):
    """
    Add a new part to the database.
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = (
            f"INSERT INTO parts (id, name, description, cost)"
            f"VALUES ('{str(uuid4())}', ?, ?, ?)"
        )
        params = [name, description, cost]
        cursor.execute(query, params)
        conn.commit()

    typer.echo(f"Added part {name} to the database.")
