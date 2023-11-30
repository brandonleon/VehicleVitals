"""
Commands to update config values in the database.
"""
import sqlite3
from typing import Annotated
from uuid import uuid4

import rich
import typer

from VehicleVitals.database_utilities import get_db_location

app = typer.Typer()


@app.command()
def fuel_type(
    fuel: Annotated[str, typer.Option(help="Name or ID of the fuel type to update")],
    name: Annotated[str, typer.Option(help="Name of the fuel type")] = None,
    octane: Annotated[int, typer.Option(help="Octane level of the fuel type")] = None,
    cetane: Annotated[int, typer.Option(help="Cetane level of the fuel type")] = None,
    confirm: Annotated[bool, typer.Option(help="Confirm the update")] = True,
):
    """
    Update a fuel type in the database.
    """
    if confirm:
        rich.print(
            "[bold red]WARNING![/bold red] Updating a fuel type will also update any associated service records."
        )
        typer.confirm("Are you sure you want to update this fuel type?", abort=True)

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()

        set_clause = [
            f"{field} = ?"
            for field, value in [
                ("name", name),
                ("octane_level", octane),
                ("cetane_level", cetane),
            ]
            if value is not None
        ]
        # Join the SET clause into a comma-separated string
        set_clause = ", ".join(set_clause)

        # Prepare the SQL query with parameterized query
        query = f"UPDATE fuel_types SET {set_clause} WHERE id = ? OR name = ?"

        params = [
            field
            for field in [
                name,
                octane,
                cetane,
            ]
            if field is not None
        ]

        params += [fuel, fuel]

        try:
            cursor.execute(query, params)
            conn.commit()
        except sqlite3.IntegrityError as e:
            raise typer.BadParameter(f"Fuel type {fuel} does not exist.") from e

    typer.echo(f"Updated fuel type {fuel} in the database.")


@app.command()
def service_type(
    service: Annotated[str, typer.Option(help="Name of the service type")],
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
    Update a service type in the database.
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()

        set_clause = [
            f"{field} = ?"
            for field, value in [
                ("description", description),
                ("interval_days", interval_days),
                ("interval_miles", interval_miles),
            ]
            if value is not None
        ]
        # Join the SET clause into a comma-separated string
        set_clause = ", ".join(set_clause)

        # Prepare the SQL query with parameterized query
        query = f"UPDATE service_types SET {set_clause} WHERE id = OR name = ?"

        params = [
            field
            for field in [
                description,
                interval_days,
                interval_miles,
            ]
            if field is not None
        ]

        params += [service, service]

        try:
            cursor.execute(query, params)
            conn.commit()
        except sqlite3.IntegrityError as e:
            raise typer.BadParameter(f"Service type {service} does not exist.") from e

    typer.echo(f"Updated service type {service} in the database.")


@app.command()
def part(
    part: Annotated[str, typer.Option(help="Name of the part")],
    cost: Annotated[float, typer.Option(help="Cost of the part")],
    description: Annotated[str, typer.Option(help="Description of the part")] = None,
):
    """
    Add a new part to the database.
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()

        set_clause = [
            f"{field} = ?"
            for field, value in [
                ("description", description),
                ("cost", cost),
            ]
            if value is not None
        ]
        # Join the SET clause into a comma-separated string
        set_clause = ", ".join(set_clause)

        # Prepare the SQL query with parameterized query
        query = f"UPDATE parts SET {set_clause} WHERE id = ? OR name = ?"

        params = [
            field
            for field in [
                description,
                cost,
            ]
            if field is not None
        ]

        params += [part, part]

        try:
            cursor.execute(query, params)
            conn.commit()
        except sqlite3.IntegrityError as e:
            raise typer.BadParameter(f"Service type {part} does not exist.") from e
