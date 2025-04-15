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
log_level = debug

; possible values for the rollback playbook suffixes are:
; date: (default) suffix with the current date (format .YYYY-MM-DD-hh-mm-ss)
; rollback: sufix is .rollback
rollback_playbook_suffix = date
```

Now, if you run a Playbook, a rollback Playbook will be created
under the `./rollback` directory. This rollback Playbook can then be
played to delete the resources previously created.

## LIMITS AND BUGS:

- `amazon.aws.ec2_vpc_nat_gateway`: 
  when creating a NAT Gateway with a dynamically created EIP, the EIP is not deleted on rollback

## SUPPORTED MODULES:

### For AWS:

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

### For GCP:

| Module                                                                  | Supported |
|:------------------------------------------------------------------------|:----------|
| ```google.cloud.gcp_appengine_firewall_rule```                          | ```No```  |
| ```google.cloud.gcp_bigquery_dataset```                                 | ```No```  |
| ```google.cloud.gcp_bigquery_table```                                   | ```No```  |
| ```google.cloud.gcp_bigtable_instance```                                | ```No```  |
| ```google.cloud.gcp_cloudbuild_trigger```                               | ```No```  |
| ```google.cloud.gcp_cloudfunctions_cloud_function```                    | ```No```  |
| ```google.cloud.gcp_cloudscheduler_job```                               | ```No```  |
| ```google.cloud.gcp_cloudtasks_queue```                                 | ```No```  |
| ```google.cloud.gcp_compute_address```                                  | ```Yes``` |
| ```google.cloud.gcp_compute_autoscaler```                               | ```Yes``` |
| ```google.cloud.gcp_compute_backend_bucket```                           | ```Yes``` |
| ```google.cloud.gcp_compute_backend_service```                          | ```No```  |
| ```google.cloud.gcp_compute_disk```                                     | ```Yes``` |
| ```google.cloud.gcp_compute_external_vpn_gateway```                     | ```No```  |
| ```google.cloud.gcp_compute_firewall```                                 | ```No```  |
| ```google.cloud.gcp_compute_forwarding_rule```                          | ```No```  |
| ```google.cloud.gcp_compute_global_address```                           | ```No```  |
| ```google.cloud.gcp_compute_global_forwarding_rule```                   | ```No```  |
| ```google.cloud.gcp_compute_health_check```                             | ```No```  |
| ```google.cloud.gcp_compute_http_health_check```                        | ```No```  |
| ```google.cloud.gcp_compute_https_health_check```                       | ```No```  |
| ```google.cloud.gcp_compute_image```                                    | ```No```  |
| ```google.cloud.gcp_compute_instance```                                 | ```Yes``` |
| ```google.cloud.gcp_compute_instance_group```                           | ```No```  |
| ```google.cloud.gcp_compute_instance_group_manager```                   | ```Yes``` |
| ```google.cloud.gcp_compute_instance_template```                        | ```Yes``` |
| ```google.cloud.gcp_compute_interconnect_attachment```                  | ```No```  |
| ```google.cloud.gcp_compute_network```                                  | ```Yes``` |
| ```google.cloud.gcp_compute_network_endpoint_group```                   | ```No```  |
| ```google.cloud.gcp_compute_node_group```                               | ```No```  |
| ```google.cloud.gcp_compute_node_template```                            | ```No```  |
| ```google.cloud.gcp_compute_region_autoscaler```                        | ```No```  |
| ```google.cloud.gcp_compute_region_backend_service```                   | ```No```  |
| ```google.cloud.gcp_compute_region_disk```                              | ```No```  |
| ```google.cloud.gcp_compute_region_health_check```                      | ```No```  |
| ```google.cloud.gcp_compute_region_health_check_info```                 | ```No```  |
| ```google.cloud.gcp_compute_region_instance_group_manager```            | ```No```  |
| ```google.cloud.gcp_compute_region_target_http_proxy```                 | ```No```  |
| ```google.cloud.gcp_compute_region_target_https_proxy```                | ```No```  |
| ```google.cloud.gcp_compute_region_url_map```                           | ```No```  |
| ```google.cloud.gcp_compute_reservation```                              | ```No```  |
| ```google.cloud.gcp_compute_resource_policy```                          | ```No```  |
| ```google.cloud.gcp_compute_route```                                    | ```No```  |
| ```google.cloud.gcp_compute_router```                                   | ```No```  |
| ```google.cloud.ggcp_compute_snapshot```                                | ```No```  |
| ```google.cloud.gcp_compute_ssl_certificate```                          | ```No```  |
| ```google.cloud.gcp_compute_ssl_policy```                               | ```No```  |
| ```google.cloud.gcp_compute_subnetwork```                               | ```Yes``` |
| ```google.cloud.gcp_compute_target_http_proxy```                        | ```No```  |
| ```google.cloud.gcp_compute_target_https_proxy```                       | ```No```  |
| ```google.cloud.gcp_compute_target_instance```                          | ```No```  |
| ```google.cloud.gcp_compute_target_pool```                              | ```No```  |
| ```google.cloud.gcp_compute_target_pool_info```                         | ```No```  |
| ```google.cloud.gcp_compute_target_ssl_proxy```                         | ```No```  |
| ```google.cloud.gcp_compute_target_tcp_proxy```                         | ```No```  |
| ```google.cloud.gcp_compute_target_vpn_gateway```                       | ```No```  |
| ```google.cloud.gcp_compute_url_map```                                  | ```No```  |
| ```google.cloud.gcp_compute_vpn_tunnel```                                | ```No```  |
| ```google.cloud.gcp_container_cluster```                                                     | ```No```  |
| ```google.cloud.gcp_container_node_pool```                                                     | ```No```  |
| ```google.cloud.gcp_dns_managed_zone```                                                     | ```No```  |
| ```google.cloud.gcp_dns_resource_record_set```                                                     | ```No```  |
| ```google.cloud.gcp_filestore_instance```                                                     | ```No```  |
| ```google.cloud.gcp_iam_role```                                                     | ```No```  |
| ```google.cloud.gcp_iam_service_account```                                                     | ```No```  |
| ```google.cloud.gcp_iam_service_account_key```                                                     | ```No```  |
| ```google.cloud.gcp_kms_crypto_key```                                                     | ```No```  |
| ```google.cloud.gcp_kms_key_ring```                                                     | ```No```  |
| ```google.cloud.gcp_logging_metric```                                                     | ```No```  |
| ```google.cloud.gcp_mlengine_model```                                                     | ```No```  |
| ```google.cloud.gcp_mlengine_version```                                                     | ```No```  |
| ```google.cloud.gcp_pubsub_subscription```                                                     | ```No```  |
| ```google.cloud.gcp_pubsub_topic```                                                     | ```No```  |
| ```google.cloud.gcp_redis_instance```                                                     | ```No```  |
| ```google.cloud.gcp_resourcemanager_project```                                                     | ```No```  |
| ```google.cloud.gcp_runtimeconfig_config```                                                     | ```No```  |
| ```google.cloud.gcp_runtimeconfig_variable```                                                     | ```No```  |
| ```google.cloud.gcp_secret_manager```                                                     | ```No```  |
| ```google.cloud.gcp_serviceusage_service```                                                     | ```No```  |
| ```google.cloud.gcp_sourcerepo_repository```                                                     | ```No```  |
| ```google.cloud.gcp_spanner_database```                                                     | ```No```  |
| ```google.cloud.gcp_spanner_instance```                                                     | ```No```  |
| ```google.cloud.gcp_sql_database```                                                     | ```No```  |
| ```google.cloud.gcp_sql_instance```                                                     | ```No```  |
| ```google.cloud.gcp_sql_ssl_cert```                                                     | ```No```  |
| ```google.cloud.gcp_sql_user```                                                     | ```No```  |
| ```google.cloud.gcp_storage_bucket```                                   | ```Yes``` |
| ```google.cloud.gcp_storage_bucket_access_control```                                                     | ```No```  |
| ```google.cloud.gcp_storage_default_object_acl```                                                     | ```No```  |
| ```google.cloud.gcp_storage_object```                                                     | ```No```  |
| ```google.cloud.gcp_tpu_node```                                                     | ```No```  |

