=========
lunchtime
=========


.. image:: https://img.shields.io/pypi/v/lunchtime.svg
        :target: https://pypi.python.org/pypi/lunchtime

.. image:: https://travis-ci.com/robertopreste/lunchtime.svg?branch=master
        :target: https://travis-ci.com/robertopreste/lunchtime

.. image:: https://readthedocs.org/projects/lunchtime/badge/?version=latest
        :target: https://lunchtime.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Ignore all terminal commands while it's lunchtime!


* Free software: MIT license
* Documentation: https://lunchtime.readthedocs.io
* GitHub repo: https://github.com/robertopreste/lunchtime


Features
--------

This is a simple command-line application that will ignore all terminal commands while it's running.

Background
==========

Most of us have a boss or supervisor that usually walks in right at lunch time, asking for updates on the job. This is quite annoying, and often things end up with people starving while they show their results to the boss.

For this reason I decided to build this tool, so you can pretend your computer is not working and hopefully convince your boss to leave and have lunch at a decent time!

**PLEASE NOTE: use at your own risk!** Use this tool wisely, as it might lead to unexpected consequences (for your job) if misused.

Installation
------------

It is possible to install lunchtime using pip::

    pip install lunchtime

Both Python2 and Python3 are supported.

Please refer to the Installation_ section of the documentation for more details.

Usage
-----

Simply launch lunchtime and enjoy a broken terminal::

    $ lunchtime

A new clean terminal will open, where you can type your commands and no response will be produced. The lunchtime will stop when the ``exit`` command is issued.

If you want to astonish your boss even more, you can use the ``--crazy`` option::

    $ lunchtime --crazy

In this case, a weird string will be returned after each command!

Please refer to the Usage_ section of the documentation for more details.

Credits
-------

This package was created with Cookiecutter_ and the `cc-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cc-pypackage`: https://github.com/robertopreste/cc-pypackage
.. _Installation: https://lunchtime.readthedocs.io/en/latest/installation.html
.. _Usage: https://lunchtime.readthedocs.io/en/latest/usage.html
