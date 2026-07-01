# AWS Certified Solutions Architect - Associate: IAM Study Notes

Current focus: AWS Identity and Access Management (IAM) for SAA-C03 secure architecture questions.

## Exam Weight

IAM is most directly tested in Domain 1: Design Secure Architectures, especially Task Statement 1.1: Design secure access to AWS resources. Expect IAM to appear inside multi-account, least privilege, cross-account access, federation, application access, data access, and KMS policy scenarios.

Key exam framing:

- Prefer role-based temporary credentials over long-term access keys.
- Prefer centralized workforce access with IAM Identity Center or federation over individual IAM users.
- Use least privilege, MFA, and separation of duties.
- Understand which policy type grants access, which policy type limits access, and how explicit denies override allows.

## Core IAM Building Blocks

### Root User

The root user has full account access and should not be used for daily administration.

Exam answers usually favor:

- Enable MFA on the root user.
- Do not create root access keys.
- Use root only for account-level tasks that require it.
- Create administrative access through IAM Identity Center or tightly controlled IAM roles.

### IAM Users

IAM users are long-term identities in a single AWS account. They can have passwords for the console and access keys for programmatic access.

Use IAM users only when a role or federation is not supported, such as some legacy tools, certain external clients, or emergency access patterns. Avoid choosing IAM users for EC2, Lambda, ECS, applications, or human workforce access when roles or federation are available.

### IAM Groups

Groups are collections of IAM users. Policies attached to a group apply to all users in the group.

Important limitations:

- Groups contain users, not roles or other groups.
- Groups are an account-level IAM management convenience.
- Groups are not used for AWS service workloads.

### IAM Roles

IAM roles are assumable identities with temporary credentials. Roles do not have long-term passwords or access keys.

Use roles for:

- AWS services such as EC2, Lambda, ECS, and AWS Glue.
- Cross-account access.
- Federation from corporate identity providers.
- Third-party delegated access.
- Applications that need AWS API access.

Exam rule: If a workload runs on AWS and needs AWS permissions, attach or assign a role. Do not store access keys on the instance, in code, or in configuration files.

## Policy Types

### Identity-Based Policies

Attached to IAM users, groups, or roles. They define what the principal can do.

Examples:

- Allow a role to read from an S3 bucket.
- Allow a user group to manage EC2 instances.
- Allow a role to call `sts:AssumeRole` into another account.

### Resource-Based Policies

Attached to a resource. They define who can access that resource.

Common exam examples:

- S3 bucket policies.
- KMS key policies.
- SQS queue policies.
- SNS topic policies.
- Lambda resource policies.

Resource policies are commonly used for cross-account access when the service supports them. Some scenarios still require an IAM role, especially when the caller needs broad access to multiple resources or the service does not support direct resource policies.

### Trust Policies

A trust policy is a resource-based policy attached to an IAM role. It defines who or what can assume the role.

A role usually needs two sides:

- Trust policy: who can assume the role.
- Permissions policy: what the role can do after it is assumed.

Cross-account example:

- Account A owns the resource and creates a role.
- Account A role trust policy trusts Account B or a specific principal in Account B.
- Account A role permissions policy grants access to the required resources.
- Account B principal has permission to call `sts:AssumeRole` on the role in Account A.

### Permissions Boundaries

A permissions boundary sets the maximum permissions that an IAM user or role can receive from identity-based policies.

Important:

- A boundary does not grant permissions by itself.
- Effective permissions are the intersection of the identity-based policy and the boundary.
- Explicit deny still wins.
- Useful when delegating IAM administration while preventing privilege escalation.

Exam scenario: A developer can create roles, but must not create an admin role. Use a permissions boundary on roles the developer creates.

### Service Control Policies (SCPs)

SCPs are AWS Organizations guardrails that set maximum available permissions for accounts in an organization.

Important:

- SCPs do not grant permissions.
- SCPs apply to member accounts, not the management account.
- Effective permissions are limited by the intersection of IAM permissions and applicable SCPs.
- Explicit deny in an SCP overrides an allow in IAM.
- SCPs require AWS Organizations with all features enabled.

Exam scenario: Prevent all member accounts from disabling CloudTrail or leaving approved Regions. Use SCPs.

## Policy Evaluation Logic

Core sequence to memorize:

1. AWS authenticates the principal when required.
2. AWS gathers the request context.
3. AWS evaluates applicable policies.
4. Default result is implicit deny.
5. An explicit allow is required.
6. Any explicit deny overrides all allows.

Effective permission patterns:

- Identity policy + resource policy in same account: union of allows, unless explicit deny.
- Identity policy + permissions boundary: intersection.
- Identity policy + SCP: intersection.
- Identity policy + SCP + permissions boundary: must be allowed by all applicable limiting policies.

Shortcut:

- Grants: identity policies and resource policies.
- Limits: permissions boundaries and SCPs.
- Overrides: explicit deny.

## STS and Temporary Credentials

AWS Security Token Service (STS) issues temporary security credentials.

Common operations and concepts:

- `AssumeRole`: used for cross-account access and role switching.
- `AssumeRoleWithSAML`: used for SAML federation.
- `AssumeRoleWithWebIdentity`: used for OIDC federation, such as some external identity providers or Kubernetes service account patterns.
- Temporary credentials include access key ID, secret access key, and session token.

Exam rule: For delegated or federated access, choose STS and roles instead of distributing long-term IAM user access keys.

Role chaining:

- A role assumes another role.
- Role chaining sessions are limited to a maximum of 1 hour.
- This limit can matter in troubleshooting or design questions.

## Federation and IAM Identity Center

Federation lets users authenticate with an external identity provider and receive AWS role-based access.

Use federation for:

- Corporate directory users.
- SAML 2.0 identity providers.
- OIDC identity providers.
- Workforce access across many AWS accounts.

IAM Identity Center is the preferred service for centralized workforce access to multiple AWS accounts and cloud applications. It integrates with AWS Organizations and external identity providers.

Exam clues:

- "Employees already use corporate Active Directory / Okta / Entra ID": choose federation or IAM Identity Center.
- "Need centralized access to multiple AWS accounts": choose IAM Identity Center with permission sets.
- "Avoid creating IAM users in every account": choose federation / IAM Identity Center.

## Cross-Account Access

Preferred pattern: create a role in the account that owns the resource, and allow trusted principals from another account to assume it.

Design checklist:

- Resource-owning account creates the role.
- Trust policy allows the external principal or account.
- Role permissions allow the needed actions on resources.
- Calling principal has permission to call `sts:AssumeRole`.
- Use an external ID for third-party access to reduce confused deputy risk.

Resource policy alternative:

- Use when the service supports it and the access is resource-specific.
- Common for S3 bucket policies, SQS queue policies, SNS topic policies, KMS key policies, and Lambda invoke permissions.

Third-party vendor scenario:

- Create a role in your account.
- Trust the vendor's AWS account.
- Require an external ID.
- Grant only required permissions.

## Least Privilege and Access Management

Least privilege means granting only the actions and resources required.

Useful tools and patterns:

- Start broad only when necessary, then refine using IAM Access Analyzer or last accessed data.
- Use AWS managed policies for quick starts, but prefer customer managed policies for production least privilege.
- Use condition keys to restrict access by MFA, source VPC endpoint, source IP, requested Region, resource tags, or principal tags.
- Use ABAC when access maps naturally to tags.
- Use resource-level permissions where supported.
- Rotate or remove unused access keys.

Common condition examples:

- Require MFA for sensitive actions.
- Restrict S3 access to a VPC endpoint.
- Restrict actions to approved AWS Regions.
- Allow access only when `PrincipalTag` matches `ResourceTag`.

## IAM and AWS Organizations

Use Organizations for multi-account governance.

Common services and patterns:

- AWS Organizations: account hierarchy and SCPs.
- Organizational units (OUs): group accounts by environment, workload, or compliance boundary.
- AWS Control Tower: landing zone and account governance.
- IAM Identity Center: centralized workforce login and permission sets.
- SCPs: maximum permissions guardrails.

Exam decision examples:

- Need to centrally block actions across accounts: SCP.
- Need to create secure multi-account baseline: Control Tower.
- Need centralized human access: IAM Identity Center.
- Need per-account workload permissions: IAM roles and identity/resource policies.

## Common Scenario Patterns

### EC2 Needs S3 Access

Best answer: Attach an IAM role through an instance profile to the EC2 instance.

Avoid:

- Storing access keys on the instance.
- Hardcoding credentials in the application.

### Lambda Needs DynamoDB Access

Best answer: Attach an execution role to the Lambda function with least-privilege permissions for the target DynamoDB table.

### Cross-Account S3 Access

Possible answers:

- S3 bucket policy that allows the external account or role.
- Cross-account IAM role if the external principal needs a broader delegated session.

Also check KMS if the bucket uses SSE-KMS. The caller needs both S3 permissions and KMS key permissions.

### Vendor Needs Access to Your Account

Best answer: Cross-account IAM role with external ID and least-privilege permissions.

Avoid:

- IAM user access keys for the vendor.
- Sharing root credentials.

### Developers Need to Create Roles, But Not Admin Roles

Best answer: Use permissions boundaries.

### Block Dangerous Actions Across All Member Accounts

Best answer: Use SCPs in AWS Organizations.

Remember: SCPs limit maximum permissions but do not grant permissions.

### Users Need One Login Across Many AWS Accounts

Best answer: IAM Identity Center integrated with the corporate identity provider and AWS Organizations.

### Mobile or Web App Users Need App-Level AWS Access

Best answer often involves Amazon Cognito for application user identity, not IAM users for each app user.

## Policy Troubleshooting Checklist

When access is denied, check:

1. Is there an explicit deny?
2. Is there an identity-based allow?
3. Is a resource policy required or blocking access?
4. Is an SCP limiting the account?
5. Is a permissions boundary limiting the principal?
6. Is a session policy limiting the assumed role session?
7. Is the KMS key policy allowing the action?
8. Is the resource ARN correct?
9. Does the condition match the request context?
10. Is the principal using the expected role/session?

## High-Yield Exam Reminders

- IAM is global, not Regional.
- IAM users and groups are account-scoped.
- Roles are assumable and use temporary credentials.
- Groups cannot contain groups.
- Resource policies are attached to resources.
- Trust policies are attached to roles.
- Permissions boundaries and SCPs do not grant permissions.
- Explicit deny always wins.
- Use roles for AWS services.
- Use external ID for third-party cross-account role access.
- Use IAM Identity Center for centralized workforce access.
- Use SCPs for multi-account guardrails.
- Use KMS key policies plus IAM policies for KMS access.
- Do not use root for daily work.
- Do not hardcode access keys in applications.

## Practice Questions

### 1. EC2 and S3

An application on EC2 needs to read objects from one S3 bucket. What is the most secure design?

Answer: Create an IAM role with least-privilege S3 read access and attach it to the EC2 instance through an instance profile.

Why: The application receives temporary credentials automatically. No long-term access keys are stored.

### 2. Third-Party Audit

A third-party auditor needs read-only access to resources in your AWS account. What should you configure?

Answer: Create a cross-account IAM role with read-only permissions, trust the auditor's AWS account, and require an external ID.

Why: This provides delegated access with temporary credentials and reduces confused deputy risk.

### 3. Organization-Wide Guardrail

A company must prevent all member accounts from disabling AWS CloudTrail. What should be used?

Answer: An SCP attached to the appropriate OU or root of the organization.

Why: SCPs set maximum permissions across member accounts. Use care when applying SCPs broadly.

### 4. Permission Boundary

A platform team lets developers create IAM roles, but developers must not create roles with permissions above a defined limit. What should be used?

Answer: Permissions boundaries.

Why: The boundary limits the maximum permissions that identity-based policies can grant.

### 5. Corporate Login

Employees authenticate with a corporate identity provider and need access to multiple AWS accounts. What is the best approach?

Answer: IAM Identity Center integrated with the identity provider and AWS Organizations.

Why: This centralizes workforce access and avoids creating IAM users in each account.

## Sources

- AWS Certified Solutions Architect - Associate exam page: https://aws.amazon.com/certification/certified-solutions-architect-associate/
- AWS Certified Solutions Architect - Associate SAA-C03 exam guide: https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf
- IAM policy evaluation logic: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
- IAM roles: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html
- AWS Organizations SCPs: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html
