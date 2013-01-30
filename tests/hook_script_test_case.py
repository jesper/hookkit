#!/usr/bin/env python

import unittest
import sys
import os
import shutil

sys.path.append("..")
import test_helpers


class hook_script_test_case(unittest.TestCase):

    def setUp(self):
        # Let's set up a base repo
        repo_original = 'test_original_repo'
        os.mkdir(repo_original)
        test_helpers.runCommandInPath('git init', repo_original)
        test_helpers.runCommandInPath('touch testfile.py', repo_original)
        test_helpers.runCommandInPath('git add testfile.py', repo_original)
        test_helpers.runCommandInPath('git commit -a -m adding:testfile.py',
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
