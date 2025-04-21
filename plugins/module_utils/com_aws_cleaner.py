# Driver for AWS Resources

import sys
from .cleaner_base import CleanerBase, not_supported, check_state_present


class CommunityAWSCleaner(CleanerBase):
    def __init__(self, callback):
        super().__init__(callback)
        callback._debug("CommunityAWSCleaner __init__")

    # @abstractmethod
    def get_collection_prefix(self):
        return "community.aws"

    # @override
    def _generate_actions(self, actions, module_name, result):
        '''
        Generate the rollback actions
        :param actions: list of actions
        :param module_name: original module name
        :param result: result of original action
        :return: list of actions to render in YAML
        '''
        if type(actions) != list:
            actions = [actions]

        task_name = result._task_fields.get('name')
        module_args = result._result.get('invocation').get('module_args')
        final_actions = []

        for action in actions:
            # create a new dict to make sure the 'name' key will be the first one at dump time
            final_action = {
                'name': "(UNDO) " + str(task_name) if task_name else "empty",
            }
            final_action |= action

            # if the current action is an amazon.aws module, we merge specific keys
            action_module_name = list(action.keys())[0]
            if action_module_name.startswith(self.get_collection_prefix()):
                # TODO: handle secret ! do not write sensitive data
                for key in ('access_key', 'secret_key', 'region', 'aws_config', 'profile', 'session_token'):
                    if value := module_args.get(key):
                        final_action[action_module_name][key] = self._to_text(value)

            final_actions.append(final_action)

        return final_actions

# EOF
