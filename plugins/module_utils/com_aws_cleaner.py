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

    @check_state_present
    def _api_gateway(self, module_name, result):
        # if lookup == tags: use tags or name, if no tags=> create a new api => api_id in result
        # if lookup == id: use api_id
        module_args = result._result.get('invocation').get('module_args')
        lookup = module_args.get('lookup')
        if lookup != 'tag':
            return None

        api_id = result._result.get('api_id')

        return {
            module_name: {
                'state': 'absent',
                'lookup': 'id',
                'api_id': api_id,
            }
        }

    @check_state_present
    def _autoscaling_launch_config(self, module_name, result):
        # TODO: not tested, only Launch Templates are supported in my account
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _cloudfront_distribution(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        tags = module_args.get('tags')
        caller_ref = result._result.get('caller_reference')

        return {
            module_name: {
                'state': 'absent',
                'caller_reference': caller_ref,
                'tags': tags,
            }
        }

    @check_state_present
    def _cloudfront_origin_access_identity(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        caller_ref = module_args.get('caller_reference')

        return {
            module_name: {
                'state': 'absent',
                'caller_reference': caller_ref,
            }
        }

    @check_state_present
    def _cloudfront_response_headers_policy(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _config_rule(self, module_name, result):
        action = self._simple_name_rollback(module_name, result)
        module_args = result._result.get('invocation').get('module_args')
        action[module_name]['source'] = module_args.get('source')
        return action

    @check_state_present
    def _dynamodb_table(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _efs(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _elasticache(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _elb_network_lb(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        deletion_protection = module_args.get('deletion_protection')
        nlb_name = module_args.get('name')

        actions = [self._simple_name_rollback(module_name, result)]

        # Removing of deletion_protection is not easily supported
        self._warning(f"Removing a NLB with deletion_protection set to True is not supported")
        # if deletion_protection:
        #     protect_off = {
        #         module_name: {
        #             'state': 'present',
        #             'name': nlb_name,
        #             'deletion_protection': False,
        #         }
        #     }
        #     actions.insert(0, protect_off)

        # Add some time to avoid locking
        actions.append(self._add_pause())

        return actions

    @check_state_present
    def _elb_target_group(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _s3_lifecycle(self, module_name, result):
        action = self._simple_name_rollback(module_name, result)
        # status must also be enabled
        module_args = result._result.get('invocation').get('module_args')
        status = module_args.get('status')
        if status != 'enabled':
            return None

        prefix = module_args.get('prefix')
        action[module_name]['prefix'] = prefix
        return action

    @check_state_present
    def _s3_logging(self, module_name, result):
        # TODO: needs S3 ACL support which are deprecated
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _s3_website(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _sns_topic(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _sqs_queue(self, module_name, result):
        action = self._simple_name_rollback(module_name, result)
        module_args = result._result.get('invocation').get('module_args')
        action[module_name]['queue_type'] = module_args.get('queue_type')

        return action

    @check_state_present
    def _waf_condition(self, module_name, result):
        action = self._simple_name_rollback(module_name, result)
        module_args = result._result.get('invocation').get('module_args')
        action[module_name]['type'] = module_args.get('type')
        action[module_name]['waf_regional'] = module_args.get('waf_regional')

        return action

    @check_state_present
    def _waf_rule(self, module_name, result):
        action = self._simple_name_rollback(module_name, result)
        module_args = result._result.get('invocation').get('module_args')
        action[module_name]['waf_regional'] = module_args.get('waf_regional')

        return action

    @check_state_present
    def _waf_web_acl(self, module_name, result):
        action = self._simple_name_rollback(module_name, result)
        module_args = result._result.get('invocation').get('module_args')
        action[module_name]['waf_regional'] = module_args.get('waf_regional')

        return action

    @check_state_present
    def _wafv2_ip_set(self, module_name, result):
        action = self._simple_name_rollback(module_name, result)
        module_args = result._result.get('invocation').get('module_args')
        action[module_name]['scope'] = module_args.get('scope')

        return action

    @check_state_present
    def _wafv2_resources(self, module_name, result):
        action = self._simple_name_rollback(module_name, result)
        module_args = result._result.get('invocation').get('module_args')
        action[module_name]['scope'] = module_args.get('scope')
        action[module_name]['arn'] = module_args.get('arn')

        return action

    @check_state_present
    def _wafv2_rule_group(self, module_name, result):
        # TODO: limited because may add or delete rule from a group
        action = self._simple_name_rollback(module_name, result)
        module_args = result._result.get('invocation').get('module_args')
        action[module_name]['scope'] = module_args.get('scope')

        return action

    @check_state_present
    def _wafv2_web_acl(self, module_name, result):
        action = self._simple_name_rollback(module_name, result)
        module_args = result._result.get('invocation').get('module_args')
        action[module_name]['scope'] = module_args.get('scope')

        return action

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
                        final_action[action_module_name][key] = value

            final_actions.append(final_action)

        return final_actions

# EOF
