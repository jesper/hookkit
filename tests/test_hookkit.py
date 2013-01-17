#!/usr/bin/env python

import unittest
import sys
import os
import shutil

sys.path.append("..")
import test_helpers


class test_hookkit(unittest.TestCase):

    def setUp(self):
        # Let's set up a base repo
        repo_original = 'test_original_repo'
        os.mkdir(repo_original)
        test_helpers.runCommandInPath('git init', repo_original)
        test_helpers.runCommandInPath('touch testfile.txt', repo_original)
        test_helpers.runCommandInPath('git add testfile.txt', repo_original)
        test_helpers.runCommandInPath('git commit -a -m adding:testfile.txt',
                                      repo_original)

        # Let's clone a server copy to work from in the future.
        test_helpers.runCommandInPath(('git clone --bare ' + repo_original +
                                       ' ' + test_helpers.repo_server), '.')
        shutil.rmtree(repo_original)
        test_helpers.runCommandInPath(('git clone ' +
                                       test_helpers.repo_server + ' ' +
                                       test_helpers.repo_checkout), '.')

    def tearDown(self):
        shutil.rmtree(test_helpers.repo_server)
        shutil.rmtree(test_helpers.repo_checkout)

    def test_multiple_same_scripts_for_one_hook_valid_second_script(self):
        test_helpers.deployHookkit('test_hookkit_config.json')

        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.txt')
        test_helpers.gitCommitWithMessage('Test message that should pass '
                                          'first hook: bar')

        self.assertFalse(test_helpers.gitPush(), 'Pushing a commit that '
                                                 'violates the second script '
                                                 'for a hook - missing foo')

    def test_multiple_same_scripts_for_one_hook_valid_first_script(self):
        test_helpers.deployHookkit('test_hookkit_config.json')

        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.txt')
        test_helpers.gitCommitWithMessage('Test message that should pass '
                                          'first hook: foo')

        self.assertFalse(test_helpers.gitPush(), 'Pushing a commit that '
                                                 'violates the first script '
                                                 'for a hook - missing bar')

    def test_multiple_same_scripts_both_valid(self):
        test_helpers.deployHookkit('test_hookkit_config.json')

        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.txt')
        test_helpers.gitCommitWithMessage('Test message that should pass '
                                          'both: foo bar')

        self.assertTrue(test_helpers.gitPush(), 'Pushing a commit that should '
                                                'be valid for both hooks')

    def test_multiple_same_scripts_both_invalid(self):
        test_helpers.deployHookkit('test_hookkit_config.json')

        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.txt')
        test_helpers.gitCommitWithMessage('Test message that should fail both '
                                          'hooks')

        self.assertFalse(test_helpers.gitPush(), 'Pushing a commit that '
                                                 'should be invalid for both '
                                                 'hooks')

    def test_push_to_branch(self):
        test_helpers.deployHookkit('test_hookkit_config.json')
        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.txt')
        test_helpers.runCommandInPath('git checkout -b test_branch',
                                      test_helpers.repo_checkout)
        test_helpers.gitCommitWithMessage('foo bar commit to push to a branch')
        self.assertTrue(test_helpers.gitPush('origin test_branch'),
                        'Push to a branch should work.')

    def test_push_delete_branch(self):
        self.test_push_to_branch()
        del_result = test_helpers.runCommandInPath('git push origin '
                                                   ':test_branch',
                                                   test_helpers.repo_checkout)
        self.assertTrue(del_result, "Push to delete branch should work")


    def test_push_tag(self):
        test_helpers.deployHookkit('test_hookkit_config.json')
        test_helpers.runCommandInPath('git tag test_tag',
                                      test_helpers.repo_checkout)
        result = test_helpers.runCommandInPath('git push --tags',
                                               test_helpers.repo_checkout)

        self.assertTrue(result, "Pushing tags should work")

if __name__ == '__main__':
    unittest.main()
