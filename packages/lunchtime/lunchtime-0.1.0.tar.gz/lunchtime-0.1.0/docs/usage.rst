=====
Usage
=====

Simply launch lunchtime and enjoy a broken terminal::

    $ lunchtime

A new clean terminal will open, where you can type your commands and no response will be produced. The lunchtime will stop when the ``exit`` command is issued.

If you want to astonish your boss even more, you can use the ``--crazy`` option::

    $ lunchtime --crazy
    # or also
    $ lunchtime -c

In this case, a weird string will be returned after each command!

When starting and stopping lunchtime, a simple message is printed and a 2-second sleep is performed. If you're in a hurry because your boss is approaching, you can use the ``--silent`` option to skip these and jump right into the (broken) terminal::

    $ lunchtime --silent
    # or also
    $ lunchtime -s

As usual, type ``exit`` to go back to your functioning terminal.
