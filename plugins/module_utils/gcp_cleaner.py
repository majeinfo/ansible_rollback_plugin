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
        return self._simple_name_rollback(module_name, result)

    @gcp_check_state_present
    def _gcp_compute_autoscaler(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        zone = module_args.get('zone')
        target = module_args.get('target')
        self_link = target.get('selfLink')
        autoscaling_policy = module_args.get('autoscaling_policy')
        self.callback._debug(f"GCP Compute Autoscaler {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'zone': self._to_text(zone),
                'target': { 'selfLink': self._to_text(self_link) }, # why so ?
                'autoscaling_policy': { 'max_num_replicas': 0 }    # autoscaling_policy, # why so ?
            }
        }

    @gcp_check_state_present
    def _gcp_compute_backend_bucket(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        bucket_name = module_args.get('bucket_name')
        self.callback._debug(f"GCP Compute Backend Bucket {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'bucket_name': self._to_text(bucket_name),
            }
        }

    @gcp_check_state_present
    def _gcp_compute_backend_service(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

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

    @gcp_check_state_present
    def _gcp_compute_firewall(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @not_supported
    def _gcp_compute_forwarding_rule(self, module_name, result):
        pass

    @gcp_check_state_present
    def _gcp_compute_global_address(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @not_supported
    def _gcp_compute_global_forwarding_rule(self, module_name, result):
        pass

    @gcp_check_state_present
    def _gcp_compute_health_check(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @gcp_check_state_present
    def _gcp_compute_http_health_check(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @gcp_check_state_present
    def _gcp_compute_https_health_check(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @not_supported
    def _gcp_compute_image(self, module_name, result):
        pass

    @gcp_check_state_present
    def _gcp_compute_instance(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        zone = module_args.get('zone')

        # nothing to rollback if this is not a real instance creation, just a modification:
        if not module_args.get('disks') and not module_args.get('network_interfaces'):
            return None

        deletion_protection = module_args.get('deletion_protection')
        self.callback._debug(f"GCP Compute Instance {name}")

        actions = [{
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'zone': self._to_text(zone),
            }
        }]

        if deletion_protection:
            protect_off = {
                module_name: {
                    'state': 'present',
                    'name': self._to_text(name),
                    'zone': self._to_text(zone),
                    'deletion_protection': False,
                }
            }
            actions.insert(0, protect_off)

        # Add some time to avoid locking
        actions.append(self._add_pause())

        return actions


    @gcp_check_state_present
    def _gcp_compute_instance_group(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        zone = module_args.get('zone')
        self.callback._debug(f"GCP Compute Instance Group {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'zone': self._to_text(zone),
            }
        }

    @gcp_check_state_present
    def _gcp_compute_instance_group_manager(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        zone = module_args.get('zone')
        base_instance_name = module_args.get('base_instance_name')
        instance_template = module_args.get('instance_template')
        self_link = instance_template.get('selfLink')
        self.callback._debug(f"GCP Compute Instance Group Manager {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'zone': self._to_text(zone),
                'base_instance_name': self._to_text(base_instance_name),
                'instance_template': { 'selfLink': self._to_text(self_link) },
            }
        }

    @gcp_check_state_present
    def _gcp_compute_instance_template(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @not_supported
    def _gcp_compute_interconnect_attachment(self, module_name, result):
        pass

    @gcp_check_state_present
    def _gcp_compute_network(self, module_name, result):
        # If subnets have been create automatically, they are also deleted
        # by the Ansible module
        return self._simple_name_rollback(module_name, result)

    @not_supported
    def _gcp_compute_network_endpoint_group(self, module_name, result):
        pass

    @gcp_check_state_present
    def _gcp_compute_node_group(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        zone = module_args.get('zone')
        node_template = module_args.get('node_template')
        self_link = node_template.get('selfLink')
        size = module_args.get('size')
        self.callback._debug(f"{module_name}: {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'zone': self._to_text(zone),
                'node_template': { 'selfLink': self._to_text(self_link) },
                'size': self._to_text(size),
            }
        }

    @gcp_check_state_present
    def _gcp_compute_node_template(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @gcp_check_state_present
    def _gcp_compute_region_autoscaler(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        region = module_args.get('region')
        target = module_args.get('target')
        #autoscaling_policy = module_args.get('autoscaling_policy')
        self.callback._debug(f"GCP Compute Region Autoscaler {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'region': self._to_text(region),
                'target': self._to_text(target),
                'autoscaling_policy': { 'max_num_replicas': 0 }    # autoscaling_policy, # why so ?
            }
        }

    @gcp_check_state_present
    def _gcp_compute_region_backend_service(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        region = module_args.get('region')
        self.callback._debug(f"GCP Compute Region Backend Service {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'region': self._to_text(region),
            }
        }

    @gcp_check_state_present
    def _gcp_compute_region_disk(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        region = module_args.get('region')
        replica_zones = module_args.get('replica_zones')
        self.callback._debug(f"GCP Compute Region Disk {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'region': self._to_text(region),
                'replica_zones': [self._to_text(rz) for rz in replica_zones],
            }
        }

    @gcp_check_state_present
    def _gcp_compute_region_health_check(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @gcp_check_state_present
    def _gcp_compute_region_instance_group_manager(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        region = module_args.get('region')
        base_instance_name = module_args.get('base_instance_name')
        instance_template = module_args.get('instance_template')
        self_link = instance_template.get('selfLink')
        self.callback._debug(f"GCP Compute Region Instance Group Manager {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'region': self._to_text(region),
                'base_instance_name': self._to_text(base_instance_name),
                'instance_template': { 'selfLink': self._to_text(self_link) },
            }
        }

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

    @gcp_check_state_present
    def _gcp_compute_route(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        dest_range = module_args.get('dest_range')
        network = module_args.get('network')
        self_link = network.get('selfLink')
        self.callback._debug(f"GCP Compute Route {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'dest_range': self._to_text(dest_range),
                'network': { 'selfLink': self._to_text(self_link) },
            }
        }

    @gcp_check_state_present
    def _gcp_compute_router(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        region = module_args.get('region')
        network = module_args.get('network')
        self_link = network.get('selfLink')
        self.callback._debug(f"GCP Compute Router {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'region': self._to_text(region),
                'network': { 'selfLink': self._to_text(self_link) },
            }
        }

    @not_supported
    def _gcp_compute_snapshot(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_ssl_certificate(self, module_name, result):
        pass

    @not_supported
    def _gcp_compute_ssl_policy(self, module_name, result):
        pass

    @gcp_check_state_present
    def _gcp_compute_subnetwork(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        ip_cidr_range = module_args.get('ip_cidr_range')
        network = module_args.get('network')
        self_link = network.get('selfLink')
        self.callback._debug(f"GCP Compute Subnetwetwork {name}")

        # If subnets have been create automatically, they are also deleted
        # by the Ansible module

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'ip_cidr_range': self._to_text(ip_cidr_range),
                'network': { 'selfLink': self._to_text(self_link) },
            }
        }

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

    @gcp_check_state_present
    def _gcp_iam_role(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @gcp_check_state_present
    def _gcp_iam_service_account(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        #project = module_args.get('project')
        name = result._result.get('name')
        self.callback._debug(f"GCP IAM Service Account Key {name}")
        #full_name = f"{name}@{project}.iam.gserviceaccount.com"

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
            }
        }

    @gcp_check_state_present
    def _gcp_iam_service_account_key(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        path = module_args.get('path')
        #service_account = result._result.get('serviceAccount')
        name = result._result.get('name')
        self.callback._debug(f"GCP IAM Service Account Key {name}")

        return {
            module_name: {
                'state': 'absent',
                #'service_account': service_account,
                'path': self._to_text(path),
            }
        }

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

    @gcp_check_state_present
    def _gcp_storage_bucket(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

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

    # Simple rollback base on object name only
    def _simple_name_rollback(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        self.callback._debug(f"{module_name}: {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
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
