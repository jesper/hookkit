r"""

Description
^^^^^^^^^^^
Search a commit field (author email, commit message) for a specific pattern.
Useful for enforcing things such as issue refs, author email whitelists, etc.

Arguments
^^^^^^^^^
<*commit field*> <*regexp*>

* **Example**: ``message (^|\s)#(\d+)(\s|$)``
    * Scans the commit messages for a issue ID, for example: " #123 ".

Suggestion
^^^^^^^^^^
Run on each_commit as a pre-receive or update hook.

"""

import sys
import re

sys.path.append('..')
from libhookkit import LibHookKit, HookScript


class scan_commit_field(HookScript):

    def run(self, sha1):
        args = self.args.split(' ')

        field_to_scan = args[0]

        if field_to_scan == 'message':
            field_value = LibHookKit.get_commit_message(sha1)
        elif field_to_scan == 'author_email':
            field_value = LibHookKit.get_commit_author_email(sha1)

# Remove the field to scan, and joint the rest of the args back together
        args.pop(0)
        scan_regexp = ' '.join(args)

        return re.search(scan_regexp, field_value)
