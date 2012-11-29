#!/usr/bin/env python

import unittest
import sys
import os
import shutil
import socket

sys.path.append("..")
import test_helpers


class test_script_ping_url(unittest.TestCase):

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

    def test_notification(self):
        test_helpers.deployHookkit('test_script_ping_url_config.json')

        os.system(('echo foo >> ' + test_helpers.repo_checkout +
                   '/testfile.txt'))
        test_helpers.gitCommitWithMessage("Testing notifications")

 # Fork a listening socket for the hook to push into
        pid = os.fork()
        if pid:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', 4891))
            s.listen(1)
            conn, addr = s.accept()
            server_data_received = conn.recv(1024)
            conn.sendall('HTTP/1.1 200 OK\r\n')
            conn.close()
# make sure the child process gets cleaned up
            os.waitpid(pid, 0)
        else:
            self.assertTrue(test_helpers.gitPush(),
                            "Pushing a commit and receiving a url ping")
            os._exit(0)

        self.assertEqual('GET / HTTP/1.1', server_data_received.split('\r')[0])

if __name__ == '__main__':
    unittest.main()
