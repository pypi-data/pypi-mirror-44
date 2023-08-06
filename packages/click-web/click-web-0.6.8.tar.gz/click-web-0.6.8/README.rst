click-web
=========

Serve click scripts over the web with minimal effort.

*Caution*: No security (login etc.), do not serve scripts publicly.

Usage
-----

See this demo `screen capture`_.

.. _screen capture: https://github.com/fredrik-corneliusson/click-web/raw/master/doc/click-web-demo.gif

Take an existing click script, like this one:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``example_command.py``

::

   import click
   import time

   @click.group()
   def cli():
       'A stupid script to test click-web'
       pass

   @cli.command()
   @click.option("--delay", type=float, default=0.01, help='delay for every line print')
   @click.argument("lines", default=10, type=int)
   def print_rows(lines, delay):
       'Print lines with a delay'
       click.echo(f"writing: {lines} with {delay}")
       for i in range(lines):
           click.echo(f"Hello row: {i}")
           time.sleep(delay)

   if __name__ == '__main__':
       cli()

Create a minimal script to run with flask
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``app.py``

::

   from click_web import create_click_web_app
   import example_command

   app = create_click_web_app(example_command, example_command.cli)

Running example app:
~~~~~~~~~~~~~~~~~~~~

In Bash:

::

   export FLASK_ENV=development
   export FLASK_APP=app.py
   flask run

Unsupported click features
==========================

It has only been tested with basic click features, and most advanced
features will probably not work.

- Variadic arguments of file and path type
- Promts (probably never will)
- Custom ParamTypes (depending on implementation)

TODO
====

- Abort started/running processes.
- Browser history


Included 3:rd party libraries
=============================
`SplitJs`_ - Copyright (c) 2018 Nathan Cahill (MIT license)

.. _SplitJs: https://github.com/nathancahill/split/blob/master/packages/splitjs/LICENSE.txt
