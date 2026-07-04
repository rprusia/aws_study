# AWS Certified Solutions Architect – Associate (SAA-C03)
## Core Services Study Guide

> Condensed from the "Core Services" course transcript. Organized for quick lookup — use the Table of Contents to jump to a section. **💡 Exam Tip** callouts highlight the points the instructor repeatedly flagged as exam-critical.

---

## Table of Contents

1. [AWS IAM (Identity and Access Management)](#1-aws-iam-identity-and-access-management)
   - [1.1 IAM Overview & Root User](#11-iam-overview--root-user)
   - [1.2 IAM Users & Groups](#12-iam-users--groups)
   - [1.3 IAM Policies](#13-iam-policies)
   - [1.4 Access Keys & Credential Reports](#14-access-keys--credential-reports)
   - [1.5 IAM Roles, Trust Policies & STS](#15-iam-roles-trust-policies--sts)
2. [AWS CloudShell](#2-aws-cloudshell)
3. [Amazon VPC Fundamentals](#3-amazon-vpc-fundamentals)
   - [3.1 VPC Overview & CIDR Math](#31-vpc-overview--cidr-math)
   - [3.2 Subnets & Route Tables](#32-subnets--route-tables)
   - [3.3 Security Groups vs. NACLs](#33-security-groups-vs-nacls)
   - [3.4 DHCP Option Sets](#34-dhcp-option-sets)
4. [VPC Peering, Gateways & Endpoints](#4-vpc-peering-gateways--endpoints)
   - [4.1 VPC Peering](#41-vpc-peering)
   - [4.2 NAT Gateway & Elastic IPs](#42-nat-gateway--elastic-ips)
   - [4.3 Gateway Endpoints vs. Interface Endpoints](#43-gateway-endpoints-vs-interface-endpoints)
5. [Amazon EC2](#5-amazon-ec2)
   - [5.1 EC2 & AMI Overview](#51-ec2--ami-overview)
   - [5.2 Instance Types & Sizing](#52-instance-types--sizing)
   - [5.3 EC2 Storage: EBS & Instance Store](#53-ec2-storage-ebs--instance-store)
   - [5.4 EBS Snapshots & Encryption](#54-ebs-snapshots--encryption)
   - [5.5 Connecting to EC2 (SSH/RDP/Session Manager/Bastion)](#55-connecting-to-ec2-sshrdpsession-managerbastion)
   - [5.6 ENI, EIP & Enhanced Networking](#56-eni-eip--enhanced-networking)
   - [5.7 Placement Groups & Outposts](#57-placement-groups--outposts)
   - [5.8 EC2 Pricing Models](#58-ec2-pricing-models)
6. [File Storage: EFS & FSx](#6-file-storage-efs--fsx)
7. [Amazon S3](#7-amazon-s3)
   - [7.1 S3 Overview & Buckets](#71-s3-overview--buckets)
   - [7.2 S3 Storage Classes](#72-s3-storage-classes)
   - [7.3 Versioning, Lifecycle & Replication](#73-versioning-lifecycle--replication)
   - [7.4 S3 Important Features](#74-s3-important-features)
   - [7.5 S3 Security](#75-s3-security)
8. [Amazon Route 53](#8-amazon-route-53)
   - [8.1 DNS & Hosted Zones](#81-dns--hosted-zones)
   - [8.2 Record Types](#82-record-types)
   - [8.3 Routing Policies](#83-routing-policies)
   - [8.4 Health Checks & Hybrid DNS](#84-health-checks--hybrid-dns)
9. [VPNs & Direct Connect](#9-vpns--direct-connect)
   - [9.1 VPN Options](#91-vpn-options)
   - [9.2 Direct Connect](#92-direct-connect)
   - [9.3 Direct Connect Gateway & Transit Gateway](#93-direct-connect-gateway--transit-gateway)
10. [Advanced VPC Security Features](#10-advanced-vpc-security-features)
11. [AWS Directory Services & IAM Identity Center](#11-aws-directory-services--iam-identity-center)
12. [Advanced IAM: Policy Evaluation & Conditions](#12-advanced-iam-policy-evaluation--conditions)

---

## 1. AWS IAM (Identity and Access Management)

### 1.1 IAM Overview & Root User

- **IAM** = a global service offering a unique authentication database, logically isolated to a single AWS account.
- Lets you create **users**, **groups**, and **roles**, and define access controls for what they can/can't do.
- **Root user** = the account created with your sign-up email. Has full, unfederated (total) access — can erase everything, change billing, close the account.

> 💡 **Exam Tips**
> - IAM is a **global** service.
> - **Immediately enable MFA** on the root user.
> - **Never use root for daily tasks** — create an IAM user instead.
> - **Never create access keys for the root user.**
> - Root user email must be **globally unique** across AWS accounts (use email aliasing to reuse an inbox).

### 1.2 IAM Users & Groups

- **IAM User** = entity representing a human or service needing long-term credentials.
- **IAM Group** = collection of users for simplified permission management (assign once to the group, all members inherit it).
- Users can belong to **multiple groups** (permissions are additive).
- **Groups cannot be nested** inside other groups.
- Two authentication methods for users: **basic auth** (username/password, console) and **access keys** (programmatic).

> 💡 **Exam Tip:** Best practice is to always assign permissions via **groups**, not directly to individual users.

### 1.3 IAM Policies

An IAM policy is a JSON document that defines permissions for an identity or resource.

**Six policy types exist**, but the two core ones for this exam are:

| Type | Attached To | Notes |
|---|---|---|
| **Identity-based** | Users, groups, roles | Grants permissions to an identity |
| **Resource-based** | AWS resources (e.g., S3 bucket, KMS key) | Grants a specific *principal* access to that resource; useful for **cross-account access** |

**Identity-based policy subtypes:**

| Subtype | Reusable? | Notes |
|---|---|---|
| **AWS Managed** | Yes | Created/maintained by AWS, usable by everyone, no account ID in ARN |
| **Customer Managed** | Yes | You create/manage/reuse; best practice = start from an AWS managed policy baseline |
| **Inline** | **No** | One-to-one with a single identity; deleted when the identity is deleted; best for narrow one-off needs |

**Policy JSON fields:**

| Field | Required? | Purpose |
|---|---|---|
| `Version` | Yes | Policy language version |
| `Statement` | Yes | List of permission statements |
| `Sid` | No | Human-readable statement ID |
| `Effect` | Yes | `Allow` or `Deny` |
| `Principal` | Resource-based only | Who the policy applies to |
| `Action` | Yes | API calls being allowed/denied |
| `Resource` | Yes | ARNs the actions apply to |
| `Condition` | No | Extra restrictions (e.g., require MFA, restrict by source IP) |

> 💡 **Exam Tips**
> - **Default is implicit deny** — if not explicitly allowed, it's denied.
> - You **must** be able to read/interpret a policy document — this shows up on the exam.
> - Prefer **customer/AWS managed** policies over inline whenever possible (easier management, reusability).
> - Resource-based policies are **inline by nature** — deleting the resource deletes the policy.

### 1.4 Access Keys & Credential Reports

- **Access keys** = long-term credentials (Access Key ID + Secret Access Key) for **programmatic** access only (CLI/SDK) — never used for console login.
- The **Secret Access Key is only viewable once**, at creation.
- **IAM Credential Reports**: downloadable CSV of all users, password status, access key status, MFA status — used for **auditing/compliance**.

> 💡 **Exam Tips**
> - If a key pair is compromised, **deactivate immediately** (don't need to delete right away).
> - Rotate keys/passwords regularly (common practice: every 90 days).
> - Credential reports only refresh with **new data every 4 hours** — generating multiple reports within that window returns identical data.

### 1.5 IAM Roles, Trust Policies & STS

- **IAM Role** = an assumable identity (not logged into directly) using **temporary, rotating credentials**.
- Backed by **AWS Security Token Service (STS)** — generates short-lived credentials (as little as 15 min, up to 12 hours).
- A **session** created by assuming a role includes an Access Key, Secret Key, **and a Session Token** (session token is required to use the temporary creds).
- **Role types**: service-linked role, instance profile (for EC2), federated identity roles (SAML/OIDC).

**Two policies work together for a role:**
| Policy | Purpose |
|---|---|
| **Permissions policy** | What the role can do |
| **Trust policy** | **Who** can assume the role (resource-based JSON; action = `sts:AssumeRole`) |

**Common role use cases:** Lambda accessing DynamoDB, EC2 accessing S3 (via **instance profile**), cross-account access for auditors/third parties.

> 💡 **Exam Tips**
> - **Always prefer roles over long-term access keys** wherever possible — this is one of the most repeated tips in the course.
> - A role **requires** a trust policy — no trust = no one can assume it.
> - EC2 instances need an **instance profile** attached to a role to use it — you don't attach the role directly.
> - Remember the key action: `sts:AssumeRole`.

---

## 2. AWS CloudShell

- A **browser-based shell** pre-authenticated with your current console credentials (IAM user or assumed role).
- Comes with pre-installed software/tools (including the **AWS CLI**, already configured).
- Great for quick CLI tasks without configuring a local CLI.

> 💡 **Exam Tip:** If a scenario needs a *quick, pre-installed, pre-authenticated* CLI environment, think **CloudShell**.

---

## 3. Amazon VPC Fundamentals

### 3.1 VPC Overview & CIDR Math

- A **VPC** = logically isolated network in AWS Cloud where you control CIDR ranges, subnets, route tables, gateways.
- **Default VPC**: auto-created per region (CIDR `172.31.0.0/16`), gives instances **public IPs by default** — never use for production.
- **Custom VPC**: you define the CIDR — use this for real workloads.
- VPCs are **regional resources** (never span regions). Soft limit: **5 VPCs per region per account**.
- IPv4 CIDR: **required**, range **/16 to /28**. IPv6 CIDR: optional, range **/44 to /60**.
- Must fall within **RFC 1918 private IP ranges**:

| Range | CIDR |
|---|---|
| 10.0.0.0 | /8 |
| 172.16.0.0 | /12 |
| 192.168.0.0 | /16 |

**CIDR math:** total bits = 32. Usable IPs = `2^(32 - prefix length)`. Example: `/16` → 2^16 = 65,536 IPs.

> 💡 **Exam Tips**
> - Practice CIDR math — it comes up.
> - Private IP ranges are **not publicly resolvable**.
> - Never leave production workloads in the **default VPC**.

### 3.2 Subnets & Route Tables

- **Subnets** are reserved IP ranges **within a single Availability Zone** (never span AZs).
- Support IPv4, IPv6, and dual-stack.
- **Public subnet** = has a route to an Internet Gateway; **private subnet** = does not.
- A subnet gets **exactly one route table**; a route table **can** be associated with **multiple subnets**.
- Every VPC has a **main route table** (default for unassociated subnets).
- Route table fields: **Destination** (traffic/IP range) and **Target** (where it's routed).
- Longest prefix match (**most specific route wins**).
- **AWS reserves 5 IP addresses per subnet CIDR** (e.g., a /24 with 256 IPs → only 251 usable).

> 💡 **Exam Tip:** Remember the "5 reserved IPs per subnet" rule — commonly tested in capacity-planning questions.

### 3.3 Security Groups vs. NACLs

| Feature | Security Group | NACL |
|---|---|---|
| **State** | **Stateful** (return traffic auto-allowed) | **Stateless** (must define inbound *and* outbound separately) |
| **Applies to** | ENI / instance level | Subnet level |
| **Rules** | **Allow only** (no explicit deny) | Allow **and** deny |
| **Evaluation** | All rules evaluated; combined/aggregated across multiple SGs attached | **Rules processed in number order — first match wins** |
| **Scope** | Can attach multiple SGs to a resource | **One NACL per subnet** (but one NACL can apply to multiple subnets) |

> 💡 **Exam Tips**
> - You can **reference a security group ID as the source** in another SG's rule instead of an IP range — very efficient, common exam scenario.
> - NACLs are a fast, cost-effective way to **block malicious IP ranges** across many resources at once.

### 3.4 DHCP Option Sets

- Specify DHCP-related settings (domain name, DNS servers, NTP, NetBIOS) for the VPC.

> 💡 **Exam Tip:** DHCP option sets **cannot be modified once created** — you must create a new set and associate it, then remove the old one.

---

## 4. VPC Peering, Gateways & Endpoints

### 4.1 VPC Peering

- Direct, private connection between two VPCs over the AWS backbone (no public internet).
- Supports **same account, cross-account, and cross-region** peering.
- Process: **Requester** VPC sends the request → **Acceptor** VPC accepts/denies. Each connection gets a unique **Peering Connection ID** and ARN.
- After acceptance: must update **route tables** in both VPCs, plus configure NACLs/SGs correctly.

> 💡 **Exam Tips**
> - **No overlapping CIDRs allowed** between peered VPCs — will not work at all.
> - **Peering is NOT transitive** (if A↔B and A↔C, B cannot talk to C through A — a direct B↔C peer is required).
> - You can reference **peered VPC security group IDs** in rules (same region only).
> - **Use cases**: centralized shared services hub, multi-region app deployments, cross-account M&A integrations.
> - For "connect many VPCs to one shared service" at scale, think **AWS PrivateLink** instead of peering (no route table updates, no NAT/IGW needed on the consumer side; requires an NLB on the provider side).

### 4.2 NAT Gateway & Elastic IPs

- **NAT Gateway**: lets **private subnet** resources reach the internet outbound while remaining unreachable from the internet inbound.
- Must be deployed in a **public subnet** with a route to an Internet Gateway.
- Scales automatically up to **100 Gbps**; fully managed (no infrastructure to maintain).
- **Redundant only within its own AZ** — deploy one per AZ for high availability.
- **You do NOT attach security groups to a NAT Gateway** (control access via NACLs at the subnet level instead).
- **Elastic IP (EIP)**: a static, public IPv4 address you allocate to your account; regional; billed while allocated; doesn't change over time (unlike ephemeral public IPs).

> 💡 **Exam Tips**
> - NAT Gateway = the go-to answer for "private resources need secure outbound internet access."
> - No security groups on NAT Gateways — common trick question.
> - Deploy NAT Gateways in **multiple AZs** for HA.

### 4.3 Gateway Endpoints vs. Interface Endpoints

Both let you reach AWS services **without traversing the public internet**.

| Feature | Gateway Endpoint | Interface Endpoint |
|---|---|---|
| Mechanism | Route table entry pointing to a managed prefix list | Deploys an **ENI** into a subnet |
| Cost | **Free** | Costs money (ENI + data processing) |
| Supported services | **Only S3 and DynamoDB** | Many more AWS services |
| Security control | Via route tables/endpoint policy | Via **security groups** (like an EC2 instance) |
| Powered by | — | **AWS PrivateLink** |

> 💡 **Exam Tips**
> - **S3 supports BOTH** endpoint types — choice comes down to cost (gateway) vs. control/broader service support (interface).
> - Gateway endpoints only work for **S3 and DynamoDB** — memorize this, it narrows down answers fast.
> - Turn on **private DNS** in the VPC so standard AWS service DNS names automatically route through interface endpoints.

---

## 5. Amazon EC2

### 5.1 EC2 & AMI Overview

- EC2 = on-demand, scalable virtual machines (IaaS). Pay only while running.
- **Key Pairs**: asymmetric key used **only** to connect to instances (SSH into Linux directly; decrypt the Windows admin password for RDP). Not used for data encryption.
- **AMI (Amazon Machine Image)**: template containing OS + config needed to launch an instance. Must select one before launch.
  - **Public AMI**: available to everyone (base OS images).
  - **Private AMI**: yours, optionally shared with specific accounts — great for "golden images" with pre-baked patches/software.

### 5.2 Instance Types & Sizing

Naming convention example: `t4g.micro` → **Family (T)** + **Generation (4g)** + **Size (micro)**.

| Family | Best For | Example Types |
|---|---|---|
| General Purpose | Balanced compute/memory/network; burstable workloads | M, T |
| Compute Optimized | High-performance processing, batch/modeling | C |
| Memory Optimized | Large in-memory datasets, caching | R, X, Z |
| Accelerated Computing | GPU workloads — video transcoding, rendering, ML | P, G |
| Storage Optimized | High sequential read/write, high IOPS | I |
| HPC Optimized | Genomics, simulations, large-scale ML | Hpc-family |

> 💡 **Exam Tip:** T-family instances are **burstable** (can temporarily exceed baseline using credits).

### 5.3 EC2 Storage: EBS & Instance Store

Two EC2 storage categories: **Block storage** (EBS, Instance Store) and **File storage** (EFS, FSx — covered later).

**Amazon EBS**
- Durable, network-attached block storage that behaves like a local disk.
- Bound to a **single EC2 instance** (except multi-attach) and a **single AZ**.
- **Root volume**: default = **deleted on termination**. Additional volumes: default = **NOT deleted on termination** (opposite defaults — commonly tested).
- Billed for **provisioned** capacity, regardless of usage.
- Can resize and change volume type **without downtime**.

**EBS Volume Types**

| Category | Types | Best For |
|---|---|---|
| General Purpose SSD | gp2, **gp3** (prefer gp3) | Balanced cost/performance, boot volumes |
| Provisioned IOPS SSD | io1, **io2** (prefer io2 — cheaper, more durable) | Databases, latency-sensitive, high IOPS |
| Magnetic (HDD) | st1 (throughput optimized), sc1 (cold, cheapest) | Archives, infrequent access, high throughput sequential |

> 💡 **Exam Tips**
> - **IOPS** = reads/writes per second → choose **io1/io2** when the question emphasizes input/output performance.
> - **Throughput** = MB/s of data moved → choose **st1** when the question emphasizes large datasets/throughput.
> - **EBS Multi-Attach**: only on provisioned IOPS volumes, up to **16 instances**, **same AZ only**, requires a **cluster-aware file system** (e.g., not ext4/XFS — needs something like a Gluster-based FS).

**EC2 Instance Store**
- **Ephemeral** (temporary) block storage physically attached to the host.
- Data is **lost** on stop, hibernate, or terminate (survives reboot).
- Best for: buffers, caches, scratch/temporary data — nothing you need to keep.

### 5.4 EBS Snapshots & Encryption

- **Snapshot** = point-in-time, **incremental** backup of an EBS volume, stored in **S3** (but you have **no direct access** to that underlying S3 storage — manage only via the EBS console).
- First snapshot = full copy (slower); subsequent snapshots = delta only (faster).
- Snapshots can be **shared across accounts** and **copied across regions**.
- **Fast Snapshot Restore**: eliminates initial I/O latency when creating a volume from a snapshot (only for snapshots ≤ 16 TiB).
- **EBS Encryption**: uses **AWS KMS**, AES-256. Encrypts data at rest, in-transit between volume and instance, and all future snapshots/volumes derived from it.

> 💡 **Exam Tips**
> - You **cannot directly encrypt** an existing unencrypted volume — create a **snapshot**, then create a new **encrypted** volume from it.
> - Use snapshots to move EBS data between **AZs or regions**.

### 5.5 Connecting to EC2 (SSH/RDP/Session Manager/Bastion)

| Method | Port/Mechanism | Notes |
|---|---|---|
| **SSH** | 22 | Linux; uses private key directly |
| **RDP** | 3389 | Windows; private key decrypts the admin password |
| **EC2 Instance Connect** | Port 22 under the hood | Pushes a temporary key via API; must allow AWS's IP range |
| **Session Manager (SSM)** | Agent-based, no inbound ports needed | **Most secure option** — no open inbound SG rules required |
| **Bastion Host / Jump Box** | SSH into a public-subnet server, then hop to private resources | Used when you need custom OS-level firewall/auth control |

- **Session Manager** requires: correct **IAM permissions**, network connectivity to SSM (via IGW, NAT Gateway, or **VPC interface endpoints** for SSM, SSM Messages, EC2 Messages), and the **SSM Agent** running.
- **Instance Metadata Service (IMDS)**: query at `169.254.169.254` (same URL for both IMDSv1 and IMDSv2) for user data, hostname, security groups, temporary IAM role credentials, etc.

> 💡 **Exam Tips**
> - **Favor Session Manager over Bastion hosts** in almost every scenario — it's the recommended, most secure default answer.
> - Memorize the IMDS URL: **169.254.169.254**.
> - Bastion hosts sit in a **public subnet**; you can reference the Bastion's SG ID as the allowed source in internal SGs.

### 5.6 ENI, EIP & Enhanced Networking

- **ENI (Elastic Network Interface)**: virtual network card; bound to a **single AZ**; can be detached/reattached to another instance in the same AZ; carries private IPv4/IPv6, optional EIP, and its **security groups travel with it**.
- **Ephemeral public IPv4**: pulled from AWS's pool; released when the instance is stopped/hibernated/terminated or when an EIP is assigned — **do not assume it stays the same**.
- **Elastic IP (EIP)**: static, doesn't change; regional; soft limit of 5 per region per account; prefer DNS names over EIPs when possible; use EIPs only when a **static IP is genuinely required**.

**Enhanced Networking Options**

| Type | Best For | Notes |
|---|---|---|
| ENI | Basic day-to-day networking | Standard |
| Elastic Network Adapter (ENA) | High-performance networking, up to 100 Gbps | Preferred over Intel 82599 VF |
| Elastic Fabric Adapter (EFA) | HPC & Machine Learning | Uses **OS-Bypass**; **Linux only**, not supported on Windows |

### 5.7 Placement Groups & Outposts

| Placement Strategy | Behavior | Use Case |
|---|---|---|
| **Cluster** | Instances packed close together, single AZ | Low-latency, high-throughput (HPC) |
| **Spread** | Instances on distinct hardware/racks (own power/network) | Small number of critical, isolated instances |
| **Partition** | Instances spread across logical partitions (separate hardware) | Large distributed workloads (Hadoop, Cassandra) — up to 7 partitions |

- **AWS Outposts**: brings AWS infrastructure/services on-prem. **Racks** (42U, scalable to 96 racks) or **Servers** (1U/2U, small footprint like retail/branch offices).

> 💡 **Exam Tip:** "Extend AWS into your own data center" = **AWS Outposts**.

### 5.8 EC2 Pricing Models

| Model | Description | Discount |
|---|---|---|
| **On-Demand** | Pay by hour/second, no commitment | Baseline price |
| **Spot Instances** | Bid on unused capacity; can be interrupted | Up to 90% off — **never use for critical workloads** |
| **Reserved Instances** | 1 or 3-year commitment | Up to 72% off (being phased out in favor of Savings Plans) |
| **Savings Plans** (Compute / EC2 Instance / SageMaker) | Commit to $/hr spend | Compute SP up to 66%, EC2 Instance SP up to 72% |
| **Dedicated Instances** | Instance runs on hardware not shared with others | Most expensive EC2 option |
| **Dedicated Hosts** | Entire physical server allocated to you | Most expensive overall — needed for per-socket/per-core licensing |
| **Spot Blocks** | Spot capacity for 1–6 hours, fewer interruptions | Smaller discount than standard Spot |

- **AWS Compute Optimizer**: ML-based recommendations for right-sizing EC2, EBS, ECS, Lambda, RDS. Must be **opted in**.

---

## 6. File Storage: EFS & FSx

**Amazon EFS (Elastic File System)**
- Managed **NFS v4.1** file storage, **automatically scales** to petabytes, pay only for what you use (no pre-provisioning).
- Supports **thousands of concurrent connections**; **read-after-write consistency**.
- Regional by default — stored across multiple AZs = highly durable/available.
- Storage classes: **Standard, Infrequent Access, Archive** (use lifecycle policies to transition).

> 💡 **Exam Tip:** "Highly-scalable shared storage via NFS across many instances" = **EFS**.

**Amazon FSx**

| Variant | Use Case |
|---|---|
| **FSx for Windows File Server** | SMB shares for Windows apps — SharePoint, SQL Server, IIS |
| **FSx for Lustre** | High-speed, high-capacity distributed storage — HPC, financial modeling; can integrate directly with S3 |
| **FSx for NetApp ONTAP** | Migrating/using existing NetApp ONTAP file systems |
| **FSx for OpenZFS** | Open-source ZFS-compatible file systems |

---

## 7. Amazon S3

### 7.1 S3 Overview & Buckets

- **Object storage** service: secure, durable, highly scalable, low cost.
- S3 the **service is global**, but **buckets are regional resources** — a very common point of confusion on the exam.
- Bucket names are **globally unique** (shared namespace across all AWS accounts).
- Max object size: **5 TB**. No limit on total storage or number of objects.
- **Not suitable** for running an OS or a database.
- Durability: **11 nines (99.999999999%)**. Availability: **99.95%–99.99%** depending on storage class.
- **Strong read-after-write consistency** for both new object writes and overwrites, and for LIST operations.

> 💡 **Exam Tip:** "S3 is global, but its buckets are regional" — remember this distinction; it's explicitly called out as tricky.

### 7.2 S3 Storage Classes

| Class | Access Pattern | Key Notes |
|---|---|---|
| **S3 Standard** | Frequent access | Default class; 99.99% availability, 11 nines durability |
| **S3 Express One Zone** | Frequent, latency-sensitive | Single-AZ, single-digit ms latency (HPC/ML) |
| **S3 Standard-IA** | Infrequent, but need fast access | Multi-AZ; retrieval fee; good for backups |
| **S3 One Zone-IA** | Infrequent, less critical | Single AZ; ~20% cheaper than Standard-IA, less resilient |
| **S3 Glacier Instant Retrieval** | Rarely accessed, need it in ms | Real-time access when needed |
| **S3 Glacier Flexible Retrieval** | Rarely accessed, retrieval OK in minutes | Not real-time |
| **S3 Glacier Deep Archive** | Almost never accessed | Cheapest; retrieval can take **up to 48 hours** |
| **S3 Intelligent-Tiering** | Unknown/changing access patterns | Auto-moves objects between tiers; **no retrieval fees**, small monitoring fee |

Minimum storage duration (fees apply if deleted early): Instant/Flexible Retrieval = **90 days**, Deep Archive = **180 days**.

> 💡 **Exam Tip:** Pay attention to **retrieval time requirements** in scenario questions — that's usually what distinguishes the correct Glacier tier.

### 7.3 Versioning, Lifecycle & Replication

- **Versioning states**: Unversioned (default) → Enabled → **Suspended** (you can never fully "disable" once enabled — only suspend).
- Objects existing before versioning is turned on get a **null version ID**.
- Deleting a versioned object inserts a **delete marker** (a new "version"); removing the delete marker restores visibility of the object.
- **Lifecycle rules**: automate moving objects between storage classes (**Transition actions**) or deleting them (**Expiration actions**); can apply to current or noncurrent (older) versions.
- **Replication (CRR/SRR)**: requires **versioning enabled** on both buckets; only replicates objects created **after** replication is turned on; **delete markers are not replicated by default**.

### 7.4 S3 Important Features

| Feature | Purpose |
|---|---|
| **S3 Batch Operations** | Run one operation (copy, tag, encrypt) across **billions of objects** in one job |
| **S3 Select / Glacier Select** | SQL-based **server-side filtering** of a single object (CSV, JSON, Parquet, GZIP/BZIP2); best for small/simple queries, reduces cost & latency — **not for large-scale retrieval** |
| **S3 Storage Lens** | Organization-wide insights — find data hotspots/anomalies |
| **S3 Event Notifications** | Trigger workflows on events (object created/removed, replication, tagging) → destinations: **Lambda, SQS, SNS, EventBridge** |
| **S3 Transfer Acceleration** | Speeds up uploads/downloads globally via CloudFront edge locations |
| **S3 Static Website Hosting** | Client-side scripts OK (JS); **no server-side rendering/processing supported** |
| **Byte-Range Fetches** | Download large objects in smaller chunks for resiliency/performance (opposite of multipart upload) |
| **Multipart Upload** | Upload large objects (**AWS recommends for >5GB**) in parts, with automatic retries |

### 7.5 S3 Security

- Buckets and objects are **private by default**.
- **Bucket Policy** (resource-based JSON) — preferred over ACLs whenever possible. Common uses: allow public access, require encryption/TLS, grant cross-account access.
- **Block Public Access** setting can override any ACL/policy that would otherwise allow public access.
- **Encryption at rest** (new buckets are encrypted by default):

| Method | Who manages the key |
|---|---|
| SSE-S3 | AWS-managed (default) |
| SSE-KMS | Customer-specified KMS key (has cost & quota limits — use **bucket keys** to reduce KMS costs) |
| SSE-C | Customer-provided key (you manage/rotate; must provide via headers) |
| Client-side encryption | Encrypted before upload; AWS has no visibility into it |

- **S3 Access Points**: simplify/customize granular access to buckets and objects.
- **S3 Server Access Logs**: log requests to a bucket — the **destination bucket must be in the same region**.
- **Presigned URLs**: time-limited access to objects (e.g., paywalled content); can fail if expired or if the generating user's permissions don't actually allow the action.
- **S3 Object Lambda**: transform objects on the fly before returning to the client (e.g., redact PII).
- **MFA Delete**: requires versioning; only the **bucket owner (root)** can enable/disable it.
- **Object Lock (WORM)**:
  - **Governance mode**: normal users can't overwrite/delete unless granted special permission (good for testing).
  - **Compliance mode**: **no one**, including root, can overwrite/delete until retention expires.
- **Glacier Vault Lock**: enforce WORM compliance controls on a Glacier vault via a lock policy that, once locked, **cannot be changed**.

> 💡 **Exam Tip:** Bucket policies > ACLs whenever you have the choice.

---

## 8. Amazon Route 53

### 8.1 DNS & Hosted Zones

- Route 53 = highly available, fully managed, **authoritative** DNS service. **100% availability SLA**. Named for **port 53** (DNS traffic).
- Functions: domain registration, DNS routing, health checks.

| Hosted Zone Type | Purpose |
|---|---|
| **Public** | Routes traffic on the public internet |
| **Private** | Routes traffic within a VPC/private network; must be **associated with VPC(s)**; requires DNS hostnames/resolution enabled |

### 8.2 Record Types

| Record | Purpose |
|---|---|
| **A** | Maps to an IPv4 address |
| **AAAA** | Maps to an IPv6 address |
| **CNAME** | Maps one domain name to another; **cannot be used at the zone apex** |
| **Alias** | AWS-specific record that fronts AWS resources (ELB, CloudFront, S3 website, etc.) — **preferred over CNAME for AWS resources**, and works at the zone apex |
| **NS** | Name server records |
| **SOA** | Start of Authority — zone administrative info |

### 8.3 Routing Policies

| Policy | Behavior |
|---|---|
| **Simple** | Basic single/multiple-value routing, no health checks |
| **Weighted** | Distributes traffic by relative weight (e.g., weights of 50/10/15/25 → each record gets weight/sum-of-weights of traffic) |
| **Failover** | Active-passive; **requires health checks**; primary handles traffic until unhealthy, then fails to secondary |
| **Geolocation** | Routes based on the **geographic origin** of the query (compliance/localization); requires a default record for unmatched locations |
| **Geoproximity** | Routes based on geographic location of users AND resources; uses a **bias** value (+1 to +99 to expand, -1 to -99 to shrink) a region's pull; requires **Traffic Flow** to configure/view |
| **Latency-based** | Routes to the **AWS region with lowest latency** for the user — do NOT confuse with geolocation |
| **Multi-value answer** | Returns up to **8 healthy records**; uses health checks; **not a substitute for a real load balancer** |

> 💡 **Exam Tip:** The #1 confusion pair on this exam is **Latency-based vs. Geolocation** — Latency = performance-based; Geolocation = origin-location-based (compliance/localization), not performance.

### 8.4 Health Checks & Hybrid DNS

**Three health check types:**
1. **Endpoint monitoring** — requires a publicly resolvable IP.
2. **Calculated health checks** — monitor other health checks.
3. **CloudWatch alarm monitoring** — good for checking **private hosted zone** records.

**Hybrid DNS (Route 53 Resolver)**
- Lets you connect on-prem DNS with AWS Route 53 bidirectionally (e.g., during cloud migrations).
- The **Route 53 Resolver** uses the reserved **+2 IP address** in a subnet's CIDR.
- **Inbound endpoints**: resolve DNS queries coming **into** your VPC.
- **Outbound endpoints**: resolve DNS queries going **out of** your VPC.
- **Route 53 Resolver DNS Firewall**: filters **outbound DNS traffic only**.

---

## 9. VPNs & Direct Connect

### 9.1 VPN Options

Key components: **Virtual Private Gateway (VGW)** — the VPN concentrator on the AWS side, attached to a VPC; **Customer Gateway (CGW)** — represents your on-prem hardware/software appliance.

| VPN Type | Best For |
|---|---|
| **Site-to-Site (S2S) VPN** | Most secure — **IPSec** tunnel between your network and AWS; requires publicly resolvable CGW IP and **route propagation enabled** |
| **AWS Client VPN** | Managed, **client-based** (per-device) VPN using OpenVPN/TLS from anywhere |
| **VPN CloudHub** | Hub-and-spoke management of **multiple Site-to-Site VPNs**; doesn't require a VPC |
| **Third-Party VPN** | Only when specific customization needs can't be met by the above |

> 💡 **Exam Tips**
> - "Need IPSec" → **Site-to-Site VPN**.
> - "Need TLS/OpenVPN from any device" → **Client VPN**.
> - "Simplify managing several Site-to-Site VPNs" → **VPN CloudHub**.

### 9.2 Direct Connect

- **AWS Direct Connect (DX)**: dedicated, private (physical) network connection from on-prem to AWS.
- Benefits: lower network costs, higher/more consistent bandwidth, more reliable than internet-based connections.
- **Private, but NOT encrypted by default** — run a VPN over DX if encryption is required.

| Connection Type | Description |
|---|---|
| **Dedicated** | Physical Ethernet connection for a single customer; 1/10/100/400 Gbps; highest performance, less flexible |
| **Hosted** | Provisioned by a DX Partner on your behalf; 50 Mbps up to 25 Gbps; more capacity flexibility |

- **Virtual Interfaces (VIFs)**:
  - **Public VIF** → access AWS **public** resources (S3, DynamoDB, Route 53, etc.).
  - **Private VIF** → access **private** VPC resources (EC2, RDS, VPC endpoints).

> 💡 **Exam Tip:** DX connections are **private but unencrypted** — a very commonly tested fact.

### 9.3 Direct Connect Gateway & Transit Gateway

| Service | Purpose |
|---|---|
| **Direct Connect Gateway** | Connect a single DX connection to **multiple VPCs**, across regions/accounts |
| **Transit Gateway** | Hub-and-spoke **transitive** routing between VPCs and on-prem networks; supports **VPC, VPN, and Peering attachments**; supports **IP multicast**; can be shared cross-account via **Resource Access Manager (RAM)** |

> 💡 **Exam Tip:** If you see a requirement for **IP multicast** or need transitive routing between many VPCs, think **Transit Gateway**.

---

## 10. Advanced VPC Security Features

| Feature | Purpose |
|---|---|
| **NACLs for blocking bad IPs** | Fast, cost-effective way to block malicious ranges across many resources at once |
| **VPC Flow Logs** | Capture IP traffic metadata for ENIs/subnets/VPCs. **Not for deep packet inspection.** Destinations: **S3, CloudWatch Logs, Kinesis Data Firehose** |
| **VPC Traffic Mirroring** | Copy traffic from an ENI to a security/monitoring appliance for inspection; sources = ENI; targets = ENI, NLB, or GWLB; can be cross-account |
| **Egress-Only Internet Gateway** | **IPv6-only**, outbound-only equivalent of a NAT Gateway |

> 💡 **Exam Tip:** VPC Flow Logs give you traffic **metadata**, not packet contents — don't pick this for "deep packet inspection" scenarios.

---

## 11. AWS Directory Services & IAM Identity Center

**AWS Directory Services (3 options):**

| Option | Description | Best For |
|---|---|---|
| **AWS Managed Microsoft AD** | Full AD suite, powered by Windows Server domain controllers | **Only option supporting trusts** (1-way/2-way); required for AWS Enterprise services (Chime, Identity Center, WorkSpaces); best for 5,000+ users |
| **AD Connector** | Gateway/redirector to your **existing on-prem AD**; caches nothing in the cloud | Best when you must **avoid data retention in AWS** |
| **Simple AD** | Standalone, Samba-4-based AD-compatible directory | Cheapest; subset of features only (no trusts, no MFA, no PowerShell); cannot join existing on-prem AD; simple workloads |

**AWS IAM Identity Center (SSO)**
- Central place to manage login across **multiple AWS accounts** and cloud/SAML 2.0 applications.
- Requires **AWS Organizations** to be set up (even for a single account).
- **Permission Sets** = IAM policies assigned to users/groups for account access.
- **Application Assignments** = grant access to cloud apps (Salesforce, Jira, Confluence, etc.).
- **ABAC (Attribute-Based Access Control)**: fine-grained access using user attributes (department, title, location).
- Can integrate with external identity providers (Okta, Microsoft AD, OneLogin) or manage users directly.

> 💡 **Exam Tips**
> - "Need trusts" → **Managed Microsoft AD** (only option that supports it).
> - "Must avoid caching AD data in the cloud" → **AD Connector**.
> - "Need SSO across multiple AWS accounts" → **IAM Identity Center**.

---

## 12. Advanced IAM: Policy Evaluation & Conditions

**IAM Permission Evaluation Order** (memorize this order):

1. **Explicit Deny** (anywhere in the chain — always wins, no exceptions)
2. **Service Control Policy (SCP)** — AWS Organizations level
3. **Resource-based policy** (e.g., S3 bucket policy)
4. **Identity-based policy** (attached to user/role)
5. **Permissions boundary**
6. **Session policy**

- By default, all new IAM entities start with **zero permissions** (implicit deny).

**Permissions Boundaries**
- A managed policy that sets the **maximum** permissions an identity-based policy can grant — it does **not grant** permissions itself, only limits them.
- Classic use case: an IAM administrator can create users/policies, but a boundary caps what they're allowed to delegate.

**Key Condition Keys to Memorize:**

| Condition Key | Purpose | Common Use Case |
|---|---|---|
| **`aws:ExternalID`** | Requires a unique ID when a role is assumed from another account | Prevents the **"confused deputy"** problem — third-party vendor access |
| **`aws:MultiFactorAuthPresent`** | Checks a boolean for whether MFA was used | Protecting sensitive actions (e.g., MFA Delete, instance termination) |
| **`aws:SourceIp`** | Restrict/allow based on requester's IP | Limit API calls to office/corporate IP ranges |
| **`aws:PrincipalOrgID`** | Validates request comes from an account inside your AWS Organization | Cross-account resource sharing restricted to your org (e.g., a central logging S3 bucket) |

> 💡 **Exam Tips**
> - **Explicit deny always wins** — no matter what else is allowed elsewhere.
> - See "**confused deputy**" in a question → answer involves **ExternalID**.
> - Permissions boundaries **restrict**, they never **grant**.

---

## Quick-Reference Cheat Sheet (Top "Don't Confuse These" Pairs)

| Concept A | Concept B | How to Tell Them Apart |
|---|---|---|
| Security Group | NACL | SG = stateful/instance-level/allow-only; NACL = stateless/subnet-level/allow+deny, first-match-wins |
| Gateway Endpoint | Interface Endpoint | Gateway = free, S3/DynamoDB only, route-table based; Interface = paid, many services, ENI + security groups |
| Latency Routing Policy | Geolocation Routing Policy | Latency = performance/fastest response; Geolocation = origin location (compliance/localization) |
| CNAME | Alias Record | Alias is AWS-specific, works at zone apex, preferred for AWS resources |
| Identity-based Policy | Resource-based Policy | Identity = attached to user/group/role; Resource = attached to the AWS resource itself (e.g., bucket policy) |
| Managed Policy | Inline Policy | Managed = reusable, own ARN; Inline = one-to-one, deleted with the identity |
| EBS | Instance Store | EBS = persistent, network-attached; Instance Store = ephemeral, lost on stop/terminate |
| Direct Connect | Site-to-Site VPN | DX = private but unencrypted; VPN = encrypted (IPSec) |
| Session Manager | Bastion Host | Session Manager = agent-based, no open inbound ports, generally preferred; Bastion = SSH jump box, more manual control |
