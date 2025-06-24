# AWS EC2 Billable Resource Discovery Solution
 
**Version:** 1.0  
**Date:** June 24, 2025  

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Introduction](#introduction)
3. [Solution Architecture](#solution-architecture)
4. [Installation and Setup](#installation-and-setup)
5. [Usage Guide](#usage-guide)
6. [Technical Implementation](#technical-implementation)
7. [Output Formats and Examples](#output-formats-and-examples)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [Future Enhancements](#future-enhancements)
11. [Appendices](#appendices)

---

## Executive Summary

The AWS EC2 Billable Resource Discovery Solution is a comprehensive Python-based tool designed to identify and catalog all billable resources associated with a selected Amazon EC2 instance. This solution addresses the critical need for organizations to understand their AWS resource dependencies and associated costs by providing a systematic approach to resource discovery and documentation.

The solution leverages the AWS SDK for Python (Boto3) to programmatically query AWS services and retrieve detailed information about resources that are directly or indirectly associated with an EC2 instance. These resources include Elastic Block Store (EBS) volumes, network interfaces, snapshots, Amazon Machine Images (AMIs), Security Groups, and Elastic IP addresses. The tool presents this information in well-formatted tables that can be exported to various formats for further analysis and reporting.

Key benefits of this solution include enhanced cost visibility, improved resource management, simplified compliance reporting, and streamlined infrastructure auditing. The tool is designed to be user-friendly, requiring only an EC2 instance ID as input while providing comprehensive output that can be customized based on specific requirements.

## Introduction

In today's cloud-first environment, organizations increasingly rely on Amazon Web Services (AWS) to host their applications and infrastructure. As cloud deployments grow in complexity, understanding the relationships between different AWS resources becomes crucial for effective cost management, security compliance, and operational efficiency. EC2 instances, being the cornerstone of many AWS deployments, often have numerous associated resources that contribute to the overall infrastructure cost and complexity.

The challenge many organizations face is the lack of visibility into these resource relationships. While the AWS Management Console provides detailed information about individual resources, it does not offer a consolidated view of all resources associated with a specific EC2 instance. This gap in visibility can lead to several issues including unexpected costs, orphaned resources, security vulnerabilities, and compliance challenges.

The AWS EC2 Billable Resource Discovery Solution was developed to address these challenges by providing a programmatic approach to resource discovery and documentation. The solution is built on the principle that understanding resource relationships is fundamental to effective cloud management. By identifying all billable resources associated with an EC2 instance, organizations can make informed decisions about resource optimization, cost allocation, and infrastructure planning.

The solution is particularly valuable for cloud architects, DevOps engineers, financial analysts, and compliance officers who need to understand the complete scope of resources associated with specific workloads. It can be used for various purposes including cost analysis, security audits, compliance reporting, disaster recovery planning, and infrastructure documentation.

## Solution Architecture

The AWS EC2 Billable Resource Discovery Solution follows a modular architecture that separates concerns and promotes maintainability. The architecture consists of three main components: the Resource Discovery Engine, the Table Formatting Module, and the Command Line Interface (CLI).

### Resource Discovery Engine

The Resource Discovery Engine is the core component responsible for interacting with AWS services and retrieving resource information. This component is implemented in the `EC2ResourceDiscovery` class, which encapsulates all the logic for connecting to AWS services and querying resource data.

The engine uses the AWS SDK for Python (Boto3) to establish connections with AWS services. It supports both AWS CLI profiles and environment-based authentication, providing flexibility in how credentials are managed. The engine implements error handling for common scenarios such as invalid instance IDs, missing permissions, and network connectivity issues.

The resource discovery process follows a systematic approach where the engine first validates the provided EC2 instance ID and retrieves basic instance information. It then proceeds to discover associated resources by querying different AWS services. The discovery process is designed to be comprehensive, ensuring that all relevant billable resources are identified and cataloged.

### Table Formatting Module

The Table Formatting Module is responsible for presenting the discovered resource information in a user-friendly format. This component is implemented in the `ResourceTableFormatter` class, which provides multiple formatting options and export capabilities.

The module supports various table formats including grid, simple, fancy grid, and many others, allowing users to choose the presentation style that best suits their needs. It also provides specialized formatting for different resource types, ensuring that the most relevant information is displayed for each resource category.

The formatting module includes export functionality that allows users to save the discovered information in CSV and JSON formats. This capability is essential for integration with other tools and systems, enabling further analysis and reporting.

### Command Line Interface

The CLI component provides the user interface for the solution, handling command-line arguments, orchestrating the discovery process, and presenting results to the user. The CLI is designed to be intuitive and follows standard command-line conventions.

The interface supports various options including region specification, AWS profile selection, output formatting, and export options. It includes comprehensive help documentation and examples to guide users in effectively utilizing the tool.

### Data Flow and Processing

The solution follows a clear data flow pattern that begins with user input and ends with formatted output. The process starts when the user provides an EC2 instance ID through the CLI. The CLI validates the input and passes it to the Resource Discovery Engine.

The engine then establishes connections with AWS services and begins the resource discovery process. For each resource type, the engine executes specific queries to retrieve relevant information. The discovered data is structured into a consistent format that can be processed by the formatting module.

Once all resources are discovered, the data is passed to the Table Formatting Module, which applies the requested formatting and generates the final output. The output can be displayed on the console, exported to files, or both, depending on the user's requirements.

## Installation and Setup

### Prerequisites

Before installing and using the AWS EC2 Billable Resource Discovery Solution, ensure that your system meets the following requirements:

**System Requirements:**
- Python 3.7 or higher
- Operating System: Linux, macOS, or Windows
- Minimum 512 MB of available RAM
- Network connectivity to AWS services

**AWS Requirements:**
- Valid AWS account with appropriate permissions
- AWS CLI configured with credentials (optional but recommended)
- IAM permissions for EC2, EBS, and related services

### Required Python Packages

The solution depends on several Python packages that must be installed before use:

```bash
pip3 install boto3 tabulate pandas
```

**Package Descriptions:**
- **boto3**: The AWS SDK for Python, providing programmatic access to AWS services
- **tabulate**: A library for creating well-formatted tables in various formats
- **pandas**: A data manipulation library used for data structuring and CSV export

### AWS Credentials Configuration

The solution requires AWS credentials to access AWS services. There are several ways to configure credentials:

**Method 1: AWS CLI Configuration**
```bash
aws configure
```

This method prompts for AWS Access Key ID, Secret Access Key, default region, and output format.

**Method 2: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region
```

**Method 3: IAM Roles (for EC2 instances)**
If running the solution on an EC2 instance, you can attach an IAM role with appropriate permissions.

### Required IAM Permissions

The solution requires specific IAM permissions to function correctly. Create an IAM policy with the following permissions:

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

### Installation Steps

1. **Download the Solution Files**
   Download all solution files to a directory on your system:
   - `aws_ec2_resource_discovery.py` (main CLI script)
   - `ec2_resource_discovery.py` (resource discovery engine)
   - `table_formatter.py` (table formatting module)

2. **Make Scripts Executable**
   ```bash
   chmod +x aws_ec2_resource_discovery.py
   chmod +x ec2_resource_discovery.py
   ```

3. **Install Dependencies**
   ```bash
   pip3 install boto3 tabulate pandas
   ```

4. **Verify Installation**
   ```bash
   python3 aws_ec2_resource_discovery.py --help
   ```

### Configuration Verification

To verify that the solution is properly configured, run the following test:

```bash
python3 aws_ec2_resource_discovery.py --version
```

This command should display the version information without any errors. If you encounter authentication errors, verify your AWS credentials configuration.

## Usage Guide

### Basic Usage

The most basic usage of the AWS EC2 Billable Resource Discovery Solution requires only an EC2 instance ID:

```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0
```

This command will discover all billable resources associated with the specified instance and display them in a formatted table using the default settings.

### Command Line Options

The solution provides numerous command-line options to customize its behavior:

**Region Specification:**
```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --region us-west-2
```

**Profile Selection:**
```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --profile myprofile
```

**Output Formatting:**
```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --format fancy_grid
```

**Detailed Output:**
```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --detailed
```

**Summary Only:**
```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --summary-only
```

### Export Options

The solution supports exporting discovered information to various formats:

**CSV Export:**
```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --export-csv resources.csv
```

**JSON Export:**
```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --export-json discovery_result.json
```

**Combined Export:**
```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --export-csv resources.csv --export-json discovery_result.json
```

### Advanced Usage Scenarios

**Multi-Region Analysis:**
For organizations with resources across multiple regions, you can run the tool for each region:

```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --region us-east-1 --export-csv us-east-1-resources.csv
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --region us-west-2 --export-csv us-west-2-resources.csv
```

**Automated Reporting:**
The solution can be integrated into automated reporting workflows:

```bash
#!/bin/bash
INSTANCES=("i-1234567890abcdef0" "i-abcdef1234567890")
for instance in "${INSTANCES[@]}"; do
    python3 aws_ec2_resource_discovery.py $instance --export-csv "${instance}_resources.csv"
done
```

**Custom Formatting for Documentation:**
For documentation purposes, you might prefer specific table formats:

```bash
python3 aws_ec2_resource_discovery.py i-1234567890abcdef0 --format mediawiki --detailed
```

### Understanding the Output

The solution provides several types of output, each serving different purposes:

**Instance Details Section:**
This section displays basic information about the EC2 instance, including instance type, state, availability zone, VPC ID, and launch time. This information provides context for the associated resources.

**Resource Summary Table:**
The summary table provides a high-level overview of the discovered resources, showing the count of each resource type. This is useful for quickly understanding the scope of resources associated with the instance.

**Detailed Resource Tables:**
When using the `--detailed` option, the solution displays separate tables for each resource type. These tables include specific attributes relevant to each resource category, providing comprehensive information for analysis and documentation.

### Error Handling and Troubleshooting

The solution includes comprehensive error handling for common scenarios:

**Invalid Instance ID:**
If you provide an invalid instance ID, the solution will display a clear error message and exit gracefully.

**Authentication Errors:**
If AWS credentials are not properly configured, the solution will provide guidance on how to resolve the issue.

**Permission Errors:**
If the configured credentials lack necessary permissions, the solution will indicate which permissions are missing.

**Network Connectivity Issues:**
If there are network connectivity problems, the solution will provide appropriate error messages and suggestions for resolution.

## Technical Implementation

### Core Architecture Principles

The AWS EC2 Billable Resource Discovery Solution is built on several key architectural principles that ensure reliability, maintainability, and extensibility. The solution follows object-oriented design patterns, with clear separation of concerns between different functional areas.

The modular design allows for easy testing and maintenance, with each component having well-defined responsibilities. The Resource Discovery Engine handles all AWS API interactions, the Table Formatting Module manages data presentation, and the CLI provides user interface functionality.

Error handling is implemented at multiple levels, ensuring that failures are caught and handled gracefully. The solution uses defensive programming techniques to validate inputs and handle edge cases appropriately.

### Resource Discovery Implementation

The resource discovery process is implemented through a series of specialized methods, each responsible for discovering a specific type of resource. This approach ensures that the discovery logic is organized and maintainable.

**EC2 Instance Discovery:**
The instance discovery process begins by validating the provided instance ID and retrieving basic instance information. This step serves as both validation and the foundation for subsequent resource discovery operations.

```python
def get_instance_details(self, instance_id: str) -> Dict[str, Any]:
    try:
        instance = self.ec2_resource.Instance(instance_id)
        instance.load()
        # Process instance attributes and return structured data
    except ClientError as e:
        # Handle specific AWS errors
```

**Volume Discovery:**
EBS volume discovery involves querying the EC2 service for volumes attached to the specified instance. The implementation retrieves comprehensive volume information including size, type, encryption status, and performance characteristics.

**Network Interface Discovery:**
Network interface discovery identifies all ENIs associated with the instance. This includes both primary and secondary network interfaces, along with their configuration details and associated security groups.

**Snapshot Discovery:**
Snapshot discovery is more complex as snapshots are not directly associated with instances. The implementation first identifies volumes associated with the instance and then finds snapshots created from those volumes.

**AMI Discovery:**
AMI discovery retrieves information about the Amazon Machine Image used to launch the instance. This includes details about the image's configuration, creation date, and ownership.

**Security Group Discovery:**
Security group discovery identifies all security groups associated with the instance and retrieves detailed information about their rules and configuration.

**Elastic IP Discovery:**
Elastic IP discovery identifies any Elastic IP addresses associated with the instance or its network interfaces.

### Data Structure Design

The solution uses consistent data structures throughout the discovery and formatting process. Each discovered resource is represented as a dictionary with standardized keys, ensuring compatibility across different components.

The data structure design includes metadata about each resource type, allowing the formatting module to present information appropriately. Common fields such as resource type, resource ID, and tags are standardized across all resource types.

### Error Handling Strategy

The solution implements a comprehensive error handling strategy that addresses various failure scenarios:

**AWS Service Errors:**
The solution handles AWS service errors gracefully, providing meaningful error messages and suggestions for resolution. Common errors such as invalid instance IDs, permission issues, and service unavailability are handled specifically.

**Network Errors:**
Network connectivity issues are detected and reported with appropriate guidance for resolution. The solution includes retry logic for transient network errors.

**Data Processing Errors:**
The solution includes validation and error handling for data processing operations, ensuring that malformed or unexpected data does not cause failures.

### Performance Considerations

The solution is designed with performance in mind, implementing several optimization strategies:

**Parallel Processing:**
Where possible, the solution uses parallel processing to reduce discovery time. Independent resource discovery operations can be executed concurrently.

**Efficient API Usage:**
The solution minimizes API calls by using efficient query patterns and batch operations where supported by the AWS APIs.

**Memory Management:**
The solution is designed to handle large datasets efficiently, using streaming and pagination where appropriate to manage memory usage.

### Security Implementation

Security is a primary consideration in the solution's design:

**Credential Management:**
The solution supports multiple credential management approaches, allowing organizations to use their preferred security model. It never stores or logs credentials.

**Least Privilege Access:**
The solution requires only the minimum necessary permissions to function, following the principle of least privilege.

**Data Protection:**
The solution handles sensitive data appropriately, ensuring that confidential information is not inadvertently exposed in logs or output files.

## Output Formats and Examples

### Table Format Options

The AWS EC2 Billable Resource Discovery Solution supports numerous table formats to accommodate different use cases and preferences. Each format has specific characteristics that make it suitable for particular scenarios.

**Grid Format (Default):**
The grid format provides a clean, professional appearance with clear borders and alignment. This format is ideal for console output and general documentation purposes.

**Fancy Grid Format:**
The fancy grid format uses Unicode characters to create visually appealing tables with enhanced borders. This format is excellent for presentations and high-quality documentation.

**Simple Format:**
The simple format provides a minimalist appearance without borders, making it suitable for environments where visual simplicity is preferred.

**Pipe Format:**
The pipe format is compatible with Markdown table syntax, making it ideal for documentation that will be processed by Markdown renderers.

**HTML Format:**
The HTML format generates tables that can be embedded directly into web pages or HTML documents.

### Sample Output Examples

**Resource Summary Table:**
```
+--------------------+-------+
| Resource Type      | Count |
+====================+=======+
| Volumes            |     2 |
+--------------------+-------+
| Network Interfaces |     1 |
+--------------------+-------+
| Snapshots          |     3 |
+--------------------+-------+
| Amis               |     1 |
+--------------------+-------+
| Security Groups    |     2 |
+--------------------+-------+
| Elastic Ips        |     1 |
+--------------------+-------+
| TOTAL              |    10 |
+--------------------+-------+
```

**Detailed Volume Information:**
```
+------------------------+---------+------+--------+----------+-----------+------+------------------+
| Volume ID              | Size GB | Type | State  | Device   | Encrypted | IOPS | Delete on Term   |
+========================+=========+======+========+==========+===========+======+==================+
| vol-1234567890abcdef0  |      20 | gp3  | in-use | /dev/sda1|      True | 3000 |             True |
+------------------------+---------+------+--------+----------+-----------+------+------------------+
| vol-abcdef1234567890   |     100 | gp3  | in-use | /dev/sdf |      True | 3000 |            False |
+------------------------+---------+------+--------+----------+-----------+------+------------------+
```

### Export Format Examples

**CSV Export Structure:**
The CSV export includes all discovered resource information in a flattened structure suitable for spreadsheet analysis and data processing tools.

**JSON Export Structure:**
The JSON export maintains the hierarchical structure of the discovered data, making it suitable for programmatic processing and integration with other tools.

### Customization Options

The solution provides several customization options for output formatting:

**Column Selection:**
Users can customize which columns are displayed for each resource type by modifying the formatting templates.

**Sorting Options:**
The output can be sorted by various criteria including resource type, creation date, or resource ID.

**Filtering Capabilities:**
The solution can be extended to include filtering capabilities based on resource attributes such as tags, state, or size.

## Troubleshooting

### Common Issues and Solutions

**Issue: "AWS credentials not found"**
This error occurs when the solution cannot locate valid AWS credentials.

*Solution:*
1. Verify that AWS CLI is installed and configured: `aws configure`
2. Check environment variables: `echo $AWS_ACCESS_KEY_ID`
3. Verify IAM role attachment if running on EC2
4. Use the `--profile` option to specify a specific credential profile

**Issue: "Instance not found"**
This error indicates that the specified instance ID does not exist or is not accessible.

*Solution:*
1. Verify the instance ID format (should be i-xxxxxxxxxxxxxxxxx)
2. Check that you're querying the correct region using `--region`
3. Ensure the instance exists and is not terminated
4. Verify that your credentials have permission to access the instance

**Issue: "Permission denied" errors**
This error occurs when the configured credentials lack necessary permissions.

*Solution:*
1. Review the required IAM permissions in the installation section
2. Attach the necessary policies to your IAM user or role
3. Verify that there are no explicit deny policies blocking access
4. Check for resource-based policies that might restrict access

**Issue: "Network timeout" errors**
This error indicates connectivity issues with AWS services.

*Solution:*
1. Check internet connectivity
2. Verify that security groups allow outbound HTTPS traffic
3. Check for proxy configurations that might interfere
4. Try specifying a different region that might be more accessible

### Debugging Techniques

**Verbose Output:**
While the current version doesn't include verbose logging, you can modify the scripts to add debug output for troubleshooting purposes.

**Credential Testing:**
Test your AWS credentials independently using the AWS CLI:
```bash
aws ec2 describe-instances --instance-ids i-1234567890abcdef0
```

**Permission Testing:**
Test specific permissions by running individual AWS CLI commands:
```bash
aws ec2 describe-volumes --filters "Name=attachment.instance-id,Values=i-1234567890abcdef0"
```

### Performance Troubleshooting

**Slow Discovery Performance:**
If the discovery process is slow, consider the following:

1. Check network latency to AWS services
2. Verify that you're using the optimal region
3. Consider running the tool from within AWS (EC2) for better performance
4. Check for rate limiting by AWS services

**Memory Usage Issues:**
For instances with many associated resources, memory usage might be a concern:

1. Monitor system memory during execution
2. Consider processing resources in batches for very large deployments
3. Use the `--summary-only` option for quick overviews

### Getting Additional Help

**AWS Support:**
For AWS-specific issues, consult the AWS documentation or contact AWS support.

**Community Resources:**
The AWS community forums and Stack Overflow are excellent resources for troubleshooting AWS-related issues.

**Solution Updates:**
Check for updates to the solution that might address known issues or add new features.

## Best Practices

### Security Best Practices

**Credential Management:**
Always use the principle of least privilege when configuring IAM permissions. Create dedicated IAM users or roles specifically for resource discovery activities, and avoid using root account credentials.

Store credentials securely using AWS-recommended methods such as IAM roles for EC2 instances, AWS CLI profiles, or environment variables. Never hardcode credentials in scripts or configuration files.

Regularly rotate access keys and review IAM permissions to ensure they remain appropriate for current needs.

**Network Security:**
When running the solution from on-premises environments, ensure that network connections to AWS are secure. Consider using VPN connections or AWS Direct Connect for enhanced security.

If running the solution on EC2 instances, ensure that security groups are properly configured to allow only necessary outbound connections.

### Operational Best Practices

**Regular Auditing:**
Implement regular resource discovery audits to maintain visibility into your AWS infrastructure. Consider automating these audits using scheduled scripts or CI/CD pipelines.

Document discovered resources and their relationships to support operational procedures and troubleshooting activities.

**Cost Management:**
Use the resource discovery information to identify opportunities for cost optimization. Look for unused or underutilized resources that can be rightsized or terminated.

Implement tagging strategies that support cost allocation and resource management. The solution can help identify resources that lack proper tagging.

**Compliance and Governance:**
Use the solution's output to support compliance reporting and governance activities. The detailed resource information can help demonstrate adherence to security and operational policies.

Maintain historical records of resource discovery results to support audit activities and change tracking.

### Integration Best Practices

**Automation Integration:**
Integrate the solution into existing automation workflows using its command-line interface and export capabilities. The JSON export format is particularly suitable for programmatic processing.

Consider creating wrapper scripts that process multiple instances or integrate with configuration management systems.

**Monitoring Integration:**
Use the solution's output to enhance monitoring and alerting systems. Resource discovery information can help identify monitoring gaps and improve incident response procedures.

**Documentation Integration:**
Integrate resource discovery results into infrastructure documentation and runbooks. The various output formats support different documentation systems and requirements.

### Performance Best Practices

**Efficient Execution:**
When processing multiple instances, consider running discovery operations in parallel to reduce total execution time.

Use appropriate AWS regions to minimize network latency and improve performance.

**Resource Optimization:**
Regularly review discovered resources to identify optimization opportunities. Look for oversized volumes, unused network interfaces, and unnecessary snapshots.

Use the solution's detailed output to support capacity planning and resource allocation decisions.

### Maintenance Best Practices

**Regular Updates:**
Keep the solution and its dependencies updated to ensure compatibility with AWS service changes and security updates.

Monitor AWS service announcements for changes that might affect the solution's functionality.

**Testing and Validation:**
Regularly test the solution in non-production environments to ensure continued functionality.

Validate the accuracy of discovered information by comparing results with AWS console data.

**Backup and Recovery:**
Maintain backups of the solution scripts and any customizations you've made.

Document any modifications or customizations to support maintenance and troubleshooting activities.

## Future Enhancements

### Planned Features

**Multi-Instance Support:**
Future versions of the solution will support processing multiple EC2 instances in a single execution. This enhancement will include batch processing capabilities and consolidated reporting across multiple instances.

**Cost Integration:**
Integration with AWS Cost Explorer APIs will provide actual cost information for discovered resources. This feature will enable comprehensive cost analysis and optimization recommendations.

**Historical Analysis:**
The solution will be enhanced to support historical resource discovery, allowing users to track changes in resource associations over time.

**Advanced Filtering:**
Enhanced filtering capabilities will allow users to focus on specific resource types, states, or attributes. This will be particularly useful for large environments with many associated resources.

### Potential Integrations

**AWS Config Integration:**
Integration with AWS Config will provide additional resource configuration details and compliance information.

**AWS CloudFormation Integration:**
The solution could be enhanced to identify CloudFormation stacks associated with discovered resources, providing additional context about resource relationships.

**Third-Party Tool Integration:**
Future versions may include direct integration with popular infrastructure management tools and monitoring systems.

### Scalability Improvements

**Parallel Processing:**
Enhanced parallel processing capabilities will improve performance for large-scale resource discovery operations.

**Caching Mechanisms:**
Intelligent caching will reduce API calls and improve performance for repeated discovery operations.

**Database Integration:**
Optional database integration will support persistent storage of discovery results and historical analysis.

### User Experience Enhancements

**Web Interface:**
A web-based interface will provide an alternative to the command-line interface, making the solution accessible to users who prefer graphical interfaces.

**Interactive Reporting:**
Interactive reports with drill-down capabilities will enhance the analysis experience.

**Customizable Templates:**
User-customizable output templates will provide greater flexibility in report formatting and content.

## Appendices

### Appendix A: Complete Command Reference

```bash
# Basic usage
python3 aws_ec2_resource_discovery.py <instance-id>

# With region specification
python3 aws_ec2_resource_discovery.py <instance-id> --region <region-name>

# With profile specification
python3 aws_ec2_resource_discovery.py <instance-id> --profile <profile-name>

# With custom table format
python3 aws_ec2_resource_discovery.py <instance-id> --format <format-name>

# Detailed output
python3 aws_ec2_resource_discovery.py <instance-id> --detailed

# Summary only
python3 aws_ec2_resource_discovery.py <instance-id> --summary-only

# Export to CSV
python3 aws_ec2_resource_discovery.py <instance-id> --export-csv <filename.csv>

# Export to JSON
python3 aws_ec2_resource_discovery.py <instance-id> --export-json <filename.json>

# Combined options
python3 aws_ec2_resource_discovery.py <instance-id> --region us-west-2 --profile myprofile --format fancy_grid --detailed --export-csv resources.csv --export-json results.json
```

### Appendix B: Supported Table Formats

- plain
- simple
- github
- grid (default)
- fancy_grid
- pipe
- orgtbl
- jira
- presto
- pretty
- psql
- rst
- mediawiki
- moinmoin
- youtrack
- html
- unsafehtml
- latex
- latex_raw
- latex_booktabs
- latex_longtabu
- textile
- tsv

### Appendix C: Required IAM Policy

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

### Appendix D: File Structure

```
aws-ec2-resource-discovery/
├── aws_ec2_resource_discovery.py    # Main CLI script
├── ec2_resource_discovery.py        # Resource discovery engine
├── table_formatter.py               # Table formatting module
├── test_solution.py                 # Test script with mock data
├── README.md                        # Basic usage instructions
└── documentation.md                 # This comprehensive documentation
```

---

*This documentation provides comprehensive guidance for using the AWS EC2 Billable Resource Discovery Solution. For additional support or questions, please refer to the troubleshooting section or consult the AWS documentation for service-specific information.*

