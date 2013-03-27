#!/usr/bin/env python

import unittest
import sys
import os

sys.path.append('..')
import test_helpers
from hook_script_test_case import hook_script_test_case


class test_script_scan_commit_field(hook_script_test_case):

    CONFIG_FILE = 'test_script_scan_commit_field_config.json'

    def test_local_invalid_message(self):
        test_helpers.deployLocalHookKit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        result = test_helpers.gitCommitWithMessage("I'm an invalid commit!")
        self.assertFalse(result, 'Pushing invalid commit to local repo')

    def test_local_valid_message(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        result = test_helpers.gitCommitWithMessage("I'm a valid commit! #123")
        self.assertTrue(result, "Pushing a valid commit message to local repo")

    def test_valid_message(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")
        self.assertTrue(test_helpers.gitPush(),
                        "Pushing a valid commit messages")

    def test_invalid_message(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm an invalid commit!")
        self.assertFalse(test_helpers.gitPush(),
                         'Pushing invalid commit messages')

    def test_tricky_invalid_message(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("I'm an invalid commit! #abc")
        self.assertFalse(test_helpers.gitPush(),
                         'Pushing invalid commit messages')

    def test_combined_invalid_message(self):
        test_helpers.deployHookKit(self.CONFIG_FILE)

        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.py')
        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")
        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.py')
        test_helpers.gitCommitWithMessage("I'm an invalid #123commit!")
        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.py')
        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")
        self.assertFalse(test_helpers.gitPush(),
                         "Pushing a combo of valid & invalid commit messages")

if __name__ == '__main__':
    unittest.main()
