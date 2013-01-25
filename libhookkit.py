import json
from subprocess import Popen, PIPE
import sys
import os

DEFAULT_CONFIG_FILE_PATH = (os.path.dirname(os.path.abspath(__file__)) +
                            '/hookkit_config.json')


class LibHookKit:

    @staticmethod
    def run_git_command(args):
        p = Popen(['git'] + args, stdout=PIPE, stderr=PIPE)
        [result, error] = p.communicate()
        if p.returncode != 0:
            print >> sys.stderr, 'Error running: git ' + ' '.join(args) + error
            return False

        return result

    @staticmethod
    def get_sha1_list_between_commits(old_sha1, new_sha1):

        if old_sha1 == new_sha1:
            return [new_sha1]

        sha1s = LibHookKit.run_git_command(['log', '--pretty=format:%H',
                                            '--no-merges',
                                            old_sha1 + '..' + new_sha1])
        if sha1s == '':
            return None
        else:
            return sha1s.split('\n')

    @staticmethod
    def get_commit_author_email(sha1):
        return LibHookKit.run_git_command(['log', '-1',
                                           '--pretty=format:%ae', sha1])

    @staticmethod
    def get_commit_message(sha1):
        return LibHookKit.run_git_command(['log', '-1',
                                           '--pretty=format:%s\n%b\n%N', sha1])

    @staticmethod
    def get_files_affected_between_two_commits(old_sha1, new_sha1):
        files_affected = LibHookKit.run_git_command(['diff', '--name-only',
                                                     old_sha1, new_sha1])
        return files_affected.split('\n')

    @staticmethod
    def extract_file_at_sha1_to_path(file_name, sha1, path):
        p = Popen(['git', 'archive', sha1, file_name],
                  stderr=PIPE, stdout=PIPE)

        p2 = Popen(['tar', 'x'], cwd=path, stdin=p.stdout,
                   stderr=PIPE, stdout=PIPE)

        [output, error] = p2.communicate()

        if p2.returncode != 0:
            sys.stderr.write(('Error while trying to extract the file:' +
                              file_name + ' from sha1:' + sha1 + ' to path:' +
                              path + ':\n' + error + '\n'))
            return False

        return True


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
                dynamic_script_module = __import__('hook-scripts.' + script,
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

# Must be re-implemented by hook-scripts - this is what will be called!
    def run(self):
        print "!! You need to implement run() for" + self.file_name
        return False

# May be implemented by hook scripts to set up special system settings
# or to check dependcies.
    def setup(self):
        return True


class HookScriptLegacy(HookScript):

    def run(self, old_sha1, new_sha1, ref):
        p = Popen(([sys.executable, 'hook-scripts/' + self.file_name] +
                  self.args.split(' ')), stdin=PIPE, stdout=PIPE, stderr=PIPE)

        [output, error] = p.communicate(old_sha1 + ' ' + new_sha1 + ' ' + ref)
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
