"""
This is the main entry point for the application. It creates the Typer app and
defines the commands that can be run from the command line.
"""
import typer

from . import add_record
from . import config
from . import display
from . import edit
from .database_utilities import initialize_database

initialize_database()  # Initialize the database (Create tables if they don't exist)

app = typer.Typer()
app.add_typer(display.app, name="display", help="Display records from the database.")
app.add_typer(add_record.app, name="add", help="Add records to the database.")
app.add_typer(edit.app, name="edit", help="Edit records in the database.")
app.add_typer(config.app, name="config", help="Configure the application.")


if __name__ == "__main__":
    app()
