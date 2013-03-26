.. _hookkit:

hookkit.py
==============

*hookkit.py* is the first point of contact for when git itself interacts with HookKit.
*hookkit.py* queries the :ref:`config-file` for which scripts it should execute, how, and when.

This program should not be executed by the user, but rather purely from git - via a link created by :ref:`install-hooks`.
