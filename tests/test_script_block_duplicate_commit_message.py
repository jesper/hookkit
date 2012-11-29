#!/usr/bin/env python

import unittest
import sys
import os
import shutil

sys.path.append('..')
import test_helpers


class test_script_block_duplicate_commit_message(unittest.TestCase):

    CONFIG_FILE = 'test_script_block_duplicate_commit_message_config.json'

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

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

        test_helpers.gitCommitWithMessage("I'm a valid commit too! #123")

        self.assertTrue(test_helpers.gitPush(),
                        "Pushing valid commit messages")

    def test_invalid_message(self):
        test_helpers.deployHookkit(self.CONFIG_FILE)
        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

        test_helpers.gitCommitWithMessage("I'm a future invalid commit!")
        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

        test_helpers.gitCommitWithMessage("I'm a future invalid commit!")
        self.assertFalse(test_helpers.gitPush(),
                         'Pushing invalid commit messages')

    def test_invalid_message_inbetween_push(self):
        test_helpers.deployHookkit(self.CONFIG_FILE)
        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

        test_helpers.gitCommitWithMessage("I'm a future invalid commit!")
        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

        test_helpers.gitCommitWithMessage("I'm a valid commit! #123")

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))

        self.assertTrue(test_helpers.gitPush(),
                        "Pushing valid commit messages")

        test_helpers.gitCommitWithMessage("I'm a future invalid commit!")
        self.assertFalse(test_helpers.gitPush(),
                         'Pushing invalid commit messages')

if __name__ == '__main__':
    unittest.main()
