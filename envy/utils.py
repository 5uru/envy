import contextlib
import subprocess
import os


def find_pythons():
    """
    Searches for Python executables in the system's PATH and returns a dictionary
    mapping each Python version to its executable path.
    """
    # Initialize a list to store paths of Python executables found
    python_versions = []

    # Define a list of common Python executable names to check
    common_paths = [
        "python",
        "python3",
        "python3.6",
        "python3.7",
        "python3.8",
        "python3.9",
        "python3.10",
        "python3.11",
        "python3.12",
    ]

    # Split the system PATH based on the operating system
    paths = (
        os.environ["PATH"].split(";")
        if os.name == "nt"
        else os.environ["PATH"].split(":")
    )

    # Check each directory in the PATH for Python executables
    for path in paths:
        for python_exe in common_paths:
            python_path = os.path.join(path, python_exe)
            # Ensure the path is unique and the executable exists
            if os.path.exists(python_path) and python_path not in python_versions:
                try:
                    # Attempt to get the version of the Python executable
                    version = subprocess.run(
                        [python_path, "--version"], capture_output=True, text=True
                    )
                    # If successfully obtained the version, add it to the list
                    if version.returncode == 0:
                        python_versions.append(
                            (python_path, version.stdout.strip()))
                except Exception:
                    continue

    # Return a dictionary mapping from version to executable path
    return {version: python_path for python_path, version in python_versions}
