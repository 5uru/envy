# Envy

## Overview

`Envy` is a tool to manage Python virtual environments efficiently. It allows users to create, activate, install packages, and manage models for their environments with ease. The application
leverages `typer` for command-line interactions, `InquirerPy` for user prompts, and `rich` for enhanced console output.

## Features

- **Create Environments:** Create new virtual environments with the desired Python version and pre-installed models.
- **Activate Environments:** Activate virtual environments in the user's preferred shell.
- **Install Packages:** Install Python packages in the specified environment.
- **List Environments and Models:** List all available environments and predefined models.
- **Add New Models:** Add new models to the collection.
- **Delete Environments:** Delete existing virtual environments.

## Installation

To use `Envy`, you need to have Python installed. Additionally, you need to install the required dependencies:

```sh
pip install typer InquirerPy rich
```

## Usage

### Create a New Environment

```sh
python envy.py create <env_name>
```

- Prompts to select the Python version.
- Optionally installs a predefined model.

### Activate an Environment

```sh
python envy.py activate <env_name>
```

- Activates the specified environment in the user's shell.

### Install a Package

```sh
python envy.py install <package_name>
```

- Installs the specified package in the current environment.

### List Environments and Models

```sh
python envy.py list
```

- Lists all available environments and predefined models.

### Add a New Model

```sh
python envy.py new
```

- Prompts to add a new model with a list of packages.

### Delete an Environment

```sh
python envy.py delete <env_name>
```

- Deletes the specified environment after confirmation.

## File Structure

```
envy/
envy.py                # Main script
envs/                  # Directory for virtual environments
  model_collections.json  # JSON file with predefined models
utils.py               # Utility functions
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Remaining Tasks

- **Makefile:** Create a `Makefile` to simplify common tasks such as setting up the environment, installing dependencies, and running the script.
