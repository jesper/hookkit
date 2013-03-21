HookKit
=======

This is a toolkit aimed at simplifying the deployment and maintenance of server-side git hooks.

_hookkit_config.json_
  * stage (pre-receieve)
  * mode (legacy (normal stand alone hook) or hookkit (simpler to write from scratch)) 
  * script (the name of the script)
  * args (any arguments to pass to the script)

_hookkit.py_
  * Actual hook "dispatcher"

_libhookkit.py_
  * Configuration parsing & hook support

_link\_hooks.py_
  * Creates symlinks for all the hooks defined in hookkit.config to point to hook.py

_hooks/_
  * Various git hooks that can be enabled.

_tests/_
  * Tests for libhookkit as well as the hook_scripts.

**Special thanks to SpreadPointe for sponsoring the development of Hookkit**
