# jklib

## Description
Package with useful snippets for Django and general Python development.

The snippets are split into folders/categories:
- `dj`: Web development around **Django** and **Django Rest Framework** 
- `meili`: Utilities to interact with **MeiliSearch** (with a subfolder for `dj` **Django**)
- `std`: Generic utilities around the standard library that can be used in any project 


## Pre-commit hooks
The project uses `pre-commit` hooks to keep a consistent file structure

As such, if you want to make some changes while using the pre-commit hooks:
- Install the necessary libraries: `pip install -r requirements-dev.txt`
- Use them (through your IDE) to automatically format/check your files
- Setup pre-commit by running `pre-commit install`
