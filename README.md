# Ansible Collection - majeinfo.resource_cleaner

This collection installs a callback plugins that generates 
rollback playbooks when a playbook generates dynamic resources in the Cloud.

In this version, only some of AWS resources types are supported:
EC2 instance, VPC, VPC Subnet, TAG, AMI, Security Group, EIP, ENI, KEY, Volume
(see the list of supported modules below)

In order to enable this Callback Plugin, add the following parameters
in your ansible.cfg file :

```
[defaults]
callbacks_enabled = resource_cleaner
callback_plugins = majeinfo/resource_cleaner/plugins/callback

[resource_cleaner]
playbook_output_path = ./rollback
hide_sensitive_data = false
log_level = debug
```

Now, if you run a Playbook, a rollback Playbook will be created
under the ./rollback directory. This rollback Playbook can then be
played to delete the resources previously created.

LIMITS AND BUGS:

- amazon.aws.ec2_vpc_nat_gateway: 
  when creating a NAT Gateway with a dynamically created EIP, the EIP is not deleted on rollback

- amazon.aws.s3_object:
  when creating a directory in a S3 bucket, it is not deleted when using "mode: delobj" on rollback

SUPPORTED MODULES:

For AWS:

| Module | Supported |
| :--- |:----------|
| ```amazon.aws.autoscaling_instance``` | ```Yes``` |
| ```amazon.aws.backup_plan``` | ```Yes``` |
| ```amazon.aws.backup_selection``` | ```Yes``` |
| ```amazon.aws.backup_tag``` | ```No```  |
| ```amazon.aws.backup_vault``` | ```Yes``` |
| ```amazon.aws.cloudformation``` | ```No```  |
| ```amazon.aws.cloudtrail``` | ```Yes``` |
| ```amazon.aws.cloudwatch_metric_alarm``` | ```Yes``` |
| ```amazon.aws.cloudwatchevent_rule``` | ```Yes``` |
| ```amazon.aws.cloudwatchlogs_log_group``` | ```Yes``` |
| ```amazon.aws.ec2_ami``` | ```Yes``` |
| ```amazon.aws.ec2_eip``` | ```Yes``` |
| ```amazon.aws.ec2_eni``` | ```Yes``` |
| ```amazon.aws.ec2_key``` | ```Yes``` |
| ```amazon.aws.ec2_instance``` | ```Yes``` |
| ```amazon.aws.ec2_launch_template``` | ```Yes``` |
| ```amazon.aws.ec2_placement_group``` | ```Yes``` |
| ```amazon.aws.ec2_security_group``` | ```Yes``` |
| ```amazon.aws.ec2_snapshot``` | ```Yes``` |
| ```amazon.aws.ec2_spot_instance``` | ```Yes``` |
| ```amazon.aws.ec2_tag``` | ```Yes``` |
| ```amazon.aws.ec2_transit_gateway``` | ```No```  |
| ```amazon.aws.ec2_transit_gateway_vpc_attachment``` | ```No```  |
| ```amazon.aws.ec2_vol``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_dhcp_option``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_egress_igw``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_endpoint``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_igw``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_nacl``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_nat_gateway``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_net``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_peering``` | ```No```  |
| ```amazon.aws.ec2_vpc_route_table``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_net``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_subnet``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_vgw``` | ```Yes``` |
| ```amazon.aws.ec2_vpc_vpn``` | ```Yes``` |
| ```amazon.aws.elb_application_lb``` | ```Yes``` |
| ```amazon.aws.elb_classic_lb``` | ```Yes``` |
| ```amazon.aws.iam_access_key``` | ```Yes``` |
| ```amazon.aws.iam_group``` | ```Yes``` |
| ```amazon.aws.iam_instance_profile``` | ```Yes``` |
| ```amazon.aws.iam_managed_policy``` | ```Yes``` |
| ```amazon.aws.iam_password_policy``` | ```No```  |
| ```amazon.aws.iam_policy``` | ```Yes``` |
| ```amazon.aws.iam_role``` | ```Yes``` |
| ```amazon.aws.iam_user``` | ```Yes``` |
| ```amazon.aws.kms_key``` | ```Yes``` |
| ```amazon.aws.lambda``` | ```Yes``` |
| ```amazon.aws.lambda_alias``` | ```Yes``` |
| ```amazon.aws.lambda_event``` | ```No```  |
| ```amazon.aws.lambda_layer``` | ```Yes``` |
| ```amazon.aws.lambda_policy``` | ```No```  |
| ```amazon.aws.rds_cluster``` | ```Yes``` |
| ```amazon.aws.rds_cluster_param_group``` | ```No```  |
| ```amazon.aws.rds_cluster_snapshot``` | ```No```  |
| ```amazon.aws.rds_instance``` | ```No```  |
| ```amazon.aws.rds_instance_param_group``` | ```No```  |
| ```amazon.aws.rds_instance_snapshot``` | ```No```  |
| ```amazon.aws.rds_option_group``` | ```No```  |
| ```amazon.aws.route53``` | ```Yes``` |
| ```amazon.aws.route53_key_signing_key``` | ```No```  |
| ```amazon.aws.route53_zone``` | ```No```  |
| ```amazon.aws.s3_bucket``` | ```Yes``` |
| ```amazon.aws.s3_object``` | ```Yes``` |

