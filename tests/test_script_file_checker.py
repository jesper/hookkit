#!/usr/bin/env python

import unittest
import sys
import os

sys.path.append("..")
import test_helpers
from hook_script_test_case import hook_script_test_case


class test_script_file_checker(hook_script_test_case):

    def test_valid_code(self):
        test_helpers.deployHookKit('test_script_file_checker_config.json')

        os.system(('echo "print "valid indentation rocks"" >> ' +
                  test_helpers.repo_checkout + '/testfile.py'))

        test_helpers.gitCommitWithMessage('Testing File Checker with '
                                          'a valid file')

        self.assertTrue(test_helpers.gitPush(),
                        'Pushing a well formatted Python file')

    def test_invalid_code_that_shouldnt_be_scanned(self):
        test_helpers.deployHookKit('test_script_file_checker_config.json')

        os.system(('echo "    print "invalid indent - nobody checks it"" >> ' +
                  test_helpers.repo_checkout + '/testfile.cpp'))

        test_helpers.runCommandInPath('git add testfile.cpp',
                                      test_helpers.repo_checkout)

        test_helpers.gitCommitWithMessage('Testing File Checker with a '
                                          'file it should ignore')

        self.assertTrue(test_helpers.gitPush(),
                        "Pushing a badly formatted file "
                        "which shouldn't be scanned")

    def test_invalid_code(self):
        test_helpers.deployHookKit('test_script_file_checker_config.json')

        os.system(('echo "   print "invalid indent makes snakes cry"" >> ' +
                  test_helpers.repo_checkout + '/testfile.py'))

        test_helpers.gitCommitWithMessage("Testing File Checker with an "
                                          "invalid file")

        self.assertFalse(test_helpers.gitPush(),
                         "Pushing a badly formatted Python file")

    def test_invalid_code_in_blacklisted_dir(self):
        test_helpers.deployHookKit('test_script_file_checker_config.json')

        os.system('mkdir ' + test_helpers.repo_checkout + '/blacklist')

        os.system(('echo "   print "invalid indent makes snakes cry"" >> ' +
                  test_helpers.repo_checkout + '/blacklist/testfile.py'))

        test_helpers.runCommandInPath('git add blacklist/testfile.py',
                                      test_helpers.repo_checkout)

        test_helpers.gitCommitWithMessage("Testing File Checker with an "
                                          "invalid file in blacklist dir")

        self.assertTrue(test_helpers.gitPush(),
                        "Pushing a badly formatted Python file in"
                        " a blacklisted directory should work")

    def test_invalid_file_checker_program(self):
        test_helpers.deployHookKit('test_script_file_checker_config_invalid'
                                   '_file_checker_program.json')

        os.system(('echo "print "valid indentation rocks"" >> ' +
                  test_helpers.repo_checkout + '/testfile.py'))

        test_helpers.gitCommitWithMessage('Testing File Checker with '
                                          'a valid file but broken checker')

        self.assertFalse(test_helpers.gitPush(),
                         "Pushing a valid commit to a server with and invalid "
                         "file checker configured should fail.")

    def test_move_valid_code(self):
        test_helpers.deployHookKit('test_script_file_checker_config.json')

        os.system(('echo "print "valid indentation rocks"" >> ' +
                  test_helpers.repo_checkout + '/testfile.py'))

        test_helpers.gitCommitWithMessage('Testing File Checker with '
                                          'a valid file')

        test_helpers.gitPush()

        test_helpers.runCommandInPath('git mv testfile.py testfile2.py',
                                      test_helpers.repo_checkout)

        test_helpers.gitCommitWithMessage('Testing File Checker with '
                                          'moving a valid file')

        self.assertTrue(test_helpers.gitPush(),
                        'Pushing a well formatted Python file that was moved')

    def test_delete_valid_code(self):
        test_helpers.deployHookKit('test_script_file_checker_config.json')

        os.system(('echo "print "valid indentation rocks"" >> ' +
                  test_helpers.repo_checkout + '/testfile.py'))

        test_helpers.gitCommitWithMessage('Testing File Checker with '
                                          'a valid file')

        test_helpers.gitPush()

        test_helpers.runCommandInPath('git rm testfile.py',
                                      test_helpers.repo_checkout)

        test_helpers.gitCommitWithMessage('Testing File Checker with '
                                          'removing a valid file')

        self.assertTrue(test_helpers.gitPush(),
                        'Pushing a delete of a well formatted Python file')


if __name__ == '__main__':
    unittest.main()
