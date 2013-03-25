"""

Description
^^^^^^^^^^^
Used for running a program against against files \
changed in a push. A coding style checker for example.

Arguments
^^^^^^^^^
<*file filter regexp*> <*program*>

* **Example**: ``\.py$ pylint``
    * Execute "pylint" on all files ending with ".py"

Suggestion
^^^^^^^^^^
Run on last_commit, as you likely only care about the final state of the repo

"""

import sys
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

        files = LibHookKit.get_files_modified_between_two_commits(old_sha1,
                                                                  new_sha1)
        for file_path in files:
            if re.search(file_regexp, file_path):
                temp_path = tempfile.mkdtemp()

                if not LibHookKit.extract_file_at_sha1_to_path(file_path,
                                                               new_sha1,
                                                               temp_path):
                    return False

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
