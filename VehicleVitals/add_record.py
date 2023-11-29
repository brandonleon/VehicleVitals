"""
This module contains the functions to write from the database.
"""
import sqlite3
from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import uuid4

import typer

from .database_utilities import get_db_location

# Create the Typer app
app = typer.Typer()


def fuel_types():
    """
    Returns a list of fuel types fetched from the database as an Enum class.
    Returns: Enum

    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = "SELECT name FROM fuel_types"
        cursor.execute(query)
        enum_values = [row[0] for row in cursor.fetchall()]

    # Creating an Enum class with both name and value
    return Enum("FuelTypes", list(zip(enum_values, enum_values)))


def service_types():
    """
    Returns a list of service types fetched from the database as an Enum class.
    Returns: Enum
    """

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = "SELECT name FROM service_types"
        cursor.execute(query)
        enum_values = [str(row[0]) for row in cursor.fetchall()]

    return Enum("ServiceTypes", list(zip(enum_values, enum_values)))


@app.command()
def fuel_up(
    vehicle_id: Annotated[str, typer.Option(help="Vehicle ID")],
    odometer: Annotated[float, typer.Option(help="Odometer reading")],
    gallons: Annotated[float, typer.Option(help="Gallons filled")],
    cost_per_gallon: Annotated[float, typer.Option(help="Cost per gallon")],
    fuel_type: Annotated[fuel_types(), typer.Option(help="Type of fuel")],
    filled_up: Annotated[bool, typer.Option(help="Filled up the tank")] = True,
    missed_last_fill_up: Annotated[bool, typer.Option(help="Missed fill up")] = False,
    entry_date: Annotated[
        str, typer.Option(help="Date of service")
    ] = datetime.now().strftime("%Y-%m-%d"),
    entry_time: Annotated[
        str, typer.Option(help="Time of service")
    ] = datetime.now().strftime("%I:%M %p"),
    location: Annotated[str, typer.Option(help="Location of service")] = "Home",
):
    """
    Add a fuel up entry to the database.

    Example:
        vv add fuel-up --vehicle-id 23b3db142984 --odometer 1000 --gallons 10.0 --cost-per-gallon 2.50
    """

    # convert Fuel type to the format used in the database:
    # "Regular" -> "Regular [Octane: 87]"
    # "Diesel" -> "Diesel [Centane: 40]"
    is_fill_up = "Unknown"  # Set a default value
    match (filled_up, missed_last_fill_up):
        case (True, False):
            is_fill_up = "Full"
        case (False, True):
            is_fill_up = "Reset"
        case (True, True):
            is_fill_up = "Reset"
        case (False, False):
            is_fill_up = "Partial"

    # get the fuel type details from the database
    fuel_type = fuel_type.value
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM fuel_types WHERE name = ?"
        cursor.execute(query, (fuel_type,))
        fuel_type_details = cursor.fetchone()

    octane_level = fuel_type_details[2] if fuel_type_details[2] is not None else None
    cetane_level = fuel_type_details[3] if fuel_type_details[3] is not None else None

    if octane_level is not None:
        octane_or_cetane = f"Octane: {octane_level}"
    elif cetane_level is not None:
        octane_or_cetane = f"Cetane: {cetane_level}"
    else:
        octane_or_cetane = "Unknown"

    with sqlite3.connect(get_db_location()) as conn:
        if is_fill_up == "Full":
            cursor = conn.cursor()
            # Fetch the last fuel up entry for the vehicle to determine the MPG
            last_fuel_up_query = """
                        SELECT OdometerReading, GallonsFilled
                        FROM logs
                        WHERE VehicleID = ? and EntryType = 'Gas'
                        ORDER BY EntryDate DESC, EntryTime DESC
                        LIMIT 1
                        """
            cursor.execute(last_fuel_up_query, (vehicle_id,))
            if last_fuel_up := cursor.fetchone():
                last_odometer, last_gallons = last_fuel_up
                mpg = (odometer - last_odometer) / gallons if last_gallons > 0 else None
            else:
                mpg = None

        # Insert the fuel up entry
        query = """
            INSERT INTO logs (
                ID, VehicleID, EntryType, MPG, OdometerReading, IsFillUp,
                EntryDate, EntryTime, Location, CostPerGallon, 
                GallonsFilled, TotalCost, OctaneRating
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                str(uuid4()),
                vehicle_id,
                "Gas",
                mpg,
                odometer,
                is_fill_up,
                entry_date,
                entry_time,
                location,
                f"${cost_per_gallon:.3f}",
                gallons,
                f"${cost_per_gallon * gallons:.2f}",
                f"{fuel_type} [{octane_or_cetane}]",  # Fuel type [Octane / Cetane
            ),
        ),

        query = "UPDATE vehicles SET mileage = ? WHERE id = ?"
        cursor.execute(query, (odometer, vehicle_id))
        conn.commit()
        typer.echo(f"Added log entry for {vehicle_id}.")


@app.command()
def service(
    vehicle_id: Annotated[str, typer.Option(help="Vehicle ID")],
    odometer: Annotated[float, typer.Option(help="Odometer reading")],
    service_type: Annotated[service_types(), typer.Option(help="Type of service")],
    cost: Annotated[float, typer.Option(help="Cost of service ($0.00)")],
    entry_date: Annotated[
        str, typer.Option(help="Date of service")
    ] = datetime.now().strftime("%Y-%m-%d"),
    entry_time: Annotated[
        str, typer.Option(help="Time of service")
    ] = datetime.now().strftime("%I:%M %p"),
    location: Annotated[str, typer.Option(help="Location of service")] = None,
):
    """
    Add a service entry to the database.

    Example:
        vv add service --vehicle-id 23b3db142984 --odometer 1000 --service-type "Oil Change" --cost 50.00
    """
    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO logs (
                ID, VehicleID, EntryType, OdometerReading, 
                EntryDate, EntryTime, Location, TotalCost, Services
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                str(uuid4()),
                vehicle_id,
                "Service",
                odometer,
                entry_date,
                entry_time,
                location,
                f"${cost:.2f}",
                service_type.value,
            ),
        ),
        query = "UPDATE vehicles SET mileage = ? WHERE id = ?"
        cursor.execute(query, (odometer, vehicle_id))
        conn.commit()
        typer.echo(f"Added log entry for {vehicle_id}.")


@app.command()
def vehicle(
    year: Annotated[int, typer.Option(help="Year of vehicle")],
    make: Annotated[str, typer.Option(help="Make of vehicle")],
    model: Annotated[str, typer.Option(help="Model of vehicle")],
    color: Annotated[str, typer.Option(help="Color of vehicle")],
    mileage: Annotated[float, typer.Option(help="Odometer reading")],
    name: Annotated[str, typer.Option(help="Short name of vehicle")] = None,
    trim: Annotated[str, typer.Option(help="Trim level vehicle")] = None,
    engine: Annotated[str, typer.Option(help="Engine of vehicle")] = None,
):
    """
    Inserts a new vehicle record into the database.

    Example:
        vv add vehicle --year 2021 --make Honda --model Civic --mileage 1000 --color Red
    """

    with sqlite3.connect(get_db_location()) as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO vehicles (
                id, name, Year, Make, Model, mileage, trim, Engine, Color
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        try:
            cursor.execute(
                query,
                (
                    str(uuid4()),
                    name,
                    year,
                    make,
                    model,
                    mileage,
                    trim,
                    engine,
                    color,
                ),
            ),
            conn.commit()
        except sqlite3.IntegrityError as e:
            raise typer.BadParameter(
                f"Vehicle {year} {make} {model} already exists."
            ) from e
        typer.echo(f"Added vehicle {year} {make} {model}, to the database.")


if __name__ == "__main__":
    app()
