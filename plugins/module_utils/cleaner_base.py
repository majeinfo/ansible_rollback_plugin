'''
Base class for the Cloud cleaners
'''
from abc import ABC, abstractmethod
from ansible.utils.display import Display

display = Display()


class CleanerBase(ABC):
    def __init__(self, callback):
        self.callback = callback
        self.actions = {}               # must be defined in children classes

    # handle an Action
    # return can be None or a list of actions (usually a single one)
    def handle_action(self, action_name, result):
        # get the last part of the module name: add a leading '_'
        # to avoid name collision with Python keywords like "lambda" !
        short_action_name = '_' + action_name[len(self.get_collection_prefix()) + 1:]
        if not hasattr(self, short_action_name):
            display.warning(f"Action {action_name} not supported (yet ?)")
            return [self._commented_action(action_name, result)]

        method = getattr(self, short_action_name)
        actions = method(action_name, result)
        if actions is not None:
            return self._generate_actions(actions, action_name, result)

        return None

    @abstractmethod
    def get_collection_prefix(self):
        pass

    @abstractmethod
    def _generate_actions(self, action, action_name, result):
        pass

    # Generate a commented Action (usually when the rollback cannnot be generated)
    def _commented_action(self, action_name, result):
        task_name = result._task_fields.get('name')
        return {
            'name': str(task_name) if task_name else "empty",
            'message': f"module {action_name} not supported yet",
            '_is_comment_': True,
        }

    # Generate a pause between actions
    def _add_pause(self):
        self.callback._debug('_add_pause')
        return {
            'ansible.builtin.pause': {
                'seconds': '{{ pause_seconds|int }}',
            }
        }

    # Wrap the action into a until/retries loop
    def _wrap_until_retries(self, action):
        action |= {
            #'register': 'result',
            #'until': 'result is not failed',
            'retries': '{{ retry_count|int }}',
            'delay': '{{ retry_delay|int }}',
        }
        return action

    # Generates warning
    def _warning(selfself, *args):
        display.warning(*args)

    # Simple rollback base on object name only
    def _simple_name_rollback(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        self.callback._debug(f"{module_name}: {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': name,
            }
        }


# Decorator for unsupported module - returns a commented action
def not_supported(func):
    def _not_supported(self, module_name, result):
        display.warning(f"Module {module_name} not yet implemented !")
        return [self._commented_action(module_name, result)]

    return _not_supported


def check_state_present(func):
    '''
    Decorator that ensures the resource is created (state: present)
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

# EOF
