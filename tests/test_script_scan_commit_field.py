#!/usr/bin/env python

import unittest
import sys
import os
import shutil

sys.path.append('..')
import test_helpers


class test_script_scan_commit_field(unittest.TestCase):

    CONFIG_FILE = 'test_script_scan_commit_field_config.json'

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

    def test_valid_message(self):
        test_helpers.deployHookkit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")
        self.assertTrue(test_helpers.gitPush(),
                        "Pushing a valid commit messages")

    def test_invalid_message(self):
        test_helpers.deployHookkit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

        test_helpers.gitCommitWithMessage("I'm an invalid commit!")
        self.assertFalse(test_helpers.gitPush(),
                         'Pushing invalid commit messages')

    def test_tricky_invalid_message(self):
        test_helpers.deployHookkit(self.CONFIG_FILE)

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

        test_helpers.gitCommitWithMessage("I'm an invalid commit! #abc")
        self.assertFalse(test_helpers.gitPush(),
                         'Pushing invalid commit messages')

    def test_combined_invalid_message(self):
        test_helpers.deployHookkit(self.CONFIG_FILE)

        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.txt')
        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")
        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.txt')
        test_helpers.gitCommitWithMessage("I'm an invalid #123commit!")
        os.system('echo A >> ' + test_helpers.repo_checkout + '/testfile.txt')
        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")
        self.assertFalse(test_helpers.gitPush(),
                         "Pushing a combo of valid & invalid commit messages")

if __name__ == '__main__':
    unittest.main()
