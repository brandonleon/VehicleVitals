import tomllib as toml
import re
import os

# Read the version from pyproject.toml
with open("pyproject.toml") as f:
    pyproject_toml = toml.load(f)
    version = pyproject_toml["tool"]["poetry"]["version"]

# Define the Python files to update
python_files = ["VehicleVitals/add_record.py"]  # Add more files as needed

# Update the __version__ variable in the Python files
for file in python_files:
    with open(file, "r") as f:
        content = f.read()
    content = re.sub(r'__version__ = "[\d\.]+"', f'__version__ = "{version}"', content)
    with open(file, "w") as f:
        f.write(content)
