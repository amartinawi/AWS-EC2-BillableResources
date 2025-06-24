#!/usr/bin/env python3
"""
AWS EC2 Billable Resource Discovery CLI Tool

This is the main CLI script that combines resource discovery and table formatting
to provide a complete solution for identifying and displaying EC2-related billable resources.
"""

import sys
import argparse
from datetime import datetime
from ec2_resource_discovery import EC2ResourceDiscovery
from table_formatter import ResourceTableFormatter


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Discover and display all billable resources associated with an EC2 instance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s i-1234567890abcdef0
  %(prog)s i-1234567890abcdef0 --region us-west-2
  %(prog)s i-1234567890abcdef0 --profile myprofile --format fancy_grid
  %(prog)s i-1234567890abcdef0 --export-csv resources.csv
  %(prog)s i-1234567890abcdef0 --export-json discovery_result.json

Supported table formats:
  plain, simple, github, grid, fancy_grid, pipe, orgtbl, jira, presto, 
  pretty, psql, rst, mediawiki, moinmoin, youtrack, html, unsafehtml, 
  latex, latex_raw, latex_booktabs, latex_longtabu, textile, tsv
        """
    )
    
    parser.add_argument(
        'instance_id',
        help='EC2 instance ID (e.g., i-1234567890abcdef0)'
    )
    
    parser.add_argument(
        '--region',
        help='AWS region name (default: uses AWS CLI default or environment)'
    )
    
    parser.add_argument(
        '--profile',
        help='AWS profile name (default: uses AWS CLI default)'
    )
    
    parser.add_argument(
        '--format',
        default='grid',
        help='Table format for output (default: grid)'
    )
    
    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Show detailed tables grouped by resource type'
    )
    
    parser.add_argument(
        '--export-csv',
        metavar='FILENAME',
        help='Export resources to CSV file'
    )
    
    parser.add_argument(
        '--export-json',
        metavar='FILENAME',
        help='Export complete discovery result to JSON file'
    )
    
    parser.add_argument(
        '--summary-only',
        action='store_true',
        help='Show only the resource summary table'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='AWS EC2 Resource Discovery Tool v1.0'
    )
    
    args = parser.parse_args()
    
    # Validate instance ID format (basic check)
    if not args.instance_id.startswith('i-') or len(args.instance_id) != 19:
        print(f"Error: Invalid instance ID format: {args.instance_id}")
        print("Instance ID should be in format: i-1234567890abcdef0")
        sys.exit(1)
    
    print(f"AWS EC2 Resource Discovery Tool")
    print(f"{'=' * 50}")
    print(f"Instance ID: {args.instance_id}")
    print(f"Region: {args.region or 'default'}")
    print(f"Profile: {args.profile or 'default'}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 50}")
    
    try:
        # Initialize the discovery tool
        discovery = EC2ResourceDiscovery(region_name=args.region, profile_name=args.profile)
        
        # Discover all resources
        result = discovery.discover_all_resources(args.instance_id)
        
        if not result:
            print("Resource discovery failed.")
            sys.exit(1)
        
        # Initialize the table formatter
        formatter = ResourceTableFormatter()
        
        # Print instance details
        instance_details = result['instance_details']
        print(f"\\nInstance Details:")
        print(f"  Instance Type: {instance_details['instance_type']}")
        print(f"  State: {instance_details['state']}")
        print(f"  Availability Zone: {instance_details['availability_zone']}")
        print(f"  VPC ID: {instance_details['vpc_id']}")
        print(f"  Launch Time: {instance_details['launch_time']}")
        
        # Print summary table
        print(f"\\nResource Summary:")
        summary_table = formatter.format_summary_table(result['summary'], args.format)
        print(summary_table)
        
        # Print detailed tables if not summary-only
        if not args.summary_only:
            print(f"\\nDetailed Resource Information:")
            print(f"{'-' * 50}")
            
            if args.detailed:
                detailed_table = formatter.format_detailed_resources_table(
                    result['resources'], args.format
                )
                print(detailed_table)
            else:
                simple_table = formatter.format_resources_table(
                    result['resources'], args.format
                )
                print(simple_table)
        
        # Export to CSV if requested
        if args.export_csv:
            csv_message = formatter.export_to_csv(result['resources'], args.export_csv)
            print(f"\\n{csv_message}")
        
        # Export to JSON if requested
        if args.export_json:
            json_message = formatter.export_to_json(result, args.export_json)
            print(f"\\n{json_message}")
        
        print(f"\\nResource discovery completed successfully!")
        print(f"Total billable resources found: {result['summary']['total_resources']}")
        
    except KeyboardInterrupt:
        print("\\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

