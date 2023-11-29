"""
This module contains the commands to configure the application.
"""
import typer

from .config_commands import create
from .config_commands import delete
from .config_commands import read
from .config_commands import update

# Create the Typer app
app = typer.Typer()

app.add_typer(
    read.app, name="read", help="Read configuration values from the database."
)
app.add_typer(
    create.app, name="create", help="Create configuration values in the database."
)
app.add_typer(delete.app, name="delete", help="Delete configuration values.")
app.add_typer(update.app, name="update", help="Update configuration values.")
