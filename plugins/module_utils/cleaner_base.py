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
            return None

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


# Decorator for unsupported module
def not_supported(func):
    def _not_supported(self, module_name, result):
        display.warning(f"Module {module_name} not yet implemented !")
        return None

    return _not_supported

# EOF
