#!/usr/bin/env python

import unittest
import sys

sys.path.append("..")
import libhookkit


class test_libhookkit_hookkitconfiguration(unittest.TestCase):

    CONFIG_PREFIX = 'data/test_libhookkit_hookkitconfiguration_'

    def setUp(self):
        self.config = libhookkit.HookkitConfiguration()

    def test_load_scripts_for_hook(self):
        results = self.config.load_entries_for_hook('pre-receive',
                                                    (self.CONFIG_PREFIX +
                                                    'valid_config.json'))
        self.assertNotEqual(results,
                            [],
                            'Valid config should not return empty script list')

        results = self.config.load_entries_for_hook('undefined-hook',
                                                    (self.CONFIG_PREFIX +
                                                    'valid_config.json'))

        self.assertEqual(results,
                         [],
                         'Valid config file with invalid hook should '
                         'return empty script list')

        results = self.config.load_entries_for_hook('pre-receive',
                                                    (self.CONFIG_PREFIX +
                                                     'invalid_config.json'))

        self.assertEqual(results, [], 'Invalid config file with a valid hook')

        results = self.config.load_entries_for_hook('invalid',
                                                    'data/doesnt-exist.json')

        self.assertEqual(results, [],
                         'Invalid config file with an invalid hook')

    def test_get_available_hooks(self):
        results = self.config.get_available_hooks((self.CONFIG_PREFIX +
                                                   'valid_config.json'))

        self.assertEqual(results, ['pre-receive', 'post-receive'],
                         'Load valid config file and get expected ' +
                         'number of hooks')

        results = self.config.get_available_hooks('invalid-config')
        self.assertEqual(results, [],
                         'Load invalid config file and get no hooks')

    def test_multiple_same_scripts_for_hook(self):
        results = self.config.load_entries_for_hook('pre-receive',
                                                    'data/test_hookkit_'
                                                    'config.json')

        self.assertEqual(len(results), 2,
                         'Config with two identical scripts for a hook should '
                         'return both')

if __name__ == '__main__':
    unittest.main()
