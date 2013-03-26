.. _config-file:

Configuration File
====================

The HookKit configuration file (hookkit_config.json) is the core of how your instance of HookKit will operate.

It glues the :ref:`hook-scripts` to their arguments as well as specifying when and how they should be executed.

As the config file extension suggests, the config file is simply plain `JSON <http://en.wikipedia.org/wiki/JSON>`_.

JSON makes a good format for the configuration for at least two reasons:

#. Human readable & easy to edit. There are plenty of web-based JSON editors available to ease the process & avoid forgetting a brace.
#. Plain text which can be committed to git & diffed in a straight forward way.



Writing a config file may seem a little intimidating at first, but it's actually quite straight forward.
To get started, it might be easiest to start from a sample config file template, found under "sample_configs/" in HookKit.

All config files must include the "hooks" section:

.. code-block:: javascript

  {
    "hooks": {
    }
  }



*hooks* should contain the stages for which you'd like to execute your hooks.
The stages for which you can execute hooks are explained well in the `git documentation <http://git-scm.com/book/en/Customizing-Git-Git-Hooks#Server-Side-Hooks>`_.

In general, you'll likely want to use:

* update - Used as a "gate". When you want to check/inspect commits **before** they are written to the repo, rejecting them if they don't adhere to your criteria/requirements.
* post-receive - For notification. This is triggered after the commits are actually pushed to the branch.


.. code-block:: javascript

  {
    "hooks": {
      "update": {
      },
      "post-receive": {
      }
    }
  }

*Note that in this example we have both "update" and "post-receive" sections. It's perfectly fine to omit one of them entirely if it's not needed.*



Next up, we need to populate each stage with the rules that we'd like to utilize.
Each rule should consist of a short and descriptive label, as well as the following sub-elements:

* script: hook-script to execute. The hook-scripts available are listed on the :ref:`hook-scripts` page.
* error_message: Error message to show the user if the hook fails
* args: hook-script specific arguments. The arguments a hook script requires is documented on the :ref:`hook-scripts` page.
* frequency: either *each_commit* or *last_commit*

  * *each_commit* will run the script on each commit. Good for strict checks per commit.
  * *last_commit* will only run the script on the last (final) commit. Good for if you only care about the "final" state of a repo after a push for example.


.. code-block:: javascript

  {
    "hooks": {
      "update": {
        "Pyflakes Code Check": {
          "script":"file_checker",
          "error_message":"Code failed the Pyflakes code check",
          "args":"\\.py$ pyflakes",
          "frequency":"last_commit",
          "mode":"hookkit"
        },
        "Email Whitelist": {
          "script":"scan_commit_field",
          "error_message":"Commit author e-mail address is not in the whitelist",
          "args":"author_email (developer1|developer2|developern)@company.com",
          "frequency":"each_commit",
          "mode":"hookkit"
        }
      },
      "post-receive": {
        "Notify Redmine": {
          "script":"ping_url",
          "error_message":"Unable to notify redmine.",
          "args":"https://company.com/redmine/sys/fetch_changesets?key=foobar",
          "frequency":"last_commit",
          "mode":"hookkit"
        }
      }
    }
  }

*Note that escaping slahes in the arguments is required!*
