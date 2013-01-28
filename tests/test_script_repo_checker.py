#!/usr/bin/env python

import unittest
import sys
import os
import shutil

sys.path.append("..")
import test_helpers


class test_script_repo_checker(unittest.TestCase):

    def setUp(self):
#FIXME Should pull this out into the git_helpers
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

    def test_valid_commit(self):
        test_helpers.deployHookKit('test_script_repo_checker_config.json')

        os.system(('echo "no thanksgivings birds here" >> ' +
                  test_helpers.repo_checkout + '/testfile.txt'))

        test_helpers.gitCommitWithMessage('Testing Repo Checker with '
                                          'a valid file')

        self.assertTrue(test_helpers.gitPush(),
                        'Pushing a valid file')

    def test_invalid_commit(self):
        test_helpers.deployHookKit('test_script_repo_checker_config.json')

        os.system(('echo "Gobble gobble - a turkey lives here" >> ' +
                  test_helpers.repo_checkout + '/testfile.txt'))

        test_helpers.gitCommitWithMessage('Testing Repo Checker with '
                                          'an invalid file')

        self.assertFalse(test_helpers.gitPush(),
                         'Pushing an invalid file')


if __name__ == '__main__':
    unittest.main()
