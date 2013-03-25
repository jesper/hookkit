"""

Description
^^^^^^^^^^^
Used for running a program against an entire repository.
Executing unit tests for example.
If the command returns a non-zero exit code, the push is rejected.

Arguments
^^^^^^^^^
<*command to execute*>

* **Example**: ``bin/run_tests.sh``
    * Execute bin/run_tests.sh.

Suggestion
^^^^^^^^^^
Run on last_commit, as you likely only care about the final state of the repo.

"""

import sys
import tempfile
import subprocess
import shutil

sys.path.append('..')
from libhookkit import HookScript, LibHookKit


class repo_checker(HookScript):

    def run(self, old_sha1, new_sha1, ref):
        temp_path = tempfile.mkdtemp()
        LibHookKit.extract_repo_at_sha1_to_path(new_sha1, temp_path)

        p = subprocess.Popen(self.args.split(), cwd=temp_path,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        [output, error] = p.communicate()

        shutil.rmtree(temp_path)

        if p.returncode != 0:
            print error
            return False

        return True

    def checker(self):
        return self.args.split()[0]

# Let's make sure that the configured program is available
    def setup(self):
        if not LibHookKit.is_program_available(self.checker()):
            print ("Repo Checker Hook-Script could not find checker: " +
                   self.checker())
            return False
        else:
            return True
