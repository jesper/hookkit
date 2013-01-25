#   Hook Name: scan_commit_field
#   Arguments: commit_field regexp
# Description: Used to regexp commit fields. Good for author whitelists, etc.
#  Suggestion: Run on each_commit as a pre-receive or update hook
#      Author: Jesper Thomschutz (jesper@jespersaur.com)

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

        if re.search(scan_regexp, field_value):
            return True
        else:
            return False
