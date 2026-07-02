#!/usr/bin/env python3
"""Terminal flashcard trainer for AWS Certified Solutions Architect - Associate."""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from textwrap import fill


PROGRESS_FILE = Path(__file__).with_name("aws_flashcard_progress.json")
WRAP_WIDTH = 92


@dataclass(frozen=True)
class Card:
    id: str
    day: int
    focus: str
    question: str
    answer: str
    practical: str


CARDS = [
    Card("d01-q1", 1, "AWS basics", "What is an AWS Region?", "A Region is a separate geographic area that contains multiple Availability Zones. Choose Regions based on latency, compliance, service availability, and cost.", "Mark two Regions on a simple AWS global map."),
    Card("d01-q2", 1, "AWS basics", "What is an Availability Zone?", "An Availability Zone is one or more isolated data centers inside a Region. Multi-AZ designs protect workloads from a single AZ failure.", "Draw one Region with three AZs."),
    Card("d01-q3", 1, "AWS basics", "What does AWS manage in the shared responsibility model?", "AWS manages security of the cloud: facilities, physical hardware, networking, virtualization, and managed service infrastructure.", "Label AWS-owned responsibilities in your model."),
    Card("d02-q1", 2, "IAM", "What is an IAM user?", "An IAM user is a long-term identity inside an AWS account. For workforce access, prefer IAM Identity Center or federation when possible.", "Create a test IAM user without admin access."),
    Card("d02-q2", 2, "IAM", "What is an IAM role?", "An IAM role is an assumable identity that provides temporary credentials. Use roles for AWS services, applications, federation, and cross-account access.", "Create a role for an AWS service."),
    Card("d02-q3", 2, "IAM", "What does least privilege mean?", "Least privilege means granting only the actions, resources, and conditions needed for a task, then reviewing and removing unused access over time.", "Write a narrow read-only policy for one S3 bucket."),
    Card("d03-q1", 3, "IAM advanced", "What does AWS STS do?", "AWS Security Token Service issues temporary security credentials for assumed roles, federation, and cross-account access.", "Find where AssumeRole appears in a trust policy."),
    Card("d03-q2", 3, "IAM advanced", "What is an IAM permission boundary?", "A permission boundary limits the maximum permissions an IAM user or role can receive. It does not grant permissions by itself.", "Compare a policy allow against a boundary limit."),
    Card("d03-q3", 3, "IAM advanced", "What is required for cross-account role access?", "The target account role needs a trust policy allowing the external principal, and the caller needs permission to run sts:AssumeRole.", "Sketch the trusted account and target account."),
    Card("d03-q4", 3, "IAM advanced", "What wins during IAM policy evaluation?", "An explicit deny always wins. If there is no explicit allow, the result is implicit deny.", "Trace a request through deny, allow, and default deny."),
    Card("d03-q5", 3, "IAM advanced", "What is an IAM identity-based policy?", "An identity-based policy attaches to a user, group, or role and defines what that identity can do.", "Attach a read-only policy to a role."),
    Card("d03-q6", 3, "IAM advanced", "What is an IAM resource-based policy?", "A resource-based policy attaches to a resource and defines who can access that resource.", "Find a bucket policy or Lambda resource policy."),
    Card("d03-q7", 3, "IAM advanced", "What does an IAM role trust policy control?", "A trust policy controls which principals are allowed to assume the role.", "Identify the Principal in a role trust policy."),
    Card("d03-q8", 3, "IAM advanced", "Why should applications use IAM roles instead of access keys?", "Roles provide temporary credentials that rotate automatically and avoid long-term secrets stored in code or configuration.", "Replace static keys with an EC2 instance profile."),
    Card("d03-q9", 3, "IAM advanced", "What is an IAM instance profile?", "An instance profile is the container that lets an EC2 instance receive an IAM role and temporary credentials.", "Find the instance profile on an EC2 instance."),
    Card("d03-q10", 3, "IAM advanced", "When should you use IAM Identity Center?", "Use IAM Identity Center for workforce access to multiple AWS accounts and applications, especially with a corporate identity provider.", "Map a user group to a permission set."),
    Card("d03-q11", 3, "IAM advanced", "What is an IAM permission set?", "A permission set defines permissions that IAM Identity Center assigns to users or groups for target AWS accounts.", "Create an admin and read-only permission set design."),
    Card("d03-q12", 3, "IAM advanced", "What is the purpose of an external ID?", "An external ID helps prevent confused deputy problems when a third party assumes a role in your account.", "Add an external ID condition to a vendor role."),
    Card("d03-q13", 3, "IAM advanced", "What is role chaining?", "Role chaining is assuming a role using credentials from another assumed role, with a maximum session duration of one hour.", "Spot role chaining in a troubleshooting scenario."),
    Card("d03-q14", 3, "IAM advanced", "What is an IAM service-linked role?", "A service-linked role is predefined by an AWS service and includes permissions the service needs to manage resources on your behalf.", "Find a service-linked role in an account."),
    Card("d03-q15", 3, "IAM advanced", "What is an IAM condition key used for?", "Condition keys restrict when a policy statement applies, such as by MFA, source IP, VPC endpoint, principal tag, or requested Region.", "Add a condition requiring MFA."),
    Card("d03-q16", 3, "IAM advanced", "How can tags be used in IAM access control?", "Attribute-based access control uses principal, resource, or request tags in policy conditions to make access decisions.", "Design access based on a Project tag."),
    Card("d03-q17", 3, "IAM advanced", "What is the difference between AWS managed and customer managed policies?", "AWS managed policies are created and maintained by AWS; customer managed policies are created and controlled in your account.", "Choose a customer managed policy for custom least privilege."),
    Card("d03-q18", 3, "IAM advanced", "What are IAM groups used for?", "IAM groups organize IAM users so policies can be assigned to multiple users at once.", "Put users with the same job function in a group."),
    Card("d03-q19", 3, "IAM advanced", "Can IAM groups contain roles or other groups?", "No. IAM groups can contain IAM users only.", "Avoid nesting groups in an IAM design."),
    Card("d03-q20", 3, "IAM advanced", "What is the exam guidance for the AWS root user?", "Enable MFA, do not create root access keys, and use the root user only for account-level tasks that require it.", "List two tasks that require root."),
    Card("d03-q21", 3, "IAM advanced", "What does MFA add to IAM security?", "MFA requires an additional authentication factor and can be enforced for console access or sensitive API actions.", "Add an MFA condition to a deny or allow policy."),
    Card("d03-q22", 3, "IAM advanced", "What does IAM Access Analyzer help identify?", "IAM Access Analyzer helps find resources shared with external principals and can help validate policies.", "Use Access Analyzer to inspect a public bucket policy."),
    Card("d03-q23", 3, "IAM advanced", "What does IAM credential report show?", "The credential report lists IAM users and credential status such as password use, access keys, MFA, and rotation age.", "Find stale access keys in a credential report."),
    Card("d03-q24", 3, "IAM advanced", "How should unused IAM access be handled?", "Review last accessed information, remove unused permissions, rotate or delete unused keys, and narrow policies over time.", "Remove one unused action from a policy."),
    Card("d03-q25", 3, "IAM advanced", "What is a session policy?", "A session policy is an inline policy passed when assuming a role to further limit the temporary session permissions.", "Limit an assumed role session to one S3 prefix."),
    Card("d03-q26", 3, "IAM advanced", "How do SCPs interact with IAM permissions?", "SCPs set maximum permissions for accounts in AWS Organizations but do not grant permissions by themselves.", "Compare an IAM allow that is blocked by an SCP."),
    Card("d03-q27", 3, "IAM advanced", "Why might an IAM principal with an allow still be denied access?", "Access can be blocked by explicit deny, missing resource policy, permissions boundary, SCP, session policy, VPC endpoint policy, or KMS key policy.", "Build a checklist for an access denied error."),
    Card("d04-q1", 4, "EC2 basics", "What is an AMI?", "An Amazon Machine Image is the template used to launch an EC2 instance. It includes the operating system and can include application configuration.", "Find the AMI field in an EC2 launch screen."),
    Card("d04-q2", 4, "EC2 basics", "What is an EC2 instance type?", "An instance type defines the CPU, memory, storage, and network capacity of an EC2 instance. Pick it based on workload shape.", "Match t, m, c, r, and g families to workload types."),
    Card("d04-q3", 4, "EC2 basics", "What does EC2 user data do?", "User data runs bootstrapping commands when an instance launches. It is commonly used to install packages or configure an application.", "Write a small user-data script that installs a web server."),
    Card("d05-q1", 5, "EC2 pricing", "When is EC2 On-Demand the right pricing model?", "Use On-Demand for short-term, unpredictable, or spiky workloads where you do not want a long-term usage commitment.", "Pick On-Demand for a temporary test environment."),
    Card("d05-q2", 5, "EC2 pricing", "When is EC2 Spot the right pricing model?", "Use Spot for flexible, fault-tolerant, interruptible workloads such as batch jobs, CI workers, or stateless processing.", "Identify which workloads can tolerate interruption."),
    Card("d05-q3", 5, "EC2 pricing", "When should you use a Savings Plan?", "Use Savings Plans for steady compute usage when you can commit to a dollars-per-hour spend for one or three years.", "Estimate steady hourly compute spend for a workload."),
    Card("d06-q1", 6, "EBS and instance storage", "What is Amazon EBS?", "Amazon EBS provides persistent block storage for EC2 instances. EBS volumes can survive instance stop/start and support snapshots.", "Attach an EBS volume to an EC2 instance."),
    Card("d06-q2", 6, "EBS and instance storage", "What is EC2 instance store?", "Instance store is temporary block storage physically attached to the host. Data is lost when the instance stops, terminates, or the disk fails.", "Identify a workload that can use temporary scratch storage."),
    Card("d06-q3", 6, "EBS and instance storage", "What are EBS snapshots used for?", "EBS snapshots are point-in-time backups stored in S3-managed storage. They are used to restore volumes, copy data, and build AMIs.", "Create a snapshot and restore it as a new volume."),
    Card("d06-q4", 6, "EC2 operations", "What is an EC2 launch template used for?", "A launch template stores instance launch settings such as AMI, instance type, security groups, IAM instance profile, storage, and user data.", "Create a launch template for a web tier."),
    Card("d06-q5", 6, "EC2 operations", "Why prefer launch templates over launch configurations?", "Launch templates support versioning and newer EC2 features and are the preferred option for Auto Scaling groups.", "Update an Auto Scaling group to a new template version."),
    Card("d06-q6", 6, "EC2 operations", "What happens when you stop an EBS-backed EC2 instance?", "The instance shuts down, compute billing stops, EBS volumes persist and continue billing, and the instance can be started again.", "Compare stop/start against terminate."),
    Card("d06-q7", 6, "EC2 operations", "What happens when you terminate an EC2 instance?", "The instance is deleted, attached instance store data is lost, and EBS root volume deletion depends on the delete-on-termination setting.", "Check delete-on-termination for a root volume."),
    Card("d06-q8", 6, "EC2 operations", "What is EC2 hibernation used for?", "Hibernation saves memory contents to the encrypted EBS root volume so an instance can resume faster with in-memory state.", "Identify a workload that benefits from hibernation."),
    Card("d06-q9", 6, "EC2 operations", "What is an Elastic IP used for?", "An Elastic IP is a static public IPv4 address that can be remapped to another instance or network interface.", "Move an Elastic IP during a simple failover."),
    Card("d06-q10", 6, "EC2 operations", "What is an Elastic Network Interface?", "An ENI is a virtual network card with private IPs, security groups, MAC address, and optional public or Elastic IP association.", "Attach a secondary ENI to an instance."),
    Card("d06-q11", 6, "EC2 operations", "How should an EC2 instance in a private subnet get outbound internet access?", "Route outbound internet traffic through a NAT Gateway in a public subnet.", "Place a NAT Gateway in a VPC diagram."),
    Card("d06-q12", 6, "EC2 operations", "How should users reach EC2 instances over HTTP at scale?", "Put instances behind an Application Load Balancer and use an Auto Scaling group across multiple Availability Zones.", "Draw a two-AZ web tier behind an ALB."),
    Card("d06-q13", 6, "EC2 operations", "What is EC2 detailed monitoring?", "Detailed monitoring sends EC2 metrics to CloudWatch at one-minute granularity instead of the default five-minute granularity.", "Choose detailed monitoring for faster scaling signals."),
    Card("d06-q14", 6, "EC2 operations", "What should you check when an EC2 instance is unreachable by SSH?", "Check security group rules, network ACLs, route tables, public IP or bastion path, OS firewall, key pair, and instance status checks.", "Build an SSH troubleshooting checklist."),
    Card("d06-q15", 6, "EC2 operations", "What do EC2 system status checks indicate?", "System status checks detect AWS infrastructure problems such as host hardware or network issues.", "Decide when to stop/start or recover an instance."),
    Card("d06-q16", 6, "EC2 operations", "What do EC2 instance status checks indicate?", "Instance status checks detect problems inside the instance such as OS, network configuration, or exhausted resources.", "Investigate a failed instance status check."),
    Card("d06-q17", 6, "EC2 operations", "What is an EC2 placement group?", "A placement group controls how instances are placed on underlying hardware for latency, fault isolation, or partitioned workloads.", "Choose cluster, spread, or partition placement."),
    Card("d06-q18", 6, "EC2 operations", "When should you use a cluster placement group?", "Use a cluster placement group for low-latency, high-throughput workloads that benefit from instances close together in one Availability Zone.", "Choose it for HPC node communication."),
    Card("d06-q19", 6, "EC2 operations", "When should you use a spread placement group?", "Use a spread placement group to place a small number of critical instances on distinct hardware for failure isolation.", "Place critical replicas on separate racks."),
    Card("d06-q20", 6, "EC2 operations", "When should you use a partition placement group?", "Use a partition placement group for large distributed systems that need groups of instances isolated across hardware partitions.", "Choose it for Hadoop, Cassandra, or Kafka."),
    Card("d06-q21", 6, "EC2 operations", "What is a Dedicated Host?", "A Dedicated Host is a physical server dedicated to your use, often chosen for compliance or bring-your-own-license requirements.", "Match BYOL licensing to Dedicated Hosts."),
    Card("d06-q22", 6, "EC2 operations", "What is a Dedicated Instance?", "A Dedicated Instance runs on hardware dedicated to one customer account, but without the same host-level control as Dedicated Hosts.", "Compare Dedicated Instances with Dedicated Hosts."),
    Card("d06-q23", 6, "EC2 operations", "What is EC2 Auto Recovery?", "Auto Recovery can recover an impaired instance onto different hardware while preserving instance ID, private IP, Elastic IP, and metadata.", "Use recovery for a failed system status check."),
    Card("d06-q24", 6, "EC2 operations", "When should you use Compute Savings Plans?", "Use Compute Savings Plans for steady compute spend across EC2, Fargate, and Lambda with flexibility across instance family, size, Region, OS, or tenancy.", "Compare Compute Savings Plans with Reserved Instances."),
    Card("d06-q25", 6, "EC2 operations", "When should you use EC2 Instance Savings Plans?", "Use EC2 Instance Savings Plans for steady usage in a specific instance family and Region when you want a larger discount than Compute Savings Plans.", "Match a stable m-family workload to an EC2 Instance Savings Plan."),
    Card("d06-q26", 6, "EC2 operations", "What is the key exam rule for Spot Instances?", "Use Spot only for workloads that can tolerate interruption, such as batch, stateless workers, CI jobs, and distributed processing.", "Identify which tier can safely run on Spot."),
    Card("d06-q27", 6, "EC2 operations", "What is a Spot interruption notice?", "AWS provides a two-minute warning before interrupting a Spot Instance when capacity is reclaimed.", "Design checkpointing for a Spot worker."),
    Card("d06-q28", 6, "EC2 operations", "What EBS volume type is the default general-purpose SSD choice?", "gp3 is the current general-purpose SSD choice and lets you provision IOPS and throughput independently from volume size.", "Choose gp3 for a typical boot or app volume."),
    Card("d06-q29", 6, "EC2 operations", "When should you choose io2 or io2 Block Express?", "Choose io2 for mission-critical workloads that need high IOPS, low latency, and higher durability than general-purpose SSD.", "Match io2 to a high-performance database volume."),
    Card("d06-q30", 6, "EC2 operations", "What is the difference between EBS and instance store for persistence?", "EBS persists independently of the instance lifecycle, while instance store is temporary and tied to the underlying host.", "Choose EBS for durable database files."),
    Card("d07-q1", 7, "Load balancing", "When should you use an Application Load Balancer?", "Use an ALB for HTTP and HTTPS workloads that need layer 7 routing, host-based routing, path-based routing, or container-friendly targets.", "Put two web instances behind an ALB."),
    Card("d07-q2", 7, "Load balancing", "When should you use a Network Load Balancer?", "Use an NLB for very high-performance layer 4 TCP, UDP, or TLS traffic, static IP requirements, or preserving source IP.", "Choose NLB for a low-latency TCP service."),
    Card("d07-q3", 7, "Load balancing", "What does a load balancer health check do?", "A health check verifies whether a target can receive traffic. Unhealthy targets are removed from rotation until they recover.", "Configure a target group health check path."),
    Card("d08-q1", 8, "Auto Scaling", "What is an Auto Scaling group desired capacity?", "Desired capacity is the current number of instances the Auto Scaling group tries to maintain.", "Set desired capacity to two in a sample design."),
    Card("d08-q2", 8, "Auto Scaling", "What does an Auto Scaling launch template define?", "A launch template defines instance settings such as AMI, instance type, security group, IAM instance profile, storage, and user data.", "Review a launch template field list."),
    Card("d08-q3", 8, "Auto Scaling", "What is a target tracking scaling policy?", "Target tracking adjusts capacity to keep a metric near a chosen target, such as average CPU utilization or request count per target.", "Design a policy that targets 50 percent CPU."),
    Card("d09-q1", 9, "S3 basics", "What is an S3 bucket?", "An S3 bucket is a Region-scoped container for objects. Bucket names are globally unique across AWS.", "Create a bucket name that would be globally unique."),
    Card("d09-q2", 9, "S3 basics", "What does S3 versioning do?", "S3 versioning keeps multiple versions of an object, which helps recover from accidental deletion or overwrite.", "Enable versioning on a test bucket."),
    Card("d09-q3", 9, "S3 basics", "What does S3 Block Public Access do?", "S3 Block Public Access provides account-level and bucket-level controls that prevent public access from policies or ACLs.", "Check whether Block Public Access is enabled."),
    Card("d10-q1", 10, "S3 advanced", "When should you use S3 Standard-IA?", "Use S3 Standard-IA for infrequently accessed data that still needs milliseconds retrieval and multi-AZ resilience.", "Move old objects to Standard-IA with a lifecycle rule."),
    Card("d10-q2", 10, "S3 advanced", "What does an S3 lifecycle rule do?", "A lifecycle rule automatically transitions objects to another storage class or expires them after defined conditions are met.", "Create a transition rule for objects older than 30 days."),
    Card("d10-q3", 10, "S3 advanced", "What is S3 replication used for?", "S3 replication automatically copies objects to another bucket in the same or another Region for compliance, locality, or resilience.", "Sketch source and destination replication buckets."),
    Card("d10-q4", 10, "S3 advanced", "What is the exam-safe default for public S3 access?", "Keep buckets private, enable S3 Block Public Access, and grant only required access through IAM, bucket policies, or CloudFront origin access control.", "Review a bucket and confirm Block Public Access is enabled."),
    Card("d10-q5", 10, "S3 advanced", "When should you use an S3 bucket policy?", "Use a bucket policy for resource-based access such as cross-account access, public website read access, CloudFront OAC, or organization-wide conditions.", "Write a bucket policy statement for one allowed role."),
    Card("d10-q6", 10, "S3 advanced", "What does S3 Object Lock provide?", "S3 Object Lock provides WORM-style retention so protected object versions cannot be deleted or overwritten until retention allows it.", "Compare governance mode and compliance mode."),
    Card("d10-q7", 10, "S3 advanced", "When should you choose SSE-KMS for S3 encryption?", "Choose SSE-KMS when you need customer-managed keys, key policy control, audit visibility, or tighter separation of encryption permissions.", "Identify the KMS permissions needed to read an object."),
    Card("d10-q8", 10, "S3 advanced", "What extra permissions are needed to read SSE-KMS encrypted objects?", "The caller needs both S3 permissions and KMS permissions such as kms:Decrypt on the relevant key.", "Troubleshoot an S3 allow that still cannot decrypt."),
    Card("d10-q9", 10, "S3 advanced", "When should you choose S3 Intelligent-Tiering?", "Use Intelligent-Tiering when object access patterns are unknown or changing and automatic tier movement is worth the monitoring cost.", "Choose a storage class for unpredictable access."),
    Card("d10-q10", 10, "S3 advanced", "When is S3 One Zone-IA appropriate?", "Use One Zone-IA for infrequently accessed, re-creatable data when lower cost matters and single-AZ resilience is acceptable.", "Mark a re-creatable dataset that can tolerate AZ loss."),
    Card("d10-q11", 10, "S3 advanced", "Which S3 storage classes fit archive workloads?", "Use Glacier Instant Retrieval for archive data needing milliseconds access, Glacier Flexible Retrieval for lower-cost slower retrieval, and Deep Archive for the lowest-cost long-term archive.", "Match retention and retrieval time to a Glacier class."),
    Card("d10-q12", 10, "S3 advanced", "What is required before enabling S3 replication?", "Versioning must be enabled on both source and destination buckets, and replication needs an IAM role with required permissions.", "Check a source and destination bucket for versioning."),
    Card("d10-q13", 10, "S3 advanced", "When should you use S3 Cross-Region Replication?", "Use CRR for compliance, regional locality, lower-latency regional reads, or disaster recovery copies in another Region.", "Sketch a source bucket and destination Region."),
    Card("d10-q14", 10, "S3 advanced", "What is the S3 static website hosting access requirement?", "The S3 website endpoint requires public read access to hosted objects. For private CloudFront access, use the S3 REST endpoint with OAC instead.", "Compare website endpoint versus REST endpoint."),
    Card("d10-q15", 10, "S3 advanced", "When should you use an S3 pre-signed URL?", "Use a pre-signed URL when a user or app needs temporary upload or download access to a specific object without AWS credentials.", "Create a short-lived upload URL in a design."),
    Card("d10-q16", 10, "S3 advanced", "What are S3 Access Points used for?", "S3 Access Points provide separate hostnames and policies for different applications, teams, or access patterns against shared buckets.", "Design two access points for one shared data bucket."),
    Card("d10-q17", 10, "S3 advanced", "How can private subnets access S3 without public internet routing?", "Use an S3 Gateway VPC endpoint or an Interface endpoint when PrivateLink-style access is required.", "Add an S3 gateway endpoint to a VPC route table."),
    Card("d10-q18", 10, "S3 advanced", "How can S3 trigger processing when an object is uploaded?", "Configure S3 Event Notifications to targets such as Lambda, SQS, SNS, or EventBridge.", "Trigger a Lambda function from a new object event."),
    Card("d10-q19", 10, "S3 advanced", "When should multipart upload be used?", "Use multipart upload for large objects to improve throughput, upload parts in parallel, and resume failed parts.", "Add a lifecycle rule for incomplete multipart uploads."),
    Card("d10-q20", 10, "S3 advanced", "What feature speeds S3 uploads for distant users through AWS edge locations?", "S3 Transfer Acceleration can improve long-distance uploads by routing traffic through AWS edge locations.", "Decide whether a global upload app should test acceleration."),
    Card("d10-q21", 10, "S3 advanced", "What is S3 Inventory used for?", "S3 Inventory generates scheduled reports about objects and metadata such as encryption status, storage class, replication status, and versioning.", "Use inventory to audit unencrypted objects."),
    Card("d10-q22", 10, "S3 advanced", "How do you apply an action to millions of existing S3 objects?", "Use S3 Batch Operations with an inventory report or manifest.", "Plan a batch tagging job for old objects."),
    Card("d10-q23", 10, "S3 advanced", "What is the difference between S3 Select and Athena?", "S3 Select retrieves subsets from one object, while Athena runs SQL across datasets in S3.", "Choose Athena for a data-lake query across many files."),
    Card("d10-q24", 10, "S3 advanced", "What should you use to migrate large on-premises file datasets into S3?", "Use AWS DataSync to automate and accelerate migration from supported on-premises or edge storage sources into S3.", "Plan a DataSync migration from NFS to S3."),
    Card("d10-q25", 10, "S3 advanced", "What does S3 Requester Pays do?", "Requester Pays makes the requester pay request and data-transfer costs instead of the bucket owner.", "Choose Requester Pays for a shared public dataset."),
    Card("d11-q1", 11, "Databases overview", "When should you choose Amazon RDS?", "Choose RDS when you need a managed relational database engine such as MySQL, PostgreSQL, MariaDB, Oracle, or SQL Server.", "Match RDS to a relational app requirement."),
    Card("d11-q2", 11, "Databases overview", "When should you choose DynamoDB?", "Choose DynamoDB for serverless NoSQL workloads that need high scale, key-value or document access, and single-digit millisecond latency.", "Map a shopping cart access pattern to DynamoDB."),
    Card("d11-q3", 11, "Databases overview", "When should you choose Redshift?", "Choose Redshift for managed data warehousing and analytics across large structured datasets, not for transactional OLTP workloads.", "Identify an analytics workload for Redshift."),
    Card("d12-q1", 12, "RDS and Aurora", "What does RDS Multi-AZ provide?", "RDS Multi-AZ provides high availability by maintaining a standby in another Availability Zone and failing over during outages or maintenance.", "Design an RDS deployment with Multi-AZ enabled."),
    Card("d12-q2", 12, "RDS and Aurora", "What are RDS read replicas used for?", "Read replicas scale read traffic and can support some disaster recovery patterns. They are not the primary high-availability failover feature.", "Add read replicas to a read-heavy design."),
    Card("d12-q3", 12, "RDS and Aurora", "Why is Amazon Aurora high-yield for the exam?", "Aurora uses AWS-designed distributed storage, supports fast failover, read replicas, automated backups, and strong performance for relational workloads.", "Compare Aurora benefits against standard RDS."),
    Card("d13-q1", 13, "DynamoDB", "What is a DynamoDB partition key?", "The partition key determines the physical partition where an item is stored. Choose a high-cardinality key with even access distribution.", "Pick a partition key for a cart table."),
    Card("d13-q2", 13, "DynamoDB", "What is a DynamoDB sort key?", "A sort key orders items with the same partition key and enables range queries and one-to-many access patterns.", "Use a sort key to model cart line items."),
    Card("d13-q3", 13, "DynamoDB", "When should you use DynamoDB global tables?", "Use global tables for active-active multi-Region DynamoDB applications that need low-latency regional reads and writes.", "Design a cart table for two Regions."),
    Card("d14-q1", 14, "Networking basics", "What is a VPC?", "A VPC is a logically isolated virtual network where you define IP ranges, subnets, routing, gateways, and network security controls.", "Draw a VPC CIDR block."),
    Card("d14-q2", 14, "Networking basics", "What makes a subnet public?", "A subnet is public when its route table sends internet-bound traffic to an internet gateway and resources have public IP addressing as needed.", "Mark public subnets in a VPC diagram."),
    Card("d14-q3", 14, "Networking basics", "What does a NAT Gateway do?", "A NAT Gateway lets resources in private subnets initiate outbound internet access without allowing unsolicited inbound internet connections.", "Place a NAT Gateway in a public subnet."),
    Card("d15-q1", 15, "Network security", "What is a security group?", "A security group is a stateful virtual firewall attached to an elastic network interface. It supports allow rules only.", "Write a security group rule for HTTPS."),
    Card("d15-q2", 15, "Network security", "What is a network ACL?", "A network ACL is a stateless subnet-level firewall. It supports allow and deny rules for inbound and outbound traffic.", "Write matching inbound and outbound NACL rules."),
    Card("d15-q3", 15, "Network security", "What are VPC Flow Logs used for?", "VPC Flow Logs record metadata about accepted and rejected IP traffic for VPCs, subnets, or network interfaces.", "Use flow logs to investigate blocked traffic."),
    Card("d16-q1", 16, "Hybrid networking", "When should you use AWS Site-to-Site VPN?", "Use Site-to-Site VPN for encrypted connectivity between on-premises networks and AWS over the internet.", "Choose VPN for a quick encrypted hybrid link."),
    Card("d16-q2", 16, "Hybrid networking", "When should you use AWS Direct Connect?", "Use Direct Connect when you need private, dedicated connectivity with more consistent network performance than internet-based VPN.", "Choose Direct Connect for steady hybrid traffic."),
    Card("d16-q3", 16, "Hybrid networking", "What is the main exam trap with VPC peering?", "VPC peering is not transitive. If VPC A peers with B and B peers with C, A cannot reach C through B.", "Draw a non-transitive peering example."),
    Card("d17-q1", 17, "DNS and CDN", "What does Route 53 do?", "Route 53 provides DNS hosted zones, domain registration, health checks, and routing policies for directing users to endpoints.", "Create a simple hosted-zone diagram."),
    Card("d17-q2", 17, "DNS and CDN", "What does CloudFront do?", "CloudFront is a content delivery network that caches content at edge locations to reduce latency and offload origins.", "Put CloudFront in front of an S3 static site."),
    Card("d17-q3", 17, "DNS and CDN", "What is CloudFront origin access control?", "Origin access control lets CloudFront securely access a private S3 bucket so users cannot bypass CloudFront and reach S3 directly.", "Sketch private S3 access through CloudFront."),
    Card("d18-q1", 18, "Serverless", "What does AWS Lambda do?", "Lambda runs code in response to events without requiring you to manage servers. It is best for event-driven, short-running compute.", "Add Lambda to an event-driven diagram."),
    Card("d18-q2", 18, "Serverless", "What does API Gateway do?", "API Gateway creates and manages APIs, handles request routing, throttling, authorization options, and integration with backends such as Lambda.", "Place API Gateway before a Lambda function."),
    Card("d18-q3", 18, "Serverless", "What does EventBridge do?", "EventBridge routes events from AWS services, SaaS providers, and custom applications to targets using event buses and rules.", "Create an event rule for a business event."),
    Card("d19-q1", 19, "Messaging", "When should you use SQS Standard?", "Use SQS Standard for high-throughput decoupling when at-least-once delivery and best-effort ordering are acceptable.", "Put SQS between a producer and worker."),
    Card("d19-q2", 19, "Messaging", "When should you use SQS FIFO?", "Use SQS FIFO when message ordering within a group and exactly-once processing semantics are required.", "Identify a workload that needs ordered messages."),
    Card("d19-q3", 19, "Messaging", "When should you use SNS?", "Use SNS for pub/sub fan-out when one published message should notify multiple subscribers such as queues, Lambda functions, or endpoints.", "Fan out one alert to multiple targets."),
    Card("d20-q1", 20, "Containers", "What is Amazon ECS?", "Amazon ECS is AWS-native container orchestration for running and scaling containers without needing Kubernetes.", "Choose ECS for an AWS-native container service."),
    Card("d20-q2", 20, "Containers", "What is Amazon EKS?", "Amazon EKS is managed Kubernetes on AWS. Choose it when you need Kubernetes APIs, ecosystem compatibility, or portability.", "Choose EKS for a Kubernetes requirement."),
    Card("d20-q3", 20, "Containers", "What is AWS Fargate?", "Fargate is serverless compute for containers. It runs ECS or EKS tasks without you managing EC2 worker nodes.", "Pick Fargate for a small operations team."),
    Card("d21-q1", 21, "Storage services", "When should you use Amazon EFS?", "Use EFS for shared elastic Linux file storage over NFS across multiple EC2 instances or containers.", "Mount EFS from two Linux instances."),
    Card("d21-q2", 21, "Storage services", "When should you use Amazon FSx for Windows File Server?", "Use FSx for Windows File Server when applications need managed Windows file shares, SMB protocol, and Active Directory integration.", "Choose FSx for a Windows file-share scenario."),
    Card("d21-q3", 21, "Storage services", "What is AWS DataSync used for?", "DataSync automates and accelerates data movement between on-premises storage, edge locations, and AWS storage services.", "Plan a migration from on-premises NFS to AWS."),
    Card("d22-q1", 22, "Monitoring", "What does CloudWatch provide?", "CloudWatch provides metrics, logs, dashboards, alarms, and events for monitoring AWS resources and applications.", "Create an alarm for high CPU."),
    Card("d22-q2", 22, "Monitoring", "What does CloudTrail record?", "CloudTrail records AWS API activity, including who made a request, when it happened, and which resources were affected.", "Use CloudTrail to find who changed a security group."),
    Card("d22-q3", 22, "Monitoring", "What does AWS Config track?", "AWS Config records resource configuration history and evaluates resources against compliance rules.", "Use Config to detect unencrypted resources."),
    Card("d23-q1", 23, "Security services", "What is AWS KMS used for?", "KMS creates and manages encryption keys used by AWS services and applications for encryption and decryption operations.", "Choose KMS for encrypting an RDS database."),
    Card("d23-q2", 23, "Security services", "What is AWS WAF used for?", "AWS WAF filters HTTP and HTTPS requests using rules that block common web attacks such as SQL injection and cross-site scripting.", "Place WAF in front of CloudFront or an ALB."),
    Card("d23-q3", 23, "Security services", "What is GuardDuty used for?", "GuardDuty is a threat detection service that analyzes logs and signals to identify suspicious or malicious activity.", "Use GuardDuty findings in an incident review."),
    Card("d24-q1", 24, "Reliability", "What is a backup and restore disaster recovery strategy?", "Backup and restore stores backups and rebuilds the environment after a disaster. It is low cost but usually has higher RTO and RPO.", "Choose backup and restore for a low-budget workload."),
    Card("d24-q2", 24, "Reliability", "What is a pilot light disaster recovery strategy?", "Pilot light keeps critical core components running in another Region while the full environment is scaled up during recovery.", "Identify the minimum components for pilot light."),
    Card("d24-q3", 24, "Reliability", "What is a warm standby disaster recovery strategy?", "Warm standby runs a scaled-down functional environment that can scale up quickly during a disaster.", "Compare warm standby against pilot light."),
    Card("d25-q1", 25, "Cost optimization", "How does right sizing reduce AWS cost?", "Right sizing matches resource size to actual demand so you do not overpay for unused CPU, memory, storage, or throughput.", "Review one EC2 instance for overprovisioning."),
    Card("d25-q2", 25, "Cost optimization", "How can Spot Instances reduce cost?", "Spot Instances use spare EC2 capacity at large discounts, but they can be interrupted. Use them only for interruption-tolerant work.", "Find a batch workload suitable for Spot."),
    Card("d25-q3", 25, "Cost optimization", "How does S3 Intelligent-Tiering help with cost?", "S3 Intelligent-Tiering moves objects between access tiers automatically when access patterns are unknown or changing.", "Choose Intelligent-Tiering for unpredictable object access."),
    Card("d26-q1", 26, "Architecture patterns", "Why is stateless compute important?", "Stateless compute stores session state outside instances so workloads can scale horizontally and replace failed instances easily.", "Move session state out of a web server."),
    Card("d26-q2", 26, "Architecture patterns", "Why is caching used in AWS architectures?", "Caching reduces latency, lowers backend load, and can improve resilience during read spikes.", "Add a cache to a read-heavy application."),
    Card("d26-q3", 26, "Architecture patterns", "Why is decoupling used in AWS architectures?", "Decoupling separates components so failures and traffic spikes do not immediately cascade through the whole system.", "Put a queue between web and worker tiers."),
    Card("d27-q1", 27, "Exam domain review", "What does secure architecture mean on the SAA-C03 exam?", "Secure architecture focuses on least privilege, encryption, private access where appropriate, network controls, logging, and protection from common threats.", "Rewrite one security topic as a decision rule."),
    Card("d27-q2", 27, "Exam domain review", "What does resilient architecture mean on the SAA-C03 exam?", "Resilient architecture keeps workloads available through failures using Multi-AZ, backups, failover, loose coupling, and recovery planning.", "Rewrite one resilience topic as a decision rule."),
    Card("d27-q3", 27, "Exam domain review", "What does cost-optimized architecture mean on the SAA-C03 exam?", "Cost-optimized architecture meets requirements at the lowest reasonable cost without breaking availability, performance, or security constraints.", "Rewrite one cost topic as a decision rule."),
    Card("d28-q1", 28, "Practice exam 1", "What should you document for a wrong practice-exam answer?", "Document why your answer was tempting, why it was wrong, why the correct answer wins, and the decision rule to remember.", "Review every wrong answer."),
    Card("d28-q2", 28, "Practice exam 1", "How should you handle uncertain practice-exam questions?", "Mark uncertain questions, choose the best answer on the first pass, then return after finishing the full set.", "Practice marking and revisiting questions."),
    Card("d28-q3", 28, "Practice exam 1", "What should you do after a timed practice exam?", "Review wrong and guessed questions first, group misses by topic, and retake targeted flashcards for weak areas.", "Build a weak-topic list."),
    Card("d29-q1", 29, "Practice exam 2", "What does 'least operational effort' usually imply?", "It usually points toward managed services, serverless options, automation, and avoiding custom administration when requirements allow.", "Find least-operational-effort wording in a question."),
    Card("d29-q2", 29, "Practice exam 2", "What does 'real-time' usually imply in service selection?", "Real-time usually requires low-latency streaming, event processing, or immediate delivery rather than batch movement.", "Identify whether a scenario needs streaming."),
    Card("d29-q3", 29, "Practice exam 2", "What does 'no code changes' imply in an AWS scenario?", "Prefer infrastructure, routing, configuration, migration, caching, or managed-service options that do not require modifying application logic.", "Eliminate answers requiring application rewrites."),
    Card("d30-q1", 30, "Final review", "Which IAM rule is high-yield for final review?", "Use roles and temporary credentials instead of long-term access keys wherever possible.", "Retake IAM missed cards."),
    Card("d30-q2", 30, "Final review", "Which VPC rule is high-yield for final review?", "Public subnets route to an internet gateway; private subnets usually use NAT Gateway for outbound-only internet access.", "Retake VPC missed cards."),
    Card("d30-q3", 30, "Final review", "Which S3 rule is high-yield for final review?", "Keep buckets private by default, use Block Public Access, enable encryption, and use lifecycle rules for cost control.", "Retake S3 missed cards."),
    Card("vpc-q1", 14, "VPC", "Is a VPC regional or global?", "Regional.", "Note the Region selector when creating a VPC."),
    Card("vpc-q2", 14, "VPC", "Is a subnet regional or Availability Zone scoped?", "Availability Zone scoped.", "Map subnets to specific AZs in a diagram."),
    Card("vpc-q3", 14, "VPC", "What makes a subnet public?", "Its route table has a route to an internet gateway, and resources use public IP addressing.", "Trace a public subnet route to an internet gateway."),
    Card("vpc-q4", 14, "VPC", "What lets private subnet instances initiate outbound IPv4 internet access?", "A NAT gateway in a public subnet.", "Place a NAT gateway in a public subnet."),
    Card("vpc-q5", 14, "VPC", "What is the IPv6 equivalent for outbound-only internet access?", "An egress-only internet gateway.", "Add an egress-only internet gateway for IPv6."),
    Card("vpc-q6", 14, "VPC", "Which VPC firewall is stateful?", "Security group.", "Recall that return traffic is auto-allowed."),
    Card("vpc-q7", 14, "VPC", "Which VPC firewall is stateless?", "Network ACL.", "Recall that return traffic needs its own rule."),
    Card("vpc-q8", 14, "VPC", "Do security groups support explicit deny rules?", "No. Security groups support allow rules only.", "Design access using allow rules only."),
    Card("vpc-q9", 14, "VPC", "Do network ACLs support allow and deny rules?", "Yes.", "Write a NACL deny rule for a specific CIDR."),
    Card("vpc-q10", 14, "VPC", "What route is automatically present in every VPC route table?", "The local route for VPC-internal traffic.", "Find the local route in a route table."),
    Card("vpc-q11", 14, "VPC", "What VPC component enables internet access for public subnets?", "Internet gateway.", "Attach an internet gateway to a VPC."),
    Card("vpc-q12", 14, "VPC", "For high availability, how should NAT gateways be deployed?", "Deploy a NAT gateway in each Availability Zone used by private workloads.", "Add a NAT gateway per AZ in a design."),
    Card("vpc-q13", 14, "VPC", "Which endpoint type supports S3 and DynamoDB through route tables?", "Gateway VPC endpoint.", "Add a gateway endpoint route for S3."),
    Card("vpc-q14", 14, "VPC", "Which endpoint type uses elastic network interfaces and PrivateLink?", "Interface VPC endpoint.", "Identify the ENI created by an interface endpoint."),
    Card("vpc-q15", 14, "VPC", "What service helps privately expose a service to consumers without public internet routing?", "AWS PrivateLink.", "Sketch a provider service reached via PrivateLink."),
    Card("vpc-q16", 14, "VPC", "Is VPC peering transitive?", "No.", "Draw a non-transitive peering example."),
    Card("vpc-q17", 14, "VPC", "What is the best AWS networking hub for connecting many VPCs and on-premises networks?", "AWS Transit Gateway.", "Replace a peering mesh with a Transit Gateway hub."),
    Card("vpc-q18", 14, "VPC", "What hybrid connection uses encrypted tunnels over the internet?", "AWS Site-to-Site VPN.", "Choose VPN for a quick encrypted hybrid link."),
    Card("vpc-q19", 14, "VPC", "What hybrid connection provides a dedicated private network link to AWS?", "AWS Direct Connect.", "Choose Direct Connect for steady private traffic."),
    Card("vpc-q20", 14, "VPC", "What captures metadata about accepted and rejected IP traffic in a VPC?", "VPC Flow Logs.", "Enable flow logs to investigate blocked traffic."),
    Card("vpc-q21", 14, "VPC", "Do VPC Flow Logs capture packet payloads?", "No. They capture flow metadata, not payloads.", "Note that payload inspection needs packet mirroring."),
    Card("vpc-q22", 14, "VPC", "What tool can analyze whether one AWS resource can reach another through a network path?", "VPC Reachability Analyzer.", "Run a reachability check between two instances."),
    Card("vpc-q23", 14, "VPC", "Where are security groups attached?", "To elastic network interfaces.", "Find the security groups on an ENI."),
    Card("vpc-q24", 14, "VPC", "Where are network ACLs applied?", "At the subnet level.", "Associate a NACL with a subnet."),
    Card("vpc-q25", 14, "VPC", "If a private subnet needs private access to S3 without internet routing, what should you use?", "An S3 gateway VPC endpoint.", "Add an S3 gateway endpoint to a route table."),
    Card("vpc-q26", 14, "VPC", "If two VPCs have overlapping CIDR blocks, can they be peered?", "No.", "Check CIDR overlap before peering."),
    Card("vpc-q27", 14, "VPC", "What must be updated after creating VPC peering?", "Route tables, and security rules if needed.", "Update route tables on both sides of a peering."),
    Card("vpc-q28", 14, "VPC", "Which VPC setting helps EC2 instances receive public DNS names when they have public IPs?", "DNS hostnames.", "Enable DNS hostnames on a VPC."),
    Card("vpc-q29", 14, "VPC", "What VPC feature can customize DNS servers handed to instances?", "DHCP options set.", "Configure a custom DHCP options set."),
    Card("vpc-q30", 14, "VPC", "What is the safest default architecture for databases in a VPC?", "Place databases in private subnets with restrictive security groups.", "Move a database into a private subnet."),
    # --- AWS Global Footprint (AWS basics) ---
    Card("gf-q1", 1, "AWS basics", "What is an AWS edge location?", "An edge location is an AWS site meant to deliver content with the lowest possible latency, closer to end users than Regions and AZs. Edge locations use points of presence and regional edge caches.", "Explain why CloudFront uses edge locations instead of a Region."),
    Card("gf-q2", 1, "AWS basics", "Why do AWS Regions provide the greatest fault tolerance and stability?", "Each Region is a completely separate geographic area hosting its own AWS data centers, so a problem in one Region does not affect workloads deployed in another Region.", "Deploy the same workload to two Regions for isolation."),
    Card("gf-q3", 1, "AWS basics", "Why are Availability Zones physically separate?", "AZs are isolated, independent locations within a Region with their own redundant power, networking, and low-latency links. Physical separation reduces the impact of a single disaster.", "Spread instances across AZs to survive one AZ failure."),
    Card("gf-q4", 1, "AWS basics", "In the shared responsibility model, what is security IN the cloud?", "Security in the cloud is the customer's responsibility: encrypting customer data, backing up customer data, and controlling access and authorization.", "List which security tasks belong to the customer."),
    Card("gf-q5", 1, "AWS basics", "In the shared responsibility model, what is security OF the cloud?", "Security of the cloud is AWS's responsibility: the software behind AWS services and the physical security and redundancy of the infrastructure.", "List which security tasks belong to AWS."),
    # --- Well-Architected Framework (new topic) ---
    Card("waf-q1", 1, "Well-Architected Framework", "What is the AWS Well-Architected Framework?", "It is a set of principles and best practices you should aim to apply to all AWS-based workloads, organized into six pillars.", "Name a design decision that improves a pillar in your workload."),
    Card("waf-q2", 1, "Well-Architected Framework", "What are the six pillars of the Well-Architected Framework?", "Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability.", "Recite the six pillars from memory."),
    Card("waf-q3", 1, "Well-Architected Framework", "What is the Operational Excellence pillar?", "The ability to support development, run workloads effectively, gain insight into operations, and continuously improve supporting processes to deliver business value. Example: operations as code, small frequent changes, using managed services.", "Turn a manual task into operations as code."),
    Card("waf-q4", 1, "Well-Architected Framework", "What is the Security pillar?", "Taking advantage of cloud technologies to protect data, systems, and assets. Example: maintaining traceability, applying security in layers, encrypting data in transit and at rest, and keeping people away from data.", "Add a layer of security to one workload."),
    Card("waf-q5", 1, "Well-Architected Framework", "What is the Reliability pillar?", "The ability for a workload to perform correctly and consistently and to recover quickly. Example: automating recovery from failure, testing recovery procedures, and scaling horizontally.", "Design an automated recovery step for a failure."),
    Card("waf-q6", 1, "Well-Architected Framework", "What is the Performance Efficiency pillar?", "The ability to use the correct computing resources and maintain efficiency as scaling demands change (remove bottlenecks, reduce waste). Example: using serverless architecture, deploying globally using Regions, and experimenting often.", "Pick a service that removes a scaling bottleneck."),
    Card("waf-q7", 1, "Well-Architected Framework", "What is the Cost Optimization pillar?", "The ability to run systems that deliver business value at the lowest price point (spend only what you have to). Example: adopting a consumption model, measuring overall efficiency, and letting AWS handle the heavy lifting of infrastructure.", "Find one workload that could spend less."),
    Card("waf-q8", 1, "Well-Architected Framework", "What is the Sustainability pillar?", "The ability to continually improve sustainability impact by reducing energy consumption, increasing efficiency across components, maximizing benefits from provisioned resources, and minimizing total resources required. Example: understand your impact, maximize utilization, use managed services.", "Identify a way to raise utilization and cut waste."),
    # --- High Availability & Fault Tolerance (new topic) ---
    Card("ha-q1", 1, "High availability and fault tolerance", "What is high availability?", "Systems designed to remain operational for long periods, where failures typically result in minimal downtime or brief interruptions, using redundancy and failover mechanisms to recover quickly.", "Add redundancy so one failure causes minimal downtime."),
    Card("ha-q2", 1, "High availability and fault tolerance", "What uptime goal is commonly associated with high availability?", "A goal of about 99.99% uptime.", "State the HA uptime target."),
    Card("ha-q3", 1, "High availability and fault tolerance", "How is high availability achieved in AWS?", "Through redundancy and failover, such as deploying across multiple Availability Zones (Multi-AZ), load balancing, and Auto Scaling to replace failed components.", "Draw a Multi-AZ design that survives one AZ loss."),
    Card("ha-q4", 1, "High availability and fault tolerance", "How does fault tolerance differ from high availability?", "High availability minimizes downtime and recovers quickly from failures, while fault tolerance lets a system keep operating with no downtime even when a component fails.", "Classify a design as HA versus fault tolerant."),
    # --- IAM overview (IAM) ---
    Card("iam-q1", 2, "IAM", "What is AWS IAM?", "AWS Identity and Access Management is a unique authentication database that is logically isolated to one AWS account. It lets you create users, groups, and roles and control access to AWS resources and services.", "Explain that IAM is scoped to one account."),
    Card("iam-q2", 2, "IAM", "What is the AWS root account and how should it be secured?", "The root account is the email address used to sign up for AWS and has full administrative access. Immediately turn on MFA, avoid using it for normal tasks, and do not create access keys for it.", "List the three root account do's and don'ts."),
    Card("iam-q3", 2, "IAM", "What is an IAM group and can a user belong to more than one?", "An IAM group is a collection of IAM users used to simplify permission management. A user can belong to multiple IAM groups at once, and groups can contain users only.", "Group users by job function."),
    Card("iam-q4", 2, "IAM", "What long-term credentials do IAM users have?", "IAM users authenticate with a username and password (console) or with static IAM access keys (programmatic).", "Identify the two IAM user credential types."),
    Card("iam-q5", 2, "IAM", "What permissions does a new IAM identity start with?", "New IAM identities always start with zero permissions; access is implicitly denied until a policy grants it.", "Remember that access must be explicitly granted."),
    # --- IAM Policies (IAM advanced) ---
    Card("iampol-q1", 3, "IAM advanced", "What is an IAM policy?", "A policy is an object in AWS that, when associated with an identity or resource, defines their permissions.", "Attach a policy and describe what it allows."),
    Card("iampol-q2", 3, "IAM advanced", "How are identity-based policies written and stored?", "They are attached to IAM identities to grant permissions and are written and stored as JSON documents. By default, permissions are implicitly denied.", "Read the Effect, Action, and Resource of a JSON policy."),
    Card("iampol-q3", 3, "IAM advanced", "What are the two forms of identity-based policies?", "Managed policies and inline policies.", "Decide managed versus inline for a reusable policy."),
    Card("iampol-q4", 3, "IAM advanced", "What are managed policies?", "Attachable, standalone, reusable policies that are given a resource ARN after creation. They come in two kinds: AWS managed policies (created and managed by AWS, usable by everyone) and customer managed policies (you create, manage, and reuse them however you want).", "Choose a customer managed policy for custom least privilege."),
    Card("iampol-q5", 3, "IAM advanced", "What is an inline policy?", "An inline policy is embedded directly into a single user, group, or role. It is not standalone or reusable and is deleted when the identity is deleted.", "Use inline only for a one-off permission."),
    Card("iampol-q6", 3, "IAM advanced", "What is a resource-based policy?", "A resource-based policy is attached directly to a resource (such as an S3 bucket or Lambda function) and specifies which principals may access that resource.", "Write a bucket policy that names an allowed principal."),
    Card("iampol-q7", 3, "IAM advanced", "What are the high-priority factors in IAM access evaluation?", "Know the order: an explicit deny always wins, then Service Control Policies, then resource-based policies, and permission boundaries and identity-based allows must also permit the action.", "Trace why an allowed principal is still denied."),
    Card("iampol-q8", 3, "IAM advanced", "Which IAM condition keys are commonly tested?", "ExternalId, aws:MultiFactorAuthPresent, aws:SourceIp, and aws:PrincipalOrgID.", "Add a condition requiring MFA or a source IP range."),
    # --- Directory Services (new topic) ---
    Card("ds-q1", 3, "Directory services", "What does AWS Directory Service provide?", "It provides several options to set up and run Microsoft Active Directory (AD) with other AWS services, offloading the painful parts of keeping AD on-premises while still giving you the control and flexibility of AD.", "Match a directory need to a Directory Service option."),
    Card("ds-q2", 3, "Directory services", "What is AWS Managed Microsoft AD?", "It is the entire Active Directory suite run and managed by AWS, and it supports trusts with an existing on-premises Active Directory.", "Choose Managed Microsoft AD when full AD features are needed."),
    Card("ds-q3", 3, "Directory services", "What is AD Connector?", "AD Connector is a directory gateway that redirects directory requests to your on-premises Active Directory without caching information in the cloud.", "Use AD Connector to reuse an existing on-prem AD."),
    Card("ds-q4", 3, "Directory services", "What is Simple AD?", "Simple AD is a standalone, Samba-based directory that is compatible with basic Active Directory features, at low cost.", "Pick Simple AD for basic, low-cost directory needs."),
    # --- VPC fundamentals & peering additions (VPC) ---
    Card("vpc-q31", 14, "VPC", "How should you think about an Amazon VPC?", "Think of a VPC as your very own virtual data center network in the cloud: a logically isolated part of AWS where you control the IP address ranges, subnets, route tables, and network gateways.", "Describe your VPC as a private cloud network."),
    Card("vpc-q32", 14, "VPC", "How is a default VPC created and what is its CIDR?", "A default VPC is automatically created by AWS when you create an AWS account, with a default CIDR of 172.31.0.0/16.", "Recall the default VPC CIDR block."),
    Card("vpc-q33", 14, "VPC", "What is a custom VPC?", "A custom VPC is created by you with a custom CIDR block range, giving more granular control over your network.", "Choose a custom CIDR for a new environment."),
    Card("vpc-q34", 14, "VPC", "What IPv4 CIDR block sizes are allowed for a VPC?", "A private IPv4 CIDR block is required and can range from /16 to /28.", "Pick a valid IPv4 CIDR size for a VPC."),
    Card("vpc-q35", 14, "VPC", "What IPv6 CIDR block sizes are allowed for a VPC?", "An IPv6 CIDR block is optional and ranges from /44 to /60.", "Note that IPv6 CIDR is optional on a VPC."),
    Card("vpc-q36", 14, "VPC", "What are the important components of a VPC?", "CIDR block, subnets, route tables, security groups, network ACLs, and network gateways.", "Label these components in a VPC diagram."),
    Card("vpc-q37", 14, "VPC", "What is VPC peering and where does its traffic stay?", "VPC peering enables secure, direct communication between VPCs so private resources can interact. Traffic remains within the AWS network infrastructure and there is no single point of failure for the connection.", "Connect two VPCs privately with peering."),
    Card("vpc-q38", 14, "VPC", "What scopes can VPC peering connect?", "Peering can connect VPCs cross-account, in the same account, and even cross-Region.", "List the three peering scopes."),
    Card("vpc-q39", 14, "VPC", "What are common VPC peering use cases?", "A centralized shared-services VPC, multi-Region internal application deployment, and cross-account VPC integration for collaboration or a merger/acquisition.", "Match a scenario to a peering use case."),
    Card("vpc-q40", 14, "VPC", "AWS Transit Gateway: what is it, when do you use it, and why?", "What: a regional network hub that connects many VPCs and on-premises networks (VPN/Direct Connect) through a single central gateway, with transitive routing. When: when you have many VPCs and/or hybrid connections and a full peering mesh becomes hard to manage. Why: peering is not transitive and a mesh grows to N-squared connections, so a hub-and-spoke Transit Gateway simplifies routing and scales connectivity centrally.", "Replace a tangled peering mesh with one Transit Gateway hub."),
    Card("vpc-q41", 14, "VPC", "AWS Site-to-Site VPN: what is it, when do you use it, and why?", "What: an encrypted IPsec tunnel connecting an on-premises network to a VPC over the public internet. When: when you need hybrid connectivity quickly and can tolerate internet-based performance. Why: it is fast to set up and low cost compared to dedicated links, and encryption keeps traffic private even though it traverses the public internet.", "Choose VPN for a quick, encrypted hybrid link."),
    Card("vpc-q42", 14, "VPC", "Gateway VPC endpoint: what is it, when do you use it, and why?", "What: a VPC endpoint that adds a route-table target to reach S3 and DynamoDB privately. When: when private-subnet resources need to reach S3 or DynamoDB without internet routing. Why: traffic stays on the AWS network instead of going through an internet or NAT gateway, improving security and avoiding NAT data-processing cost. It is also free.", "Add an S3 gateway endpoint route to a private subnet's route table."),
    Card("vpc-q43", 14, "VPC", "DHCP options set: what is it, when do you use it, and why?", "What: a VPC configuration that controls the DHCP settings handed to instances, such as domain name and DNS servers. When: when you need instances to use custom DNS servers or a specific domain name (for example, to resolve on-premises hostnames). Why: it lets you override the default Amazon-provided DNS so instances integrate with your own naming and resolution.", "Configure a custom DHCP options set pointing at your DNS servers."),
    Card("vpc-q44", 14, "VPC", "AWS Direct Connect: what is it, when do you use it, and why?", "What: a dedicated, private physical network link between your data center and AWS. When: when you need consistent, high-throughput hybrid connectivity and predictable latency for steady traffic. Why: it bypasses the public internet, giving more reliable performance and often lower data-transfer cost than internet-based VPN for large, ongoing workloads.", "Choose Direct Connect for steady, high-volume hybrid traffic."),
    Card("vpc-q45", 14, "VPC", "VPC DNS hostnames: what are they, when do you enable them, and why?", "What: a VPC setting that gives instances public DNS hostnames when they have public IP addresses. When: enable it when instances need to be reachable or identified by a public DNS name rather than only by IP. Why: it lets other services and users resolve instances by name, which is required for many public-facing and name-based access patterns.", "Enable DNS hostnames on a VPC hosting public instances."),
    Card("vpc-q46", 14, "VPC", "S3 gateway VPC endpoint: what is it, when do you use it, and why?", "What: a gateway-type VPC endpoint specifically for private access to Amazon S3 via route-table entries. When: when instances in a private subnet must read from or write to S3 without a NAT gateway or internet gateway. Why: it keeps S3 traffic inside the AWS network for better security, removes exposure to the internet, and avoids NAT processing charges (the endpoint itself is free).", "Add an S3 gateway endpoint so a private subnet reaches S3 without internet routing."),
    Card("vpc-q47", 14, "VPC", "VPC Reachability Analyzer: what is it, when do you use it, and why?", "What: a network diagnostic tool that analyzes the configured path between two resources and reports whether traffic can reach the destination. When: when you are troubleshooting connectivity or want to validate a path before deploying. Why: it inspects security groups, NACLs, route tables, and gateways to pinpoint exactly where a path is blocked, without sending real packets.", "Run a reachability check between two instances to find a blocked hop."),
    Card("vpc-q48", 14, "VPC", "AWS PrivateLink and interface VPC endpoints: what are they, when do you use them, and why?", "What: an interface VPC endpoint creates an elastic network interface with a private IP in your subnet, and AWS PrivateLink uses it to privately connect to AWS services, partner services, or your own services. When: when you need private access to a service that is not supported by gateway endpoints, or to expose your own service to consumers privately. Why: traffic never leaves the AWS network and consumers reach the service by private IP, avoiding public internet exposure and overlapping-CIDR problems.", "Add an interface endpoint so a private subnet reaches an AWS service over PrivateLink."),
    # --- VPC deep dive: public/private subnets ---
    Card("vpc-q49", 14, "VPC", "How many IP addresses are usable in a VPC subnet?", "AWS reserves 5 IP addresses in every subnet (the first four and the last one). For example, a /24 has 256 addresses but only 251 are usable. This is a classic capacity-planning gotcha.", "Subtract 5 reserved IPs when sizing a subnet."),
    Card("vpc-q50", 14, "VPC", "Can a VPC use more than one CIDR block?", "Yes. A VPC has a primary IPv4 CIDR and can have secondary CIDR blocks added later to expand its address space.", "Add a secondary CIDR when a VPC runs low on IPs."),
    Card("vpc-q51", 14, "VPC", "What actually makes a subnet public versus private?", "Only its route table. A subnet is public when its route table has a 0.0.0.0/0 route to an internet gateway; it is private when that route points to a NAT (or is absent). There is no 'public' checkbox - NAT, IGW, and security groups only support the routing decision.", "Read a route table to classify a subnet."),
    Card("vpc-q52", 14, "VPC", "How many internet gateways can a VPC have and where is it attached?", "One IGW per VPC, attached to the VPC itself (not to a subnet). It is horizontally scaled and redundant, and performs 1:1 NAT for instances that have a public IP.", "Attach a single IGW to the VPC."),
    Card("vpc-q53", 14, "VPC", "What is the local route in a route table?", "Every route table automatically includes a local route (for example 10.0.0.0/16 -> local) that lets all resources inside the VPC communicate. It cannot be removed.", "Find the non-removable local route."),
    Card("vpc-q54", 14, "VPC", "Where must a NAT gateway be placed, and why?", "In a public subnet, because it needs its own route to the internet gateway to forward outbound traffic from private subnets. Placing it in a private subnet is a common mistake.", "Put the NAT gateway in a public subnet."),
    Card("vpc-q55", 14, "VPC", "How do you make outbound internet access from private subnets highly available?", "Deploy one NAT gateway per Availability Zone and point each AZ's private route table at its local NAT gateway. A single NAT gateway is an AZ-level single point of failure - if that AZ fails, all private subnets lose internet access.", "Add a NAT gateway per AZ for HA."),
    Card("vpc-q56", 14, "VPC", "NAT gateway versus NAT instance?", "A NAT gateway is AWS-managed, auto-scaling, and highly available within an AZ - the exam's best-practice answer. A NAT instance is a self-managed EC2 acting as NAT: legacy, cheaper for low traffic, but you manage patching, scaling, and failover yourself.", "Pick NAT gateway as the best-practice option."),
    Card("vpc-q57", 14, "VPC", "What does a NAT gateway require for a stable outbound address?", "An Elastic IP - a static public IPv4 address associated with the NAT gateway.", "Attach an EIP when creating a NAT gateway."),
    Card("vpc-q58", 14, "VPC", "How do you make a database subnet the most secure, beyond security groups?", "Place the database in an isolated subnet whose route table has no 0.0.0.0/0 route to an IGW or NAT at all. The database never needs outbound internet, so removing the route provides defense in depth even if a security group is misconfigured.", "Give a DB subnet no internet route."),
    Card("vpc-q59", 14, "VPC", "What are the key differences between security groups and network ACLs?", "Security group: instance/ENI level, stateful (return traffic auto-allowed), allow rules only, all rules evaluated, default denies inbound and allows outbound, applies only to instances that reference it. Network ACL: subnet level, stateless (must allow both directions), allow and deny rules, rules processed in number order with first match winning, applies to every instance in the subnet.", "Fill in an SG-versus-NACL comparison from memory."),
    Card("vpc-q60", 14, "VPC", "Why must network ACLs allow the ephemeral port range?", "Because NACLs are stateless, return traffic is not automatically allowed. You must explicitly open the ephemeral port range (1024-65535) for responses. Security groups do not need this because they are stateful.", "Add an outbound/inbound ephemeral-port rule to a NACL."),
    Card("vpc-q61", 14, "VPC", "Gateway endpoint versus interface (PrivateLink) endpoint?", "Gateway endpoint: free, only for S3 and DynamoDB, added as a route-table target. Interface endpoint (PrivateLink): an ENI with a private IP in your subnet, works for most other AWS services, and incurs hourly plus data-processing cost.", "Choose gateway for S3/DynamoDB, interface for others."),
    Card("vpc-q62", 14, "VPC", "How does a private-subnet EC2 instance reach S3 without a NAT gateway?", "Use an S3 Gateway VPC endpoint. It is the exam-correct answer because it is cheaper, more secure, and keeps traffic off the internet entirely with no internet exposure.", "Replace a NAT path to S3 with a gateway endpoint."),
    Card("vpc-q63", 14, "VPC", "How do you get SSH/RDP access to private instances without exposing them?", "Use a bastion host in a public subnet, or better, AWS Systems Manager Session Manager, which needs no open SSH port and no bastion host at all.", "Prefer Session Manager over an open SSH bastion."),
    Card("vpc-q64", 14, "VPC", "What is special about the default VPC?", "Every AWS account gets a default VPC per Region, with a default subnet in every AZ that is public by default. Custom VPCs, by contrast, have no subnets or internet routing until you create them.", "Contrast default (all public) with custom VPCs."),
    Card("vpc-q65", 14, "VPC", "Can a subnet span multiple Availability Zones?", "No. A subnet lives in exactly one Availability Zone and cannot span AZs. High availability comes from spreading subnets across multiple AZs.", "Map each subnet to a single AZ."),
    # --- Service Definitions (SAA-C03 service catalog: definition + use case) ---
    # Compute
    Card("svc-q1", 0, "Service Definitions", "EC2 (Elastic Compute Cloud): definition and use case?", "Virtual servers in the cloud where you choose instance type (CPU/RAM/network profile), OS, and storage. Use for general-purpose workloads, hosting apps, and when you need full OS control. Key concepts: On-Demand, Reserved Instances, Spot, Savings Plans, and instance families (T=burstable, M=general, C=compute-optimized, R=memory-optimized, I=storage-optimized).", "Match an instance family letter to a workload."),
    Card("svc-q2", 0, "Service Definitions", "Auto Scaling Groups (ASG): definition and use case?", "Automatically adds or removes EC2 instances based on demand or a schedule. Use for maintaining availability and controlling cost by matching capacity to load.", "Set desired/min/max capacity for a scaling group."),
    Card("svc-q3", 0, "Service Definitions", "Elastic Load Balancing (ELB): definition, types, and use case?", "Distributes incoming traffic across multiple targets (EC2, containers, IPs). Types: Application Load Balancer (Layer 7, HTTP/HTTPS routing), Network Load Balancer (Layer 4, ultra-high performance/static IP), Gateway Load Balancer (third-party appliances). Use for high availability, fault tolerance, and distributing traffic.", "Pick ALB vs NLB vs GWLB for a scenario."),
    Card("svc-q4", 0, "Service Definitions", "AWS Lambda: definition, limits, and use case?", "Serverless, event-driven compute that runs code without provisioning servers, billed per invocation/duration. Use for short-lived tasks, event processing (S3 triggers, API Gateway backends), microservices, and glue logic. Limits to know: 15-minute max execution; memory and CPU scale together.", "Recall the 15-minute Lambda execution limit."),
    Card("svc-q5", 0, "Service Definitions", "Elastic Beanstalk: definition and use case?", "A PaaS where you upload code and AWS handles provisioning, load balancing, scaling, and monitoring. Use for quickly deploying web apps without managing infrastructure directly.", "Choose Beanstalk to deploy an app fast without ops."),
    Card("svc-q6", 0, "Service Definitions", "ECS, EKS, and Fargate: definitions and use case?", "ECS is AWS's native container orchestration service; EKS is managed Kubernetes; Fargate is the serverless compute engine for containers (no EC2 management) that works with both ECS and EKS. Use for containerized applications at scale.", "Choose Fargate when you don't want to manage nodes."),
    # Storage
    Card("svc-q7", 0, "Service Definitions", "Amazon S3 (Simple Storage Service): definition, features, and use case?", "Object storage with virtually unlimited capacity and 11 nines durability. Storage classes: Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier Instant Retrieval, Glacier Flexible Retrieval, Glacier Deep Archive. Use for static website hosting, backups, data lakes, and any unstructured data. Key features: versioning, lifecycle policies, cross-region replication, encryption (SSE-S3, SSE-KMS, SSE-C).", "Match a storage class to an access pattern."),
    Card("svc-q8", 0, "Service Definitions", "EBS (Elastic Block Store): definition, types, and use case?", "Persistent block storage volumes attached to EC2 instances, like a virtual hard drive. Types: gp3/gp2 (general SSD), io1/io2 (provisioned IOPS for high-performance DBs), st1 (throughput HDD), sc1 (cold HDD). Use for boot volumes and databases needing low-latency block storage. Tied to a single AZ.", "Pick an EBS type for a high-IOPS database."),
    Card("svc-q9", 0, "Service Definitions", "EFS (Elastic File System): definition and use case?", "Managed, scalable NFS file storage shareable across multiple EC2 instances and AZs. Use for shared file storage across many instances, such as content management or shared home directories.", "Choose EFS when multiple instances share files."),
    Card("svc-q10", 0, "Service Definitions", "S3 Glacier: definition and use case?", "Low-cost archival storage. Use for long-term backup/archive with infrequent, delayed access needs.", "Choose Glacier for cheap long-term archive."),
    Card("svc-q11", 0, "Service Definitions", "Storage Gateway: definition and use case?", "A hybrid storage service connecting on-premises environments to AWS storage. Use for extending on-prem storage to the cloud and backup/DR for hybrid environments.", "Bridge on-prem storage to AWS with Storage Gateway."),
    Card("svc-q12", 0, "Service Definitions", "AWS Backup: definition and use case?", "A centralized backup management service across AWS services. Use for automating and consolidating backup policies (EBS, RDS, DynamoDB, EFS, and more).", "Centralize backup policies across services."),
    # Databases
    Card("svc-q13", 0, "Service Definitions", "Amazon RDS (Relational Database Service): definition, features, and use case?", "Managed relational databases (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora-compatible). Use for traditional relational/transactional workloads; AWS handles patching, backups, and failover. Key features: Multi-AZ (failover/HA) and Read Replicas (scaling reads).", "Distinguish Multi-AZ (HA) from read replicas (scale)."),
    Card("svc-q14", 0, "Service Definitions", "Amazon Aurora: definition and use case?", "An AWS-built, MySQL/PostgreSQL-compatible relational database with higher performance and scalability than standard RDS. Use for high-performance relational workloads needing better throughput, with Aurora Serverless for variable workloads.", "Choose Aurora for high-throughput relational needs."),
    Card("svc-q15", 0, "Service Definitions", "Amazon DynamoDB: definition and use case?", "A fully managed, serverless NoSQL key-value/document database with single-digit millisecond latency at any scale. Use for high-scale, low-latency applications (gaming, IoT, mobile backends). Supports on-demand or provisioned capacity, and DAX for caching.", "Map a low-latency key-value pattern to DynamoDB."),
    Card("svc-q16", 0, "Service Definitions", "Amazon ElastiCache: definition and use case?", "Managed in-memory caching (Redis or Memcached). Use for speeding up application response times and reducing database load (session storage, leaderboards, caching layer).", "Add ElastiCache to cut database read load."),
    Card("svc-q17", 0, "Service Definitions", "Amazon Redshift: definition and use case?", "A managed data warehouse for large-scale analytics (petabyte scale, columnar storage). Use for business intelligence and complex analytical queries across large structured datasets.", "Choose Redshift for analytics, not OLTP."),
    # Networking & Content Delivery
    Card("svc-q18", 0, "Service Definitions", "Amazon VPC (Virtual Private Cloud): definition and key components?", "Your isolated, logically defined network within AWS. Key components: subnets (public/private), route tables, internet gateway (public access), NAT gateway (outbound-only internet for private subnets), security groups (stateful, instance-level firewall), and NACLs (stateless, subnet-level firewall).", "Label public vs private subnet routing."),
    Card("svc-q19", 0, "Service Definitions", "Amazon Route 53: definition, routing policies, and use case?", "A managed DNS service that also supports domain registration and health checks. Routing policies: Simple, Weighted, Latency-based, Failover, Geolocation, Geoproximity, Multi-value. Use for DNS resolution, traffic routing strategies, and domain health monitoring.", "Match a routing policy to a requirement."),
    Card("svc-q20", 0, "Service Definitions", "Amazon CloudFront: definition and use case?", "A content delivery network (CDN) that caches content at edge locations globally. Use for reducing latency for static/dynamic content, DDoS mitigation (with Shield), and it integrates with S3/ALB as origin.", "Put CloudFront in front of an S3 or ALB origin."),
    Card("svc-q21", 0, "Service Definitions", "AWS Direct Connect: definition and use case?", "A dedicated private network connection from on-premises to AWS that bypasses the public internet. Use for consistent, low-latency, high-bandwidth hybrid connectivity (versus VPN, which uses the public internet).", "Choose Direct Connect over VPN for steady bandwidth."),
    Card("svc-q22", 0, "Service Definitions", "AWS VPN (Site-to-Site / Client VPN): definition and use case?", "An encrypted connection over the public internet between on-prem and AWS, or between a client and AWS. Use for quick, lower-cost hybrid connectivity versus Direct Connect.", "Choose VPN for a fast, low-cost hybrid link."),
    Card("svc-q23", 0, "Service Definitions", "AWS Transit Gateway: definition and use case?", "A central hub connecting multiple VPCs and on-prem networks. Use for simplifying complex multi-VPC/multi-account network architectures (replaces messy VPC peering webs).", "Replace a peering mesh with a Transit Gateway."),
    Card("svc-q24", 0, "Service Definitions", "Amazon API Gateway: definition and use case?", "A fully managed service for creating, publishing, and securing APIs at scale. Use as the front door for applications to access backend services, often paired with Lambda.", "Place API Gateway in front of a Lambda backend."),
    # Security, Identity & Compliance
    Card("svc-q25", 0, "Service Definitions", "AWS IAM (Identity and Access Management): definition and key concept?", "Controls authentication and authorization to AWS resources (users, groups, roles, policies). Key concept: roles are assumed for temporary credentials and are preferred over long-term access keys, especially for EC2/Lambda accessing other services.", "Use a role instead of static keys for a service."),
    Card("svc-q26", 0, "Service Definitions", "AWS Organizations: definition and use case?", "Centralized management of multiple AWS accounts, with Service Control Policies (SCPs) to set permission guardrails. Use for multi-account governance and consolidated billing.", "Apply an SCP guardrail across accounts."),
    Card("svc-q27", 0, "Service Definitions", "AWS KMS (Key Management Service): definition and use case?", "Managed creation and control of encryption keys. Use for encrypting data at rest across AWS services (S3, EBS, RDS, and more).", "Encrypt an S3 bucket or EBS volume with a KMS key."),
    Card("svc-q28", 0, "Service Definitions", "AWS Secrets Manager: definition and use case?", "Securely stores, rotates, and manages secrets (DB credentials, API keys). Use for automatic secret rotation and avoiding hardcoded credentials.", "Rotate a database credential automatically."),
    Card("svc-q29", 0, "Service Definitions", "AWS Shield and AWS WAF: definitions and use case?", "Shield is DDoS protection (Standard = free/automatic, Advanced = paid with extra features). WAF is a Web Application Firewall that filters malicious HTTP traffic such as SQL injection and XSS at the application layer.", "Add WAF for app-layer filtering and Shield for DDoS."),
    Card("svc-q30", 0, "Service Definitions", "Amazon Cognito: definition and use case?", "Manages user sign-up/sign-in and access control for web and mobile apps. Use for adding authentication (user pools) and federated/temporary AWS credentials (identity pools) to applications.", "Distinguish user pools from identity pools."),
    # Management, Monitoring & Governance
    Card("svc-q31", 0, "Service Definitions", "Amazon CloudWatch: definition and use case?", "Monitoring and observability: metrics, logs, alarms, and dashboards. Use for triggering Auto Scaling actions, alerting on thresholds, and centralizing logs.", "Create an alarm that triggers scaling."),
    Card("svc-q32", 0, "Service Definitions", "AWS CloudTrail: definition and use case?", "Logs API calls and account activity across AWS services. Use for auditing, security analysis, compliance, and tracking who did what.", "Use CloudTrail to find who changed a resource."),
    Card("svc-q33", 0, "Service Definitions", "AWS Config: definition and use case?", "Tracks resource configurations and changes over time and evaluates them against compliance rules. Use for compliance auditing and configuration drift detection.", "Detect configuration drift with a Config rule."),
    Card("svc-q34", 0, "Service Definitions", "AWS Trusted Advisor: definition and use case?", "Provides real-time recommendations across cost optimization, performance, security, and fault tolerance.", "Review Trusted Advisor for cost and security wins."),
    Card("svc-q35", 0, "Service Definitions", "AWS Systems Manager: definition and use case?", "A suite of operational management tools (Patch Manager, Session Manager, Parameter Store, Run Command). Use for centralized operational tasks, secure shell access without SSH keys or bastion hosts (Session Manager), and storing config/secrets (Parameter Store).", "Use Session Manager to reach an instance without SSH."),
    # Application Integration
    Card("svc-q36", 0, "Service Definitions", "Amazon SQS (Simple Queue Service): definition, types, and use case?", "A managed message queuing service that decouples application components. Types: Standard (at-least-once, best-effort ordering) and FIFO (exactly-once, ordered). Use for decoupling producers/consumers, buffering requests, and smoothing traffic spikes.", "Choose Standard vs FIFO for an ordering need."),
    Card("svc-q37", 0, "Service Definitions", "Amazon SNS (Simple Notification Service): definition and use case?", "Pub/sub messaging that pushes messages to multiple subscribers (email, SMS, SQS, Lambda). Use for fan-out patterns, alerting, and broadcasting events to multiple consumers.", "Fan out one event to several subscribers."),
    Card("svc-q38", 0, "Service Definitions", "AWS Step Functions: definition and use case?", "Orchestrates multi-step workflows across AWS services using state machines. Use for coordinating Lambda functions and other services into complex workflows with a visual flow.", "Model a multi-step workflow as a state machine."),
    Card("svc-q39", 0, "Service Definitions", "Amazon EventBridge: definition and use case?", "A serverless event bus for building event-driven architectures, including from SaaS sources. Use for routing events between AWS services and applications based on rules.", "Route a SaaS or service event with an EventBridge rule."),
    # Migration & Transfer
    Card("svc-q40", 0, "Service Definitions", "AWS Snow Family (Snowball, Snowcone, Snowmobile): definition and use case?", "Physical devices for transferring large amounts of data into or out of AWS when network transfer is impractical. Use for petabyte-scale data migration and edge computing in disconnected environments.", "Choose Snow devices when the network is too slow."),
    Card("svc-q41", 0, "Service Definitions", "AWS DMS (Database Migration Service): definition and use case?", "Migrates databases to AWS with minimal downtime, supporting homogeneous and heterogeneous migrations. Use for moving on-prem databases to RDS/Aurora, often paired with the Schema Conversion Tool (SCT) for engine changes.", "Pair DMS with SCT for a cross-engine migration."),
    # --- Shared Responsibility Model ---
    Card("srm-q1", 1, "Shared Responsibility Model", "What is the AWS Shared Responsibility Model?", "A model that divides security duties between AWS and the customer: AWS is responsible for security OF the cloud (the infrastructure that runs the services), and the customer is responsible for security IN the cloud (their data and configuration).", "State who owns 'of' versus 'in' the cloud."),
    Card("srm-q2", 1, "Shared Responsibility Model", "What does 'security OF the cloud' cover, and who owns it?", "AWS owns it. It covers the infrastructure that runs AWS services: physical data centers, hardware, networking, and the virtualization/host software plus managed-service infrastructure.", "List AWS-owned layers of the stack."),
    Card("srm-q3", 1, "Shared Responsibility Model", "What does 'security IN the cloud' cover, and who owns it?", "The customer owns it. It covers what the customer puts in and configures: their data, encryption choices, IAM users/roles/permissions, and for EC2 the guest OS, patches, and network/firewall configuration.", "List customer-owned responsibilities."),
    Card("srm-q4", 1, "Shared Responsibility Model", "Who is responsible for the physical security of AWS data centers?", "AWS. Physical security and infrastructure redundancy are part of security OF the cloud.", "Assign physical security to AWS."),
    Card("srm-q5", 1, "Shared Responsibility Model", "Who patches the guest operating system on an EC2 instance?", "The customer. Guest OS patching and configuration are the customer's responsibility for IaaS like EC2.", "Assign guest OS patching to the customer."),
    Card("srm-q6", 1, "Shared Responsibility Model", "Who patches the underlying host, hypervisor, and hardware?", "AWS, as part of securing the infrastructure that runs the services.", "Assign host/hypervisor patching to AWS."),
    Card("srm-q7", 1, "Shared Responsibility Model", "Who manages IAM users, roles, and permissions?", "The customer. Controlling access and authorization is a customer responsibility.", "Assign IAM/access control to the customer."),
    Card("srm-q8", 1, "Shared Responsibility Model", "Who is responsible for encrypting customer data and choosing encryption settings?", "The customer. AWS provides encryption tools and key services, but the customer decides what to encrypt and how.", "Assign data encryption choices to the customer."),
    Card("srm-q9", 1, "Shared Responsibility Model", "Who configures security groups, network ACLs, and firewall rules?", "The customer. Network and firewall configuration is part of security IN the cloud.", "Assign SG/NACL configuration to the customer."),
    Card("srm-q10", 1, "Shared Responsibility Model", "How does responsibility shift for managed/abstracted services such as S3, DynamoDB, and Lambda?", "AWS takes on more (operating system, patching, and platform infrastructure), while the customer still owns their data, access policies, and encryption configuration.", "Explain the shift for a managed service."),
    Card("srm-q11", 1, "Shared Responsibility Model", "Where is customer responsibility greatest: IaaS like EC2 or abstracted managed services?", "Greatest with IaaS like EC2 (OS, patching, network, firewall). It is smaller with abstracted/managed services, where AWS handles the OS and platform.", "Rank responsibility by service model."),
    Card("srm-q12", 1, "Shared Responsibility Model", "What are 'shared controls' in the model?", "Controls both parties handle from their own side, such as patch management, configuration management, and awareness/training.", "Give an example of a shared control."),
    Card("srm-q13", 1, "Shared Responsibility Model", "Who is responsible for backing up customer data?", "The customer, though AWS provides backup features and services to make it easier.", "Assign data backup to the customer."),
    Card("srm-q14", 1, "Shared Responsibility Model", "Who ensures the durability and availability of the underlying storage infrastructure?", "AWS provides the durable, redundant infrastructure; the customer is responsible for how they use it, such as access policies, versioning, and replication settings.", "Split infra durability (AWS) from usage config (customer)."),
    # --- EC2 scenario decision cards ---
    Card("ec2-scn-q1", 6, "EC2 scenarios", "Application must survive an AZ failure.", "Use an Auto Scaling group across multiple AZs behind an ALB.", "Draw a multi-AZ ASG behind an ALB."),
    Card("ec2-scn-q2", 6, "EC2 scenarios", "Need lowest latency between EC2 nodes.", "Use a cluster placement group.", "Pick cluster placement for tightly coupled HPC nodes."),
    Card("ec2-scn-q3", 6, "EC2 scenarios", "Need EC2 instances isolated across hardware.", "Use a spread placement group.", "Pick spread placement to isolate critical instances."),
    Card("ec2-scn-q4", 6, "EC2 scenarios", "Need cheaper compute for fault-tolerant batch jobs.", "Use Spot Instances.", "Match interruptible batch work to Spot."),
    Card("ec2-scn-q5", 6, "EC2 scenarios", "Need predictable discount for steady usage.", "Use Savings Plans or Reserved Instances.", "Match steady baseline usage to a commitment discount."),
    Card("ec2-scn-q6", 6, "EC2 scenarios", "Need capacity guaranteed in one AZ.", "Use a Capacity Reservation.", "Reserve capacity in a specific AZ."),
    Card("ec2-scn-q7", 6, "EC2 scenarios", "Need bootstrapping on first launch.", "Use user data.", "Add a user-data script to bootstrap an instance."),
    Card("ec2-scn-q8", 6, "EC2 scenarios", "Need secure AWS credentials on EC2.", "Attach an IAM role to the instance.", "Attach an instance profile instead of storing keys."),
    Card("ec2-scn-q9", 6, "EC2 scenarios", "Need to protect metadata credentials from SSRF risk.", "Require IMDSv2.", "Enforce IMDSv2 on the instance metadata options."),
    Card("ec2-scn-q10", 6, "EC2 scenarios", "Need to replace unhealthy servers automatically.", "Use EC2 Auto Scaling with health checks.", "Let an ASG replace instances that fail health checks."),
    # --- Amazon DocumentDB ---
    Card("docdb-q1", 11, "DocumentDB", "What is Amazon DocumentDB?", "A fully managed, MongoDB-compatible document (NoSQL) database service that stores, queries, and indexes JSON data. AWS handles provisioning, patching, backups, and scaling.", "Choose DocumentDB for a managed MongoDB-compatible workload."),
    Card("docdb-q2", 11, "DocumentDB", "When should you choose DocumentDB over DynamoDB?", "Choose DocumentDB when you need MongoDB API compatibility and rich document queries or are migrating an existing MongoDB workload. Choose DynamoDB for serverless key-value scale with single-digit millisecond latency.", "Map a MongoDB migration to DocumentDB."),
    Card("docdb-q3", 11, "DocumentDB", "How does DocumentDB provide high availability?", "It separates compute from storage: the cluster volume replicates data six ways across three Availability Zones, and you can add up to 15 read replicas that can be promoted on failover.", "Design a Multi-AZ DocumentDB cluster with read replicas."),
    Card("docdb-q4", 11, "DocumentDB", "How does DocumentDB scale reads and storage?", "Add read replicas to scale read throughput, and the cluster storage grows automatically in 10 GB increments up to 64 TB without manual provisioning.", "Add replicas for reads and let storage auto-grow."),
    Card("docdb-q5", 11, "DocumentDB", "How is a DocumentDB cluster kept secure and private?", "It runs inside your VPC (no public access by default), supports encryption at rest with KMS and in transit with TLS, and uses security groups plus IAM for access control.", "Place DocumentDB in private subnets with KMS encryption."),
    # --- Amazon Neptune ---
    Card("neptune-q1", 11, "Neptune", "What is Amazon Neptune?", "A fully managed graph database service optimized for storing and querying highly connected data through relationships between data points.", "Choose Neptune for a workload centered on relationships."),
    Card("neptune-q2", 11, "Neptune", "What are typical use cases for Neptune?", "Social networks, recommendation engines, fraud detection, knowledge graphs, and network/IT operations graphs, where the connections between items matter as much as the items themselves.", "Match a recommendation or fraud-detection scenario to Neptune."),
    Card("neptune-q3", 11, "Neptune", "Which graph models and query languages does Neptune support?", "Property Graph queried with Apache TinkerPop Gremlin or openCypher, and RDF graphs queried with SPARQL.", "Pick Gremlin/openCypher for property graphs, SPARQL for RDF."),
    Card("neptune-q4", 11, "Neptune", "How does Neptune provide high availability and durability?", "Its cluster storage replicates six copies of data across three Availability Zones and auto-grows, and you can add up to 15 read replicas that can be promoted on failover.", "Design a Multi-AZ Neptune cluster with read replicas."),
    Card("neptune-q5", 11, "Neptune", "When should you choose Neptune over a relational database?", "Choose Neptune when queries traverse many-to-many relationships (multiple joins/hops), which graph databases handle far more efficiently than relational joins.", "Replace deep multi-join queries with a graph traversal."),
    # --- AWS Global Accelerator ---
    Card("ga-q1", 17, "Global Accelerator", "What is AWS Global Accelerator?", "A networking service that improves availability and performance for global users by routing traffic over the AWS global backbone network to the nearest healthy endpoint instead of the public internet.", "Choose Global Accelerator to speed up global traffic."),
    Card("ga-q2", 17, "Global Accelerator", "What do the two static anycast IP addresses provide?", "Global Accelerator gives you two fixed anycast IPs that act as a single stable entry point for your application, so client-facing IPs never change even as backend endpoints move or fail over.", "Use the static IPs as a fixed front door for the app."),
    Card("ga-q3", 17, "Global Accelerator", "How does Global Accelerator differ from CloudFront?", "CloudFront is a CDN that caches HTTP/HTTPS content at edge locations. Global Accelerator does not cache; it optimizes network routing for any TCP/UDP traffic and provides static entry IPs.", "Pick CloudFront for cached content, Global Accelerator for TCP/UDP routing."),
    Card("ga-q4", 17, "Global Accelerator", "How does Global Accelerator handle endpoint failure?", "It continuously health-checks endpoints and instantly reroutes traffic to the next nearest healthy endpoint in another Region or AZ, improving availability without DNS changes.", "Rely on health checks for fast cross-Region failover."),
    Card("ga-q5", 17, "Global Accelerator", "What endpoint types can Global Accelerator route to?", "Application Load Balancers, Network Load Balancers, EC2 instances, and Elastic IP addresses, across one or more AWS Regions.", "Point an accelerator at ALBs or NLBs in multiple Regions."),
    # --- Key Management (AWS KMS) ---
    Card("kms-q1", 23, "Key Management", "What is AWS KMS?", "AWS Key Management Service is a managed service for creating and controlling encryption keys (KMS keys). It integrates with most AWS services and logs all key usage to CloudTrail for auditing.", "Use KMS to create and audit encryption keys."),
    Card("kms-q2", 23, "Key Management", "What are the three ownership types of KMS keys?", "AWS owned keys (owned/managed by AWS, shared across accounts, not visible to you), AWS managed keys (created by a service in your account, prefixed aws/, key policy managed by AWS), and customer managed keys (you create and fully control policy, rotation, and lifecycle).", "Classify a key as AWS owned, AWS managed, or customer managed."),
    Card("kms-q3", 23, "Key Management", "When should you use a customer managed key instead of an AWS managed key?", "Use a customer managed key when you need control over the key policy, enabling/disabling, rotation schedule, deletion, and cross-account grants. AWS managed keys are simpler but you cannot manage their policy or rotation.", "Pick a customer managed key when you need policy and rotation control."),
    Card("kms-q4", 23, "Key Management", "What is the difference between symmetric and asymmetric KMS keys?", "Symmetric keys use a single 256-bit key for both encrypt and decrypt and never leave KMS unencrypted. Asymmetric keys are a public/private key pair used for encryption or digital signing, where the public key can be shared outside AWS.", "Choose symmetric for most encryption, asymmetric for signing or external parties."),
    Card("kms-q5", 23, "Key Management", "What is envelope encryption?", "Encrypting data with a data key, then encrypting that data key with a KMS key. AWS services use envelope encryption so large data is encrypted locally with the data key while only the small data key round-trips to KMS.", "Explain why data keys avoid sending bulk data to KMS."),
    Card("kms-q6", 23, "Key Management", "What does the GenerateDataKey operation return?", "It returns a plaintext data key (used to encrypt data locally, then discarded) and an encrypted copy of that data key (stored with the ciphertext and later sent to KMS to decrypt).", "Encrypt locally with the plaintext key and store the encrypted key."),
    Card("kms-q7", 23, "Key Management", "How does automatic key rotation work for customer managed keys?", "When enabled, KMS rotates the underlying key material once per year (or a configurable period) while keeping the same key ID and ARN, so applications and ciphertext references do not change.", "Enable annual rotation without breaking key references."),
    Card("kms-q8", 23, "Key Management", "What controls access to a KMS key?", "The key policy (resource-based policy on the key) is the primary control and is always required; it can be combined with IAM policies and grants for temporary, fine-grained delegation.", "Grant access via the key policy plus IAM and grants."),
    Card("kms-q9", 23, "Key Management", "What happens when you schedule a KMS key for deletion?", "KMS enforces a mandatory waiting period (7 to 30 days) during which the key is disabled but recoverable; after the period the key and its material are permanently deleted and data it protected becomes unrecoverable.", "Plan for the 7-30 day deletion window before removing a key."),
    Card("kms-q10", 23, "Key Management", "When should you use CloudHSM instead of KMS?", "Use AWS CloudHSM when you need a dedicated, single-tenant FIPS 140-2 Level 3 hardware security module with full control of key material, often for strict compliance. KMS is multi-tenant and simpler for most workloads.", "Choose CloudHSM for dedicated HSM and compliance control."),
    # --- AWS Control Tower ---
    Card("ct-q1", 23, "Control Tower", "What is AWS Control Tower?", "A service that sets up and governs a secure, compliant multi-account AWS environment (a landing zone) based on best practices, automating account provisioning and applying governance on top of AWS Organizations.", "Use Control Tower to stand up a governed multi-account landing zone."),
    Card("ct-q2", 23, "Control Tower", "What is a landing zone in Control Tower?", "A pre-configured, well-architected multi-account baseline: it creates a management account, core organizational units, log archive and audit accounts, centralized logging, and identity/access defaults.", "Recall that Control Tower builds the landing zone automatically."),
    Card("ct-q3", 23, "Control Tower", "What are guardrails (controls) in Control Tower?", "Pre-packaged governance rules applied across accounts. Preventive guardrails use SCPs to block non-compliant actions; detective guardrails use AWS Config to flag violations. They can be mandatory, strongly recommended, or elective.", "Distinguish preventive (SCP) from detective (Config) guardrails."),
    Card("ct-q4", 23, "Control Tower", "How does Control Tower relate to AWS Organizations?", "Control Tower is built on top of Organizations. Organizations provides the account structure, OUs, and SCPs, while Control Tower orchestrates, automates, and adds governance and monitoring on top.", "Explain that Control Tower automates governance over Organizations."),
    Card("ct-q5", 23, "Control Tower", "What is Account Factory in Control Tower?", "A feature that standardizes and automates provisioning of new AWS accounts using pre-approved configurations and guardrails, so new accounts are compliant from creation.", "Use Account Factory to vend pre-configured accounts."),
]


# --- Runtime card editing: user overrides layered on top of the built-in CARDS ---
CARDS_FILE = Path(__file__).with_name("aws_flashcard_cards.json")


def _load_card_overrides() -> dict:
    """Load user-created/edited cards keyed by card id."""
    if not CARDS_FILE.exists():
        return {}
    try:
        with CARDS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _apply_card_overrides(base: list[Card], overrides: dict) -> list[Card]:
    """Return the card list with overrides applied: matching ids replaced, new ids appended."""
    by_id = {card.id: card for card in base}
    for cid, data in overrides.items():
        try:
            by_id[cid] = Card(
                cid,
                int(data.get("day", 0)),
                data.get("focus", ""),
                data.get("question", ""),
                data.get("answer", ""),
                data.get("practical", ""),
            )
        except (TypeError, ValueError):
            continue
    return list(by_id.values())


def save_card_overrides() -> None:
    with CARDS_FILE.open("w", encoding="utf-8") as file:
        json.dump(CARD_OVERRIDES, file, indent=2, sort_keys=True)


def upsert_card(data: dict) -> Card:
    """Create or update a card at runtime, persist it, and refresh the in-memory CARDS list."""
    global CARDS
    CARD_OVERRIDES[data["id"]] = data
    save_card_overrides()
    CARDS = _apply_card_overrides(CARDS, {data["id"]: data})
    return next(card for card in CARDS if card.id == data["id"])


CARD_OVERRIDES = _load_card_overrides()
CARDS = _apply_card_overrides(CARDS, CARD_OVERRIDES)


def wrapped(text: str, indent: int = 0) -> str:
    return fill(text, width=WRAP_WIDTH, subsequent_indent=" " * indent)


def load_progress() -> dict:
    if not PROGRESS_FILE.exists():
        return {}
    try:
        with PROGRESS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_progress(progress: dict) -> None:
    with PROGRESS_FILE.open("w", encoding="utf-8") as file:
        json.dump(progress, file, indent=2, sort_keys=True)


def record_answer(progress: dict, card: Card, correct: bool) -> None:
    entry = progress.setdefault(
        card.id,
        {
            "day": card.day,
            "focus": card.focus,
            "seen": 0,
            "correct": 0,
            "incorrect": 0,
            "last_seen": None,
        },
    )
    entry["seen"] += 1
    entry["correct" if correct else "incorrect"] += 1
    entry["last_seen"] = datetime.now().isoformat(timespec="seconds")


def accuracy(entry: dict) -> float:
    seen = entry.get("seen", 0)
    if not seen:
        return 0.0
    return entry.get("correct", 0) / seen


def select_cards(
    *,
    topic: str | None = None,
    missed_only: bool = False,
    progress: dict | None = None,
) -> list[Card]:
    topic_lower = topic.lower() if topic else None
    selected = []
    progress = progress or {}
    for card in CARDS:
        entry = progress.get(card.id, {})
        missed = entry.get("incorrect", 0) > entry.get("correct", 0)
        if topic_lower and topic_lower not in card.focus.lower() and topic_lower not in card.question.lower():
            continue
        if missed_only and not missed:
            continue
        selected.append(card)
    return selected


def show_card_header(card: Card, index: int, total: int) -> None:
    print("\n" + "=" * WRAP_WIDTH)
    print(f"Card {index}/{total} | {card.focus}")
    print("-" * WRAP_WIDTH)


def run_round(cards: list[Card], progress: dict) -> tuple[list[Card], int, bool]:
    """Run one pass over the cards. Returns (missed cards, reviewed count, quit early)."""
    missed: list[Card] = []
    reviewed = 0
    for index, card in enumerate(cards, start=1):
        show_card_header(card, index, len(cards))
        print(wrapped("Question: " + card.question, indent=10))
        response = input("\n(Press Enter to reveal the answer, or q to quit)\n").strip().lower()
        if response == "q":
            return missed, reviewed, True

        print("\n" + wrapped("Answer: " + card.answer, indent=8))

        while True:
            verdict = input("\nDid you get it right? (y = correct, n = missed, q = quit): ").strip().lower()
            if verdict in ("y", "yes", "n", "no", "q"):
                break
            print("Please enter y, n, or q.")
        if verdict == "q":
            return missed, reviewed, True

        correct = verdict in ("y", "yes")
        record_answer(progress, card, correct)
        save_progress(progress)
        reviewed += 1
        if not correct:
            missed.append(card)
    return missed, reviewed, False


def run_quiz(cards: list[Card], *, shuffle: bool, limit: int | None, progress: dict) -> None:
    if shuffle:
        random.shuffle(cards)
    if limit:
        cards = cards[:limit]
    if not cards:
        print("No cards matched that selection.")
        return

    round_number = 1
    while cards:
        if round_number == 1:
            print(f"\nStarting quiz with {len(cards)} card(s). Type q at a prompt to quit.")
        else:
            print(f"\nRerunning {len(cards)} missed card(s). Type q at a prompt to quit.")

        missed, reviewed, quit_early = run_round(cards, progress)

        print("\nRound complete.")
        print(f"Cards reviewed: {reviewed}/{len(cards)}")
        print(f"Correct: {reviewed - len(missed)}   Incorrect: {len(missed)}")

        if quit_early:
            break
        if not missed:
            if round_number > 1:
                print("\nNice work - you cleared every missed card.")
            break

        choice = input(f"\nRerun the {len(missed)} card(s) you missed? (y/n): ").strip().lower()
        if choice not in ("y", "yes"):
            break
        cards = missed
        if shuffle:
            random.shuffle(cards)
        round_number += 1

    print("\nSession complete.")


def print_topics() -> None:
    print("\nAWS SAA-C03 flashcard topics")
    topics = sorted({card.focus for card in CARDS})
    for focus in topics:
        count = sum(1 for card in CARDS if card.focus == focus)
        print(f"- {focus} ({count} cards)")


def print_stats(progress: dict) -> None:
    total_seen = sum(entry.get("seen", 0) for entry in progress.values())
    total_correct = sum(entry.get("correct", 0) for entry in progress.values())
    total_incorrect = sum(entry.get("incorrect", 0) for entry in progress.values())
    attempted = len([entry for entry in progress.values() if entry.get("seen", 0)])
    print("\nProgress summary")
    print(f"Cards attempted: {attempted}/{len(CARDS)}")
    print(f"Answers recorded: {total_seen}")
    print(f"Correct: {total_correct}")
    print(f"Incorrect: {total_incorrect}")
    if total_seen:
        print(f"Accuracy: {total_correct / total_seen:.1%}")

    weak = sorted(
        ((card, progress.get(card.id, {})) for card in CARDS if progress.get(card.id, {}).get("seen", 0)),
        key=lambda pair: (accuracy(pair[1]), -pair[1].get("incorrect", 0)),
    )[:10]
    if weak:
        print("\nWeakest attempted cards")
        for card, entry in weak:
            print(
                f"- {card.focus}: "
                f"{entry.get('correct', 0)}/{entry.get('seen', 0)} correct - {card.question}"
            )


def interactive_menu(progress: dict) -> None:
    while True:
        print("\nAWS SAA-C03 Flashcard Trainer")
        print("1. Random quiz")
        print("2. Quiz by topic search")
        print("3. S3")
        print("4. IAM")
        print("5. EC2")
        print("6. VPC")
        print("7. Well-Architected Framework")
        print("8. High availability & fault tolerance")
        print("9. Directory Services")
        print("10. Service Definitions")
        print("11. Shared Responsibility Model")
        print("12. DocumentDB")
        print("13. Neptune")
        print("14. Global Accelerator")
        print("15. Key Management (KMS)")
        print("16. Control Tower")
        print("17. Review missed cards")
        print("18. Show topics")
        print("19. Show progress")
        print("20. Reset progress")
        print("21. Launch visual flashcard mode (GUI)")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                run_quiz(CARDS.copy(), shuffle=True, limit=None, progress=progress)
            elif choice == "2":
                topic = input("Enter topic text, for example IAM, S3, networking: ").strip()
                count = read_count()
                run_quiz(select_cards(topic=topic), shuffle=True, limit=count, progress=progress)
            elif choice == "3":
                count = read_count()
                run_quiz(select_cards(topic="S3"), shuffle=True, limit=count, progress=progress)
            elif choice == "4":
                count = read_count()
                run_quiz(select_cards(topic="IAM"), shuffle=True, limit=count, progress=progress)
            elif choice == "5":
                count = read_count()
                run_quiz(select_cards(topic="EC2"), shuffle=True, limit=count, progress=progress)
            elif choice == "6":
                count = read_count()
                run_quiz(select_cards(topic="VPC"), shuffle=True, limit=count, progress=progress)
            elif choice == "7":
                count = read_count()
                run_quiz(select_cards(topic="Well-Architected"), shuffle=True, limit=count, progress=progress)
            elif choice == "8":
                count = read_count()
                run_quiz(select_cards(topic="High availability"), shuffle=True, limit=count, progress=progress)
            elif choice == "9":
                count = read_count()
                run_quiz(select_cards(topic="Directory"), shuffle=True, limit=count, progress=progress)
            elif choice == "10":
                count = read_count()
                run_quiz(select_cards(topic="Service Definitions"), shuffle=True, limit=count, progress=progress)
            elif choice == "11":
                count = read_count()
                run_quiz(select_cards(topic="Shared Responsibility"), shuffle=True, limit=count, progress=progress)
            elif choice == "12":
                count = read_count()
                run_quiz(select_cards(topic="DocumentDB"), shuffle=True, limit=count, progress=progress)
            elif choice == "13":
                count = read_count()
                run_quiz(select_cards(topic="Neptune"), shuffle=True, limit=count, progress=progress)
            elif choice == "14":
                count = read_count()
                run_quiz(select_cards(topic="Global Accelerator"), shuffle=True, limit=count, progress=progress)
            elif choice == "15":
                count = read_count()
                run_quiz(select_cards(topic="Key Management"), shuffle=True, limit=count, progress=progress)
            elif choice == "16":
                count = read_count()
                run_quiz(select_cards(topic="Control Tower"), shuffle=True, limit=count, progress=progress)
            elif choice == "17":
                run_quiz(select_cards(missed_only=True, progress=progress), shuffle=True, limit=None, progress=progress)
            elif choice == "18":
                print_topics()
            elif choice == "19":
                print_stats(progress)
            elif choice == "20":
                confirm = input("Reset all saved progress? Type RESET to confirm: ").strip()
                if confirm == "RESET":
                    progress.clear()
                    save_progress(progress)
                    print("Progress reset.")
            elif choice == "21":
                launch_gui(progress)
            elif choice == "0":
                return
            else:
                print("Choose a number from the menu.")
        except ValueError as error:
            print(f"Invalid input: {error}")


def read_count() -> int | None:
    value = input("Number of cards, or blank for all matching cards: ").strip()
    if not value:
        return None
    count = int(value)
    if count <= 0:
        raise ValueError("Card count must be greater than zero.")
    return count


def launch_gui(progress: dict) -> bool:
    """Launch a visual flashcard UI. Returns True if it ran, False if Tkinter is unavailable."""
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
    except Exception:
        print("Tkinter is not available in this Python install, so the flashcard GUI cannot start.")
        print("Run with --cli to use the terminal menu instead.")
        return False

    ALL_TOPICS = "All topics"
    session_grades: dict[str, bool] = {}
    state = {"deck": [], "index": 0, "revealed": False}

    def grade_card(card: Card, correct: bool) -> None:
        """Record a grade once per card per session, adjusting if the user changes their answer."""
        prev = session_grades.get(card.id)
        if prev == correct:
            return
        entry = progress.setdefault(
            card.id,
            {"day": card.day, "focus": card.focus, "seen": 0, "correct": 0, "incorrect": 0, "last_seen": None},
        )
        if prev is None:
            entry["seen"] += 1
        else:
            entry["correct" if prev else "incorrect"] -= 1
        entry["correct" if correct else "incorrect"] += 1
        entry["last_seen"] = datetime.now().isoformat(timespec="seconds")
        session_grades[card.id] = correct
        save_progress(progress)

    root = tk.Tk()
    root.title("AWS SAA-C03 Flashcards")
    root.geometry("780x580")
    root.minsize(640, 480)

    # ---- top controls ----
    top = ttk.Frame(root, padding=(12, 10))
    top.pack(fill="x")
    # Topic choices mirror the terminal menu items (label -> select_cards search term).
    topic_choices = [
        (ALL_TOPICS, None),
        ("S3", "S3"),
        ("IAM", "IAM"),
        ("EC2", "EC2"),
        ("VPC", "VPC"),
        ("Well-Architected Framework", "Well-Architected"),
        ("High availability & fault tolerance", "High availability"),
        ("Directory Services", "Directory"),
        ("Service Definitions", "Service Definitions"),
        ("Shared Responsibility Model", "Shared Responsibility"),
        ("DocumentDB", "DocumentDB"),
        ("Neptune", "Neptune"),
        ("Global Accelerator", "Global Accelerator"),
        ("Key Management (KMS)", "Key Management"),
        ("Control Tower", "Control Tower"),
    ]
    topic_search = dict(topic_choices)
    ttk.Label(top, text="Topic:").pack(side="left")
    topic_var = tk.StringVar(value=ALL_TOPICS)
    topic_box = ttk.Combobox(top, textvariable=topic_var, values=[label for label, _ in topic_choices],
                             state="readonly", width=40)
    topic_box.pack(side="left", padx=(4, 12))
    missed_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(top, text="Review missed only", variable=missed_var,
                    command=lambda: rebuild_deck()).pack(side="left")

    ttk.Label(top, text="Cards:").pack(side="left", padx=(12, 0))
    count_var = tk.StringVar(value="All")
    count_box = ttk.Combobox(top, textvariable=count_var, values=["All", "5", "10", "15", "20", "25", "50"],
                             width=6)
    count_box.pack(side="left", padx=(4, 0))
    count_box.bind("<<ComboboxSelected>>", lambda e: rebuild_deck())
    count_box.bind("<Return>", lambda e: rebuild_deck())
    ttk.Button(top, text="Shuffle", command=lambda: shuffle_deck()).pack(side="right")
    ttk.Button(top, text="Edit card", command=lambda: open_editor(current_card())).pack(side="right", padx=(6, 0))
    ttk.Button(top, text="New card", command=lambda: open_editor(None)).pack(side="right", padx=(6, 0))

    # ---- flashcard ----
    card_outer = tk.Frame(root, bg="#d9dee7", padx=16, pady=12)
    card_outer.pack(fill="both", expand=True, padx=16, pady=(0, 8))
    card = tk.Frame(card_outer, bg="white", highlightbackground="#b9c2d0", highlightthickness=1)
    card.pack(fill="both", expand=True)

    header = tk.Frame(card, bg="#2f6fed")
    header.pack(fill="x")
    focus_label = tk.Label(header, text="", bg="#2f6fed", fg="white", font=("Segoe UI", 11, "bold"),
                           anchor="w", padx=12, pady=6)
    focus_label.pack(side="left")
    counter_label = tk.Label(header, text="", bg="#2f6fed", fg="white", font=("Segoe UI", 10), anchor="e", padx=12)
    counter_label.pack(side="right")

    body = tk.Frame(card, bg="white")
    body.pack(fill="both", expand=True, padx=18, pady=16)
    q_caption = tk.Label(body, text="QUESTION", bg="white", fg="#8a94a6", font=("Segoe UI", 9, "bold"), anchor="w")
    q_caption.pack(fill="x")
    question_label = tk.Label(body, text="", bg="white", fg="#1b2330", font=("Segoe UI", 15),
                              wraplength=660, justify="left", anchor="w")
    question_label.pack(fill="x", pady=(2, 12))
    answer_sep = ttk.Separator(body, orient="horizontal")
    a_caption = tk.Label(body, text="ANSWER", bg="white", fg="#8a94a6", font=("Segoe UI", 9, "bold"), anchor="w")
    answer_label = tk.Label(body, text="", bg="white", fg="#1b2330", font=("Segoe UI", 13),
                            wraplength=660, justify="left", anchor="w")

    # ---- grading + navigation ----
    correct_var = tk.BooleanVar(value=False)

    # Row above the buttons: status text on the left, grading checkbox on the right.
    controls = ttk.Frame(root, padding=(16, 4))
    controls.pack(fill="x")
    status_label = ttk.Label(controls, text="", foreground="#5a6472")
    status_label.pack(side="left", padx=12)
    correct_check = ttk.Checkbutton(controls, text="I got this correct", variable=correct_var,
                                    command=lambda: on_toggle())
    correct_check.pack(side="right")

    nav = ttk.Frame(root, padding=(16, 8))
    nav.pack(fill="x")
    # All three navigation buttons grouped on the lower right (left-to-right: Previous, Show Answer, Next).
    next_btn = ttk.Button(nav, text="Next ▶", command=lambda: go(1))
    next_btn.pack(side="right")
    reveal_btn = ttk.Button(nav, text="Show Answer", command=lambda: toggle_reveal())
    reveal_btn.pack(side="right", padx=8)
    prev_btn = ttk.Button(nav, text="◀ Previous", command=lambda: go(-1))
    prev_btn.pack(side="right")

    def current_card():
        return state["deck"][state["index"]] if state["deck"] else None

    def set_reveal(shown: bool) -> None:
        state["revealed"] = shown
        if shown:
            answer_sep.pack(fill="x", pady=(4, 8))
            a_caption.pack(fill="x")
            answer_label.pack(fill="x", pady=(2, 0))
            reveal_btn.config(text="Hide Answer")
            correct_check.config(state="normal")
        else:
            answer_label.pack_forget()
            a_caption.pack_forget()
            answer_sep.pack_forget()
            reveal_btn.config(text="Show Answer")
            correct_check.config(state="disabled")

    def update_status() -> None:
        c = current_card()
        if c is None:
            return
        if c.id in session_grades:
            status_label.config(text="Marked correct" if session_grades[c.id] else "Marked incorrect")
        elif state["revealed"]:
            status_label.config(text="Tick the box if you got it right, then click Next.")
        else:
            status_label.config(text="")

    def show_card() -> None:
        c = current_card()
        if c is None:
            focus_label.config(text="No cards")
            counter_label.config(text="")
            question_label.config(text="No cards match this selection. Pick another topic or turn off 'Review missed only'.")
            answer_label.config(text="")
            set_reveal(False)
            for btn in (prev_btn, next_btn, reveal_btn):
                btn.config(state="disabled")
            correct_check.config(state="disabled")
            status_label.config(text="")
            return
        for btn in (prev_btn, next_btn, reveal_btn):
            btn.config(state="normal")
        focus_label.config(text=c.focus)
        counter_label.config(text=f"{c.id}  •  Card {state['index'] + 1} / {len(state['deck'])}")
        question_label.config(text=c.question)
        answer_label.config(text=c.answer)
        correct_var.set(session_grades.get(c.id, False))
        set_reveal(c.id in session_grades)  # auto-reveal cards already graded this session
        update_status()

    def commit_current() -> None:
        c = current_card()
        if c is not None and state["revealed"]:
            grade_card(c, correct_var.get())

    def toggle_reveal() -> None:
        if current_card() is None:
            return
        set_reveal(not state["revealed"])
        update_status()

    def on_toggle() -> None:
        commit_current()
        update_status()

    def end_of_deck() -> None:
        deck = state["deck"]
        total = len(deck)
        # "Not correct" = everything the user did not mark correct (incorrect or skipped).
        missed = [c for c in deck if session_grades.get(c.id) is not True]
        correct = total - len(missed)
        if missed:
            review = messagebox.askyesno(
                "Deck complete",
                f"You've gone through all {total} card(s).\n\n"
                f"Correct: {correct}\n"
                f"Not correct: {len(missed)}\n\n"
                f"Review the {len(missed)} card(s) you did not get correct?\n"
                f"(Yes = retake those cards, No = quit)",
            )
            if review:
                random.shuffle(missed)
                state["deck"] = missed
                state["index"] = 0
                show_card()
            else:
                on_close()
        else:
            quit_now = messagebox.askyesno(
                "Deck complete",
                f"You've gone through all {total} card(s) and got them all correct. Nice work!\n\n"
                f"Quit now?\n(No keeps the window open.)",
            )
            if quit_now:
                on_close()

    def go(delta: int) -> None:
        commit_current()
        if not state["deck"]:
            return
        if delta > 0 and state["index"] == len(state["deck"]) - 1:
            end_of_deck()  # reached the last card and clicked Next
            return
        state["index"] = max(0, min(len(state["deck"]) - 1, state["index"] + delta))
        show_card()

    def rebuild_deck() -> None:
        topic = topic_search.get(topic_var.get())
        deck = select_cards(topic=topic, missed_only=missed_var.get(), progress=progress)
        random.shuffle(deck)  # present questions in random order
        limit = count_var.get().strip()
        if limit and limit.lower() != "all":
            try:
                n = int(limit)
                if n > 0:
                    deck = deck[:n]  # keep a random subset of the chosen size
            except ValueError:
                pass
        state["deck"] = deck
        state["index"] = 0
        show_card()

    def shuffle_deck() -> None:
        # Draw a fresh random subset for the current topic and card count.
        commit_current()
        rebuild_deck()

    def suggest_id() -> str:
        n = 1
        existing = {c.id for c in CARDS}
        while f"user-q{n}" in existing:
            n += 1
        return f"user-q{n}"

    def open_editor(existing: "Card | None") -> None:
        win = tk.Toplevel(root)
        win.title("Edit card" if existing else "New card")
        win.transient(root)
        win.grab_set()
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)
        frm.columnconfigure(1, weight=1)

        cur = current_card()

        def add_entry(label, value, row, width=52):
            ttk.Label(frm, text=label).grid(row=row, column=0, sticky="nw", pady=4, padx=(0, 8))
            entry = ttk.Entry(frm, width=width)
            entry.insert(0, value)
            entry.grid(row=row, column=1, sticky="we", pady=4)
            return entry

        def add_text(label, value, row, height):
            ttk.Label(frm, text=label).grid(row=row, column=0, sticky="nw", pady=4, padx=(0, 8))
            text = tk.Text(frm, width=52, height=height, wrap="word", font=("Segoe UI", 10))
            text.insert("1.0", value)
            text.grid(row=row, column=1, sticky="we", pady=4)
            return text

        id_entry = add_entry("ID", existing.id if existing else suggest_id(), 0, width=24)
        if existing:
            id_entry.config(state="readonly")
        day_entry = add_entry("Day", str(existing.day) if existing else "0", 1, width=10)
        focus_entry = add_entry("Focus (topic)", existing.focus if existing else (cur.focus if cur else ""), 2)
        question_text = add_text("Question", existing.question if existing else "", 3, height=4)
        answer_text = add_text("Answer", existing.answer if existing else "", 4, height=7)
        practical_entry = add_entry("Practical", existing.practical if existing else "", 5)

        msg = ttk.Label(frm, text="", foreground="#b00020")
        msg.grid(row=6, column=0, columnspan=2, sticky="w", pady=(4, 0))

        def save() -> None:
            cid = id_entry.get().strip()
            if not cid:
                msg.config(text="ID is required.")
                return
            if existing is None and any(c.id == cid for c in CARDS):
                msg.config(text="That ID already exists - use Edit instead, or pick another ID.")
                return
            try:
                day = int(day_entry.get().strip() or "0")
            except ValueError:
                msg.config(text="Day must be a whole number.")
                return
            question = question_text.get("1.0", "end").strip()
            answer = answer_text.get("1.0", "end").strip()
            if not question or not answer:
                msg.config(text="Question and answer are both required.")
                return
            card = upsert_card({
                "id": cid,
                "day": day,
                "focus": focus_entry.get().strip(),
                "question": question,
                "answer": answer,
                "practical": practical_entry.get().strip(),
            })
            # Reflect the change in the current deck and jump to the card.
            if any(c.id == cid for c in state["deck"]):
                state["deck"] = [card if c.id == cid else c for c in state["deck"]]
            else:
                state["deck"].append(card)
            for i, c in enumerate(state["deck"]):
                if c.id == cid:
                    state["index"] = i
                    break
            show_card()
            win.destroy()

        buttons = ttk.Frame(frm)
        buttons.grid(row=7, column=0, columnspan=2, sticky="e", pady=(10, 0))
        ttk.Button(buttons, text="Cancel", command=win.destroy).pack(side="right", padx=(6, 0))
        ttk.Button(buttons, text="Save", command=save).pack(side="right")

    def on_resize(event) -> None:
        width = max(360, card.winfo_width() - 60)
        question_label.config(wraplength=width)
        answer_label.config(wraplength=width)

    def on_close() -> None:
        commit_current()
        root.destroy()

    topic_box.bind("<<ComboboxSelected>>", lambda e: rebuild_deck())
    for widget in (card, body, question_label, q_caption):
        widget.bind("<Button-1>", lambda e: toggle_reveal())
    card.bind("<Configure>", on_resize)
    root.bind("<Left>", lambda e: go(-1))
    root.bind("<Right>", lambda e: go(1))
    root.protocol("WM_DELETE_WINDOW", on_close)

    rebuild_deck()
    root.mainloop()
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AWS SAA-C03 terminal flashcard trainer")
    parser.add_argument("--topic", help="Topic text to search, for example IAM, S3, networking")
    parser.add_argument("--missed", action="store_true", help="Quiz only cards with more misses than correct answers")
    parser.add_argument("--count", type=int, help="Maximum number of cards for this session")
    parser.add_argument("--list-topics", action="store_true", help="Print all topics and exit")
    parser.add_argument("--stats", action="store_true", help="Print saved progress and exit")
    parser.add_argument("--reset", action="store_true", help="Reset saved progress and exit")
    parser.add_argument("--gui", action="store_true", help="Launch the visual flashcard UI")
    parser.add_argument("--cli", action="store_true", help="Force the terminal menu instead of the GUI")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    progress = load_progress()

    if args.list_topics:
        print_topics()
        return
    if args.stats:
        print_stats(progress)
        return
    if args.reset:
        progress.clear()
        save_progress(progress)
        print("Progress reset.")
        return

    if args.gui:
        if not launch_gui(progress):
            interactive_menu(progress)
        return

    has_filters = bool(args.topic or args.missed or args.count)
    if has_filters:
        cards = select_cards(topic=args.topic, missed_only=args.missed, progress=progress)
        run_quiz(cards, shuffle=True, limit=args.count, progress=progress)
    elif args.cli:
        interactive_menu(progress)
    else:
        # Default to the visual flashcard UI; fall back to the terminal menu if Tkinter is missing.
        if not launch_gui(progress):
            interactive_menu(progress)


if __name__ == "__main__":
    main()
