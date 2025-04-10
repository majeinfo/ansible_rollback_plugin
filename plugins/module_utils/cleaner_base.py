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
                'seconds': 30,
            }
        }

    # Convert AnsibleUnsafeText into a real str (needed for the YAML dumper)
    def _to_text(self, value):
        return super(type(value), value).__str__()


# Decorator for unsupported module - returns a commented action
def not_supported(func):
    def _not_supported(self, module_name, result):
        display.warning(f"Module {module_name} not yet implemented !")
        return [self._commented_action(module_name, result)]

    return _not_supported

# EOF
