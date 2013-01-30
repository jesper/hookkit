#!/usr/bin/env python

import unittest
import sys
import os

sys.path.append("..")
import test_helpers
from hook_script_test_case import hook_script_test_case


class test_script_repo_checker(hook_script_test_case):

    def test_valid_commit(self):
        test_helpers.deployHookKit('test_script_repo_checker_config.json')

        os.system(('echo "no thanksgivings birds here" >> ' +
                  test_helpers.repo_checkout + '/testfile.py'))

        test_helpers.gitCommitWithMessage('Testing Repo Checker with '
                                          'a valid file')

        self.assertTrue(test_helpers.gitPush(),
                        'Pushing a valid file')

    def test_invalid_commit(self):
        test_helpers.deployHookKit('test_script_repo_checker_config.json')

        os.system(('echo "Gobble gobble - a turkey lives here" >> ' +
                  test_helpers.repo_checkout + '/testfile.py'))

        test_helpers.gitCommitWithMessage('Testing Repo Checker with '
                                          'an invalid file')

        self.assertFalse(test_helpers.gitPush(),
                         'Pushing an invalid file')


if __name__ == '__main__':
    unittest.main()
