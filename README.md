# AWS EC2 Billable Resource Discovery Tool

A comprehensive Python solution to discover and list all billable resources associated with an AWS EC2 instance.

## Quick Start

### Prerequisites
- Python 3.7+
- AWS credentials configured
- Required permissions: EC2 read access

### Installation
```bash
# Install dependencies
pip3 install boto3 tabulate pandas

# Make scripts executable
chmod +x aws_ec2_resource_discovery.py
```

### Basic Usage
```bash
# Discover resources for an EC2 instance
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0

# With specific region
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --region us-west-2

# Detailed output with fancy formatting
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --detailed --format fancy_grid

# Export to CSV and JSON
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --export-csv resources.csv --export-json results.json
```

## What It Discovers

The tool identifies all billable resources associated with an EC2 instance:

- **EC2 Instance** - The instance itself with configuration details
- **EBS Volumes** - All attached storage volumes
- **Network Interfaces** - ENIs and their configurations  
- **EBS Snapshots** - Snapshots created from associated volumes
- **AMIs** - The Amazon Machine Image used to launch the instance
- **Security Groups** - All associated security groups
- **Elastic IPs** - Any Elastic IP addresses attached

## Sample Output

```
Resource Summary:
+--------------------+-------+
| Resource Type      | Count |
+====================+=======+
| Volumes            |     2 |
| Network Interfaces |     1 |
| Snapshots          |     3 |
| Amis               |     1 |
| Security Groups    |     2 |
| Elastic Ips        |     1 |
| TOTAL              |    10 |
+--------------------+-------+
```

## Command Options

- `--region REGION` - Specify AWS region
- `--profile PROFILE` - Use specific AWS profile
- `--format FORMAT` - Table format (grid, fancy_grid, simple, etc.)
- `--detailed` - Show detailed tables grouped by resource type
- `--summary-only` - Show only the resource summary
- `--export-csv FILE` - Export to CSV file
- `--export-json FILE` - Export to JSON file
- `--help` - Show all options

## Required AWS Permissions

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:DescribeVolumes", 
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeSnapshots",
                "ec2:DescribeImages",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeAddresses"
            ],
            "Resource": "*"
        }
    ]
}
```

## Files Included

- `aws_ec2_resource_discovery.py` - Main CLI tool
- `ec2_resource_discovery.py` - Resource discovery engine
- `table_formatter.py` - Table formatting module
- `test_solution.py` - Test with mock data
- `documentation.md` - Comprehensive documentation

## Testing

Test the solution without AWS credentials:
```bash
python3 test_solution.py
```

## Troubleshooting

**Credentials Error:**
```bash
aws configure  # Configure AWS CLI
```

**Permission Error:**
Ensure your IAM user/role has the required EC2 read permissions listed above.

**Instance Not Found:**
- Verify the instance ID format: `i-1234567890abcdef0`
- Check you're using the correct region with `--region`

## Use Cases

- **Cost Analysis** - Understand all billable resources for an instance
- **Security Audits** - Review associated security groups and network configs
- **Compliance Reporting** - Document infrastructure components
- **Resource Cleanup** - Identify orphaned or unused resources
- **Disaster Recovery** - Document dependencies for backup planning

For detailed documentation, see `documentation.md`.

