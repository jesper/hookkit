#!/usr/bin/env python

import os

import sys
sys.path.insert(0, os.path.dirname(__file__))

import libhookkit

config = libhookkit.HookkitConfiguration()

hooks = config.get_available_hooks()

if len(hooks) == 0:
    print 'No hooks defined in "hookkit_config.json"; aborting.'
    exit(1)

exit_code = 0

for hook in hooks:
    print 'Linking hook: ' + hook

    if os.path.isfile(hook) or os.path.islink(hook):
        print 'Failed linking ' + hook + '. File already exists.'
        exit_code += 1
        continue

    try:
        os.symlink('hookkit.py', hook)
    except:
        print 'Failed link: ' + hook + '. Verify that you have write access.'
        exit_code += 1

exit(exit_code)
