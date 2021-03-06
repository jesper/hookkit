from subprocess import Popen, PIPE
import shutil
import sys

repo_server = 'test_server_repo'
repo_checkout = 'test_repo'


#FIXME replace camelcase with snake case - to stay consistent with the rest
def deployHookKit(config_file):
    shutil.copy('data/' + config_file,
                repo_server + '/hooks/hookkit_config.json')

    runCommandInPath(sys.executable + ' ../../../install_hooks.py',
                     repo_server + '/hooks/')


def deployLocalHookKit(config_file):
    shutil.copy('data/' + config_file,
                repo_checkout + '/.git/hooks/hookkit_config.json')

    runCommandInPath(sys.executable + ' ../../../../install_hooks.py',
                     repo_checkout + '/.git/hooks/')


def gitCommitWithMessage(message):
    return runCommandArrayInPath(['git', 'commit', '-a', '-m', message],
                                 repo_checkout)


def gitPush(args=''):
    return runCommandArrayInPath(['git', 'push'] + args.split(), repo_checkout)


def runCommandInPath(command, path):
    return runCommandArrayInPath(command.split(' '), path)


def runCommandArrayInPath(command, path):

    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=path)

    [output, error] = p.communicate()
    return_code = p.returncode

    if return_code == 0:
        return True
    else:
        #print "Error:" + error
        #print "Return code:" + str(return_code)
        #print "Command:" + ' '.join(command)
        #print "Output:" + output
        return False
