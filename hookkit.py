#!/usr/bin/env python

import os
import sys

# Needed to pick up the right libhookkit when soft-linked
sys.path.insert(0, os.path.dirname(__file__))

import libhookkit
from libhookkit import Hookkit

scripts_to_run_each_commit = []
scripts_to_run_on_last_commit = []


def exit_with_error_message(message):
    print message
    exit(1)


def get_active_hook():
    return os.path.basename(__file__)


def load_scripts():
    active_hook = get_active_hook()

    config = libhookkit.HookkitConfiguration()
    scripts_to_execute = config.load_entries_for_hook(active_hook)

    if len(scripts_to_execute) == 0:
        print "Unable to load any scripts, aborting."
        return False

    for script in scripts_to_execute:

        if not script.setup():
            print "Failed to setup hook-script: " + script.file_name
            return False

        if script.frequency == libhookkit.HookScriptFrequency.EACH_COMMIT:
            scripts_to_run_each_commit.append(script)
        else:
            scripts_to_run_on_last_commit.append(script)

    return True


def trigger_scripts(old_sha1, new_sha1, ref):
# Delete branch
    if new_sha1 == '0000000000000000000000000000000000000000':
        return

# New branch
    if old_sha1 == '0000000000000000000000000000000000000000':
# FIXME: This feels really wrong, but I'm not sure what I should do instead.
#        I'll do this for now, until I can think of something better.
#        (or it starts causing problems)
        old_sha1 = Hookkit.run_git_command(['merge-base', new_sha1, 'master'])
        old_sha1 = old_sha1.rstrip()

    failed = False

    script_names = []
    for script in scripts_to_run_each_commit:
        script_names.append(script.label)

    for script in scripts_to_run_on_last_commit:
        script_names.append(script.label)

    script_names = ', '.join(script_names)

    print '* Checks: ' + script_names + '\n'

    for sha1 in Hookkit.get_sha1_list_between_commits(old_sha1, new_sha1):
        for script in scripts_to_run_each_commit:
            if not script.run(sha1):
                print '\t!!! Fail: ' + sha1 + ' - ' + script.error_message
                failed = True

#should pass in a dict of args
#FIXME: This really needs tests!
    for script in scripts_to_run_on_last_commit:
        if not script.run(old_sha1, new_sha1, ref):
            print '!!! Fail: ' + script.error_message
            failed = True

    if failed:
        exit_with_error_message('\n!!! PUSH ABORTED !!!\n')


def main():

    print '\n*   Hook: ' + get_active_hook()

    if not load_scripts():
        exit_with_error_message('\n!!! ABORTED !!!\n')

    if get_active_hook() == 'update':
        trigger_scripts(sys.argv[2], sys.argv[3], sys.argv[1])
    else:
        for line in sys.stdin.xreadlines():
            arg_array = line.strip().split(' ')
            trigger_scripts(arg_array[0], arg_array[1], arg_array[2])


if __name__ == "__main__":
    main()
