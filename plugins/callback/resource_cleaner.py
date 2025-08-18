# Only for Python3
'''
A rollback playbook SHOULD NOT create another rollback playbook because it SHOULD NOT create any resources !
'''

__metaclass__ = type

DOCUMENTATION = '''
    author: J.Delamarche
    name: resource_cleaner
    type: notification
    requirements:
      - whitelist in configuration
    short_description: Intercepts Cloud resources creation
    description:
        - This is an ansible callback plugin that registers Cloud resources creation and generates a playbook to destroy them
    options:
      playbook_output_path:
        required: False
        default: .
        description: directory where playbooks must be created
        env:
          - name: RESOURCE_CLEANER_OUTPUT_PATH
        ini:
          - section: resource_cleaner
            key: playbook_output_path
      rollback_playbook_suffix:
        required: False
        default: date
        description: suffix added to the rollback playbook
        env:
          - name: ROLLBACK_PLAYBOOK_SUFFIX
        ini:
          - section: resource_cleaner
            key: rollback_playbook_suffix
      hide_sensitive_data:
        required: False
        default: false
        description: if True, replaces sensitive data by stub variables (not yet implemented)
        env:
          - name: HIDE_SENSITIVE_DATA
        ini:
          - section: resource_cleaner
            key: hide_sensitive_data
      force_ignore_errors:
        required: false
        default: true
        description: if True, adds the "ignore_errors" directive in the playbook preamble
        env:
          - name: FORCE_IGNORE_ERRORS
        ini:
          - section: resource_cleaner
            key: force_ignore_errors
'''

import sys
from datetime import datetime
from ruamel.yaml import YAML, CommentedMap, CommentedSeq
import os
import os.path
import pprint

from ansible.module_utils.common.text.converters import to_text
from ansible.plugins.callback import CallbackBase

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')
)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Here, add other Cleaner (in the future)
from plugins.module_utils.amz_aws_cleaner import AmazonAWSCleaner
from plugins.module_utils.com_aws_cleaner import CommunityAWSCleaner
from plugins.module_utils.gcp_cleaner import GCPCleaner


# Parameters and their default values
PLAYBOOK_OUTPUT_PATH = '.'
ROLLBACK_PLAYBOOK_SUFFIX = 'date'
HIDE_SENSITIVE_DATA = False
FORCE_IGNORE_ERRORS = True


class CallbackModule(CallbackBase):
    """
    This is an ansible callback plugin that registers resource creation.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'resource_cleaner'
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self, display=None):
        super().__init__(display=display)
        self.disabled = False   # True if rollback playbook cannot be generated
        self.playbook_output_path = PLAYBOOK_OUTPUT_PATH
        self.rollback_playbook_suffix = ROLLBACK_PLAYBOOK_SUFFIX
        self.playbook_full_name = None  # fullname
        self.playbook_name =  None      # basename
        self.play = None                # current play
        self.actions = []               # recorded actions for a Play
        self.hide_sensitive_data = HIDE_SENSITIVE_DATA
        self.force_ignore_errors = FORCE_IGNORE_ERRORS

        # List of handled Cloud providers
        self.providers = {
            'amazon.aws': AmazonAWSCleaner(self),
            'community.aws': CommunityAWSCleaner(self),
            'google.cloud': GCPCleaner(self),
        }

    def set_options(self, task_keys=None, var_options=None, direct=None):
        '''
        First callback to be called
        '''
        super().set_options(task_keys=task_keys, var_options=var_options, direct=direct)

        self._debug("set_options called")
        self.playbook_output_path = self.get_option('playbook_output_path')
        self.rollback_playbook_suffix = self.get_option('rollback_playbook_suffix')
        self.hide_sensitive_date = self.get_option('hide_sensitive_data')
        self.force_ignore_errors = self.get_option('force_ignore_errors') in ("True", "true", "yes", "Yes")

        # Create the output_path if necessary
        if not os.path.exists(self.playbook_output_path):
            try:
                os.mkdir(self.playbook_output_path)
            except Exception as e:
                self._display.warning(f'Cannot create the directory given by playbook_output_path parameter: {self.playbook_output_path}.')
                self._display.warning(e)
                self.disabled = True
        elif not os.path.isdir(self.playbook_output_path):
            self._display.warning(f'The path given by playbook_output_path parameter is not a directory: {self.playbook_output_path}.')
            self.disabled = True

    # Now the playbook starts !
    def v2_playbook_on_start(self, playbook):
        self._debug("v2_playbook_on_start")
        super().v2_playbook_on_start(playbook)
        self.playbook_fullname = playbook._file_name
        self.playbook_name = os.path.basename(playbook._file_name)

    # Each Play of the Playbook starts now
    def v2_playbook_on_play_start(self, play):
        self._debug("v2_playbook_on_play_start")
        super().v2_playbook_on_play_start(play)
        self._debug(play)
        self.play = play
        self.actions = []

        # disable the rollback feature in check mode
        if hasattr(play, 'check_mode') and play.check_mode:
            self._info("Rollback plugin running in CHECK MODE")
            self.disabled = True

    # A task is started now
    def v2_playbook_on_task_start(self, task, is_conditional, handler=False):
        self._debug("v2_playbook_on_start_task")
        super().v2_playbook_on_task_start(task, is_conditional)

    # A task is executed by a runner
    def v2_runner_on_start(self, host, task):
        # v2_runner_on_start was added in 2.8 so this doesn't get run for Ansible 2.7 and below.
        self._debug("v2_runner_on_start")
        super().v2_runner_on_start(host, task)

    # The runner succeeded
    def v2_runner_on_ok(self, result):
        self._debug("v2_runner_on_ok")
        self._debug(pprint.pformat(result))
        super().v2_runner_on_ok(result)

        self._debug(f"is_changed={result.is_changed()}, "
                          f"is_failed={result.is_failed()}, "
                          f"is_skipped={result.is_skipped()}, "
                          f"is_unreachable={result.is_unreachable()}, "
                          f"task_name={result.task_name}")

        # Actions executed in a loop are handled by v2_runner_item_on_ok
        if result._task.loop:
            return

        if not self.disabled: # Error or check mode
            self._handle_action(result)

    # The runner succeeded to apply an item in a loop
    def v2_runner_item_on_ok(self, result):
        self._debug("v2_runner_item_on_ok")
        self._debug(pprint.pformat(result))
        super().v2_runner_item_on_ok(result)
        self._handle_action(result)

    # handle an Action
    def _handle_action(self, result):
        # If nothing changed, there is nothing to rollback
        if not result._result.get('changed', False):
            return

        # AnsibleUnicode to str otherwise the YAML dump will fail...
        action_name = str(result._task_fields.get('action'))
        for key, cleaner in self.providers.items():
            # Look for a Provider (AWS, GCP, ...)
            if action_name.startswith(key):
                provider = self.providers[key]
                try:
                    if (actions := provider.handle_action(action_name, result)) is not None:
                        # Convert types
                        converted_actions = []
                        for action in actions:
                            converted_action = self._to_builtin_types(action)
                            converted_actions.append(converted_action)

                        self._insert_actions(converted_actions, result, action_name)
                except Exception as e:
                    self._info(f"Action {action_name} has generated an Exception {e}")
            
                break
     
    def _insert_actions(self, actions, result, module_name):
        '''
        actions: list of Playbook actions (usually a single action)
        '''
        self._debug("_insert_action")
        self._debug(actions)
        task_name = result._task_fields.get('name')

        # create a new dict to make sure the 'name' key will be the first one at dump time
        final_action_name = {
            'name': "(UNDO) " + str(task_name) if task_name else "empty",
        }
        assert type(actions) == list

        # if the handler has generated many actions, we must reverse them
        for act in reversed(actions):
            self.actions.insert(0, final_action_name | act)

    # The runner failed
    def v2_runner_on_failed(self, result, ignore_errors=False):
        self._debug("v2_runner_on_failed")
        super().v2_runner_on_failed(result, ignore_errors)

    # The runner could not reach the remote host
    def v2_runner_on_unreachable(self, result):
        self._debug("v2_runner_on_unreachable")
        super().v2_runner_on_unreachable(result)

    # The task has been skipped
    def v2_runner_on_skipped(self, result):
        self._debug("v2_runner_on_skipped")
        super().v2_runner_on_skipped(result)

    # A Handler has been called and must be started
    def v2_playbook_on_handler_task_start(self, task):
        self._debug("v2_playbook_on_handler_task_start")
        super().v2_playbook_on_handler_task_start(task)

    # This is the final call
    def v2_playbook_on_stats(self, stats):
        '''
        The Playbook has ended, we generate the Rollback Playbook
        if this Plugin has been initialized without any error.
        '''
        self._debug("v2_playbook_on_stats")
        super().v2_playbook_on_stats(stats)
        if self.disabled:
            return

        hosts = sorted(stats.processed.keys())
        self.rollback_playbook()

    # Generate the rollback playbook
    def rollback_playbook(self):
        INDENTATION = 2

        # Do not generate empty playbook
        if not len(self.actions):
            return 

        commented_maps = CommentedSeq()
        playbook = CommentedSeq([
            CommentedMap({
                'name': str(self.play.name),
                'hosts': str(self.play.hosts[0]),
                'connection': str(self.play.connection),
                'gather_facts': self.play.gather_facts,
                'ignore_errors': self.force_ignore_errors,
                'tasks': commented_maps,
            })
        ])

        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        playbook.yaml_set_start_comment(f'Rollback playbook for playbook {self.playbook_name}\nGenerated date and time: {now_str}\n\n')

        # Turn actions list into a CommentedMap list
        # Commented actions may follow each other, we must buffer them otherwise
        # only the last one will remain !
        play = playbook[0]
        current_comment = ''

        for action in self.actions:
            if '_is_comment_' in action:
                current_comment += f"\nname: {action['name']}\n{action['message']}\n\n"
            else:
                commented_maps.append(CommentedMap(action))
                if current_comment:
                    if number := len(commented_maps):
                        #play.get('tasks').yaml_set_comment_before_after_key(key=number-1, after=current_comment, indent=INDENTATION)
                        play['tasks'][number - 1].yaml_set_start_comment(current_comment, indent=INDENTATION)
                    else:
                        play.yaml_set_comment_before_after_key(key='tasks', after=current_comment, indent=INDENTATION)
                    current_comment = ''

        if current_comment:
            if number := len(commented_maps):
                play.get('tasks').yaml_set_comment_before_after_key(key=number-1, after=current_comment, indent=INDENTATION)
            else:
                play.yaml_set_comment_before_after_key(key='tasks', after=current_comment, indent=INDENTATION)

        # Compute the rollback playbook name
        suffix = now.strftime("%Y-%m-%d-%H-%M-%S")
        if self.rollback_playbook_suffix == 'rollback':
            suffix = "rollback"

        yaml = YAML()
        with open(os.path.join(self.playbook_output_path, self.playbook_name + "." + suffix), 'w') as f:
            #yaml.dump(playbook, f, Dumper=IndentDumper, sort_keys=False)
            yaml.dump(playbook, f)

    # Convert AnsibleUnsafeText into a real str (needed for the YAML dumper)
    # def _to_text(self, value):
    #     return super(type(value), value).__str__()

    # Convert any Ansible struct into a standard Python struct
    # to make the yaml.dump() possible
    def _to_builtin_types(self, obj):
        if type(obj) == str:
            return obj
        elif isinstance(obj, dict):
            return {self._to_builtin_types(k): self._to_builtin_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._to_builtin_types(i) for i in obj]
        elif isinstance(obj, tuple):
            return tuple(self._to_builtin_types(i) for i in obj)
        elif isinstance(obj, set):
            return {self._to_builtin_types(i) for i in obj}
        elif isinstance(obj, (int, float, bool, type(None))):
            return obj
        else:
            # Force fallback to string if unknown type (e.g., Ansible internal objects)
            return super(type(obj), obj).__str__()

    # Display message if display mode and verbosity is sufficient
    def _info(self, msg):
        if self._display.display:
            self._display.display("[Cleaner Callback] " + str(msg))

    # Display message if verbosity is sufficient
    def _debug(self, msg):
        if self._display.verbosity >= 1:
            self._info(msg)


# class IndentDumper(yaml.Dumper):
#     def increase_indent(self, flow=False, indentless=False):
#         return super().increase_indent(flow, False)

# EOF
