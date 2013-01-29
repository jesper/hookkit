#!/usr/bin/env python

import unittest
import sys
import os
import shutil

sys.path.append("..")
import test_helpers


class test_script_branch_name_filter(unittest.TestCase):

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
                                       test_helpers.repo_server +
                                       ' ' + test_helpers.repo_checkout), '.')

    def tearDown(self):
        shutil.rmtree(test_helpers.repo_server)
        shutil.rmtree(test_helpers.repo_checkout)

    def test_valid_branch_name(self):
        test_helpers.deployHookKit('test_script_branch_name_filter.json')

        test_helpers.runCommandInPath('git checkout -b 123-joe-bar',
                                      test_helpers.repo_checkout)

        self.assertTrue(test_helpers.gitPush('origin 123-joe-bar'),
                        'Pushing a valid branch name')

    def test_whitelist_branch_name(self):
        test_helpers.deployHookKit('test_script_branch_name_filter.json')

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

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
