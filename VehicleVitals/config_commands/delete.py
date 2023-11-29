"""
Commands to delete config values from the database.
"""
import sqlite3
from typing import Annotated
from uuid import uuid4

import rich
import typer
from rich.console import Console
from rich.table import Table

from VehicleVitals.database_utilities import get_db_location

app = typer.Typer()


@app.command()
def fuel_type(
    fuel: Annotated[str, typer.Option(help="Name or ID of the fuel type to delete")],
    confirm: Annotated[bool, typer.Option(help="Confirm the deletion")] = True,
):
    """
    Delete a fuel type from the database.
    """
    if confirm:
        rich.print(
            "[bold red]WARNING![/bold red] Deleting a fuel type will also delete any associated service records."
        )
        typer.confirm("Are you sure you want to delete this fuel type?", abort=True)

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = "DELETE FROM fuel_types WHERE id = ? or name = ?"
        params = [fuel, fuel]
        cursor.execute(query, params)
        conn.commit()

    typer.echo(f"Deleted fuel type {fuel} from the database.")


@app.command()
def service_type(
    service: Annotated[
        str, typer.Option(help="Name or ID of the service type to delete")
    ],
    confirm: Annotated[bool, typer.Option(help="Confirm the deletion")] = True,
):
    """
    Delete a service type from the database.
    """
    if confirm:
        rich.print(
            "[bold red]WARNING![/bold red] Deleting a service type will also delete any associated service records."
        )
        typer.confirm("Are you sure you want to delete this service type?", abort=True)

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = "DELETE FROM service_types WHERE id = ? or name = ?"
        params = [service, service]
        cursor.execute(query, params)
        conn.commit()

    typer.echo(f"Deleted service type {service} from the database.")


@app.command()
def part(
    part: Annotated[str, typer.Option(help="Name or ID of the part to delete")],
    confirm: Annotated[bool, typer.Option(help="Confirm the deletion")] = True,
):
    """
    Delete a part from the database.
    """
    if confirm:
        rich.print(
            "[bold red]WARNING![/bold red] Deleting a part will also delete any associated service records."
        )
        typer.confirm("Are you sure you want to delete this part?", abort=True)

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = "DELETE FROM parts WHERE id = ? or name = ?"
        params = [part, part]
        cursor.execute(query, params)
        conn.commit()

    typer.echo(f"Deleted part {part} from the database.")
