import json
from subprocess import Popen, PIPE
import sys
import os
import abc


config_path = "hooks/hookkit_config.json"

# If running in a non-bare repo, then we need to look inside ".git/hooks".
if os.path.isdir('.git'):
    config_path = os.path.join(".git", config_path)

DEFAULT_CONFIG_FILE_PATH = os.path.join(os.getcwd(), config_path)


class LibHookKit:
    """Convenience functions to be used in :ref:`hook-scripts`"""

    @staticmethod
    def run_git_command(args):
        """ Run a git command

        :param args: The arguments to pass to the git executable.
        :type args: list
        :returns:  string or False -- string is the git output in the
                   case of success, False if the command failed.

        """

        proc = Popen(['git'] + args, stdout=PIPE, stderr=PIPE)
        [result, error] = proc.communicate()
        if proc.returncode != 0:
            print >> sys.stderr, 'Error running: git ' + ' '.join(args) + error
            return False

        return result

    @staticmethod
    def get_sha1_list_between_commits(old_sha, new_sha):
        """ Get the SHA-1s of all commits between two commit SHA-1s

        :param old_sha: The earlier SHA-1
        :type old_sha: string
        :param new_sha: The later SHA-1
        :type new_sha: string
        :returns:  list -- all SHA-1s between old_sha and new_sha

        """

        if old_sha == new_sha:
            return [new_sha]

        sha1s = LibHookKit.run_git_command(['log', '--pretty=format:%H',
                                            '--no-merges',
                                            old_sha + '..' + new_sha])
        if sha1s == '':
            return None
        else:
            return sha1s.split('\n')

    @staticmethod
    def get_commit_author_email(sha):
        """ Get the author email field for a commit SHA-1

        :param sha: The commit SHA-1
        :type sha: string
        :returns:  string -- The email address

        """

        return LibHookKit.run_git_command(['log', '-1',
                                           '--pretty=format:%ae', sha])

    @staticmethod
    def get_commit_message(sha):
        """ Get the commit message for a commit SHA-1

        :param sha: The commit SHA-1
        :type sha: string
        :returns:  string -- The commit message

        """
        return LibHookKit.run_git_command(['log', '-1',
                                           '--pretty=format:%s\n%b\n%N', sha])

    @staticmethod
    def get_files_modified_between_two_commits(old_sha, new_sha):
        """ Get files added or modified between two commits. *Omits deletions.*

        :param old_sha: The earlier SHA-1
        :type old_sha: string
        :param new_sha: The later SHA-1
        :type new_sha: string
        :returns:  list -- The files which were modified or added
                   between old_sha and new_sha

        """
        return LibHookKit.get_files_affected_between_two_commits(old_sha,
                                                                 new_sha,
                                                                 "A,M")

    @staticmethod
    def get_files_affected_between_two_commits(old_sha, new_sha, filter=None):
        """ Get files affected between two commits.

        :param old_sha: The earlier SHA-1
        :type old_sha: string
        :param new_sha: The later SHA-1
        :type new_sha: string
        :param filter: The filter for what "affected" should mean.
                       Uses the same syntax as `git --diff-filter
                       <http://git-scm.com/docs/git-diff-tree>`_.
                       In the form of a comma separated list.
        :type filter: string
        :returns:  list -- The files which were modified or added
                   between old_sha and new_sha

        """
        command = ['log', '--pretty=format:', '--name-only',
                   old_sha + ".." + new_sha]

        if filter:
            command.append("--diff-filter=%s" % filter)

        files_raw = LibHookKit.run_git_command(command)

        files = files_raw.split('\n')

        # Need to strip empty elements (new lines)
        return [file for file in files if file]

    @staticmethod
    def extract_git_repo(destination, sha, path=None):
        command = ['git', 'archive', sha]

        if path:
            command.append(path)

        git_proc = Popen(command, stderr=PIPE, stdout=PIPE)

        tar_proc = Popen(['tar', 'x'], cwd=destination, stdin=git_proc.stdout,
                         stderr=PIPE, stdout=PIPE)

        [output, error] = tar_proc.communicate()
        git_proc.communicate()

        if git_proc.returncode != 0 or tar_proc.returncode != 0:
            sys.stderr.write(output)
            sys.stderr.write(error)
            return False

        return True

    @staticmethod
    def extract_file_at_sha1_to_path(file_name, sha, destination):
        """ Extract a file from git

        :param sha: The commit SHA-1 to extract.
        :type sha: string
        :param destination: destination
        :type destination: string
        :param file_name: The file to extract
        :type file_name: string
        :returns:  bool -- True for success, False for failure.

        """
        if not LibHookKit.extract_git_repo(destination, sha, file_name):
            sys.stderr.write('Error while trying to extract the file:' +
                             file_name + ' from sha:' + sha + ' to path:' +
                             destination + '\n')
            return False

        return True

    @staticmethod
    def extract_repo_at_sha1_to_path(sha, destination):
        """ Extract a git repository

        :param sha: The commit SHA-1 to extract.
        :type sha: string
        :param destination: destination
        :type destination: string
        :returns:  bool -- True for success, False for failure.

        """
        if not LibHookKit.extract_git_repo(destination, sha):
            sys.stderr.write('Error while trying to extract the repository ' +
                             'at sha:' + sha + ' to path:' + destination +
                             '\n')
            return False

        return True

    @staticmethod
    def is_exe(path):
        return os.path.isfile(path) and os.access(path, os.X_OK)

    @staticmethod
    def is_program_available(program):
        """ Check if a program is available to be executed

        :param program: The executable to look for
        :type sha: string
        :returns:  bool -- True for success, False for failure.

        """

        # "Program finding" code below is based on a Stackoverflow post by Jay:
        # http://stackoverflow.com/a/377028

        file_path = os.path.split(program)[0]

        if file_path:
            if LibHookKit.is_exe(program):
                return True
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                if LibHookKit.is_exe(exe_file):
                    return True

        return False


class LibHookKitConfiguration:

    def load_json_from_file(self, config_file_path):
        try:
            config_data = open(config_file_path).read()
            return json.loads(config_data)
        except IOError:
            print >> sys.stderr, ('Failed to open "' + config_file_path +
                                  '". Verify that it exists in the same ' +
                                  'directory as this script.')
            return []
        except:
            print >> sys.stderr, ('Failed to parse "' + config_file_path +
                                  '". Refer to the documentation on ' +
                                  'github.com/jesper/hookkit for syntax.')
            return []

    def get_available_hooks(self, config_file_path=DEFAULT_CONFIG_FILE_PATH):
        json_data = self.load_json_from_file(config_file_path)
        if json_data != []:
            return json_data['hooks'].keys()
        else:
            return json_data

    def load_entries_for_hook(self, hook,
                              config_file_path=DEFAULT_CONFIG_FILE_PATH):

        self.entries = []
        json_data = self.load_json_from_file(config_file_path)

        if len(json_data) == 0:
            print >> sys.stderr, ('Hook "' + hook +
                                  '" has not been configured in "' +
                                  config_file_path + '"')
            return self.entries

        if hook not in json_data['hooks']:
            print >> sys.stderr, ('Hook "' + hook +
                                  '" has not been configured in "' +
                                  config_file_path + '"')
            return self.entries

        for entry in json_data['hooks'][hook].keys():
            args = self.args_for_entry_in_hook_from_json(entry, hook,
                                                         json_data)

            freq = self.frequency_for_entry_in_hook_from_json(entry, hook,
                                                              json_data)

            mode = self.mode_for_entry_in_hook_from_json(entry, hook,
                                                         json_data)

            message = self.error_message_for_entry_in_hook_from_json(entry,
                                                                     hook,
                                                                     json_data)

            script = self.script_for_entry_in_hook_from_json(entry, hook,
                                                             json_data)

#FIXME Implement PROPER error handling for when a hook script fails to load (!)
            if mode == HookScriptMode.HOOKKIT:
                dynamic_script_module = __import__('hook_scripts.' + script,
                                                   fromlist=[script])

                dynamic_script_class = getattr(dynamic_script_module, script)
                script_object = dynamic_script_class(script, entry,
                                                     message, args,
                                                     freq, mode)
                self.entries.append(script_object)
            else:
                self.entries.append(HookScriptLegacy(script, entry,
                                                     message, args,
                                                     freq, mode))

        return self.entries

#FIXME: Remove use of "get_" pattern in method names. PEP8 is ruthless.
    def get_attribute_for_entry_in_hook_from_json(self, attribute, entry, hook,
                                                  json):
        if hook not in json['hooks']:
            return False

        if entry not in json['hooks'][hook]:
            return False

        if attribute not in json['hooks'][hook][entry]:
            return False

        return json['hooks'][hook][entry][attribute]

    def args_for_entry_in_hook_from_json(self, entry, hook, json):
        return self.get_attribute_for_entry_in_hook_from_json('args', entry,
                                                              hook, json)

    def error_message_for_entry_in_hook_from_json(self, entry, hook, json):
        return self.get_attribute_for_entry_in_hook_from_json('error_message',
                                                              entry,
                                                              hook,
                                                              json)

    def script_for_entry_in_hook_from_json(self, entry, hook, json):
        return self.get_attribute_for_entry_in_hook_from_json('script', entry,
                                                              hook, json)

    def mode_for_entry_in_hook_from_json(self, entry, hook, json):
        mode = self.get_attribute_for_entry_in_hook_from_json('mode', entry,
                                                              hook, json)

        if mode == 'hookkit':
            return HookScriptMode.HOOKKIT
        else:
            return HookScriptMode.LEGACY

    def frequency_for_entry_in_hook_from_json(self, entry, hook, json):
        frequency = self.get_attribute_for_entry_in_hook_from_json('frequency',
                                                                   entry,
                                                                   hook,
                                                                   json)

        if frequency == 'each_commit':
            return HookScriptFrequency.EACH_COMMIT
        else:
            return HookScriptFrequency.LAST_COMMIT


class HookScript(object):
    def __init__(self, file_name, label, error_message, args, frequency, mode):
        self.file_name = file_name
        self.args = args
        self.frequency = frequency
        self.mode = mode
        self.error_message = error_message
        self.label = label

# Must be re-implemented by hook_scripts - this is what will be called!
    @abc.abstractmethod
    def run(self):
        print "!! You need to implement run() for" + self.file_name
        return False

# May be implemented by hook scripts to set up special system settings
# or to check dependcies.
    def setup(self):
        return True


class HookScriptLegacy(HookScript):

    def run(self, old_sha, new_sha, ref):
        p = Popen((['hook_scripts/' + self.file_name] +
                  self.args.split(' ')), stdin=PIPE, stdout=PIPE, stderr=PIPE)

        [output, error] = p.communicate(old_sha + ' ' + new_sha + ' ' + ref)
        return_code = p.returncode

        if return_code == 0:
            return True
        else:
            print "Return code:" + return_code
            print "Error:" + error
            return False


class HookScriptFrequency():
#TBD: Add hooks for BRANCH_DELETE, BRANCH_CREATE
    LAST_COMMIT = 0
    EACH_COMMIT = 1


class HookScriptMode():
    HOOKKIT = 0
    LEGACY = 1
