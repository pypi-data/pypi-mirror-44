# Startin'Blox Manager

## Get started

Install the `sib` command line:
```
$ pip3 install --user -U sib-manager
```

Create a new project with your favorite modules (with optional virtualenv):
```
$ sib startproject myproject -m djangoldp_project --venv
```

And launch it locally !
```
$ cd myproject
$ sib runserver
```

## Usage

If you want the last unreleased version:
```
$ pip3 install --user -U git+https://git.happy-dev.fr/startinblox/devops/sib
```

Or work within docker:
```
$ docker run --rm -p 127.0.0.1:8000:8000 -it python:3.6 bash
# pip install sib-manager
# sib startproject myproject -m djangoldp_project
# cd myproject
# sib runserver
```
