#!/usr/bin/env python3
"""
Table Formatter for AWS EC2 Resource Discovery

This module provides functions to format the discovered AWS resources into various table formats.
"""

import pandas as pd
from tabulate import tabulate
import json
from typing import Dict, List, Any, Optional


class ResourceTableFormatter:
    """Class to format discovered AWS resources into tables."""
    
    def __init__(self):
        """Initialize the table formatter."""
        pass
    
    def format_resources_table(self, resources: List[Dict[str, Any]], 
                             table_format: str = "grid") -> str:
        """
        Format the list of resources into a table.
        
        Args:
            resources: List of resource dictionaries
            table_format: Table format for tabulate (grid, simple, fancy_grid, etc.)
            
        Returns:
            Formatted table as string
        """
        if not resources:
            return "No resources found."
        
        # Create a list to hold table rows
        table_data = []
        
        for resource in resources:
            # Extract common fields for all resource types
            row = {
                'Resource Type': resource.get('resource_type', 'Unknown'),
                'Resource ID': resource.get('resource_id', 'N/A'),
                'Details': self._format_resource_details(resource)
            }
            table_data.append(row)
        
        # Convert to DataFrame for better handling
        df = pd.DataFrame(table_data)
        
        # Use tabulate to create the table
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def format_detailed_resources_table(self, resources: List[Dict[str, Any]], 
                                      table_format: str = "grid") -> str:
        """
        Format resources into a detailed table with separate columns for key attributes.
        
        Args:
            resources: List of resource dictionaries
            table_format: Table format for tabulate
            
        Returns:
            Formatted detailed table as string
        """
        if not resources:
            return "No resources found."
        
        # Group resources by type for better organization
        resource_groups = {}
        for resource in resources:
            resource_type = resource.get('resource_type', 'Unknown')
            if resource_type not in resource_groups:
                resource_groups[resource_type] = []
            resource_groups[resource_type].append(resource)
        
        # Create separate tables for each resource type
        formatted_tables = []
        
        for resource_type, resource_list in resource_groups.items():
            formatted_tables.append(f"\n## {resource_type}s\n")
            
            if resource_type == 'EC2 Instance':
                table = self._format_ec2_instances_table(resource_list, table_format)
            elif resource_type == 'EBS Volume':
                table = self._format_volumes_table(resource_list, table_format)
            elif resource_type == 'Network Interface':
                table = self._format_network_interfaces_table(resource_list, table_format)
            elif resource_type == 'EBS Snapshot':
                table = self._format_snapshots_table(resource_list, table_format)
            elif resource_type == 'AMI':
                table = self._format_amis_table(resource_list, table_format)
            elif resource_type == 'Security Group':
                table = self._format_security_groups_table(resource_list, table_format)
            elif resource_type == 'Elastic IP':
                table = self._format_elastic_ips_table(resource_list, table_format)
            else:
                table = self._format_generic_table(resource_list, table_format)
            
            formatted_tables.append(table)
        
        return '\n'.join(formatted_tables)
    
    def _format_ec2_instances_table(self, instances: List[Dict[str, Any]], 
                                  table_format: str) -> str:
        """Format EC2 instances into a table."""
        table_data = []
        for instance in instances:
            row = {
                'Instance ID': instance.get('resource_id', 'N/A'),
                'Instance Type': instance.get('instance_type', 'N/A'),
                'State': instance.get('state', 'N/A'),
                'AZ': instance.get('availability_zone', 'N/A'),
                'VPC ID': instance.get('vpc_id', 'N/A'),
                'Private IP': instance.get('private_ip', 'N/A'),
                'Public IP': instance.get('public_ip', 'N/A'),
                'Tags': self._format_tags(instance.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_volumes_table(self, volumes: List[Dict[str, Any]], 
                            table_format: str) -> str:
        """Format EBS volumes into a table."""
        table_data = []
        for volume in volumes:
            row = {
                'Volume ID': volume.get('resource_id', 'N/A'),
                'Size (GB)': volume.get('size_gb', 'N/A'),
                'Type': volume.get('volume_type', 'N/A'),
                'State': volume.get('state', 'N/A'),
                'Device': volume.get('device', 'N/A'),
                'Encrypted': volume.get('encrypted', 'N/A'),
                'IOPS': volume.get('iops', 'N/A'),
                'Delete on Term': volume.get('delete_on_termination', 'N/A'),
                'Tags': self._format_tags(volume.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_network_interfaces_table(self, interfaces: List[Dict[str, Any]], 
                                       table_format: str) -> str:
        """Format network interfaces into a table."""
        table_data = []
        for interface in interfaces:
            row = {
                'Interface ID': interface.get('resource_id', 'N/A'),
                'Type': interface.get('interface_type', 'N/A'),
                'Status': interface.get('status', 'N/A'),
                'Subnet ID': interface.get('subnet_id', 'N/A'),
                'Private IP': interface.get('private_ip', 'N/A'),
                'Public IP': interface.get('public_ip', 'N/A'),
                'Security Groups': ', '.join(interface.get('security_groups', [])),
                'Tags': self._format_tags(interface.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_snapshots_table(self, snapshots: List[Dict[str, Any]], 
                              table_format: str) -> str:
        """Format EBS snapshots into a table."""
        table_data = []
        for snapshot in snapshots:
            row = {
                'Snapshot ID': snapshot.get('resource_id', 'N/A'),
                'Volume ID': snapshot.get('volume_id', 'N/A'),
                'Size (GB)': snapshot.get('volume_size_gb', 'N/A'),
                'State': snapshot.get('state', 'N/A'),
                'Progress': snapshot.get('progress', 'N/A'),
                'Start Time': snapshot.get('start_time', 'N/A')[:19] if snapshot.get('start_time') else 'N/A',
                'Encrypted': snapshot.get('encrypted', 'N/A'),
                'Description': snapshot.get('description', 'N/A')[:30] + '...' if len(snapshot.get('description', '')) > 30 else snapshot.get('description', 'N/A'),
                'Tags': self._format_tags(snapshot.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_amis_table(self, amis: List[Dict[str, Any]], 
                         table_format: str) -> str:
        """Format AMIs into a table."""
        table_data = []
        for ami in amis:
            row = {
                'AMI ID': ami.get('resource_id', 'N/A'),
                'Name': ami.get('name', 'N/A')[:30] + '...' if len(ami.get('name', '')) > 30 else ami.get('name', 'N/A'),
                'State': ami.get('state', 'N/A'),
                'Architecture': ami.get('architecture', 'N/A'),
                'Platform': ami.get('platform', 'N/A'),
                'Virtualization': ami.get('virtualization_type', 'N/A'),
                'Root Device': ami.get('root_device_type', 'N/A'),
                'Public': ami.get('public', 'N/A'),
                'Creation Date': ami.get('creation_date', 'N/A')[:10] if ami.get('creation_date') else 'N/A',
                'Tags': self._format_tags(ami.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_security_groups_table(self, security_groups: List[Dict[str, Any]], 
                                    table_format: str) -> str:
        """Format security groups into a table."""
        table_data = []
        for sg in security_groups:
            row = {
                'Security Group ID': sg.get('resource_id', 'N/A'),
                'Name': sg.get('name', 'N/A'),
                'Description': sg.get('description', 'N/A')[:40] + '...' if len(sg.get('description', '')) > 40 else sg.get('description', 'N/A'),
                'VPC ID': sg.get('vpc_id', 'N/A'),
                'Inbound Rules': sg.get('inbound_rules', 'N/A'),
                'Outbound Rules': sg.get('outbound_rules', 'N/A'),
                'Tags': self._format_tags(sg.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_elastic_ips_table(self, elastic_ips: List[Dict[str, Any]], 
                                table_format: str) -> str:
        """Format Elastic IPs into a table."""
        table_data = []
        for eip in elastic_ips:
            row = {
                'Allocation ID': eip.get('resource_id', 'N/A'),
                'Public IP': eip.get('public_ip', 'N/A'),
                'Private IP': eip.get('private_ip', 'N/A'),
                'Domain': eip.get('domain', 'N/A'),
                'Network Interface': eip.get('network_interface_id', 'N/A'),
                'Association ID': eip.get('association_id', 'N/A'),
                'Tags': self._format_tags(eip.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_generic_table(self, resources: List[Dict[str, Any]], 
                            table_format: str) -> str:
        """Format generic resources into a table."""
        table_data = []
        for resource in resources:
            row = {
                'Resource ID': resource.get('resource_id', 'N/A'),
                'Details': self._format_resource_details(resource)
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_resource_details(self, resource: Dict[str, Any]) -> str:
        """Format resource details into a compact string."""
        details = []
        
        # Skip common fields that are already displayed
        skip_fields = {'resource_type', 'resource_id', 'tags'}
        
        for key, value in resource.items():
            if key not in skip_fields and value is not None and value != 'N/A':
                if isinstance(value, (list, dict)):
                    if value:  # Only add if not empty
                        details.append(f"{key}: {str(value)[:50]}...")
                else:
                    details.append(f"{key}: {value}")
        
        return '; '.join(details[:3])  # Limit to first 3 details to keep it readable
    
    def _format_tags(self, tags: Dict[str, str]) -> str:
        """Format tags dictionary into a readable string."""
        if not tags:
            return 'None'
        
        tag_strings = [f"{k}:{v}" for k, v in list(tags.items())[:2]]  # Show first 2 tags
        result = ', '.join(tag_strings)
        
        if len(tags) > 2:
            result += f" (+{len(tags) - 2} more)"
        
        return result
    
    def format_summary_table(self, summary: Dict[str, Any], 
                           table_format: str = "grid") -> str:
        """
        Format the resource summary into a table.
        
        Args:
            summary: Summary dictionary from resource discovery
            table_format: Table format for tabulate
            
        Returns:
            Formatted summary table as string
        """
        table_data = []
        
        for resource_type, count in summary.items():
            if resource_type != 'total_resources':
                row = {
                    'Resource Type': resource_type.replace('_', ' ').title(),
                    'Count': count
                }
                table_data.append(row)
        
        # Add total row
        table_data.append({
            'Resource Type': 'TOTAL',
            'Count': summary.get('total_resources', 0)
        })
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def export_to_csv(self, resources: List[Dict[str, Any]], 
                     filename: str) -> str:
        """
        Export resources to CSV file.
        
        Args:
            resources: List of resource dictionaries
            filename: Output CSV filename
            
        Returns:
            Success message with filename
        """
        # Flatten the resources for CSV export
        flattened_resources = []
        
        for resource in resources:
            flattened = {}
            for key, value in resource.items():
                if isinstance(value, dict):
                    # Flatten dictionaries (like tags)
                    for sub_key, sub_value in value.items():
                        flattened[f"{key}_{sub_key}"] = sub_value
                elif isinstance(value, list):
                    # Convert lists to comma-separated strings
                    flattened[key] = ', '.join(map(str, value))
                else:
                    flattened[key] = value
            
            flattened_resources.append(flattened)
        
        df = pd.DataFrame(flattened_resources)
        df.to_csv(filename, index=False)
        
        return f"Resources exported to {filename}"
    
    def export_to_json(self, discovery_result: Dict[str, Any], 
                      filename: str) -> str:
        """
        Export complete discovery result to JSON file.
        
        Args:
            discovery_result: Complete result from resource discovery
            filename: Output JSON filename
            
        Returns:
            Success message with filename
        """
        with open(filename, 'w') as f:
            json.dump(discovery_result, f, indent=2, default=str)
        
        return f"Discovery result exported to {filename}"


def main():
    """Example usage of the ResourceTableFormatter."""
    # This is just for testing the formatter
    sample_resources = [
        {
            'resource_type': 'EC2 Instance',
            'resource_id': 'i-1234567890abcdef0',
            'instance_type': 't3.micro',
            'state': 'running',
            'availability_zone': 'us-east-1a',
            'vpc_id': 'vpc-12345678',
            'private_ip': '10.0.1.100',
            'public_ip': '54.123.45.67',
            'tags': {'Name': 'WebServer', 'Environment': 'Production'}
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
            'delete_on_termination': True,
            'tags': {'Name': 'RootVolume'}
        }
    ]
    
    formatter = ResourceTableFormatter()
    
    print("Simple Table Format:")
    print(formatter.format_resources_table(sample_resources))
    
    print("\n\nDetailed Table Format:")
    print(formatter.format_detailed_resources_table(sample_resources))


if __name__ == "__main__":
    main()

