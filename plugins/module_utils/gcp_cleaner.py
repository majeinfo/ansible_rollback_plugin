# Driver for GCP Resources

import sys
from .cleaner_base import CleanerBase


def gcp_check_state_present(func):
    '''
    Decorator that ensures the resource is created.
    There is no rollback to do if it is not !
    '''
    def _check_state_present(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        state = module_args.get('state')
        if state != 'present':
            self.callback._debug(f"module {module_name} does not create any new resource")
            return None

        return func(self, module_name, result)

    return _check_state_present

class GCPCleaner(CleanerBase):
    def __init__(self, callback):
        super().__init__(callback)
        callback._debug("GCPCleaner __init__")

    # @abstractmethod
    def get_collection_prefix(self):
        return "google.cloud"

    @gcp_check_state_present
    def _gcp_compute_disk(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        zone = module_args.get('zone')
        self.callback._debug(f"GCP Compute Disk {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'zone': self._to_text(zone),
            }
        }

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
                for key in ('project', 'auth_kind', 'service_account_file', 'region'):
                    if value := module_args.get(key):
                        final_action[action_module_name][key] = self._to_text(value)

            final_actions.append(final_action)

        return final_actions

# EOF
