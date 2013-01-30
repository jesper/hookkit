#!/usr/bin/env python

import unittest
import sys
import os

sys.path.append('..')
import test_helpers
from hook_script_test_case import hook_script_test_case


class test_script_block_duplicate_commit_message(hook_script_test_case):

    CONFIG_FILE = 'test_script_block_duplicate_commit_message_config.json'

    def test_invalid_message_with_special_characters(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("adding **kwargs support for the "
                                          "service and unit tests #363")

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("adding **kwargs support for the "
                                          "service and unit tests #363")

        self.assertFalse(test_helpers.gitPush(),
                         "Pushing invalid commit message with special chars")

    def test_valid_message_with_special_characters(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("adding **kwargs support for the "
                                          "service and unit tests #363")

        self.assertTrue(test_helpers.gitPush(),
                        "Pushing valid commit message with special characters")

    def test_valid_message(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a valid commit too! #123")

        self.assertTrue(test_helpers.gitPush(),
                        "Pushing valid commit messages")

    def test_invalid_message(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)
        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a future invalid commit!")
        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a future invalid commit!")
        self.assertFalse(test_helpers.gitPush(),
                         'Pushing invalid commit messages')

    def test_invalid_message_inbetween_push(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)
        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a future invalid commit!")
        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        self.assertTrue(test_helpers.gitPush(),
                        "Pushing valid commit messages")

        test_helpers.gitCommitWithMessage("I'm a future invalid commit!")
        self.assertFalse(test_helpers.gitPush(),
                         'Pushing invalid commit messages after push')

    def test_commit_already_exists_in_other_branch_after_merge(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)
        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a valid commit!")
        test_helpers.gitPush()

        test_helpers.runCommandInPath('git checkout -b test',
                                      test_helpers.repo_checkout)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a valid commit as well")

        result = test_helpers.runCommandInPath('git push origin test',
                                               test_helpers.repo_checkout)

        self.assertTrue(result,
                        "Pushing sha1 that already exists in other branch")

        test_helpers.runCommandInPath('git checkout master',
                                      test_helpers.repo_checkout)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a valid commit also!")
        test_helpers.gitPush()

        test_helpers.runCommandInPath('git checkout test',
                                      test_helpers.repo_checkout)

        test_helpers.runCommandInPath('git merge master',
                                      test_helpers.repo_checkout)
        result = test_helpers.runCommandInPath('git push origin test',
                                               test_helpers.repo_checkout)

        self.assertTrue(result,
                        "Pushing sha1 that already exists in other branch")

    def test_commit_already_exists_in_other_branch(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)
        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a valid commit!")
        test_helpers.gitPush()

        test_helpers.runCommandInPath('git checkout -b test',
                                      test_helpers.repo_checkout)

        result = test_helpers.runCommandInPath('git push origin test',
                                               test_helpers.repo_checkout)

        self.assertTrue(result,
                        "Pushing sha1 that already exists in other branch")


if __name__ == '__main__':
    unittest.main()
