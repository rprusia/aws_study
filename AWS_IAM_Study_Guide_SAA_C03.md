# AWS IAM Study Guide for SAA-C03

Focus: AWS Identity and Access Management (IAM), IAM Identity Center, policy evaluation, roles, federation, and common secure-access architecture patterns for the AWS Certified Solutions Architect - Associate exam.

## How to Use This Guide

Use this as a review and decision guide, not just a definition list.

1. Learn the identity types and when to use each one.
2. Memorize the policy evaluation rules.
3. Practice choosing roles, federation, and resource policies in scenario questions.
4. Review the exam traps at the end before taking practice tests.

## High-Yield Exam Rules

- Use the root user only for account-level tasks that require it.
- Enable MFA on the root user.
- Do not create root access keys.
- Prefer IAM Identity Center or federation for workforce access.
- Prefer IAM roles with temporary credentials for AWS services and applications.
- Do not store long-term access keys on EC2 instances, Lambda functions, containers, or in application code.
- Use least privilege: allow only the actions, resources, and conditions required.
- An explicit deny overrides any allow.
- Permissions boundaries and service control policies do not grant permissions; they only limit the maximum possible permissions.
- For cross-account access, the trusted account usually needs permission to call `sts:AssumeRole`, and the target role needs a trust policy allowing that principal.
- For S3, KMS, SQS, SNS, and other resource-policy services, both identity policies and resource policies may be involved.
- For KMS, the key policy is always important. IAM permissions alone are not enough unless the key policy allows IAM policies to grant access.

## IAM Mental Model

IAM answers four questions:

| Question | IAM Concept |
| --- | --- |
| Who is making the request? | Principal |
| What action do they want to perform? | Action |
| Which resource are they trying to access? | Resource |
| Under what conditions should access be allowed? | Condition |

Typical policy statement:

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::example-bucket/*",
  "Condition": {
    "StringEquals": {
      "aws:PrincipalOrgID": "o-exampleorgid"
    }
  }
}
```

## Core IAM Identities

### Root User

The root user is the original account identity and has full access to the AWS account.

Use root only for tasks such as:

- Changing account settings that require root.
- Closing an AWS account.
- Restoring IAM user permissions in a lockout scenario.
- Some billing or support-plan operations.

Exam answer pattern:

- Enable MFA.
- Use a strong password.
- Do not create access keys.
- Store credentials securely.
- Use IAM Identity Center or IAM roles for administration.

### IAM Users

IAM users are long-term identities inside one AWS account. They can have console passwords and access keys.

Use IAM users sparingly:

- Legacy workloads that cannot assume roles.
- Emergency break-glass access.
- External systems that cannot use federation or role assumption.

Avoid IAM users for:

- EC2 applications.
- Lambda functions.
- ECS tasks.
- Human workforce access in a multi-account environment.
- Cross-account application access when roles are available.

### IAM Groups

IAM groups are collections of IAM users. They simplify permission management for users.

Important limitations:

- Groups contain users, not roles.
- Groups cannot be nested.
- Groups are not principals in resource-based policies.
- Groups are not used for AWS service workloads.

### IAM Roles

IAM roles are assumable identities that provide temporary security credentials.

Use roles for:

- EC2 instance profiles.
- Lambda execution roles.
- ECS task roles.
- Cross-account access.
- Federated users.
- Third-party access.
- AWS service integrations.

Exam answer pattern:

If an AWS service or application needs AWS API permissions, assign a role. Do not put access keys in code, environment variables, AMIs, or configuration files unless there is no supported role-based option.

## IAM Identity Center

IAM Identity Center is the preferred service for centrally managing workforce access to AWS accounts and applications.

Use it when the question mentions:

- Multiple AWS accounts.
- Centralized workforce access.
- Corporate identity provider.
- Single sign-on.
- Permission sets.
- Temporary credentials for users.
- Integration with AWS Organizations.

Key concepts:

- Users and groups can come from the Identity Center directory or an external identity provider.
- Permission sets define access that is provisioned into target AWS accounts.
- Users get temporary credentials rather than long-term IAM user access keys.

Exam distinction:

- IAM users are account-local and long-term.
- IAM Identity Center is centralized and designed for workforce access across accounts.
- IAM roles are the runtime mechanism behind much of the access.

## Policy Types

### Identity-Based Policies

Attached to users, groups, or roles. They define what the identity can do.

Examples:

- Allow a role to read from an S3 bucket.
- Allow a developer group to describe EC2 instances.
- Allow a role to call `sts:AssumeRole` into another account.

### Resource-Based Policies

Attached to resources. They define who can access the resource.

Common examples:

- S3 bucket policies.
- KMS key policies.
- SQS queue policies.
- SNS topic policies.
- Lambda function resource policies.
- Secrets Manager resource policies.

Use resource policies when:

- Granting cross-account access directly to a resource.
- Allowing a service principal to access a resource.
- Restricting access based on organization, source account, source ARN, VPC endpoint, or other conditions.

### Trust Policies

A role trust policy defines who can assume the role.

Example:

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::111122223333:role/AppRole"
  },
  "Action": "sts:AssumeRole"
}
```

Common trusted principals:

- Another AWS account.
- A role in another account.
- An AWS service such as EC2 or Lambda.
- A federated identity provider.

### Permissions Boundaries

A permissions boundary sets the maximum permissions an IAM user or role can have.

It does not grant access by itself.

Use it when:

- Developers can create roles but must not exceed a defined permission limit.
- Delegated administrators need guardrails.
- You want to prevent privilege escalation while allowing local IAM management.

### Service Control Policies

Service control policies (SCPs) are AWS Organizations guardrails that set maximum permissions for accounts or organizational units.

SCPs do not grant permissions.

Use SCPs when:

- Restricting what entire accounts or OUs can do.
- Blocking use of specific regions.
- Preventing disabling of security services.
- Enforcing organization-wide restrictions.

Exam distinction:

- IAM policy grants permissions within one account.
- Permissions boundary limits a specific user or role.
- SCP limits accounts or OUs in AWS Organizations.

### Session Policies

Session policies are passed when a role is assumed. They further limit the permissions of that session.

They do not grant permissions beyond the role.

Use them when:

- Issuing scoped-down temporary credentials.
- Limiting one session for a specific task.

## Policy Evaluation

AWS evaluates access roughly like this:

1. Start with implicit deny.
2. Check for explicit deny in any applicable policy. If present, deny.
3. Check whether an applicable policy allows the action.
4. Apply limiting policies such as SCPs, permissions boundaries, and session policies.
5. If the final result includes an allow and no explicit deny blocks it, access is allowed.

Simple exam formula:

```text
Allowed = identity/resource allow
          AND within SCP limits
          AND within permissions boundary if present
          AND within session policy if present
          AND no explicit deny
```

## Common Condition Keys

Condition keys often determine the best answer in secure architecture questions.

| Condition Key | Common Use |
| --- | --- |
| `aws:MultiFactorAuthPresent` | Require MFA |
| `aws:SourceIp` | Restrict by IP address |
| `aws:SourceVpc` | Restrict by source VPC |
| `aws:SourceVpce` | Restrict by VPC endpoint |
| `aws:PrincipalOrgID` | Allow only principals from your AWS Organization |
| `aws:SourceArn` | Limit service access to a specific source resource |
| `aws:SourceAccount` | Prevent confused deputy issues |
| `s3:prefix` | Restrict S3 list operations to a prefix |
| `kms:ViaService` | Allow KMS use only through a specific AWS service |

## Roles and Temporary Credentials

Temporary credentials are issued by AWS Security Token Service (AWS STS).

Benefits:

- Short-lived.
- Automatically rotated for AWS service roles.
- Better than long-term access keys.
- Can be scoped with session policies.
- Work well with federation and cross-account access.

Common role patterns:

| Scenario | Best IAM Choice |
| --- | --- |
| EC2 app needs S3 access | EC2 instance profile role |
| Lambda function needs DynamoDB access | Lambda execution role |
| ECS task needs Secrets Manager access | ECS task role |
| Developer needs access to multiple accounts | IAM Identity Center permission sets |
| Third party needs limited account access | Cross-account role with external ID |
| App in Account A needs resource in Account B | Cross-account role or resource policy |

## Cross-Account Access

### AssumeRole Pattern

Account A principal assumes a role in Account B.

Requirements:

- The principal in Account A has permission to call `sts:AssumeRole` on the target role.
- The role in Account B has a trust policy allowing the principal from Account A.
- The role in Account B has permissions for the target actions.

Best for:

- Administrative cross-account access.
- Workloads that need broader API access in another account.
- Auditing or operations roles.

### Resource Policy Pattern

A resource in Account B directly allows a principal from Account A.

Best for:

- S3 bucket access.
- KMS key access.
- SQS queue access.
- SNS topic access.
- Lambda invocation access.

Exam tip:

For simple access to one resource that supports resource policies, a resource policy may be enough. For broader API access across many resources, use `AssumeRole`.

## External ID and Third-Party Access

Use an external ID when granting third-party access to your AWS account through an IAM role.

Purpose:

- Helps prevent confused deputy problems.
- Ensures the third party includes a unique value when assuming your role.

Exam pattern:

If a vendor, SaaS provider, or partner needs access to your account, choose a cross-account IAM role with an external ID. Do not create an IAM user with access keys for the vendor.

## MFA

MFA adds a second factor for sign-in or sensitive operations.

Use MFA for:

- Root user.
- Privileged users.
- Sensitive role assumption.
- High-risk API operations.

Common condition:

```json
"Condition": {
  "Bool": {
    "aws:MultiFactorAuthPresent": "true"
  }
}
```

Exam trap:

MFA does not replace least privilege. It should be combined with roles, policies, and proper guardrails.

## Access Keys

Access keys are long-term credentials for IAM users.

Best practices:

- Avoid them when roles or federation are available.
- Rotate if they must be used.
- Store in a secure secrets system.
- Do not embed them in code, AMIs, user data, containers, repositories, or mobile apps.
- Monitor use with CloudTrail and IAM credential reports.

Better alternatives:

- IAM roles for AWS compute.
- IAM Identity Center for humans.
- Federation for external identities.
- STS temporary credentials.

## IAM for AWS Services

### EC2

Use an IAM role attached through an instance profile.

Do not:

- Store access keys on the instance.
- Bake credentials into an AMI.
- Put credentials in user data.

### Lambda

Use a Lambda execution role.

The execution role controls what the function can access, such as DynamoDB, S3, CloudWatch Logs, and Secrets Manager.

### ECS

Use:

- Task execution role for pulling images and writing logs.
- Task role for application permissions to call AWS APIs.

Exam distinction:

The task role is what the application code uses. The task execution role is used by the ECS agent and platform.

### EKS

For Kubernetes workloads on EKS, use IAM roles for service accounts (IRSA) or newer pod identity mechanisms when available in the scenario.

Exam principle:

Assign AWS permissions to the workload identity. Do not share node instance role permissions broadly across all pods.

## S3 and IAM

S3 access commonly involves both IAM policies and bucket policies.

Use bucket policies to:

- Enforce HTTPS with `aws:SecureTransport`.
- Restrict access to a VPC endpoint.
- Allow cross-account access.
- Restrict access to your AWS Organization.
- Deny public access patterns.

Use IAM identity policies to:

- Grant specific users or roles actions on buckets and objects.
- Control application permissions.

Common exam details:

- Bucket-level actions use bucket ARN: `arn:aws:s3:::bucket-name`.
- Object-level actions use object ARN: `arn:aws:s3:::bucket-name/*`.
- `s3:ListBucket` applies to the bucket ARN, not the object ARN.
- `s3:GetObject` applies to object ARNs.

## KMS and IAM

KMS permissions are controlled by:

- KMS key policy.
- IAM policies.
- Grants.

High-yield rule:

The key policy must allow access directly or allow IAM policies in the account to grant access.

Use KMS key policies when:

- Granting cross-account access to a key.
- Defining key administrators.
- Defining key users.

Use grants when:

- AWS services need temporary or delegated use of a key.
- You need fine-grained, limited use for a service or principal.

Exam trap:

Giving an IAM role `kms:Decrypt` is not always enough. The KMS key policy must also permit the access path.

## Secrets Manager and Parameter Store

For applications that need secrets:

- Store secrets in AWS Secrets Manager or Systems Manager Parameter Store.
- Grant the application role permission to read only the required secret or parameter.
- If encrypted with a customer managed KMS key, also grant required KMS permissions.

Do not:

- Store database passwords in code.
- Store secrets in EC2 user data.
- Store secrets in plaintext environment variables without a managed secret source.

## IAM Access Analysis and Monitoring

### IAM Access Analyzer

Use IAM Access Analyzer to identify resources shared with external principals.

Good for:

- Finding public or cross-account access.
- Reviewing S3, KMS, IAM role trust, SQS, Lambda, and other resource policies.
- Validating policies before deployment.

### Credential Report

Use IAM credential reports to audit IAM users.

Useful fields:

- Password enabled.
- MFA active.
- Access key age.
- Last used dates.

### Access Advisor

Use service last accessed information to remove unused permissions.

Exam use:

Choose Access Advisor or IAM last accessed data when the scenario asks how to refine least privilege based on actual service usage.

### CloudTrail

CloudTrail records AWS API calls.

Use it to:

- Investigate who made a change.
- Track role assumption events.
- Monitor access key usage.
- Support audit and compliance.

## Least Privilege Workflow

1. Start with the minimum required actions.
2. Scope resources to exact ARNs where possible.
3. Add conditions such as MFA, source VPC endpoint, organization ID, or source account.
4. Test with IAM policy simulator or access analyzer policy checks.
5. Use CloudTrail and Access Advisor to remove unused permissions.

## Common Scenario Decisions

### Scenario: EC2 Needs to Read S3

Best answer:

- Create an IAM role with least-privilege S3 read permissions.
- Attach it to the EC2 instance as an instance profile.

Avoid:

- IAM user access keys on the instance.
- Hardcoded credentials.
- Public S3 bucket access.

### Scenario: Company Has Many AWS Accounts

Best answer:

- Use AWS Organizations.
- Use IAM Identity Center for centralized workforce access.
- Use permission sets for account-specific roles.
- Use SCPs for account guardrails.

Avoid:

- Duplicating IAM users in every account.
- Sharing root credentials.

### Scenario: Vendor Needs Access

Best answer:

- Create a cross-account IAM role.
- Require external ID in the trust policy.
- Grant least privilege.

Avoid:

- Creating an IAM user for the vendor.
- Sharing access keys.
- Granting AdministratorAccess unless explicitly required and justified.

### Scenario: S3 Bucket Must Be Accessible Only From a VPC

Best answer:

- Use a VPC endpoint for S3.
- Add a bucket policy condition requiring the correct `aws:SourceVpce`.

### Scenario: Deny All Actions Outside Approved Regions

Best answer:

- Use an SCP at the OU or account level.

Why:

- Region restrictions are organization guardrails, not individual identity grants.

### Scenario: Developers Can Create Roles but Must Not Escalate

Best answer:

- Require a permissions boundary on created roles.
- Limit `iam:PassRole`.

Why:

- Permissions boundaries cap the maximum permissions of delegated roles.

### Scenario: Lambda Needs to Read a Secret

Best answer:

- Store the secret in Secrets Manager.
- Grant the Lambda execution role `secretsmanager:GetSecretValue` for that secret.
- If using a customer managed KMS key, grant required KMS decrypt permissions through IAM and key policy.

## IAM PassRole

`iam:PassRole` allows a user or service to pass an IAM role to an AWS service.

Common examples:

- User launches an EC2 instance with an instance profile.
- User creates a Lambda function with an execution role.
- User creates an ECS task definition with a task role.

Security risk:

If a user can pass a highly privileged role to a service they control, they may escalate privileges.

Best practices:

- Restrict `iam:PassRole` to specific role ARNs.
- Use conditions such as `iam:PassedToService`.
- Combine with permissions boundaries when delegating role creation.

## Public Access Controls

IAM questions often include public exposure risk.

Use these controls:

- S3 Block Public Access.
- Bucket policies with explicit deny for insecure or public access.
- IAM Access Analyzer to detect external access.
- Resource policies scoped to account, organization, VPC endpoint, or service principal.

Exam tip:

If the scenario asks for preventing accidental public S3 exposure at scale, choose S3 Block Public Access and organization/account-level controls where appropriate.

## Quick Comparison Table

| Need | Best Service or Feature |
| --- | --- |
| Central workforce SSO across accounts | IAM Identity Center |
| App running on EC2 needs AWS permissions | IAM role with instance profile |
| Lambda needs AWS permissions | Lambda execution role |
| ECS app needs AWS permissions | ECS task role |
| Account-wide guardrails | SCP |
| Limit a delegated role creator | Permissions boundary |
| Vendor access | Cross-account role with external ID |
| Public/cross-account resource detection | IAM Access Analyzer |
| Audit IAM users and access keys | IAM credential report |
| Review actual service usage | Access Advisor |
| Track API calls | CloudTrail |
| Scope one assumed-role session | Session policy |

## Common Exam Traps

- Choosing IAM users when roles are available.
- Choosing access keys for workloads running on AWS.
- Forgetting that SCPs do not grant permissions.
- Forgetting that permissions boundaries do not grant permissions.
- Missing an explicit deny.
- Assuming an S3 bucket policy and IAM policy are the same thing.
- Granting `kms:Decrypt` in IAM but ignoring the KMS key policy.
- Allowing `iam:PassRole` too broadly.
- Creating duplicate IAM users across multiple accounts instead of using IAM Identity Center.
- Using root for administrative daily work.
- Granting cross-account access without a trust policy or resource policy.
- Forgetting object-level versus bucket-level S3 ARNs.

## Practice Questions

### 1. EC2 S3 Access

An application on EC2 needs to read objects from one S3 bucket. What is the most secure approach?

A. Store an IAM user's access keys in the application configuration.  
B. Attach an IAM role with least-privilege S3 permissions to the EC2 instance profile.  
C. Make the S3 bucket public and restrict by bucket name.  
D. Use the root user's access keys on the instance.

Answer: B

Why: EC2 should use an IAM role with temporary credentials. Access keys and public buckets are not preferred.

### 2. Multi-Account Workforce Access

A company has 30 AWS accounts and wants centralized employee sign-in using its corporate identity provider. What should it use?

A. IAM users in each account.  
B. IAM Identity Center integrated with the corporate identity provider.  
C. One shared administrator IAM user.  
D. Root user access with MFA.

Answer: B

Why: IAM Identity Center is the preferred centralized workforce access service for multi-account AWS environments.

### 3. Vendor Access

A third-party monitoring vendor needs read-only access to your AWS account. What is the best approach?

A. Create an IAM user and send the access keys to the vendor.  
B. Create a cross-account IAM role requiring an external ID.  
C. Share the root password with the vendor temporarily.  
D. Add the vendor to an IAM group.

Answer: B

Why: Third-party delegated access should use a role with external ID and least privilege.

### 4. Organization Guardrail

Security requires that no account in an OU can launch resources outside approved AWS Regions. What should be used?

A. IAM user policy.  
B. S3 bucket policy.  
C. Service control policy.  
D. Security group rule.

Answer: C

Why: SCPs define maximum permissions for accounts and OUs in AWS Organizations.

### 5. Permission Boundary

A platform team allows developers to create IAM roles, but the roles must never exceed a predefined permission limit. What should be used?

A. Permissions boundary.  
B. Resource-based policy.  
C. Access key rotation.  
D. CloudTrail.

Answer: A

Why: Permissions boundaries cap maximum permissions for IAM users or roles.

### 6. KMS Access

A role has `kms:Decrypt` in an IAM policy but still cannot decrypt with a customer managed KMS key. What is the likely issue?

A. KMS does not support IAM policies.  
B. The key policy does not allow the role or does not allow IAM policies to grant access.  
C. The role must be converted to an IAM user.  
D. MFA is always required for KMS.

Answer: B

Why: KMS authorization depends on the key policy as well as IAM permissions.

### 7. S3 Object Access

Which ARN pattern is required for `s3:GetObject` permissions?

A. `arn:aws:s3:::bucket-name`  
B. `arn:aws:s3:::bucket-name/*`  
C. `arn:aws:iam:::bucket-name/*`  
D. `arn:aws:s3:*:*:bucket-name`

Answer: B

Why: `s3:GetObject` applies to objects, so the object ARN pattern is required.

### 8. Detect External Sharing

Which service helps identify resources that are shared publicly or with external AWS accounts?

A. IAM Access Analyzer.  
B. AWS Budgets.  
C. Amazon Inspector.  
D. AWS Config only.

Answer: A

Why: IAM Access Analyzer analyzes resource policies and detects external access.

## Final Review Checklist

Before the exam, make sure you can explain:

- Difference between IAM users, groups, roles, and IAM Identity Center.
- Why roles are preferred for AWS workloads.
- How `sts:AssumeRole` works for cross-account access.
- How explicit deny affects policy evaluation.
- Difference between identity-based and resource-based policies.
- Difference between SCPs and permissions boundaries.
- Why KMS key policies matter.
- How to secure S3 access with IAM and bucket policies.
- When to use external ID.
- Why broad `iam:PassRole` is dangerous.

