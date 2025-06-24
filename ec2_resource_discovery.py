#!/usr/bin/env python3
"""
AWS EC2 Billable Resource Discovery Tool

This script discovers and lists all billable resources associated with a selected EC2 instance.
It identifies volumes, network interfaces, snapshots, AMIs, Security Groups, and Elastic IPs.
"""

import boto3
import json
import sys
from typing import Dict, List, Any
from botocore.exceptions import ClientError, NoCredentialsError


class EC2ResourceDiscovery:
    """Class to discover and collect EC2-related billable resources."""
    
    def __init__(self, region_name: str = None, profile_name: str = None):
        """
        Initialize the EC2 Resource Discovery tool.
        
        Args:
            region_name: AWS region name (optional, uses default if not provided)
            profile_name: AWS profile name (optional, uses default if not provided)
        """
        try:
            session = boto3.Session(profile_name=profile_name)
            self.ec2_client = session.client('ec2', region_name=region_name)
            self.ec2_resource = session.resource('ec2', region_name=region_name)
            self.region = region_name or session.region_name
        except NoCredentialsError:
            print("Error: AWS credentials not found. Please configure your credentials.")
            sys.exit(1)
        except Exception as e:
            print(f"Error initializing AWS session: {str(e)}")
            sys.exit(1)
    
    def get_instance_details(self, instance_id: str) -> Dict[str, Any]:
        """
        Get basic details about the EC2 instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            Dictionary containing instance details
        """
        try:
            instance = self.ec2_resource.Instance(instance_id)
            instance.load()
            
            return {
                'instance_id': instance.id,
                'instance_type': instance.instance_type,
                'state': instance.state['Name'],
                'launch_time': instance.launch_time.isoformat() if instance.launch_time else None,
                'availability_zone': instance.placement['AvailabilityZone'],
                'vpc_id': instance.vpc_id,
                'subnet_id': instance.subnet_id,
                'private_ip': instance.private_ip_address,
                'public_ip': instance.public_ip_address,
                'image_id': instance.image_id,
                'key_name': instance.key_name,
                'tags': {tag['Key']: tag['Value'] for tag in (instance.tags or [])}
            }
        except ClientError as e:
            if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
                raise ValueError(f"Instance {instance_id} not found")
            else:
                raise e
    
    def get_associated_volumes(self, instance_id: str) -> List[Dict[str, Any]]:
        """
        Get all EBS volumes associated with the EC2 instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            List of dictionaries containing volume details
        """
        volumes = []
        
        try:
            response = self.ec2_client.describe_volumes(
                Filters=[
                    {'Name': 'attachment.instance-id', 'Values': [instance_id]}
                ]
            )
            
            for volume in response['Volumes']:
                volume_info = {
                    'resource_type': 'EBS Volume',
                    'resource_id': volume['VolumeId'],
                    'size_gb': volume['Size'],
                    'volume_type': volume['VolumeType'],
                    'state': volume['State'],
                    'encrypted': volume['Encrypted'],
                    'iops': volume.get('Iops', 'N/A'),
                    'throughput': volume.get('Throughput', 'N/A'),
                    'device': None,
                    'delete_on_termination': False,
                    'tags': {tag['Key']: tag['Value'] for tag in volume.get('Tags', [])}
                }
                
                # Get attachment details
                for attachment in volume.get('Attachments', []):
                    if attachment['InstanceId'] == instance_id:
                        volume_info['device'] = attachment['Device']
                        volume_info['delete_on_termination'] = attachment['DeleteOnTermination']
                        break
                
                volumes.append(volume_info)
                
        except ClientError as e:
            print(f"Error retrieving volumes: {str(e)}")
        
        return volumes
    
    def get_associated_network_interfaces(self, instance_id: str) -> List[Dict[str, Any]]:
        """
        Get all network interfaces associated with the EC2 instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            List of dictionaries containing network interface details
        """
        network_interfaces = []
        
        try:
            response = self.ec2_client.describe_network_interfaces(
                Filters=[
                    {'Name': 'attachment.instance-id', 'Values': [instance_id]}
                ]
            )
            
            for eni in response['NetworkInterfaces']:
                eni_info = {
                    'resource_type': 'Network Interface',
                    'resource_id': eni['NetworkInterfaceId'],
                    'interface_type': eni.get('InterfaceType', 'interface'),
                    'status': eni['Status'],
                    'subnet_id': eni['SubnetId'],
                    'vpc_id': eni['VpcId'],
                    'private_ip': eni.get('PrivateIpAddress'),
                    'public_ip': eni.get('Association', {}).get('PublicIp'),
                    'security_groups': [sg['GroupId'] for sg in eni.get('Groups', [])],
                    'source_dest_check': eni.get('SourceDestCheck'),
                    'tags': {tag['Key']: tag['Value'] for tag in eni.get('TagSet', [])}
                }
                
                network_interfaces.append(eni_info)
                
        except ClientError as e:
            print(f"Error retrieving network interfaces: {str(e)}")
        
        return network_interfaces
    
    def get_associated_snapshots(self, instance_id: str) -> List[Dict[str, Any]]:
        """
        Get all snapshots created from volumes associated with the EC2 instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            List of dictionaries containing snapshot details
        """
        snapshots = []
        
        # First get the volumes associated with the instance
        volumes = self.get_associated_volumes(instance_id)
        volume_ids = [vol['resource_id'] for vol in volumes]
        
        if not volume_ids:
            return snapshots
        
        try:
            response = self.ec2_client.describe_snapshots(
                OwnerIds=['self'],
                Filters=[
                    {'Name': 'volume-id', 'Values': volume_ids}
                ]
            )
            
            for snapshot in response['Snapshots']:
                snapshot_info = {
                    'resource_type': 'EBS Snapshot',
                    'resource_id': snapshot['SnapshotId'],
                    'volume_id': snapshot['VolumeId'],
                    'volume_size_gb': snapshot['VolumeSize'],
                    'state': snapshot['State'],
                    'progress': snapshot.get('Progress', 'N/A'),
                    'start_time': snapshot['StartTime'].isoformat(),
                    'description': snapshot.get('Description', ''),
                    'encrypted': snapshot['Encrypted'],
                    'tags': {tag['Key']: tag['Value'] for tag in snapshot.get('Tags', [])}
                }
                
                snapshots.append(snapshot_info)
                
        except ClientError as e:
            print(f"Error retrieving snapshots: {str(e)}")
        
        return snapshots
    
    def get_associated_ami(self, instance_id: str) -> List[Dict[str, Any]]:
        """
        Get the AMI used to launch the EC2 instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            List containing AMI details (single item)
        """
        amis = []
        
        try:
            instance = self.ec2_resource.Instance(instance_id)
            instance.load()
            
            if instance.image_id:
                response = self.ec2_client.describe_images(
                    ImageIds=[instance.image_id]
                )
                
                for ami in response['Images']:
                    ami_info = {
                        'resource_type': 'AMI',
                        'resource_id': ami['ImageId'],
                        'name': ami.get('Name', ''),
                        'description': ami.get('Description', ''),
                        'state': ami['State'],
                        'architecture': ami.get('Architecture'),
                        'platform': ami.get('Platform', 'Linux'),
                        'virtualization_type': ami.get('VirtualizationType'),
                        'root_device_type': ami.get('RootDeviceType'),
                        'creation_date': ami.get('CreationDate', ''),
                        'public': ami.get('Public', False),
                        'tags': {tag['Key']: tag['Value'] for tag in ami.get('Tags', [])}
                    }
                    
                    amis.append(ami_info)
                    
        except ClientError as e:
            print(f"Error retrieving AMI: {str(e)}")
        
        return amis
    
    def get_associated_security_groups(self, instance_id: str) -> List[Dict[str, Any]]:
        """
        Get all security groups associated with the EC2 instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            List of dictionaries containing security group details
        """
        security_groups = []
        
        try:
            instance = self.ec2_resource.Instance(instance_id)
            instance.load()
            
            sg_ids = [sg['GroupId'] for sg in instance.security_groups]
            
            if sg_ids:
                response = self.ec2_client.describe_security_groups(
                    GroupIds=sg_ids
                )
                
                for sg in response['SecurityGroups']:
                    sg_info = {
                        'resource_type': 'Security Group',
                        'resource_id': sg['GroupId'],
                        'name': sg['GroupName'],
                        'description': sg['Description'],
                        'vpc_id': sg.get('VpcId'),
                        'inbound_rules': len(sg.get('IpPermissions', [])),
                        'outbound_rules': len(sg.get('IpPermissionsEgress', [])),
                        'tags': {tag['Key']: tag['Value'] for tag in sg.get('Tags', [])}
                    }
                    
                    security_groups.append(sg_info)
                    
        except ClientError as e:
            print(f"Error retrieving security groups: {str(e)}")
        
        return security_groups
    
    def get_associated_elastic_ips(self, instance_id: str) -> List[Dict[str, Any]]:
        """
        Get all Elastic IP addresses associated with the EC2 instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            List of dictionaries containing Elastic IP details
        """
        elastic_ips = []
        
        try:
            response = self.ec2_client.describe_addresses(
                Filters=[
                    {'Name': 'instance-id', 'Values': [instance_id]}
                ]
            )
            
            for eip in response['Addresses']:
                eip_info = {
                    'resource_type': 'Elastic IP',
                    'resource_id': eip.get('AllocationId', 'N/A'),
                    'public_ip': eip['PublicIp'],
                    'private_ip': eip.get('PrivateIpAddress'),
                    'domain': eip.get('Domain', 'vpc'),
                    'network_interface_id': eip.get('NetworkInterfaceId'),
                    'association_id': eip.get('AssociationId'),
                    'tags': {tag['Key']: tag['Value'] for tag in eip.get('Tags', [])}
                }
                
                elastic_ips.append(eip_info)
                
        except ClientError as e:
            print(f"Error retrieving Elastic IPs: {str(e)}")
        
        return elastic_ips
    
    def discover_all_resources(self, instance_id: str) -> Dict[str, Any]:
        """
        Discover all billable resources associated with an EC2 instance.
        
        Args:
            instance_id: The EC2 instance ID
            
        Returns:
            Dictionary containing all discovered resources
        """
        print(f"Discovering resources for EC2 instance: {instance_id}")
        
        try:
            # Get instance details first to validate the instance exists
            instance_details = self.get_instance_details(instance_id)
            
            # Discover all associated resources
            all_resources = []
            
            # Add instance itself as a resource
            instance_resource = {
                'resource_type': 'EC2 Instance',
                'resource_id': instance_id,
                'instance_type': instance_details['instance_type'],
                'state': instance_details['state'],
                'availability_zone': instance_details['availability_zone'],
                'vpc_id': instance_details['vpc_id'],
                'private_ip': instance_details['private_ip'],
                'public_ip': instance_details['public_ip'],
                'tags': instance_details['tags']
            }
            all_resources.append(instance_resource)
            
            # Discover associated resources
            volumes = self.get_associated_volumes(instance_id)
            network_interfaces = self.get_associated_network_interfaces(instance_id)
            snapshots = self.get_associated_snapshots(instance_id)
            amis = self.get_associated_ami(instance_id)
            security_groups = self.get_associated_security_groups(instance_id)
            elastic_ips = self.get_associated_elastic_ips(instance_id)
            
            # Combine all resources
            all_resources.extend(volumes)
            all_resources.extend(network_interfaces)
            all_resources.extend(snapshots)
            all_resources.extend(amis)
            all_resources.extend(security_groups)
            all_resources.extend(elastic_ips)
            
            return {
                'instance_details': instance_details,
                'resources': all_resources,
                'summary': {
                    'total_resources': len(all_resources),
                    'volumes': len(volumes),
                    'network_interfaces': len(network_interfaces),
                    'snapshots': len(snapshots),
                    'amis': len(amis),
                    'security_groups': len(security_groups),
                    'elastic_ips': len(elastic_ips)
                }
            }
            
        except ValueError as e:
            print(f"Error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None


def main():
    """Main function to run the resource discovery tool."""
    if len(sys.argv) < 2:
        print("Usage: python ec2_resource_discovery.py <instance-id> [region] [profile]")
        print("Example: python ec2_resource_discovery.py i-1234567890abcdef0 us-east-1 default")
        sys.exit(1)
    
    instance_id = sys.argv[1]
    region = sys.argv[2] if len(sys.argv) > 2 else None
    profile = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Initialize the discovery tool
    discovery = EC2ResourceDiscovery(region_name=region, profile_name=profile)
    
    # Discover all resources
    result = discovery.discover_all_resources(instance_id)
    
    if result:
        print(f"\nResource discovery completed successfully!")
        print(f"Region: {discovery.region}")
        print(f"Total resources found: {result['summary']['total_resources']}")
        
        # Print summary
        print("\nResource Summary:")
        for resource_type, count in result['summary'].items():
            if resource_type != 'total_resources':
                print(f"  {resource_type.replace('_', ' ').title()}: {count}")
        
        # Return the result for further processing
        return result
    else:
        print("Resource discovery failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()

