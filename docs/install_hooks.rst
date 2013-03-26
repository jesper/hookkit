.. _install-hooks:

install_hooks.py
=================

install_hooks.py is the program you execute to install/enable HookKit for your repository.

To use it, first copy a :ref:`config-file` to your "hooks" directory.

The "hooks" directory will either be  *your_repo/hooks* or *your_repo/.git/hooks* depending on how it's set up.

Once you've done that, run *hookkit_directory/install_hooks.py* from your repository's "hooks" directory.

This command will read your config file, and create links that git can understand to your HookKit checkout.
