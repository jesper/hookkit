#   Hook Name: file_checker
#   Arguments: file_filter_regexp file_checker_program
# Description: Used for running a file checker against against
#              files changed in a push. A coding style checker for example.
#  Suggestion: Run on last_commit, as you typically only care about the "last"
#              state of the files
#      Author: Jesper Thomschutz (jesper@jespersaur.com)

import sys
import os
import re
import tempfile
import subprocess
import shutil

sys.path.append('..')
from libhookkit import HookScript, LibHookKit


class file_checker(HookScript):

    def run(self, old_sha1, new_sha1, ref):
        file_regexp = self.regexp()
        file_checker = self.checker()

        files = LibHookKit.get_files_affected_between_two_commits(old_sha1,
                                                                  new_sha1)

        for file_path in files:
            if re.search(file_regexp, file_path):
                temp_path = tempfile.mkdtemp()

                LibHookKit.extract_file_at_sha1_to_path(file_path, new_sha1,
                                                        temp_path)

# File may have been deleted in git - verify it's actually there.
                if not os.path.exists(temp_path + '/' + file_path):
                    #FIXME Having this extra rmtree is ugly - refactor!
                    shutil.rmtree(temp_path)
                    continue

                p = subprocess.Popen([file_checker, file_path], cwd=temp_path,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

                [output, error] = p.communicate()

                shutil.rmtree(temp_path)

                if p.returncode != 0:
                    print output
                    return False

        return True

    def regexp(self):
        return self.args.split(' ')[0]

    def checker(self):
        return self.args.split(' ')[1]

# Let's make sure that the configured file checker is installed.
    def setup(self):
        if not LibHookKit.is_program_available(self.checker()):
            print ("File Checker Hook-Script could not find checker: " +
                   self.checker())
            return False
        else:
            return True
