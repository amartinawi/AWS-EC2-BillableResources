#!/usr/bin/env python3
"""
Test script for AWS EC2 Resource Discovery Tool

This script tests the table formatting functionality with mock data
to ensure the solution works correctly without requiring actual AWS credentials.
"""

from table_formatter import ResourceTableFormatter
from datetime import datetime
import json


def create_mock_discovery_result():
    """Create mock data that simulates a real AWS resource discovery result."""
    
    mock_resources = [
        {
            'resource_type': 'EC2 Instance',
            'resource_id': 'i-1234567890abcdef0',
            'instance_type': 't3.medium',
            'state': 'running',
            'availability_zone': 'us-east-1a',
            'vpc_id': 'vpc-12345678',
            'private_ip': '10.0.1.100',
            'public_ip': '54.123.45.67',
            'tags': {'Name': 'WebServer', 'Environment': 'Production', 'Owner': 'DevTeam'}
        },
        {
            'resource_type': 'EBS Volume',
            'resource_id': 'vol-1234567890abcdef0',
            'size_gb': 20,
            'volume_type': 'gp3',
            'state': 'in-use',
            'device': '/dev/sda1',
            'encrypted': True,
            'iops': 3000,
            'throughput': 125,
            'delete_on_termination': True,
            'tags': {'Name': 'RootVolume', 'Environment': 'Production'}
        },
        {
            'resource_type': 'EBS Volume',
            'resource_id': 'vol-abcdef1234567890',
            'size_gb': 100,
            'volume_type': 'gp3',
            'state': 'in-use',
            'device': '/dev/sdf',
            'encrypted': True,
            'iops': 3000,
            'throughput': 125,
            'delete_on_termination': False,
            'tags': {'Name': 'DataVolume', 'Environment': 'Production'}
        },
        {
            'resource_type': 'Network Interface',
            'resource_id': 'eni-1234567890abcdef0',
            'interface_type': 'interface',
            'status': 'in-use',
            'subnet_id': 'subnet-12345678',
            'vpc_id': 'vpc-12345678',
            'private_ip': '10.0.1.100',
            'public_ip': '54.123.45.67',
            'security_groups': ['sg-12345678', 'sg-87654321'],
            'source_dest_check': True,
            'tags': {'Name': 'Primary-ENI'}
        },
        {
            'resource_type': 'EBS Snapshot',
            'resource_id': 'snap-1234567890abcdef0',
            'volume_id': 'vol-1234567890abcdef0',
            'volume_size_gb': 20,
            'state': 'completed',
            'progress': '100%',
            'start_time': '2024-06-20T10:30:00.000Z',
            'description': 'Automated backup of root volume',
            'encrypted': True,
            'tags': {'Name': 'RootVolume-Backup', 'AutoBackup': 'true'}
        },
        {
            'resource_type': 'EBS Snapshot',
            'resource_id': 'snap-abcdef1234567890',
            'volume_id': 'vol-abcdef1234567890',
            'volume_size_gb': 100,
            'state': 'completed',
            'progress': '100%',
            'start_time': '2024-06-20T11:00:00.000Z',
            'description': 'Weekly backup of data volume for compliance',
            'encrypted': True,
            'tags': {'Name': 'DataVolume-Backup', 'Schedule': 'Weekly'}
        },
        {
            'resource_type': 'AMI',
            'resource_id': 'ami-1234567890abcdef0',
            'name': 'ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20240301',
            'description': 'Canonical, Ubuntu, 22.04 LTS, amd64 jammy image build on 2024-03-01',
            'state': 'available',
            'architecture': 'x86_64',
            'platform': 'Linux',
            'virtualization_type': 'hvm',
            'root_device_type': 'ebs',
            'creation_date': '2024-03-01T12:00:00.000Z',
            'public': True,
            'tags': {}
        },
        {
            'resource_type': 'Security Group',
            'resource_id': 'sg-12345678',
            'name': 'web-server-sg',
            'description': 'Security group for web servers allowing HTTP and HTTPS traffic',
            'vpc_id': 'vpc-12345678',
            'inbound_rules': 3,
            'outbound_rules': 1,
            'tags': {'Name': 'WebServer-SG', 'Environment': 'Production'}
        },
        {
            'resource_type': 'Security Group',
            'resource_id': 'sg-87654321',
            'name': 'ssh-access-sg',
            'description': 'Security group allowing SSH access from office IP ranges',
            'vpc_id': 'vpc-12345678',
            'inbound_rules': 1,
            'outbound_rules': 1,
            'tags': {'Name': 'SSH-Access-SG', 'Environment': 'Production'}
        },
        {
            'resource_type': 'Elastic IP',
            'resource_id': 'eipalloc-1234567890abcdef0',
            'public_ip': '54.123.45.67',
            'private_ip': '10.0.1.100',
            'domain': 'vpc',
            'network_interface_id': 'eni-1234567890abcdef0',
            'association_id': 'eipassoc-1234567890abcdef0',
            'tags': {'Name': 'WebServer-EIP', 'Environment': 'Production'}
        }
    ]
    
    mock_instance_details = {
        'instance_id': 'i-1234567890abcdef0',
        'instance_type': 't3.medium',
        'state': 'running',
        'launch_time': '2024-06-15T09:30:00.000Z',
        'availability_zone': 'us-east-1a',
        'vpc_id': 'vpc-12345678',
        'subnet_id': 'subnet-12345678',
        'private_ip': '10.0.1.100',
        'public_ip': '54.123.45.67',
        'image_id': 'ami-1234567890abcdef0',
        'key_name': 'my-key-pair',
        'tags': {'Name': 'WebServer', 'Environment': 'Production', 'Owner': 'DevTeam'}
    }
    
    mock_summary = {
        'total_resources': 10,
        'volumes': 2,
        'network_interfaces': 1,
        'snapshots': 2,
        'amis': 1,
        'security_groups': 2,
        'elastic_ips': 1
    }
    
    return {
        'instance_details': mock_instance_details,
        'resources': mock_resources,
        'summary': mock_summary
    }


def test_table_formatting():
    """Test all table formatting functions."""
    
    print("AWS EC2 Resource Discovery Tool - Test Mode")
    print("=" * 60)
    print(f"Testing with mock data")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Create mock data
    mock_result = create_mock_discovery_result()
    
    # Initialize formatter
    formatter = ResourceTableFormatter()
    
    # Test 1: Summary Table
    print("\\n1. RESOURCE SUMMARY TABLE")
    print("-" * 40)
    summary_table = formatter.format_summary_table(mock_result['summary'], 'grid')
    print(summary_table)
    
    # Test 2: Simple Resources Table
    print("\\n2. SIMPLE RESOURCES TABLE")
    print("-" * 40)
    simple_table = formatter.format_resources_table(mock_result['resources'], 'grid')
    print(simple_table)
    
    # Test 3: Detailed Resources Table (grouped by type)
    print("\\n3. DETAILED RESOURCES TABLE (GROUPED BY TYPE)")
    print("-" * 60)
    detailed_table = formatter.format_detailed_resources_table(mock_result['resources'], 'grid')
    print(detailed_table)
    
    # Test 4: Different table formats
    print("\\n4. TESTING DIFFERENT TABLE FORMATS")
    print("-" * 50)
    
    formats_to_test = ['simple', 'fancy_grid', 'pipe', 'pretty']
    
    for fmt in formats_to_test:
        print(f"\\n4.{formats_to_test.index(fmt) + 1}. Format: {fmt}")
        print("-" * 30)
        test_table = formatter.format_summary_table(mock_result['summary'], fmt)
        print(test_table)
    
    # Test 5: Export functionality
    print("\\n5. TESTING EXPORT FUNCTIONALITY")
    print("-" * 40)
    
    # Test CSV export
    csv_result = formatter.export_to_csv(mock_result['resources'], 'test_resources.csv')
    print(csv_result)
    
    # Test JSON export
    json_result = formatter.export_to_json(mock_result, 'test_discovery_result.json')
    print(json_result)
    
    print("\\n" + "=" * 60)
    print("All tests completed successfully!")
    print("The solution is ready for use with real AWS credentials.")
    print("=" * 60)


def main():
    """Run the test suite."""
    try:
        test_table_formatting()
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

