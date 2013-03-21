#   Hook Name: branch_name_filter
#   Arguments: name-filter-regexp
# Description: Useful for enforcing a special branch naming scheme
#  Suggestion: Run on last_commit as a pre-preceive hook
#      Author: Jesper Thomschutz (jesper@jespersaur.com)

import sys
import re

sys.path.append('..')
from libhookkit import HookScript


class branch_name_filter(HookScript):

    def run(self, old_sha1, new_sha1, ref):
        branch_name = ref.split('refs/heads')[1]
        return re.search(self.args, branch_name)
