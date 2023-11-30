"""
This module contains the functions to read from the database.
"""
import sqlite3
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from .database_utilities import get_db_location

# Create the Typer app
app = typer.Typer()


@app.command()
def logs(
    page: Annotated[int, typer.Option(help="Page number to retrieve.")] = 1,
    page_size: Annotated[int, typer.Option(help="Number of records per page.")] = 10,
    vehicle_id: Annotated[
        str, typer.Option(help="Filter by Vehicle ID (All if blank).")
    ] = "",
):
    """
    View logs with optional filtering and pagination.

    Examples:

        vv display logs


        vv display logs --vehicle-id 6a9ab94e-0cea-481d-a9d4-23b3db142984
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()

        # Calculate the OFFSET based on the page number and page size
        offset = (page - 1) * page_size

        # Prepare the SQL query with parameterized query
        query = """
            SELECT v.Year, v.Make, v.Model, v.trim, l.EntryDate, l.EntryTime,
            l.OdometerReading, l.MPG, l.EntryType, st.name as Service
            FROM logs l
            LEFT JOIN vehicles v ON l.VehicleID = v.id
            LEFT JOIN service_types st on l.service_type_id = st.id
        """

        params = ()
        if vehicle_id:
            query += " WHERE l.VehicleID = ?"
            params = (vehicle_id,)

        query += " ORDER BY l.EntryDate DESC, l.EntryTime DESC LIMIT ? OFFSET ?"
        params += (page_size, offset)

        cursor.execute(query, params)
        if log_entries := cursor.fetchall():
            print(f"Page {page}:")
            console = Console()
            table = Table(
                "Vehicle",
                "EntryDate",
                "EntryTime",
                "Odometer",
                "MPG",
                "EntryType",
                "Service",
            )
            for log in log_entries:
                table.add_row(
                    f"{log[0]} {log[1]} {log[2]} {log[3]}",
                    log[4],
                    log[5],
                    f"{float(log[6]):,.1f}"
                    if log[6] is not None
                    else "[cyan]---[/cyan]",
                    f"{float(log[7]):,.1f}"
                    if log[7] is not None
                    else "[cyan]---[/cyan]",
                    log[8],
                    log[9],
                )
            console.print(table)
        else:
            typer.echo("No logs found on this page.")


@app.command()
def vehicles(
    page: Annotated[int, typer.Option(help="Page number to retrieve.")] = 1,
    page_size: Annotated[int, typer.Option(help="Number of records per page.")] = 10,
    vehicle: Annotated[
        str, typer.Option(help="Filter by Vehicle ID or Name (All if blank).")
    ] = "",
    show_id: Annotated[bool, typer.Option(help="Show the vehicle ID")] = False,
):
    """
    View vehicles with optional filtering and pagination.

    Examples:

        vv display vehicles

        vv display vehicles --vehicle 6a9ab94e-0cea-481d-a9d4-23b3db142984

        vv display vehicles --vehicle "My Vehicle"
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        conn.row_factory = sqlite3.Row

        # Calculate the OFFSET based on the page number and page size
        if show_id:
            query = "SELECT id, name, Year, Make, Model, trim, mileage FROM vehicles"
        else:
            query = "SELECT name, Year, Make, Model, trim, mileage FROM vehicles"
        params = ()
        if vehicle:
            query += " WHERE name = ? or id = ?"
            params = (vehicle, vehicle)

        query += " ORDER BY Year DESC, Make, Model LIMIT ? OFFSET ?"
        params += (page_size, (page - 1) * page_size)

        cursor.execute(query, params)
        if vehicle_entries := cursor.fetchall():
            typer.echo(f"Page {page} of {len(vehicle_entries) // page_size + 1}:")
            console = Console()
            if show_id:
                table = Table("ID", "Name", "Vehicle Description", "Mileage")
            else:
                table = Table("Name", "Vehicle Description", "Mileage")
            for vehicle in vehicle_entries:
                v = [str(x) for x in vehicle]
                if show_id:
                    table.add_row(
                        v[0],
                        v[1],
                        f"{v[2]} {v[3]} {v[4]} {v[5]}",
                        f"{float(str(v[6]).replace(',', '')):,.1f}",
                    )
                else:
                    table.add_row(
                        v[0],
                        f"{v[1]} {v[2]} {v[3]} {v[4]}",
                        f"{float(str(v[5]).replace(',', '')):,.1f}",
                    )

            console.print(table)
        else:
            typer.echo("No vehicles found on this page.")


if __name__ == "__main__":
    app()
