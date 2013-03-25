r"""

Description
^^^^^^^^^^^
Enforce a specific branch naming scheme.

Arguments
^^^^^^^^^
<*branch name regexp*>

* **Example**: ``master|\d+-\w+-\w+``
    * Allow pushes to branches named "master" or "<number>-<word>-<word>"

Suggestion
^^^^^^^^^^
Run on last_commit as a pre-receive hook.

"""

import sys
import re

sys.path.append('..')
from libhookkit import HookScript


class branch_name_filter(HookScript):

    def run(self, _old_sha1, _new_sha1, ref):
        branch_name = ref.split('refs/heads')[1]
        return re.search(self.args, branch_name)
