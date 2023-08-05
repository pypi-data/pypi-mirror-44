[![Build Status](https://travis-ci.org/pbugnion/jupyterlab-sql.svg?branch=master)](https://travis-ci.org/pbugnion/jupyterlab-sql)
[![Latest version released on PyPi](https://img.shields.io/pypi/v/jupyterlab-sql.svg?style=flat-square&label=version)](https://pypi.python.org/pypi/jupyterlab-sql)

# jupyterlab-sql

JupyterLab extension for interacting with SQL databases.

![](./readme-images/screenshot.png)

## Installation

To install *jupyterlab-sql*, run the following commands:

```
pip install jupyterlab_sql
jupyter serverextension enable jupyterlab_sql --py --sys-prefix
jupyter lab build
```

You will then need to restart any running Jupyter servers.

*jupyterlab-sql* only works with Python 3.5 and above.

## Usage

### Starting a new SQL session

There is a SQL icon in the launcher (*File* > *New Launcher*):

![](./readme-images/launcher.png)

You can also launch a session from the command palette: search for *SQL*.

### Formulating the connection URL

The connection URL needs to be a valid database URL. Follow the
[SQLAlchemy guide](https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)
on database URLs.

### Executing statements

Press `shift` + `enter` or `ctrl` + `enter` while in the main query
area to dispatch the statement.

### Database support

*jupyterlab-sql* has been extensively tested against PostgreSQL and
MySQL databases.

It does not currently work with SQLite databases (in memory or on
disk).

## Issue reporting and contributing

Report issues using the [issue
tracker](https://github.com/pbugnion/jupyterlab-sql/issues).

Contributions are welcome. If you have not developed JupyterLab
extensions before, I recommend following [this
tutorial](https://jupyterlab.readthedocs.io/en/stable/developer/xkcd_extension_tutorial.html).
