# Driver for GCP Resources

import sys
from .cleaner_base import CleanerBase, not_supported


def gcp_check_state_present(func):
    '''
    Decorator that ensures the resource is created.
    There is no rollback to do if the resource is not created !
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

    @not_supported
    def _gcp_appengine_firewall_rule(self, module_name, result):
        pass

    @not_supported
    def _gcp_bigquery_dataset(self, module_name, result):
        pass

    @not_supported
    def _gcp_bigquery_table(self, module_name, result):
        pass

    @not_supported
    def _gcp_bigtable_instance(self, module_name, result):
        pass

    @not_supported
    def _gcp_cloudbuild_trigger(self, module_name, result):
        pass

    @not_supported
    def _gcp_cloudfunctions_cloud_function(self, module_name, result):
        pass

    @not_supported
    def _gcp_cloudscheduler_job(self, module_name, result):
        pass

    @not_supported
    def _gcp_cloudtasks_queue(self, module_name, result):
        pass

    @gcp_check_state_present
    def _gcp_compute_address(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        self.callback._debug(f"GCP Compute Address {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
            }
        }

    @not_supported
    def _gcp_compute_autoscaler(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_backend_bucket(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_backend_service(self, module_name, result):
        pass

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

    @not_supported
    def _gcp_compute_external_vpn_gateway(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_firewall(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_forwarding_rule(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_global_address(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_global_forwarding_rule(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_health_check(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_http_health_check(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_https_health_check(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_image(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_instance(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_instance_group(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_instance_group_manager(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_instance_template(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_interconnect_attachment(self, module_name, result):
        pass

    @gcp_check_state_present
    def _gcp_compute_network(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        #auto_create_subnets = module_args.get('auto_create_subnets')
        self.callback._debug(f"GCP Compute Network {name}")

        # If subnets have been create automatically, they are also deleted
        # by the Ansible module

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
            }
        }

    @not_supported
    def _gcp_compute_network(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_network_endpoint_group(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_node_group(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_node_template(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_region_autoscaler(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_region_backend_service(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_region_disk(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_region_health_check(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_region_health_check_info(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_region_instance_group_manager(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_region_target_http_proxy(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_region_target_https_proxy(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_region_url_map(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_reservation(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_resource_policy(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_route(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_router(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_snapshot(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_ssl_certificate(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_ssl_policy(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_subnetwork(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_target_http_proxy(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_target_https_proxy(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_target_instance(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_target_pool(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_target_pool_info(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_target_ssl_proxy(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_target_tcp_proxy(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_target_vpn_gateway(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_url_map(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_vpn_tunnel(self, module_name, result):
        pass

    @not_supported
    def _gcp_container_cluster(self, module_name, result):
        pass

    @not_supported
    def _gcp_container_node_pool(self, module_name, result):
        pass

    @not_supported
    def _gcp_dns_managed_zone(self, module_name, result):
        pass

    @not_supported
    def _gcp_dns_resource_record_set(self, module_name, result):
        pass

    @not_supported
    def _gcp_filestore_instance(self, module_name, result):
        pass

    @not_supported
    def _gcp_iam_role(self, module_name, result):
        pass

    @not_supported
    def _gcp_iam_service_account(self, module_name, result):
        pass

    @not_supported
    def _gcp_iam_service_account_key(self, module_name, result):
        pass

    @not_supported
    def _gcp_kms_crypto_key(self, module_name, result):
        pass

    @not_supported
    def _gcp_kms_key_ring(self, module_name, result):
        pass

    @not_supported
    def _gcp_logging_metric(self, module_name, result):
        pass

    @not_supported
    def _gcp_mlengine_model(self, module_name, result):
        pass

    @not_supported
    def _gcp_mlengine_version(self, module_name, result):
        pass

    @not_supported
    def _gcp_pubsub_subscription(self, module_name, result):
        pass

    @not_supported
    def _gcp_pubsub_topic(self, module_name, result):
        pass

    @not_supported
    def _gcp_redis_instance(self, module_name, result):
        pass

    @not_supported
    def _gcp_resourcemanager_project(self, module_name, result):
        pass

    @not_supported
    def _gcp_runtimeconfig_config(self, module_name, result):
        pass

    @not_supported
    def _gcp_runtimeconfig_variable(self, module_name, result):
        pass

    @not_supported
    def _gcp_secret_manager(self, module_name, result):
        pass

    @not_supported
    def _gcp_serviceusage_service(self, module_name, result):      
        pass

    @not_supported
    def _gcp_sourcerepo_repository(self, module_name, result):                                 
        pass

    @not_supported
    def _gcp_spanner_database(self, module_name, result):
        pass

    @not_supported
    def _gcp_spanner_instance(self, module_name, result):
        pass

    @not_supported
    def _gcp_sql_database(self, module_name, result):
        pass

    @not_supported
    def _gcp_sql_instance(self, module_name, result):
        pass

    @not_supported
    def _gcp_sql_ssl_cert(self, module_name, result):
        pass

    @not_supported
    def _gcp_sql_user(self, module_name, result):
        pass

    @not_supported
    def _gcp_storage_bucket(self, module_name, result):
        pass

    @not_supported
    def _gcp_storage_bucket_access_control(self, module_name, result):
        pass

    @not_supported
    def _gcp_storage_default_object_acl(self, module_name, result):
        pass

    @not_supported
    def _gcp_storage_object(self, module_name, result):
        pass

    @not_supported
    def _gcp_tpu_node(self, module_name, result):
        pass

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
