# AWS EC2 Billable Resource Discovery Solution Design

## 1. Introduction
This document outlines the design for an AWS solution to identify and list all billable resources associated with a selected EC2 instance. The solution will leverage the AWS SDK for Python (Boto3) to interact with AWS services and retrieve relevant resource information. The output will be presented in a clear, tabular format for easy readability and analysis.

## 2. Overall Architecture
The solution will be implemented as a Python script that takes an EC2 instance ID as input. It will then use Boto3 to query various AWS services to gather information about associated resources. The collected data will be structured and then presented in a table.

## 3. Resource Discovery Workflow

### 3.1. Input: EC2 Instance ID
The script will require a single EC2 instance ID as a command-line argument or user input.

### 3.2. Initialize Boto3 EC2 Client and Resource
We will initialize both a Boto3 EC2 client and resource. The client provides low-level access to EC2 API actions, while the resource provides a higher-level, object-oriented interface for interacting with EC2 resources.

```python
import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')
```

### 3.3. Retrieve EC2 Instance Details
Using the provided EC2 instance ID, we will retrieve detailed information about the instance, which will be crucial for identifying associated resources.

```python
instance = ec2_resource.Instance(instance_id)
instance.load()
```

### 3.4. Discover Associated Resources
For each billable resource type, we will implement a dedicated function to discover and collect relevant information. The following resource types will be covered:

#### 3.4.1. Volumes (EBS)
Volumes are block storage devices that can be attached to EC2 instances. We can find associated volumes by checking the `block_device_mappings` attribute of the EC2 instance or by filtering `ec2_client.describe_volumes` by instance ID.

#### 3.4.2. Network Interfaces (ENIs)
Network interfaces enable EC2 instances to connect to a network. Each EC2 instance has at least one primary network interface. Additional network interfaces can be attached. We can find associated network interfaces by checking the `network_interfaces` attribute of the EC2 instance or by filtering `ec2_client.describe_network_interfaces`.

#### 3.4.3. Snapshots
Snapshots are point-in-time backups of EBS volumes. While snapshots are not directly associated with an EC2 instance, they are created from volumes that *are* associated with instances. We will need to identify volumes attached to the instance and then find snapshots created from those volumes. This will involve filtering `ec2_client.describe_snapshots` by volume ID.

#### 3.4.4. AMIs (Amazon Machine Images)
An AMI provides the information required to launch an instance. Each EC2 instance is launched from an AMI. We can retrieve the AMI ID from the instance details and then use `ec2_client.describe_images` to get more information about the AMI.

#### 3.4.5. Security Groups
Security groups act as a virtual firewall for your instance to control inbound and outbound traffic. EC2 instances are associated with one or more security groups. We can find associated security groups by checking the `security_groups` attribute of the EC2 instance.

#### 3.4.6. Elastic IPs (EIPs)
Elastic IP addresses are static, public IP addresses designed for dynamic cloud computing. They can be associated with EC2 instances or network interfaces. We can find associated Elastic IPs by checking the `public_ip` attribute of the instance or by filtering `ec2_client.describe_addresses` by instance ID or network interface ID.

## 4. Data Structure for Output
The collected information for each resource type will be stored in a structured format, likely a list of dictionaries or a Pandas DataFrame, to facilitate easy table generation.

## 5. Output Formatting
The final output will be a well-formatted table, displaying the discovered resources and their relevant attributes. We will use a library like `tabulate` or `pandas` to achieve this.

## 6. Error Handling
The solution will include error handling for scenarios such as invalid instance IDs, API call failures, and missing permissions.

## 7. Future Enhancements (Out of Scope for initial delivery)
- Support for multiple EC2 instance inputs.
- Integration with AWS Cost Explorer to retrieve billing information directly.
- Exporting output to different formats (CSV, JSON).


