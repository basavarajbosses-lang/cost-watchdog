# 🐕 AWS Cost Watchdog

[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20EventBridge%20%7C%20CloudWatch-orange)](https://aws.amazon.com)
[![Terraform](https://img.shields.io/badge/Terraform-Infrastructure%20as%20Code-purple)](https://www.terraform.io)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **Automated serverless solution that reduces AWS costs by identifying and deleting orphaned EBS snapshots.**

---

## 🎯 The Problem

Every company using AWS faces this challenge: **EBS snapshots accumulate over time**, creating significant storage costs. Snapshots of terminated instances, orphaned volumes, and unattached resources silently increase your monthly bill.

### 💰 The Cost Impact:
- Each snapshot costs **\.05/GB/month**
- 100 snapshots at 100GB = **\/month wasted**
- Only grows as infrastructure scales

---

## 💡 The Solution

This **Cost Watchdog** automatically:
- 🔍 Scans all EBS snapshots in your AWS account
- 🗑️ Identifies orphaned/abandoned snapshots
- ⚡ Deletes them safely (with logging)
- 📊 Monitors everything through CloudWatch

### What it Deletes:
| Criteria | Reason |
|----------|--------|
| ❌ No associated volume | Snapshot was created but volume doesn't exist |
| ❌ Volume not found | The original volume was deleted |
| ❌ Volume not attached | Snapshot of a volume not in use |
| ❌ Instance terminated | Snapshot of a terminated EC2 instance |

---

## 🏗️ Architecture

\\\
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│   Amazon EventBridge │     │    AWS Lambda       │     │   Amazon CloudWatch │
│   (Daily Schedule)   │────▶│   (Python/Boto3)    │────▶│    (Logging)        │
│   cron(0 9 * * ? *)  │     │   Snapshot Logic    │     │   Audit Trail       │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
                                       │
                                       ▼
                             ┌─────────────────────┐
                             │   AWS EC2 API       │
                             │   Describe & Delete │
                             │   Snapshots         │
                             └─────────────────────┘
\\\

---

## 🛠️ Technology Stack

| Service | Purpose |
|---------|---------|
| **AWS Lambda** | Serverless compute for cleanup logic |
| **Amazon EventBridge** | Scheduled triggers (daily at 9 AM UTC) |
| **Amazon CloudWatch** | Monitoring and logging |
| **AWS IAM** | Least-privilege security |
| **Terraform** | Infrastructure as Code |
| **Python 3.12** | Runtime environment |
| **Boto3** | AWS SDK for Python |

---

## 🔐 Security Features

- ✅ **Least-privilege IAM roles** - Lambda only gets required permissions
- ✅ **No hardcoded credentials** - Uses IAM roles for authentication
- ✅ **Full audit trail** - CloudWatch logs all actions
- ✅ **Safe deletion** - Only deletes snapshots that meet all criteria

---

## 📦 Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| [AWS CLI](https://aws.amazon.com/cli/) | Latest | AWS authentication |
| [Terraform](https://www.terraform.io/downloads) | >= 1.0 | Infrastructure provisioning |
| [Python](https://www.python.org/downloads/) | 3.12+ | Development |
| [Git](https://git-scm.com/downloads) | Latest | Version control |

---

## 🚀 Deployment Steps

### 1. Clone the Repository
\\\ash
git clone https://github.com/basavarajbosses-lang/cost-watchdog.git
cd cost-watchdog
\\\

### 2. Configure AWS CLI
\\\ash
aws configure
# Enter:
# AWS Access Key ID: [your-key]
# AWS Secret Access Key: [your-secret]
# Default region name: us-east-1
# Default output format: json
\\\

### 3. Deploy with Terraform
\\\ash
terraform init
terraform plan
terraform apply -auto-approve
\\\

### 4. Test the Lambda
\\\ash
aws lambda invoke --function-name cost-watchdog output.txt
cat output.txt
\\\

Expected output:
\\\json
{
  "statusCode": 200,
  "body": "Deleted 0 snapshots"
}
\\\

---

## 📊 Monitoring & Logs

### View Logs in CloudWatch
\\\ash
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/cost-watchdog
aws logs get-log-events --log-group-name /aws/lambda/cost-watchdog --log-stream-name [stream-name]
\\\

### Sample Log Output
\\\
Found 2 running instances
Found 45 total snapshots
DELETING: snap-123abc - Reason: No associated volume
DELETING: snap-456def - Reason: Volume not attached to any instance
Successfully deleted 2 snapshots
\\\

---

## 💰 Cost Savings Analysis

Track your savings:

| Metric | Value |
|--------|-------|
| **Before** | 45 snapshots × 100GB × \.05 = \/month |
| **After** | 5 snapshots × 100GB × \.05 = \/month |
| **Monthly Savings** | **\ (89% reduction)** |

Use AWS Cost Explorer to monitor:
\\\ash
aws ce get-cost-and-usage --time-period Start=2026-01-01,End=2026-01-31 --granularity MONTHLY --metrics "UnblendedCost"
\\\

---

## 🔧 Local Testing

Test the logic without AWS:

\\\python
python test_locally.py
\\\

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (\git checkout -b feature/amazing-feature\)
3. Commit changes (\git commit -m 'Add amazing feature'\)
4. Push to branch (\git push origin feature/amazing-feature\)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Basavaraj Garampalli**
- GitHub: [@basavarajbosses-lang](https://github.com/basavarajbosses-lang)
- LinkedIn: [Basavaraj Garampalli](https://linkedin.com/in/basavaraj-garampalli-4b36a827a)
- Email: basavarajbosses@gmail.com

---

## 🙏 Acknowledgments

- AWS Documentation for Lambda and Boto3
- Terraform Community for IaC best practices
- Open Source community for inspiration

---

**⭐ Star this repository if you found it useful!**

