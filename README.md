# Ansible Collection - majeinfo.resource_cleaner

This collection installs a callback plugins that generates 
rollback playbooks when a playbook generates dynamic resources in the Cloud.

In this version, a large part of AWS resources and some GCP resources types are supported:
EC2 instance, VPC, VPC Subnet, TAG, AMI, Security Group, EIP, ENI, KEY, Volume
(see the list of supported modules below)

In order to enable this Callback Plugin, add the following parameters
in your `ansible.cfg` file :

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

Originally developped for Ansible version 2.18+.

- `amazon.aws.ec2_vpc_nat_gateway`: 
  when creating a NAT Gateway with a dynamically created EIP, the EIP is not deleted on rollback

## SUPPORTED MODULES:

### For AWS:

| Module                                                    | Supported              |
|:----------------------------------------------------------|:-----------------------|
| ```amazon.aws.autoscaling_instance```                     | ```Yes```              |
| ```amazon.aws.backup_plan```                              | ```Yes```              |
| ```amazon.aws.backup_selection```                         | ```Yes```              |
| ```amazon.aws.backup_tag```                               | ```No```               |
| ```amazon.aws.backup_vault```                             | ```Yes```              |
| ```amazon.aws.cloudformation```                           | ```No```               |
| ```amazon.aws.cloudtrail```                               | ```Yes```              |
| ```amazon.aws.cloudwatch_metric_alarm```                  | ```Yes```              |
| ```amazon.aws.cloudwatchevent_rule```                     | ```Yes```              |
| ```amazon.aws.cloudwatchlogs_log_group```                 | ```Yes```              |
| ```amazon.aws.ec2_ami```                                  | ```Yes```              |
| ```amazon.aws.ec2_eip```                                  | ```Yes```              |
| ```amazon.aws.ec2_eni```                                  | ```Yes```              |
| ```amazon.aws.ec2_key```                                  | ```Yes```              |
| ```amazon.aws.ec2_instance```                             | ```Yes```              |
| ```amazon.aws.ec2_launch_template```                      | ```Yes```              |
| ```amazon.aws.ec2_placement_group```                      | ```Yes```              |
| ```amazon.aws.ec2_security_group```                       | ```Yes```              |
| ```amazon.aws.ec2_snapshot```                             | ```Yes```              |
| ```amazon.aws.ec2_spot_instance```                        | ```Yes```              |
| ```amazon.aws.ec2_tag```                                  | ```Yes```              |
| ```amazon.aws.ec2_transit_gateway```                      | ```Yes```              |
| ```amazon.aws.ec2_transit_gateway_vpc_attachment```       | ```Yes```              |
| ```amazon.aws.ec2_vol```                                  | ```Yes```              |
| ```amazon.aws.ec2_vpc_dhcp_option```                      | ```Yes```              |
| ```amazon.aws.ec2_vpc_egress_igw```                       | ```Yes```              |
| ```amazon.aws.ec2_vpc_endpoint```                         | ```Yes```              |
| ```amazon.aws.ec2_vpc_igw```                              | ```Yes```              |
| ```amazon.aws.ec2_vpc_nacl```                             | ```Yes```              |
| ```amazon.aws.ec2_vpc_nat_gateway```                      | ```Yes```              |
| ```amazon.aws.ec2_vpc_net```                              | ```Yes```              |
| ```amazon.aws.ec2_vpc_peering```                          | ```Yes```              |
| ```amazon.aws.ec2_vpc_route_table```                      | ```Yes```              |
| ```amazon.aws.ec2_vpc_net```                              | ```Yes```              |
| ```amazon.aws.ec2_vpc_subnet```                           | ```Yes```              |
| ```amazon.aws.ec2_vpc_vgw```                              | ```Yes```              |
| ```amazon.aws.ec2_vpc_vpn```                              | ```Yes```              |
| ```amazon.aws.elb_application_lb```                       | ```Yes```              |
| ```amazon.aws.elb_classic_lb```                           | ```Yes```              |
| ```amazon.aws.iam_access_key```                           | ```Yes```              |
| ```amazon.aws.iam_group```                                | ```Yes```              |
| ```amazon.aws.iam_instance_profile```                     | ```Yes```              |
| ```amazon.aws.iam_managed_policy```                       | ```Yes```              |
| ```amazon.aws.iam_password_policy```                      | ```No```               |
| ```amazon.aws.iam_policy```                               | ```Yes```              |
| ```amazon.aws.iam_role```                                 | ```Yes```              |
| ```amazon.aws.iam_user```                                 | ```Yes```              |
| ```amazon.aws.kms_key```                                  | ```Yes```              |
| ```amazon.aws.lambda```                                   | ```Yes```              |
| ```amazon.aws.lambda_alias```                             | ```Yes```              |
| ```amazon.aws.lambda_event```                             | ```No```               |
| ```amazon.aws.lambda_layer```                             | ```Yes```              |
| ```amazon.aws.lambda_policy```                            | ```Yes```              |
| ```amazon.aws.rds_cluster```                              | ```Yes```              |
| ```amazon.aws.rds_cluster_param_group```                  | ```Yes```              |
| ```amazon.aws.rds_cluster_snapshot```                     | ```Yes```              |
| ```amazon.aws.rds_instance```                             | ```Yes```              |
| ```amazon.aws.rds_instance_param_group```                 | ```Yes```              |
| ```amazon.aws.rds_instance_snapshot```                    | ```Yes```              |
| ```amazon.aws.rds_option_group```                         | ```Yes```              |
| ```amazon.aws.route53```                                  | ```Yes```              |
| ```amazon.aws.route53_key_signing_key```                  | ```No```               |
| ```amazon.aws.route53_zone```                             | ```No```               |
| ```amazon.aws.s3_bucket```                                | ```Yes```              |
| ```amazon.aws.s3_object```                                | ```Yes```              |
| ```community.aws.acm_certificate```                       | ```No```               |
| ```community.aws.api_gateway```                           | ```Yes```              |
| ```community.aws.api_gateway_domain```                    | ```No```               |
| ```community.aws.application_autoscaling_policy```        | ```No```               |
| ```community.aws.autoscaling_complete_lifecycle_action``` | ```No```               |
| ```community.aws.autoscaling_launch_config```             | ```Yes (not tested)``` |
| ```community.aws.autoscaling_lifecycle_hook```            | ```No```               |
| ```community.aws.autoscaling_policy```                    | ```No```               |
| ```community.aws.autoscaling_scheduled_action```          | ```No```               |
| ```community.aws.batch_compute_environment```             | ```No```               |
| ```community.aws.batch_job_definition```                  | ```No```               |
| ```community.aws.batch_job_queue```                       | ```No```               |
| ```community.aws.cloudformation_stack_set```              | ```No```               |
| ```community.aws.cloudfront_distribution```               | ```Yes```              |
| ```community.aws.cloudfront_invalidation```               | ```n/a```              |
| ```community.aws.cloudfront_origin_access_identity```     | ```Yes```              |
| ```community.aws.cloudfront_response_headers_policy```    | ```Yes```              |
| ```community.aws.codebuild_project```                     | ```No```               |
| ```community.aws.codecommit_repository```                 | ```No```               |
| ```community.aws.codepipeline```                          | ```No```               |
| ```community.aws.config_aggregation_authorization```      | ```No```               |
| ```community.aws.config_aggregator```                     | ```No```               |
| ```community.aws.config_delivery_channel```               | ```No```               |
| ```community.aws.config_recorder```                       | ```No```               |
| ```community.aws.config_rule```                           | ```Yes```              |
| ```community.aws.data_pipeline```                         | ```No```               |
| ```community.aws.directconnect_confirm_connection```      | ```No```               |
| ```community.aws.directconnect_connection```              | ```No```               |
| ```community.aws.directconnect_gateway```                 | ```No```               |
| ```community.aws.directconnect_link_aggregation_group```  | ```No```               |
| ```community.aws.directconnect_virtual_interface```       | ```No```               |
| ```community.aws.dms_endpoint```                          | ```No```               |
| ```community.aws.dms_replication_subnet_group```          | ```No```               |
| ```community.aws.dynamodb_table```                        | ```Yes```              |
| ```community.aws.dynamodb_ttl```                          | ```No```               |
| ```community.aws.ec2_ami_copy```                          | ```Yes```              |
| ```community.aws.ec2_carrier_gateway```                   | ```No```               |
| ```community.aws.ec2_customer_gateway```                  | ```No```               |
| ```community.aws.ec2_snapshot_copy```                     | ```No```               |
| ```community.aws.ec2_win_password```                      | ```No```               |
| ```community.aws.ecs_attribute```                         | ```No```               |
| ```community.aws.ecs_cluster```                           | ```Yes```              |
| ```community.aws.ecs_ecr```                               | ```No```               |
| ```community.aws.ecs_service```                           | ```Yes```              |
| ```community.aws.ecs_tag```                               | ```Yes```              |
| ```community.aws.ecs_task```                              | ```No```               |
| ```community.aws.ecs_taskdefinition```                    | ```Yes```              |
| ```community.aws.efs```                                   | ```Yes```              |
| ```community.aws.efs_tag```                               | ```No```               |
| ```community.aws.eks_cluster```                           | ```No```               |
| ```community.aws.eks_fargate_profile```                   | ```No```               |
| ```community.aws.eks_nodegroup```                         | ```No```               |
| ```community.aws.elasticache```                           | ```Yes```              |
| ```community.aws.elasticache_parameter_group```           | ```No```               |
| ```community.aws.elasticache_snapshot```                  | ```No```               |
| ```community.aws.elasticache_subnet_group```              | ```No```               |
| ```community.aws.elasticbeanstalk_app```                  | ```No```               |
| ```community.aws.elb_instance```                          | ```No```               |
| ```community.aws.elb_network_lb```                        | ```Yes```              |
| ```community.aws.elb_target```                            | ```No```               |
| ```community.aws.elb_target_group```                      | ```Yes```              |
| ```community.aws.glue_connection```                       | ```No```               |
| ```community.aws.glue_crawler```                          | ```No```               |
| ```community.aws.glue_job```                              | ```No```               |
| ```community.aws.iam_saml_federation```                   | ```No```               |
| ```community.aws.iam_server_certificate```                | ```No```               |
| ```community.aws.inspector_target```                      | ```No```               |
| ```community.aws.kinesis_stream```                        | ```No```               |
| ```community.aws.lightsail```                             | ```No```               |
| ```community.aws.lightsail_snapshot```                    | ```No```               |
| ```community.aws.lightsail_static_ip```                   | ```No```               |
| ```community.aws.mq_broker```                             | ```No```               |
| ```community.aws.mq_broker_config```                      | ```No```               |
| ```community.aws.mq_user```                               | ```No```               |
| ```community.aws.msk_cluster```                           | ```No```               |
| ```community.aws.msk_config```                            | ```No```               |
| ```community.aws.networkfirewall```                       | ```No```               |
| ```community.aws.networkfirewall_policy```                | ```No```               |
| ```community.aws.networkfirewall_rule_group```            | ```No```               |
| ```community.aws.opensearch```                            | ```No```               |
| ```community.aws.redshift```                              | ```No```               |
| ```community.aws.redshift_cross_region_snapshots```       | ```No```               |
| ```community.aws.redshift_subnet_group```                 | ```No```               |
| ```community.aws.route53_wait```                          | ```No```               |
| ```community.aws.s3_bucket_notification```                | ```No```               |
| ```community.aws.s3_cors```                               | ```No```               |
| ```community.aws.s3_lifecycle```                          | ```Yes```              |
| ```community.aws.s3_logging```                            | ```No```               |
| ```community.aws.s3_metrics_configuration```              | ```No```               |
| ```community.aws.s3_sync```                               | ```No```               |
| ```community.aws.s3_website```                            | ```Yes```              |
| ```community.aws.secretsmanager_secret```                 | ```No```               |
| ```community.aws.ses_identity```                          | ```No```               |
| ```community.aws.ses_identity_policy```                   | ```No```               |
| ```community.aws.ses_rule_set```                          | ```No```               |
| ```community.aws.sns_topic```                             | ```Yes```              |
| ```community.aws.sqs_queue```                             | ```Yes```              |
| ```community.aws.ssm_parameter```                         | ```No```               |
| ```community.aws.stepfunctions_state_machine```           | ```No```               |
| ```community.aws.stepfunctions_state_machine_execution``` | ```No```               |
| ```community.aws.sts_session_token```                     | ```No```               |
| ```community.aws.waf_condition```                         | ```Yes```              |
| ```community.aws.waf_rule```                              | ```Yes```              |
| ```community.aws.waf_web_acl```                           | ```Yes```              |
| ```community.aws.wafv2_ip_set```                          | ```Yes```              |
| ```community.aws.wafv2_resources```                       | ```Yes```              |
| ```community.aws.wafv2_rule_group```                      | ```Yes```              |
| ```community.aws.wafv2_web_acl```                         | ```Yes```              |

### For GCP:

| Module                                                                                                  | Supported |
|:--------------------------------------------------------------------------------------------------------|:----------|
| ```google.cloud.gcp_appengine_firewall_rule```                                                          | ```No```  |
| ```google.cloud.gcp_bigquery_dataset```                                                                 | ```No```  |
| ```google.cloud.gcp_bigquery_table```                                                                   | ```No```  |
| ```google.cloud.gcp_bigtable_instance```                                                                | ```No```  |
| ```google.cloud.gcp_cloudbuild_trigger```                                                               | ```No```  |
| ```google.cloud.gcp_cloudfunctions_cloud_function```                                                    | ```No```  |
| ```google.cloud.gcp_cloudscheduler_job```                                                               | ```No```  |
| ```google.cloud.gcp_cloudtasks_queue```                                                                 | ```No```  |
| ```google.cloud.gcp_compute_address```                                                                  | ```Yes``` |
| ```google.cloud.gcp_compute_autoscaler```                                                               | ```Yes``` |
| ```google.cloud.gcp_compute_backend_bucket```                                                           | ```Yes``` |
| ```google.cloud.gcp_compute_backend_service```                                                          | ```Yes``` |
| ```google.cloud.gcp_compute_disk```                                                                     | ```Yes``` |
| ```google.cloud.gcp_compute_external_vpn_gateway```                                                     | ```No```  |
| ```google.cloud.gcp_compute_firewall```                                                                 | ```Yes``` |
| ```google.cloud.gcp_compute_forwarding_rule```                                                          | ```No```  |
| ```google.cloud.gcp_compute_global_address```                                                           | ```Yes``` |
| ```google.cloud.gcp_compute_global_forwarding_rule```                                                   | ```No```  |
| ```google.cloud.gcp_compute_health_check```                                                             | ```Yes``` |
| ```google.cloud.gcp_compute_http_health_check```                                                        | ```Yes``` |
| ```google.cloud.gcp_compute_https_health_check```                                                       | ```Yes``` |
| ```google.cloud.gcp_compute_image```                                                                    | ```No```  |
| ```google.cloud.gcp_compute_instance```                                                                 | ```Yes``` |
| ```google.cloud.gcp_compute_instance_group```                                                           | ```Yes``` |
| ```google.cloud.gcp_compute_instance_group_manager```                                                   | ```Yes``` |
| ```google.cloud.gcp_compute_instance_template```                                                        | ```Yes``` |
| ```google.cloud.gcp_compute_interconnect_attachment```                                                  | ```No```  |
| ```google.cloud.gcp_compute_network```                                                                  | ```Yes``` |
| ```google.cloud.gcp_compute_network_endpoint_group```                                                   | ```No```  |
| ```google.cloud.gcp_compute_node_group```                                                               | ```Yes``` |
| ```google.cloud.gcp_compute_node_template```                                                            | ```Yes``` |
| ```google.cloud.gcp_compute_region_autoscaler```                                                        | ```Yes``` |
| ```google.cloud.gcp_compute_region_backend_service```                                                   | ```Yes``` |
| ```google.cloud.gcp_compute_region_disk```                                                              | ```Yes``` |
| ```google.cloud.gcp_compute_region_health_check```                                                      | ```Yes``` |
| ```google.cloud.gcp_compute_region_instance_group_manager```                                            | ```Yes``` |
| ```google.cloud.gcp_compute_region_target_http_proxy```                                                 | ```No```  |
| ```google.cloud.gcp_compute_region_target_https_proxy```                                                | ```No```  |
| ```google.cloud.gcp_compute_region_url_map```                                                           | ```No```  |
| ```google.cloud.gcp_compute_reservation```                                                              | ```No```  |
| ```google.cloud.gcp_compute_resource_policy```                                                          | ```No```  |
| ```google.cloud.gcp_compute_route```                                                                    | ```Yes``` |
| ```google.cloud.gcp_compute_router```                                                                   | ```Yes``` |
| ```google.cloud.gcp_compute_snapshot```                                                                 | ```No```  |
| ```google.cloud.gcp_compute_ssl_certificate```                                                          | ```No```  |
| ```google.cloud.gcp_compute_ssl_policy```                                                               | ```No```  |
| ```google.cloud.gcp_compute_subnetwork```                                                               | ```Yes``` |
| ```google.cloud.gcp_compute_target_http_proxy```                                                        | ```No```  |
| ```google.cloud.gcp_compute_target_https_proxy```                                                       | ```No```  |
| ```google.cloud.gcp_compute_target_instance```                                                          | ```No```  |
| ```google.cloud.gcp_compute_target_pool```                                                              | ```No```  |
| ```google.cloud.gcp_compute_target_pool_info```                                                         | ```No```  |
| ```google.cloud.gcp_compute_target_ssl_proxy```                                                         | ```No```  |
| ```google.cloud.gcp_compute_target_tcp_proxy```                                                         | ```No```  |
| ```google.cloud.gcp_compute_target_vpn_gateway```                                                       | ```No```  |
| ```google.cloud.gcp_compute_url_map```                                                                  | ```No```  |
| ```google.cloud.gcp_compute_vpn_tunnel```                                                               | ```No```  |
| ```google.cloud.gcp_container_cluster```                                                                | ```No```  |
| ```google.cloud.gcp_container_node_pool```                                                              | ```No```  |
| ```google.cloud.gcp_dns_managed_zone```                                                                 | ```No```  |
| ```google.cloud.gcp_dns_resource_record_set```                                                          | ```No```  |
| ```google.cloud.gcp_filestore_instance```                                                               | ```No```  |
| ```google.cloud.gcp_iam_role```                                                                         | ```Yes``` |
| ```google.cloud.gcp_iam_service_account```                                                              | ```Yes``` |
| ```google.cloud.gcp_iam_service_account_key```                                                          | ```Yes``` |
| ```google.cloud.gcp_kms_crypto_key```                                                                   | ```No```  |
| ```google.cloud.gcp_kms_key_ring```                                                                     | ```No```  |
| ```google.cloud.gcp_logging_metric```                                                                   | ```No```  |
| ```google.cloud.gcp_mlengine_model```                                                                   | ```No```  |
| ```google.cloud.gcp_mlengine_version```                                                                 | ```No```  |
| ```google.cloud.gcp_pubsub_subscription```                                                              | ```No```  |
| ```google.cloud.gcp_pubsub_topic```                                                                     | ```No```  |
| ```google.cloud.gcp_redis_instance```                                                                   | ```No```  |
| ```google.cloud.gcp_resourcemanager_project```                                                          | ```No```  |
| ```google.cloud.gcp_runtimeconfig_config```                                                             | ```No```  |
| ```google.cloud.gcp_runtimeconfig_variable```                                                           | ```No```  |
| ```google.cloud.gcp_secret_manager```                                                                   | ```No```  |
| ```google.cloud.gcp_serviceusage_service```                                                             | ```No```  |
| ```google.cloud.gcp_sourcerepo_repository```                                                            | ```No```  |
| ```google.cloud.gcp_spanner_database```                                                                 | ```No```  |
| ```google.cloud.gcp_spanner_instance```                                                                 | ```No```  |
| ```google.cloud.gcp_sql_database```                                                                     | ```No```  |
| ```google.cloud.gcp_sql_instance```                                                                     | ```No```  |
| ```google.cloud.gcp_sql_ssl_cert```                                                                     | ```No```  |
| ```google.cloud.gcp_sql_user```                                                                         | ```No```  |
| ```google.cloud.gcp_storage_bucket```                                                                   | ```Yes``` |
| ```google.cloud.gcp_storage_bucket_access_control```                                                    | ```No```  |
| ```google.cloud.gcp_storage_default_object_acl```                                                       | ```No```  |
| ```google.cloud.gcp_storage_object```                                                                   | ```No```  |
| ```google.cloud.gcp_tpu_node```                                                                         | ```No```  |

