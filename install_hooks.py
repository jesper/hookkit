#!/usr/bin/env python

import os

import sys
sys.path.insert(0, os.path.dirname(__file__))

import libhookkit


def main():
    config = libhookkit.LibHookKitConfiguration()

    hooks = config.get_available_hooks("hookkit_config.json")

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
            os.symlink(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'hookkit.py'), hook)
        except:
            print 'Failed link: ' + hook + '. Verify you have write access.'
            exit_code += 1

    exit(exit_code)


if __name__ == '__main__':
    main()
