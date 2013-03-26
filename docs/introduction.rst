Introduction
====================

What
^^^^
HookKit is a toolkit for managing and deploying `git hooks <http://git-scm.com/book/en/Customizing-Git-Git-Hooks>`_.

Git hooks are programs that are automatically executed at specific points in the git work-flow. To simplify things, we'll categorize them into "pre' hooks and "post" hooks.

"Pre" hooks are run when a user is about to "write" a commit to either their local system or push their changes to a server. In these cases, it's useful to run a program (hook) to verify that certain conditions are met. This way, you can reject a commit that doesn't adhere to a coding style, or pass tests for example.

"Post" hooks happen after a commit has been "written" to user's workstation or pushed to a server. This is useful for notifying people or other automated systems of changes which have been made available. Triggering a package build & release for example.

Why
^^^
* Because if you **can** automate it, you **should** automate it.
* The earlier you find a bug, the `cheaper <http://www.riceconsulting.com/public_pdf/STBC-WM.pdf>`_  it is to fix it.
* `Polling <http://blogs.msdn.com/b/oldnewthing/archive/2006/01/24/516808.aspx>`_ `is <http://fatalfailure.wordpress.com/2011/12/28/triggering-jenkins-jobs-from-the-scm-push-to-avoid-the-evil-polling/>`_ `evil. <http://kohsuke.org/2011/12/01/polling-must-die-triggering-jenkins-builds-from-a-git-hook/>`_
* *Fast* feedback is fun & useful. Waiting for an email from the CI system is too *slow*.

How
^^^
HookKit is broken down into five main components:

#. :ref:`hookkit` - Facade that git interacts with; manages & dispatches your git hook scripts.
#. :ref:`link-hooks` - Used to deploy HookKit to your git repository.
#. :ref:`hook-scripts` - Directory of generic scripts which you should use to build your hooks.
#. :ref:`config-file` - Defines which hook_scripts you're using, when they should be executed, and how they're configured.
#. :ref:`libhookkit` - Functions used by hookkit and hook_scripts to interact with git and other convenience functions.
