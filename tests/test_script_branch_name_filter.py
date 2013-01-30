#!/usr/bin/env python

import unittest
import sys
import os

sys.path.append("..")
import test_helpers
from hook_script_test_case import hook_script_test_case


class test_script_branch_name_filter(hook_script_test_case):

    def test_valid_branch_name(self):
        test_helpers.deployHookKit('test_script_branch_name_filter.json')

        test_helpers.runCommandInPath('git checkout -b 123-joe-bar',
                                      test_helpers.repo_checkout)

        self.assertTrue(test_helpers.gitPush('origin 123-joe-bar'),
                        'Pushing a valid branch name')

    def test_whitelist_branch_name(self):
        test_helpers.deployHookKit('test_script_branch_name_filter.json')

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.py'))

        test_helpers.gitCommitWithMessage("test whitelist branch name")

        self.assertTrue(test_helpers.gitPush(), 'Push a whitelist branch name')

    def test_invalid_branch_name(self):
        test_helpers.deployHookKit('test_script_branch_name_filter.json')

        test_helpers.runCommandInPath('git checkout -b abc-foo-bar',
                                      test_helpers.repo_checkout)

        self.assertFalse(test_helpers.gitPush('origin abc-foo-bar'),
                         'Pushing an invalid branch name')

if __name__ == '__main__':
    unittest.main()
