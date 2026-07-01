# AWS Certified Solutions Architect - Associate: AWS Backup Study Notes

Current focus: AWS Backup for SAA-C03 questions involving centralized backup operations, backup plans, vaults, lifecycle policies, cross-Region and cross-account copy, restore design, compliance, and immutable backup protection.

## Exam Weight

AWS Backup appears most often in:

- Domain 1: Design Secure Architectures, especially backup isolation, vault policies, encryption, and immutable recovery points.
- Domain 2: Design Resilient Architectures, especially backup and restore strategies, cross-Region recovery, and recovery point retention.
- Domain 3: Design High-Performing Architectures, less directly, usually around restore time expectations and service-specific recovery patterns.
- Domain 4: Design Cost-Optimized Architectures, especially backup retention, lifecycle to cold storage, and incremental backups.

Key exam framing:

- Use AWS Backup when the question asks for centralized, policy-driven backup across multiple AWS services.
- Use backup plans to automate schedule, retention, lifecycle, and copy actions.
- Use backup vaults to store and control recovery points.
- Use cross-Region copy for regional disaster recovery or compliance separation.
- Use cross-account copy with AWS Organizations for account-level backup isolation.
- Use AWS Backup Vault Lock for WORM-style protection and retention enforcement.
- Restore usually creates a new resource rather than overwriting the original resource.

## Core AWS Backup Concepts

### AWS Backup

AWS Backup is a managed service for centralizing and automating backups across supported AWS services. It is useful when a company wants one backup policy model instead of configuring separate backup schedules in each service.

AWS Backup can manage:

- Backup schedules.
- Retention periods.
- Lifecycle to lower-cost cold storage where supported.
- Cross-Region backup copies.
- Cross-account backup copies.
- Backup monitoring and job status.
- Restore jobs.
- Compliance checks through AWS Backup Audit Manager.

Exam distinction:

- AWS Backup is for backup and restore, not live traffic failover.
- Replication services such as S3 Replication, RDS read replicas, Aurora Global Database, or DynamoDB global tables are for low-latency access and disaster recovery patterns with active replicated data.
- A backup copy is not the same as a continuously replicated active resource.

### Recovery Points

A recovery point is a backup stored in a backup vault. Recovery points are the objects you restore from, copy, retain, or delete according to policy.

Important points:

- The first backup of a supported resource is typically a full backup.
- Later periodic backups can be incremental for supported resource types.
- Not every supported service supports every feature.
- Feature availability varies by resource type and Region.

Exam rule: Do not assume every AWS Backup feature works with every supported service. If the answer depends on a specific resource, check whether that resource supports the needed feature.

## Backup Plans

A backup plan defines when and how resources are backed up.

Backup plan settings commonly include:

- Backup frequency.
- Backup window.
- Start window.
- Completion window.
- Destination backup vault.
- Retention period.
- Lifecycle transition to cold storage where supported.
- Copy actions to another Region or account.

You can create multiple backup plans for different workload tiers.

Examples:

- Mission-critical database: hourly backups, short start window, long retention, cross-Region copy.
- Compliance archive: daily backups, multi-year retention, vault lock.
- Development resources: daily or weekly backups, short retention, no cross-Region copy.

### Resource Assignment

Resources can be assigned to a backup plan directly or by tag.

Tag-based assignment is the common exam answer when:

- Many resources need the same backup policy.
- New resources should automatically be protected when tagged.
- A company wants centralized governance across many workloads.

Example:

- Resources tagged `Backup=Daily` are assigned to a daily backup plan.
- Resources tagged `Backup=Critical` are assigned to a more frequent plan with cross-Region copy.

## Backup Vaults

A backup vault is a logical container for recovery points.

Vaults are used for:

- Storing recovery points.
- Applying access policies.
- Applying encryption settings.
- Applying AWS Backup Vault Lock.
- Separating backup tiers, workloads, or compliance scopes.

Common vault design:

- Separate vaults by environment, workload criticality, or retention policy.
- Use a dedicated vault for compliance-locked backups.
- Use destination vaults in separate Regions or accounts for disaster recovery.

### Vault Access Policies

Vault access policies are resource-based policies on backup vaults. They can grant or deny permissions at the vault level.

Use vault access policies to help control:

- Who can copy backups into a vault.
- Who can start restore operations.
- Who can delete recovery points.
- Whether destructive backup actions are blocked.

Exam pattern:

- If the question asks how to prevent unauthorized deletion of backups, use vault policies and Vault Lock.
- If it asks for immutable retention that even privileged users cannot bypass after lock, use Vault Lock in compliance mode.

## Lifecycle Policies

Backup lifecycle policies control how long backups are retained and whether they transition to cold storage where supported.

Lifecycle phases:

- Warm storage: faster restore, higher cost.
- Cold storage: lower cost, slower restore, supported only for certain resource types.
- Expiration: recovery point is deleted after the retention period, unless blocked by lock or policy constraints.

Important exam points:

- Cold storage is for long-term retention, not fast recovery.
- Restoring from cold storage can take longer than restoring from warm storage.
- Cross-Region copy to cold storage is not supported directly; copy behavior depends on supported resource features.
- Lifecycle to cold storage is not supported by every resource type.

Cost framing:

- Use retention policies to avoid keeping backups indefinitely.
- Use cold storage for long retention when restore speed can be slower.
- Incremental backups reduce cost for supported resource types.

## Cross-Region Backup

Cross-Region copy copies recovery points to a backup vault in another AWS Region.

Use cross-Region backup when:

- The organization needs disaster recovery if a Region is impaired.
- Compliance requires backup data to be stored a minimum distance away.
- The restore strategy includes rebuilding resources in a separate Region.

Important behavior:

- The first copy to a new Region is generally full.
- Later copies can be incremental for supported services.
- Destination copies are encrypted with the destination vault's KMS key.
- Some resource types have service-specific copy limitations.

Exam distinction:

- Cross-Region backup copy is not the same as a multi-Region active architecture.
- If the question requires near-real-time reads or writes in another Region, choose a service-native replication design, not AWS Backup alone.

## Cross-Account Backup

Cross-account backup copy stores recovery points in a different AWS account, typically managed through AWS Organizations.

Use cross-account copy when:

- Backups must be isolated from the production account.
- The company wants a dedicated backup or security account.
- The production account could be compromised and backups must remain protected.
- Central governance is required across multiple accounts.

Typical design:

- Workload account contains production resources.
- Backup plan copies recovery points to a vault in a separate backup account.
- Destination vault has restrictive access policies.
- AWS Organizations and AWS Backup policies help manage the setup centrally.
- KMS permissions must allow the backup copy and restore workflows.

Exam pattern:

- For "protect backups if the source account is compromised," choose cross-account backup copy to a separate account plus restrictive vault policies and Vault Lock.
- For "protect against regional failure," choose cross-Region copy.
- For both account compromise and regional failure, use cross-account and cross-Region copies when supported.

## Supported Services

AWS Backup supports many AWS resource types, but feature support varies by service and Region.

Common SAA-relevant services include:

- Amazon EC2.
- Amazon EBS.
- Amazon S3.
- Amazon RDS.
- Amazon Aurora.
- Amazon DynamoDB, including advanced AWS Backup features when enabled.
- Amazon EFS.
- Amazon FSx.
- AWS Storage Gateway.
- Amazon DocumentDB.
- Amazon Neptune.
- Amazon Redshift and Redshift Serverless.
- Amazon EKS persistent storage backups.
- AWS CloudFormation stacks.

High-value exam details:

- Amazon S3 backup through AWS Backup is separate from S3 Versioning and S3 Replication.
- RDS and Aurora have native backup features, but AWS Backup can centralize policy and compliance.
- EBS snapshots and EC2 AMI-style backups are common restore patterns.
- EFS backup and restore can restore file systems and, where supported, individual file-system items.
- DynamoDB requires attention to whether standard backup support or AWS Backup advanced features are in scope.

## Restore Patterns

AWS Backup restore behavior is resource-specific, but most restores create a new resource instead of overwriting the existing resource.

Restore workflow:

1. Choose a recovery point.
2. Provide restore metadata such as VPC, subnet, security groups, IAM role, or resource-specific settings.
3. Start a restore job.
4. Validate the restored resource.
5. Redirect traffic or attach dependent resources if needed.

Important restore concepts:

- AWS Backup does not guarantee a fixed restore time SLA.
- Cold storage restores are slower than warm storage restores.
- Some resources support item-level restore.
- Some restore jobs can copy source tags to the restored resource.
- Restore testing can validate whether backup strategy meets RTO requirements.

Common examples:

- EC2: restore an instance or AMI-style backup, then validate networking, IAM role, and security groups.
- EBS: restore a volume from a snapshot and attach it to an instance.
- RDS: restore to a new DB instance or cluster, then update application endpoints or DNS.
- EFS: restore a file system or supported file-system items.
- S3: restore a bucket or individual supported objects depending on the feature and restore method.

Exam warning:

- Restoring a database does not automatically make the application use the restored database. The architecture must still update endpoints, secrets, DNS, or application configuration as needed.

## Compliance and Immutability

### AWS Backup Vault Lock

AWS Backup Vault Lock provides WORM protection for backups in a vault.

Vault Lock helps:

- Prevent early deletion of recovery points.
- Enforce retention policies.
- Protect against accidental or malicious deletion.
- Support compliance requirements that need immutable backup retention.

Vault Lock modes:

- Governance mode: users with sufficient IAM permissions can manage or remove the lock.
- Compliance mode: after the grace period expires, the lock cannot be removed or changed by any user or by AWS while recovery points remain.

Important details:

- Compliance mode has a grace period before it becomes immutable.
- After the grace period, privileged users, including root, cannot delete protected recovery points early.
- Retention must be planned carefully because locked backups can create persistent storage cost.
- Vault Lock is different from Amazon S3 Object Lock and Amazon Glacier Vault Lock.

Exam pattern:

- If the requirement says "cannot be deleted by any user, including root," choose Vault Lock compliance mode.
- If the requirement says "authorized administrators should still be able to manage the lock," governance mode may fit.

### AWS Backup Audit Manager

AWS Backup Audit Manager helps evaluate backup compliance against controls.

Use it when:

- The company needs evidence that resources are included in backup plans.
- Backups must meet minimum retention periods.
- Backup plans must include Vault Lock or cross-account copy.
- Reports are needed for audit or compliance teams.

## Encryption and KMS

AWS Backup uses encryption for recovery points. Encryption behavior depends on the source service, backup vault, and copy destination.

Exam points:

- Destination backup copies are encrypted using the destination vault's KMS key.
- Cross-account backup and restore can require KMS key policy updates.
- If the source resource uses a customer managed KMS key, the backup workflow must have permission to use it.
- A backup can exist but restore can fail if KMS permissions are wrong.

Common KMS permissions issue:

- The backup account has the recovery point, but the restore role or destination account cannot decrypt the backup because the KMS key policy does not allow it.

## AWS Organizations and Backup Policies

AWS Backup can integrate with AWS Organizations for centralized policy management across accounts.

Use AWS Organizations backup policies when:

- Many accounts need consistent backup rules.
- A central platform or security team controls retention and copy requirements.
- New accounts should inherit backup requirements through organizational units.

Exam distinction:

- AWS Organizations backup policies define backup requirements across accounts.
- SCPs set permission guardrails but do not create backups.
- IAM policies grant permissions but do not define backup schedules.

## Common Scenario Questions

### 1. Centralized Backups

A company has EC2, EBS, RDS, EFS, and DynamoDB resources across many accounts. It wants centralized backup scheduling and retention.

Answer: Use AWS Backup with backup plans, tag-based resource assignments, and AWS Organizations backup policies.

Why: AWS Backup centralizes backup policy and monitoring across supported services and accounts.

### 2. Account Compromise Protection

Production backups must remain recoverable even if the production account is compromised.

Answer: Copy backups to a vault in a separate backup account, restrict vault access, and consider Vault Lock compliance mode.

Why: Cross-account copy isolates recovery points from the source account. Vault Lock adds immutability.

### 3. Regional Disaster Recovery

Backups must be available if the primary Region is unavailable.

Answer: Configure cross-Region backup copy to a destination vault in another Region.

Why: Cross-Region copies place recovery points outside the primary Region.

### 4. Regulatory WORM Retention

Backups must be retained for seven years and cannot be deleted by administrators or the root user.

Answer: Use AWS Backup Vault Lock in compliance mode with retention settings that match the regulatory period.

Why: Compliance mode becomes immutable after the grace period and prevents early deletion.

### 5. Cost-Optimized Long-Term Retention

A workload needs backups retained for several years, but restores are rare and can tolerate slower recovery.

Answer: Use lifecycle policies to transition supported backups to cold storage and expire them after the required retention period.

Why: Cold storage lowers long-term backup cost where supported.

### 6. Fast Application Failover

An application needs another Region to serve traffic quickly with minimal data loss.

Answer: Use service-native replication or a multi-Region architecture, not AWS Backup alone.

Why: AWS Backup is for recovery point restore, not continuous active replication or automatic failover.

### 7. Restore Testing

An auditor asks for evidence that backups can be restored within the company's RTO.

Answer: Use AWS Backup restore testing and monitor restore job results.

Why: Backup existence alone does not prove restore readiness.

### 8. Backup Plan Automation

New EBS volumes should automatically receive daily backups if they belong to production applications.

Answer: Assign resources to a backup plan by tag, such as `Environment=Production`.

Why: Tag-based backup plan assignment protects new matching resources without manual selection.

## Quick Exam Memory Checks

- Backup plan: defines schedule, lifecycle, retention, vault destination, and copy actions.
- Backup vault: stores recovery points and controls access.
- Recovery point: a backup you can restore or copy.
- Lifecycle: moves supported backups to cold storage and deletes them after retention.
- Cross-Region copy: protects against regional loss.
- Cross-account copy: protects against source account compromise.
- Vault Lock: immutable WORM backup protection.
- Governance mode: removable by sufficiently privileged users.
- Compliance mode: immutable after grace period.
- Audit Manager: backup compliance checks and reports.
- Restore: usually creates a new resource, not an in-place overwrite.
- AWS Backup is not automatic application failover.

## Sources

- AWS Backup Developer Guide: https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html
- AWS Backup: How it works: https://docs.aws.amazon.com/aws-backup/latest/devguide/how-it-works.html
- Backup plans: https://docs.aws.amazon.com/aws-backup/latest/devguide/about-backup-plans.html
- AWS Backup feature availability: https://docs.aws.amazon.com/aws-backup/latest/devguide/backup-feature-availability.html
- Creating backup copies across AWS Regions: https://docs.aws.amazon.com/aws-backup/latest/devguide/cross-region-backup.html
- AWS Backup Vault Lock: https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html
- Restore a backup by resource type: https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-a-backup.html
- AWS Certified Solutions Architect - Associate exam page: https://aws.amazon.com/certification/certified-solutions-architect-associate/
