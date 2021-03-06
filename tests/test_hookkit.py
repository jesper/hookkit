#!/usr/bin/env python

import unittest
import sys
import os

sys.path.append("..")
import test_helpers
from hook_script_test_case import hook_script_test_case


class test_hookkit(hook_script_test_case):

    def test_multiple_same_scripts_for_one_hook_valid_second_script(self):
        test_helpers.deployHookKit('test_hookkit_config.json')

        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.py')
        test_helpers.gitCommitWithMessage('Test message that should pass '
                                          'first hook: bar')

        self.assertFalse(test_helpers.gitPush(), 'Pushing a commit that '
                                                 'violates the second script '
                                                 'for a hook - missing foo')

    def test_multiple_same_scripts_for_one_hook_valid_first_script(self):
        test_helpers.deployHookKit('test_hookkit_config.json')

        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.py')
        test_helpers.gitCommitWithMessage('Test message that should pass '
                                          'first hook: foo')

        self.assertFalse(test_helpers.gitPush(), 'Pushing a commit that '
                                                 'violates the first script '
                                                 'for a hook - missing bar')

    def test_multiple_same_scripts_both_valid(self):
        test_helpers.deployHookKit('test_hookkit_config.json')

        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.py')
        test_helpers.gitCommitWithMessage('Test message that should pass '
                                          'both: foo bar')

        self.assertTrue(test_helpers.gitPush(), 'Pushing a commit that should '
                                                'be valid for both hooks')

    def test_multiple_same_scripts_both_invalid(self):
        test_helpers.deployHookKit('test_hookkit_config.json')

        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.py')
        test_helpers.gitCommitWithMessage('Test message that should fail both '
                                          'hooks')

        self.assertFalse(test_helpers.gitPush(), 'Pushing a commit that '
                                                 'should be invalid for both '
                                                 'hooks')

    def test_push_to_branch(self):
        test_helpers.deployHookKit('test_hookkit_config.json')
        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.py')
        test_helpers.runCommandInPath('git checkout -b test_branch',
                                      test_helpers.repo_checkout)
        test_helpers.gitCommitWithMessage('foo bar commit to push to a branch')
        self.assertTrue(test_helpers.gitPush('origin test_branch'),
                        'Push to a branch should work.')

    def test_push_branch_identical_to_master(self):
        test_helpers.deployHookKit('test_hookkit_config.json')
        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.py')
        test_helpers.gitCommitWithMessage('foo bar commit to push to a branch')
        test_helpers.gitPush()
        test_helpers.runCommandInPath('git checkout -b test_branch',
                                      test_helpers.repo_checkout)
        self.assertTrue(test_helpers.gitPush('origin test_branch'),
                        'Push to a branch should work.')

    def test_push_delete_branch(self):
        self.test_push_to_branch()
        del_result = test_helpers.runCommandInPath('git push origin '
                                                   ':test_branch',
                                                   test_helpers.repo_checkout)
        self.assertTrue(del_result, "Push to delete branch should work")

    def test_push_tag(self):
        test_helpers.deployHookKit('test_hookkit_config.json')
        test_helpers.runCommandInPath('git tag test_tag',
                                      test_helpers.repo_checkout)
        result = test_helpers.runCommandInPath('git push --tags',
                                               test_helpers.repo_checkout)

        self.assertTrue(result, "Pushing tags should work")

if __name__ == '__main__':
    unittest.main()
