# jklib

## Description
Package with useful snippets for Django and general Python development.

The snippets are split into folders/categories:
- `dj`: Web development around **Django** and **Django Rest Framework** 
- `meili`: Utilities to interact with **MeiliSearch** (with a subfolder for `dj` **Django**)
- `std`: Generic utilities around the standard library that can be used in any project 


### Using git hooks

Git hooks are set in the [.githooks](.githooks) folder
_(as `.git/hooks` is not tracked in `.git`)_

Run the following command to tell `git` to look for hooks in this folder:

```shell
git config core.hooksPath .githooks
```
