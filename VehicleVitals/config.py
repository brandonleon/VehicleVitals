"""
This module contains the commands to configure the application.
"""
import sqlite3
from typing import Annotated

import typer

from .database_utilities import get_db_location
from .config_commands import get

# Create the Typer app
app = typer.Typer()

app.add_typer(get.app, name="get", help="Display fuel types.")
