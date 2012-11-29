#!/usr/bin/env python

import unittest
import sys
import os
import shutil

sys.path.append("..")
import test_helpers


class test_script_file_checker(unittest.TestCase):

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

    def test_valid_code(self):
        test_helpers.deployHookkit('test_script_file_checker_config.json')

        os.system(('echo "print "valid indentation rocks"" >> ' +
                  test_helpers.repo_checkout + '/test_code.py'))

        test_helpers.runCommandInPath('git add test_code.py',
                                      test_helpers.repo_checkout)

        test_helpers.gitCommitWithMessage('Testing File Checker with '
                                          'a valid file')

        self.assertTrue(test_helpers.gitPush(),
                        'Pushing a well formatted Python file')

    def test_invalid_code_that_shouldnt_be_scanned(self):
        test_helpers.deployHookkit('test_script_file_checker_config.json')

        os.system(('echo "    print "invalid indent - nobody checks it"" >> ' +
                  test_helpers.repo_checkout + '/test_code.cpp'))

        test_helpers.runCommandInPath('git add test_code.cpp',
                                      test_helpers.repo_checkout)

        test_helpers.gitCommitWithMessage('Testing File Checker with a '
                                          'file it should ignore')

        self.assertTrue(test_helpers.gitPush(),
                        "Pushing a badly formatted file "
                        "which shouldn't be scanned")

    def test_invalid_code(self):
        test_helpers.deployHookkit('test_script_file_checker_config.json')

        os.system(('echo "   print "invalid indent makes snakes cry"" >> ' +
                  test_helpers.repo_checkout + '/test_code.py'))

        test_helpers.runCommandInPath('git add test_code.py',
                                      test_helpers.repo_checkout)

        test_helpers.gitCommitWithMessage("Testing File Checker with an "
                                          "invalid file")

        self.assertFalse(test_helpers.gitPush(),
                         "Pushing a badly formatted Python file")

    def test_invalid_code_in_blacklisted_dir(self):
        test_helpers.deployHookkit('test_script_file_checker_config.json')

        os.system('mkdir ' + test_helpers.repo_checkout + '/blacklist')

        os.system(('echo "   print "invalid indent makes snakes cry"" >> ' +
                  test_helpers.repo_checkout + '/blacklist/test_code.py'))

        test_helpers.runCommandInPath('git add blacklist/test_code.py',
                                      test_helpers.repo_checkout)

        test_helpers.gitCommitWithMessage("Testing File Checker with an "
                                          "invalid file in blacklist dir")

        self.assertTrue(test_helpers.gitPush(),
                        "Pushing a badly formatted Python file in"
                        " a blacklisted directory should work")

    def test_invalid_file_checker_program(self):
        test_helpers.deployHookkit('test_script_file_checker_config_invalid'
                                   '_file_checker_program.json')

        os.system(('echo "print "valid indentation rocks"" >> ' +
                  test_helpers.repo_checkout + '/test_code.py'))

        test_helpers.runCommandInPath('git add test_code.py',
                                      test_helpers.repo_checkout)

        test_helpers.gitCommitWithMessage('Testing File Checker with '
                                          'a valid file but broken checker')

        self.assertFalse(test_helpers.gitPush(),
                         "Pushing a valid commit to a server with and invalid "
                         "file checker configured should fail.")


if __name__ == '__main__':
    unittest.main()
