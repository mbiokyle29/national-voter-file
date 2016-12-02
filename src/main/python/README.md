# Python Prepare Scripts

This directory contains the scripts required to convert the raw unformatted state level data
into a consistent format for loading into the database.

Each state has its own `<State>Prepare.py>` script for processing.

The code is python 3, it is recommended that you use virutalenv for development/running
of the scripts to handle dependencies (and get a valid python3 setup for python2 users).

### Getting Started
Assuming you have `virtualenv` installed on your local machine (`pip install virtualenv` if not):
```
virtualenv .venv3
source .venv3/bin/activate
pip install -r requirements.txt
```

At this point you should be ready to run/develop prepare scripts.

When you are done, you can get out of the virtualenv using the `deactive` command or simply kill your terminal sessions

### Tests

All of the tests live in the `tests/` subdirectory and are run via nose2. The file `nose2.cfg` contains the default test running configuration.

