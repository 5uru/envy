import json
import os
import shutil
import subprocess
import sys

import InquirerPy
import typer
import utils
from rich import print

app = typer.Typer()
ENV_DIR = os.path.join(os.path.dirname(__file__), "envs")

with open("envy/model_collections.json", "r") as file:
    model_collections = json.load(file)


@app.command("create")
def create_env(env_name: str):
    """

    :param env_name: str:
    :param env_name: str: 

    """
    env_path = os.path.join(ENV_DIR, env_name)
    if os.path.exists(env_path):
        print(f"Environment {env_name} already exists.")
        return

    python_versions_dict = utils.find_pythons()
    question = {
        "type": "list",
        "message": "Choose a Python 🐍 version:",
        "choices": list(python_versions_dict.keys()),
    }
    python_version = InquirerPy.prompt([question])[0]
    python_executable = python_versions_dict[python_version]

    model_name = None
    installed_models = InquirerPy.prompt(
        {
            "type": "list",
            "message": "Do you want to install models?",
            "choices": ["Yes", "No"],
        }
    )[0]

    if installed_models == "Yes":
        model_question = {
            "type": "list",
            "message": "Choose a model to pre-install:",
            "choices": list(model_collections.keys()),
        }
        model_name = InquirerPy.prompt([model_question])[0]
    elif installed_models == "No":
        model_name = None
    else:
        print("Invalid input")
        sys.exit(1)

    subprocess.run([python_executable, "-m", "venv", env_path])
    print(f"[green]Environment {env_name} created.[/green]")
    print(f"[green]Installing essential packages in {env_name}.[/green]")
    run_in_env(env_name, ["pip install --upgrade pip", "pip install uv"])
    activate_env(env_name)

    if model_name:
        for package in model_collections[model_name]:
            print(f"Installing {package} in {env_name}")
            run_in_env(env_name, [f"pip install {package}"])


@app.command("activate")
def activate_env(env_name: str):
    """

    :param env_name: str:
    :param env_name: str: 

    """
    # Construct the path to the virtual environment directory
    env_path = os.path.join(ENV_DIR, env_name)

    # Check if the specified environment exists
    if not os.path.exists(env_path):
        print(f"Environment {env_name} does not exist.")
        return

    # Determine the activation script based on the operating system
    if os.name == "nt":  # Check if the OS is Windows
        activate_script = os.path.join(env_path, "Scripts", "activate.bat")
        command = f'cmd /k "{activate_script}"'
    else:  # Assume OS is either macOS or Linux
        activate_script = os.path.join(env_path, "bin", "activate")
        shell = os.environ.get(
            "SHELL", "/bin/bash"
        )  # Get the default shell or use bash
        if "zsh" in shell:  # Check if the default shell is zsh
            command = f"source {activate_script} && exec zsh"
        else:  # Default to bash if not zsh
            command = f"source {activate_script} && exec bash"

    # Execute the command to activate the environment in a new shell
    if os.name == "nt":
        subprocess.run(
            command, shell=True
        )  # Use shell=True for Windows to handle batch files
    else:
        # Execute command in the specified shell
        subprocess.run([shell, "-c", command])


def run_in_env(env_name: str, commands: list):
    """

    :param env_name: str:
    :param commands: list:
    :param env_name: str: 
    :param commands: list: 

    """
    # Determine the path of the specified virtual environment
    env_path = os.path.join(ENV_DIR, env_name)

    # Check if the environment exists, if not, return
    if not os.path.exists(env_path):
        print(f"Environment {env_name} does not exist.")
        return

    # Choose the correct activation script based on the operating system
    activate_script = (
        os.path.join(env_path, "Scripts", "activate.bat")
        if os.name == "nt"
        else os.path.join(env_path, "bin", "activate")
    )

    # Construct the command string to activate the environment and execute additional commands
    if os.name == "nt":
        # Windows requires a different command format and uses shell=True to handle batch scripts
        cmd = f'{activate_script} && {" && ".join(commands)}'
        subprocess.run(cmd, shell=True)
    else:
        # Determine the shell environment, defaulting to bash if not specified
        shell = os.environ.get("SHELL", "/bin/bash")
        # Construct the command for zsh
        cmd = f'source {activate_script} && {" && ".join(commands)}'
        if "zsh" in shell:
            subprocess.run(["zsh", "-c", cmd])
        else:
            subprocess.run(["bash", "-c", cmd])


@app.command("install")
def install_package(package: str):
    """

    :param package: str:
    :param package: str: 

    """
    # This function installs a Python package using uv and pip within the current environment
    subprocess.run(["uv", "pip", "install", package])


@app.command("list")
def list_env_and_models():
    """ """
    # Check if the ENV_DIR exists, if not, notify that no environments are found
    if not os.path.exists(ENV_DIR):
        print("No environments found.")
        return

    if envs := [
        name
        for name in os.listdir(ENV_DIR)
        if os.path.isdir(os.path.join(ENV_DIR, name))
    ]:
        print("Environments:")
        for env in envs:
            print(f" - {env}")
    else:
        print("No environments found.")

    # Display the list of models stored in model_collections
    print("Models:")
    for model in model_collections.keys():
        print(f" - {model}")


@app.command("new")
def new_models():
    """ """
    # Prompt the user for the model name
    model_name = typer.prompt("What's the model name?")
    # Prompt the user for a comma-separated list of packages
    packages = typer.prompt("What's the packages list?")
    # Save the list of packages to the model_collections dictionary
    model_collections[model_name] = packages.split(",")
    # Write the updated model collections to a JSON file
    with open("envy/model_collections.json", "w") as file:
        json.dump(model_collections, file)
    print(f"Model {model_name} created.")


@app.command("delete")
def delete_env(env_name: str):
    """

    :param env_name: str:
    :param env_name: str: 

    """
    # Construct the path to the virtual environment directory
    env_path = os.path.join(ENV_DIR, env_name)
    # Check if the environment exists
    if not os.path.exists(env_path):
        print(f"Environment {env_name} does not exist.")
        return
    # Prompt for confirmation before deleting the environment
    if typer.confirm(f"Are you sure you want to delete {env_name}?", abort=True):
        # Remove the directory and all its contents
        shutil.rmtree(env_path)
        print(f"Environment {env_name} deleted.")


if __name__ == "__main__":
    app()
