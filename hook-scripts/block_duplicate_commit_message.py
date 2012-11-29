#   Hook Name: block_duplicate_commit_message
#   Arguments: none
# Description: Block commit messages that already exist in the repo.
#  Suggestion: Run on each_commit as a pre-receive or update hook
#      Author: Jesper Thomschutz (jesper@jespersaur.com)

import sys

sys.path.append('..')
from libhookkit import Hookkit, HookScript


class block_duplicate_commit_message(HookScript):

    def duplicate_found(self, new_sha1, old_sha1):
        print ("Duplicate commit message of " + new_sha1 +
               " found in " + old_sha1)
        return False

    def scan_sha1_list_for_message(self, sha1s, message):
        for sha1 in sha1s:
            if Hookkit.get_commit_message(sha1) == message:
                return sha1

        return False

    def run(self, old_sha1, new_sha1, ref):

        sha1s = Hookkit.get_sha1_list_between_commits(old_sha1, new_sha1)

        for sha1 in sha1s:
            commit_message = Hookkit.run_git_command(['log', '-1',
                                                      '--format=%s%n%b',
                                                      sha1])

# 1) Check the staged commits if they have a duplicate commit message
            other_sha1s = [e for e in sha1s if not e == sha1]

            found = self.scan_sha1_list_for_message(other_sha1s,
                                                    commit_message)

            if found:
                return self.duplicate_found(sha1, found)

# 2) Check existing commits if they have a duplicate commit message
            commit_message = commit_message.rstrip()

# Needed for multi-line comments
            grep_prefix = ''

            if '\n' in commit_message:
                grep_prefix = '/'

            match_sha1s = Hookkit.run_git_command(['log', '--format=%H',
                                                   '--grep=' + grep_prefix +
                                                   '^%s$' % commit_message])

            match_sha1s = filter(None, match_sha1s.split('\n'))

# sha1s may contain partial matches - refine it down to exact matches
            for _sha1 in match_sha1s:
                old_message = Hookkit.get_commit_message(_sha1).rstrip()
                if old_message == commit_message:
                    return self.duplicate_found(sha1, _sha1)

        return True
