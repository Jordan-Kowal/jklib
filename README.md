# jklib

## Description
My personal python library containing my frequently used code snippets I've accumulated over the years

The snippets are split into folders/categories:
- `db`: Database and object storage management
- `django`: Web development around **Django** and **Django Rest Framework** 
- `dtsci`: Data-science, mostly revolving around **Numpy** and **Pandas**
- `std`: Utility functions often unrelated to 3rd party packages, usually built around the standard library
- `web`: Web scrapping and web browsing, mostly around **requests**, **selenium**, and the likes

## Pre-commit hooks
The project uses `pre-commit` hooks to keep a consistent file structure

As such, if you want to make some changes while using the pre-commit hooks:
- Install the necessary libraries: `pip install mypy isort black flake8`
- Use them (through your IDE) to automatically format/check your files
- Install pre-commit: `pip install pre-commit`
- Setup pre-commit by running `pre-commit install`
