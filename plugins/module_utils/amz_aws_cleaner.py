# Driver for AWS Resources

import sys
from .cleaner_base import CleanerBase, not_supported, check_state_present

class AmazonAWSCleaner(CleanerBase):
    def __init__(self, callback):
        super().__init__(callback)
        callback._debug("AmazonAWSCleaner __init__")

    # @abstractmethod
    def get_collection_prefix(self):
        return "amazon.aws"

    @check_state_present
    def _autoscaling_group(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        self.callback._debug(f"created ASG: {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
            }
        }

    @not_supported
    def _autoscaling_instance(self, module_name, result):
        pass

    @check_state_present
    def _backup_plan(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        backup_plan_name = module_args.get('backup_plan_name')
        self.callback._debug(f"created Vault Plan: {backup_plan_name}")

        return {
            module_name: {
                'state': 'absent',
                'backup_plan_name': self._to_text(backup_plan_name),
            }
        }

    @check_state_present
    def _backup_selection(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        backup_plan_name = module_args.get('backup_plan_name')
        backup_selection_name = module_args.get('backup_selection_name')
        self.callback._debug(f"created Backup Selection: {backup_selection_name}")

        return {
            module_name: {
                'state': 'absent',
                'backup_plan_name': self._to_text(backup_plan_name),
                'backup_selection_name': self._to_text(backup_selection_name),
            }
        }

    @not_supported
    def _backup_tag(self, module_name, result):
        pass

    @check_state_present
    def _backup_vault(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        backup_vault_name = module_args.get('backup_vault_name')
        self.callback._debug(f"created Vault: {backup_vault_name}")

        return {
            module_name: {
                'state': 'absent',
                'backup_vault_name': self._to_text(backup_vault_name),
            }
        }

    @not_supported
    def _cloudformation(self, module_name, result):
        pass

    @check_state_present
    def _cloudtrail(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _cloudwatch_metric_alarm(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _cloudwatchevent_rule(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _cloudwatchlogs_log_group(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        log_group_name = module_args.get('log_group_name')
        self.callback._debug(f"created Cloudwatch Log Group: {log_group_name}")

        return {
            module_name: {
                'state': 'absent',
                'log_group_name': self._to_text(log_group_name),
            }
        }

    @check_state_present
    def _ec2_ami(self, module_name, result):
        image_id = result._result.get('image_id')
        self.callback._debug(f"created AMI: {image_id}")

        return {
            module_name: {
                'state': 'absent',
                'image_id': self._to_text(image_id),
            }
        }

    @check_state_present
    def _ec2_eip(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        in_vpc = module_args.get('in_vpc')
        allocation_id = result._result.get('allocation_id')
        public_ip = result._result.get('public_ip')
        self.callback._debug(f"EIP allocation_id {allocation_id}")

        return self._ec2_eip_internal(public_ip, in_vpc)

    def _ec2_eip_internal(self, public_ip, in_vpc):
        # Generate amazon.aws.ec2_eip delete !
        return {
            'amazon.aws.ec2_eip': {
                'state': 'absent',
                'public_ip': self._to_text(public_ip),
                'in_vpc': in_vpc,
                'release_on_disassociation': True,
            }
        }

    @check_state_present
    def _ec2_eni(self, module_name, result):
        interface = result._result.get('interface')
        eni_id = interface.get('id')
        self.callback._debug(f"ENI eni_id {eni_id}")

        return {
            module_name: {
                'state': 'absent',
                'eni_id': self._to_text(eni_id),
            }
        }
  
    @check_state_present
    def _ec2_key(self, module_name, result):
        key = result._result.get('key')
        key_id = key.get('id')
        key_name = key.get('name')
        self.callback._debug(f"Key name {key_name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(key_name),
            }
        }

    # Do not put the @check_state_present !
    def _ec2_instance(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        state = module_args.get('state')
        if state != 'running':
            return None

        termination_protection = module_args.get('termination_protection')
        changed_ids = result._result.get('changed_ids')
        instance_ids = result._result.get('instance_ids')
        self.callback._debug(f"instances created: {instance_ids}, instances changed: {changed_ids}, termination_protection: {termination_protection}")
        if changed_ids is not None:
            instance_ids = changed_ids

        self.callback._debug(f"created instances: {instance_ids}")

        actions = [{
            module_name: {
                'state': 'terminated',
                'instance_ids': [self._to_text(id) for id in instance_ids],
            }
        }]
        
        if termination_protection:
            protect_off = {
                module_name: {
                    'termination_protection': False,
                    'instance_ids': [self._to_text(id) for id in instance_ids],
                }
            }
            actions.insert(0, protect_off)

        # Add some time to avoid locking
        actions.append(self._add_pause())

        return actions

    @check_state_present
    def _ec2_launch_template(self, module_name, result):
        template = result._result.get('template')
        template_name = template.get('launch_template_name')
        self.callback._debug(f"Launch Template {template_name}")

        return {
            module_name: {
                'state': 'absent',
                'template_name': self._to_text(template_name),
            }
        }

    @check_state_present
    def _ec2_placement_group(self, module_name, result):
        placement_group = result._result.get('placement_group')
        name = placement_group.get('name')
        self.callback._debug(f"Placement Group {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
            }
        }

    @check_state_present
    def _ec2_security_group(self, module_name, result):
        group_id = result._result.get('group_id')
        self.callback._debug(f"security_group {group_id}")

        return {
            module_name: {
                'state': 'absent',
                'group_id': self._to_text(group_id),
            }
        }

    @check_state_present
    def _ec2_snapshot(self, module_name, result):
        snapshot_id = result._result.get('snapshot_id')
        self.callback._debug(f"snapshot {snapshot_id}")

        return {
            module_name: {
                'state': 'absent',
                'snapshot_id': self._to_text(snapshot_id),
            }
        }

    @check_state_present
    def _ec2_spot_instance(self, module_name, result):
        spot_request = result._result.get('spot_request')
        spot_instance_request_id = spot_request.get('spot_instance_request_id')
        self.callback._debug(f"spot instance request {spot_instance_request_id}")

        return {
            module_name: {
                'state': 'absent',
                'spot_instance_request_ids': [self._to_text(spot_instance_request_id)],
            }
        }

    @check_state_present
    def _ec2_tag(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        resource = module_args.get('resource')
        tags = module_args.get('tags')
        self.callback._debug(f"Tags on resource {resource}")

        tag_dict = {self._to_text(key): self._to_text(value) for key, value in tags.items()}
        return {
            module_name: {
                'state': 'absent',
                'resource': self._to_text(resource),
                'tags': tag_dict,
            }
        }

    @check_state_present
    def _ec2_transit_gateway(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        description = module_args.get('description')
        self.callback._debug(f"Transit Gateway {description}")

        return {
            module_name: {
                'state': 'absent',
                'description': self._to_text(description),
            }
        }

    @check_state_present
    def _ec2_transit_gateway_vpc_attachment(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _ec2_vol(self, module_name, result):
        volume = result._result.get('volume')
        volume_id = volume.get('id')
        self.callback._debug(f"volume {volume_id}")

        return {
            module_name: {
                'state': 'absent',
                'id': self._to_text(volume_id),
            }
        }

    @check_state_present
    def _ec2_vpc_dhcp_option(self, module_name, result):
        dhcp_options_id = result._result.get('dhcp_options_id')
        self.callback._debug(f"dhcp options {dhcp_options_id}")

        return {
            module_name: {
                'state': 'absent',
                'dhcp_options_id': self._to_text(dhcp_options_id),
            }
        }
    
    @not_supported
    def _ec2_vpc_egress_igw(self, module_name, result):
        pass

    @check_state_present
    def _ec2_vpc_endpoint(self, module_name, result):
        vpc_endpoint_id = result._result.get('result').get('vpc_endpoint_id')
        self.callback._debug(f"vpc endpoint {vpc_endpoint_id}")

        return {
            module_name: {
                'state': 'absent',
                'vpc_endpoint_id': self._to_text(vpc_endpoint_id),
            }
        }
    
    @check_state_present
    def _ec2_vpc_igw(self, module_name, result):
        gateway_id = result._result.get('gateway_id')
        vpc_id = result._result.get('vpc_id')
        self.callback._debug(f"vpc igw {gateway_id}")

        return {
            module_name: {
                'state': 'absent',
                #'gateway_id': self._to_text(gateway_id),
                'vpc_id': self._to_text(vpc_id),
            }
        }
    
    @check_state_present
    def _ec2_vpc_nacl(self, module_name, result):
        nacl_id = result._result.get('nacl_id')
        self.callback._debug(f"vpc nacl {nacl_id}")

        return {
            module_name: {
                'state': 'absent',
                'nacl_id': self._to_text(nacl_id),
            }
        }

    @check_state_present
    def _ec2_vpc_nat_gateway(self, module_name, result):
        '''
        Deleting a NAT GW is more complex: it may be needed
        to delete dynamically allocated EIP ! That's why this
        function returns a list of Ansible Playbook actions
        '''
        actions = []
        nat_gateway_id = result._result.get('nat_gateway_id')
        self.callback._debug(f"nat gateway {nat_gateway_id}")

        # if allocation_id is not se, an EIP will be allocated
        # TODO: not supported
        module_args = result._result.get('invocation').get('module_args')
        allocation_id = module_args.get('allocation_id')
        if not allocation_id:
            nat_gw_addrs = result._result.get('nat_gateway_addresses')
            for eip in nat_gw_addrs:
                allocation_id = eip['allocation_id']
                if 'public_ip' not in eip:
                    self.callback._info(f"public_ip missing for allocated_ip {allocation_id}: this EIP will not be deleted")
                    continue

                public_ip = eip['public_ip']
                action = self._ec2_eip_internal(public_ip, in_vpc=True)
                actions.append(action)

        # Generate amazon.aws.ec2_vpc_nat_gateway delete !
        actions.append({
            module_name: {
                'state': 'absent',
                'nat_gateway_id': self._to_text(nat_gateway_id),
            }
        })

        # Add some time to avoid locking
        actions.append(self._add_pause())

        return actions

    @check_state_present
    def _ec2_vpc_net(self, module_name, result):
        vpc = result._result.get('vpc')
        vpc_id = vpc.get('id')
        self.callback._debug(f"vpc {vpc_id}")

        return {
            module_name: {
                'state': 'absent',
                'vpc_id': self._to_text(vpc_id),
            }
        }

    @check_state_present
    def _ec2_vpc_peering(self, module_name, result):
        peering_id = result._result.get('peering_id')
        self.callback._debug(f"VPC Peering {peering_id}")

        return {
            module_name: {
                'state': 'absent',
                'peering_id': self._to_text(peering_id),
            }
        }

    @check_state_present
    def _ec2_vpc_route_table(self, module_name, result):
        route_table = result._result.get('route_table')
        route_table_id = route_table.get('route_table_id')
        self.callback._debug(f"route table {route_table_id}")

        return {
            module_name: {
                'state': 'absent',
                #'vpc_id': self._to_text(vpc_id),
                'route_table_id': self._to_text(route_table_id),
                'lookup': 'id',
            }
        }

    @check_state_present
    def _ec2_vpc_subnet(self, module_name, result):
        subnet = result._result.get('subnet')
        subnet_id = self._to_text(subnet.get('id'))
        vpc_id = subnet.get('vpc_id')
        cidr_block = subnet.get('cidr_block')
        self.callback._debug(f"subnet {subnet_id}")

        return {
            module_name: {
                'state': 'absent',
                'vpc_id': self._to_text(vpc_id),
                'cidr': self._to_text(cidr_block),
            }
        }

    @not_supported
    def _ec2_vpc_vgw(self, module_name, result):
        pass

    @not_supported
    def _ec2_vpc_vpn(self, module_name, result):
        pass

    @check_state_present
    def _elb_application_lb(self, module_name, result):
        load_balancer_name = result._result.get('load_balancer_name')

        # Shoud add "wait: true" and "wait_timeout: 600" ?
        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(load_balancer_name),
            }
        }

    @check_state_present
    def _elb_classic_lb(self, module_name, result):
        load_balancer = result._result.get('load_balancer')
        load_balancer_name = load_balancer.get('load_balancer_name')

        # Shoud add "wait: true" and "wait_timeout: 600" ?
        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(load_balancer_name),
            }
        }

    @check_state_present
    def _iam_access_key(self, module_name, result):
        access_key = result._result.get('access_key')
        access_key_id = access_key.get('access_key_id')
        user_name = access_key.get('user_name')
        self.callback._debug(f"IAM Access Key {access_key_id}")

        return {
            module_name: {
                'state': 'absent',
                'id': self._to_text(access_key_id),
                'user_name': self._to_text(user_name),
            }
        }

    @check_state_present
    def _iam_group(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _iam_instance_profile(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _iam_managed_policy(self, module_name, result):
        policy = result._result.get('policy')
        policy_name = policy.get('policy_name')
        self.callback._debug(f"IAM Managed Policy {policy_name}")

        return {
            module_name: {
                'state': 'absent',
                'policy_name': self._to_text(policy_name),
            }
        }

    @not_supported
    def _iam_password_policy(self, module_name, result):
        '''
        There is only one password policy available !
        '''
        pass

    @check_state_present
    def _iam_policy(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        iam_type = module_args.get('iam_type')
        policy_name = module_args.get('policy_name')
        iam_name = module_args.get('iam_name')

        return {
            module_name: {
                'state': 'absent',
                'iam_type': self._to_text(iam_type),
                'iam_name': self._to_text(iam_name),
                'policy_name': self._to_text(policy_name),
            }
        }

    @check_state_present
    def _iam_role(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _iam_user(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _kms_key(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        alias = module_args.get('alias')
        self.callback._debug(f"KMS Key {alias}")

        return {
            module_name: {
                'state': 'absent',
                'alias': self._to_text(alias),
            }
        }

    @check_state_present
    def _lambda(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _lambda_alias(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        function_name = module_args.get('function_name')
        self.callback._debug(f"Lambda Function Alias {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'function_name': self._to_text(function_name),
            }
        }

    @not_supported
    def _lambda_event(self, module_name, result):
        pass

    @check_state_present
    def _lambda_layer(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        name = module_args.get('name')
        layer_versions = result._result.get('layer_versions')
        version = layer_versions[0].get('version')
        self.callback._debug(f"Lambda Function Layer {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'version': int(version),
            }
        }

    @not_supported
    def _lambda_policy(self, module_name, result):
        pass

    @check_state_present
    def _rds_cluster(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        for parm in ('cluster_name', 'cluster_id', 'id', 'db_cluster_identifier'):
            cluster_name = module_args.get(parm)
            if cluster_name: break

        username = module_args.get('password')
        password = module_args.get('password')
        engine = module_args.get('engine')
        deletion_protection = module_args.get('deletion_protection')
        self.callback._debug(f"RDS Cluster {cluster_name}")

        # if engine not set but deletion_protection is set, this is a rollback action:
        # nothing to rollback !
        if not engine and not deletion_protection:
            return None

        actions = [{
            module_name: {
                'state': 'absent',
                'cluster_name': self._to_text(cluster_name),
                'skip_final_snapshot': True,
            }
        }]

        if deletion_protection:
            protect_off = {
                module_name: {
                    'state': 'present',
                    'cluster_name': self._to_text(cluster_name),
                    'deletion_protection': False,
                }
            }
            actions.insert(0, protect_off)

        return actions

    @check_state_present
    def _rds_cluster_param_group(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _rds_cluster_snapshot(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        for parm in ('instance_id', 'id', 'db_cluster_snapshot_identifier', 'snapshot_name'):
            db_cluster_snapshot_identifier = module_args.get(parm)
            if db_cluster_snapshot_identifier: break

        self.callback._debug(f"RDS Cluster Snapshot {db_cluster_snapshot_identifier}")

        return {
            module_name: {
                'state': 'absent',
                'db_cluster_snapshot_identifier': self._to_text(db_cluster_snapshot_identifier),
            }
        }

    @check_state_present
    def _rds_instance(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        for parm in ('instance_id', 'id', 'db_instance_identifier'):
            instance_id = module_args.get(parm)
            if instance_id: break

        username = module_args.get('password')
        password = module_args.get('password')
        engine = module_args.get('engine')
        deletion_protection = module_args.get('deletion_protection')
        self.callback._debug(f"RDS Instance {instance_id}")

        # if engine not set but deletion_protection is set, this is a rollback action:
        # nothing to rollback !
        if not engine and not deletion_protection:
            return None

        actions = [{
            module_name: {
                'state': 'absent',
                'instance_id': self._to_text(instance_id),
                'skip_final_snapshot': True,
            }
        }]

        if deletion_protection:
            protect_off = {
                module_name: {
                    'state': 'present',
                    'instance_id': self._to_text(instance_id),
                    'deletion_protection': False,
                }
            }
            actions.insert(0, protect_off)

        return actions

    @check_state_present
    def _rds_instance_param_group(self, module_name, result):
        return self._simple_name_rollback(module_name, result)

    @check_state_present
    def _rds_instance_snapshot(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        for parm in ('instance_id', 'id', 'db_snapshot_identifier'):
            db_snapshot_identifier = module_args.get(parm)
            if db_snapshot_identifier: break

        self.callback._debug(f"RDS Cluster Snapshot {db_snapshot_identifier}")

        return {
            module_name: {
                'state': 'absent',
                'db_snapshot_identifier': self._to_text(db_snapshot_identifier),
            }
        }

    @check_state_present
    def _rds_option_group(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        option_group_name = module_args.get('option_group_name')
        self.callback._debug(f"{module_name}: {option_group_name}")

        return {
            module_name: {
                'state': 'absent',
                'option_group_name': self._to_text(option_group_name),
            }
        }

    @check_state_present
    def _route53(self, module_name, result):
        module_args = result._result.get('invocation').get('module_args')
        zone = module_args.get('zone')
        record = module_args.get('record')
        rtype = module_args.get('type')
        self.callback._debug(f"Route53 {record}")

        return {
            module_name: {
                'state': 'absent',
                'zone': self._to_text(zone),
                'record': self._to_text(record),
                'type': self._to_text(rtype),
            }
        }

    @not_supported
    def _route53_key_signing_key(self, module_name, result):
        pass

    @not_supported
    def _route53_zone(self, module_name, result):
        pass

    @check_state_present
    def _s3_bucket(self, module_name, result):
        name = result._result.get('name')
        self.callback._debug(f"S3 bucket {name}")

        return {
            module_name: {
                'state': 'absent',
                'name': self._to_text(name),
                'force': True,
            }
        }

    def _s3_object(self, module_name, result):
        '''
        Many cases according the "mode" parameter:
        "create": used to create Bucket directories
        "copy": copy an object stored in another Bucket
        "put": upload a file
        '''
        module_args = result._result.get('invocation').get('module_args')
        mode = module_args.get('mode')
        bucket_name = module_args.get("bucket")
        self.callback._debug(f"S3 object {bucket_name}")

        if mode == "put" or mode == "copy":
            object_name = module_args.get("object")
            return {
                module_name: {
                    'mode': 'delobj',
                    'object': self._to_text(object_name),
                    'bucket': self._to_text(bucket_name),
                }
            }

        if mode == "create":
            object_name = module_args.get("object")
            if object_name:
                # delete object
                return {
                    module_name: {
                        'mode': 'delobj',
                        'object': self._to_text(object_name),
                        'bucket': self._to_text(bucket_name),
                    }
                }

            # delete the whole Bucket (must use another module !)
            return {
                'amazon.aws.s3_bucket': {
                    'state': 'absent',
                    'bucket': self._to_text(bucket_name),
                }
            }

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
                for key in ('access_key', 'secret_key', 'region', 'aws_config', 'profile', 'session_token'):
                    if value := module_args.get(key):
                        final_action[action_module_name][key] = self._to_text(value)

            final_actions.append(final_action)

        return final_actions

# EOF
