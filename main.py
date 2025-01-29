#!/usr/bin/env python3
import os 
from dotenv import load_dotenv
import argparse
import json
from typing import List
from pathlib import Path

load_dotenv()

project_path = os.getenv("PROJECT_PATH")

# List of valid services
VALID_SERVICES = [
    "CustomerWebAPI",
    "DocumentWebAPI",
    "EmailWebAPI",
    "EurodisWebAPI",
    "EventTowerWebAPI",
    "GatewayWebAPI",
    "GeocodeWebAPI",
    "HistoryWebAPI",
    "HubCompanionWebAPI",
    "IntegrationWebAPI",
    "LockerWebAPI",
    "NotificationWebAPI",
    "PushNotificationWebAPI",
    "RoutingWebAPI",
    "ShipmentWebAPI",
    "SmsWebAPI",
    "TaskWebAPI",
    "TrackingWebAPI",
    "UserWebAPI",
    "VersioningWebAPI",
    "ViberWebAPI"
]

APPSETTINGS_MAPPING = {
    "hr": ["appsettings.AdxPreprod.json", "appsettings.CityexpressPreprod.json", "appsettings.Development.json", "appsettings.OverseasPreprod.json", "appsettings.json"],
    "si": ["appsettings.ExpressoneBAProd.json", "appsettings.ExpressoneMEProd.json", "appsettings.ExpressonePreprod.json", "appsettings.ExpressoneStaging.json"],
    "sps": ["appsettings.SPSPreprod.json", "appsettings.SPSProd.json", "appsettings.SPSStaging.json"],
    "az": ["appsettings.StarexpressPreprod.json"]
}

# Create a mapping of simplified names to full service names
SERVICE_MAPPING = {
    service.lower().replace('webapi', ''): service 
    for service in VALID_SERVICES
}

def validate_service(service: str) -> str:
    # Convert input to lowercase and remove 'webapi' if present
    simplified_input = service.lower().replace('webapi', '')
    
    if simplified_input in SERVICE_MAPPING:
        return SERVICE_MAPPING[simplified_input]
    
    # If not found, show available options in the error
    available_options = ', '.join(sorted(SERVICE_MAPPING.keys()))
    raise argparse.ArgumentTypeError(
        f"Invalid service: {service}. Must be one of: {available_options}"
        "\n(You can use these names directly, 'WebAPI' will be added automatically)"
    )

def parse_comma_separated_envs(value: str) -> List[str]:
    envs = [env.strip().lower() for env in value.split(',') if env.strip()]
    # Validate each environment
    for env in envs:
        if env not in APPSETTINGS_MAPPING:
            raise argparse.ArgumentTypeError(
                f"Invalid environment: {env}. Must be one of: {', '.join(APPSETTINGS_MAPPING.keys())}"
            )
    return envs

def get_file_path(service_path: str, appsettings_file: str) -> Path:
    """
    Determine the correct file path based on PROJECT_PATH environment variable.
    If PROJECT_PATH is set, use it as the base path.
    If not, look in the current directory structure.
    """
    if project_path:
        return Path(project_path) / service_path / appsettings_file
    
    # Try current directory first
    current_path = Path.cwd() / appsettings_file
    if current_path.exists():
        return current_path
    
    # Try service subdirectory
    service_dir_path = Path.cwd() / service_path / appsettings_file
    if service_dir_path.exists():
        return service_dir_path
    
    # If neither exists, return the service directory path as default
    return service_dir_path

def update_appsettings_file(service_path: str, appsettings_file: str, flag_name: str, set_true: bool = False):
    file_path = get_file_path(service_path, appsettings_file)
    
    try:
        # Read the existing JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Add the new flag to the Actions section
        if 'Actions' not in config:
            config['Actions'] = {}
        
        # Add the flag with specified value
        config['Actions'][flag_name] = set_true
        
        # Sort the Actions dictionary by keys
        config['Actions'] = dict(sorted(config['Actions'].items()))
        
        # Write the updated JSON back to file with proper formatting
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            f.write('\n')  # Add newline at end of file
            
        status = "set to true" if set_true else "set to false"
        print(f"  ✓ Added flag '{flag_name}' ({status}) to {file_path}")
        
    except FileNotFoundError:
        print(f"  ⚠ Warning: File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"  ⚠ Warning: Invalid JSON in file: {file_path}")
    except Exception as e:
        print(f"  ⚠ Error processing {file_path}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Feature flag configuration tool')
    parser.add_argument(
        "--name", 
        type=str, 
        required=True,
        help="Name of the feature flag",
    )
    parser.add_argument(
        "--service", 
        type=validate_service, 
        required=True,
        help="Service to configure the flag for"
    )
    parser.add_argument(
        "--env", 
        type=parse_comma_separated_envs,
        required=True,
        help=f"Comma-separated list of environments. Available: {', '.join(APPSETTINGS_MAPPING.keys())}"
    )
    args = parser.parse_args()

    base_path = project_path if project_path else "current directory"
    print(f"Configuring flag '{args.name}' for service '{args.service}'")
    print(f"Base path: {base_path}\n")
    print(f"Setting flag to true for environments: {', '.join(args.env)}")
    other_envs = [env for env in APPSETTINGS_MAPPING.keys() if env not in args.env]
    if other_envs:
        print(f"Setting flag to false for environments: {', '.join(other_envs)}\n")

    print(f"Processing appsettings files for {args.service}:")
    
    # Process environments where flag should be true
    for env in args.env:
        print(f"\nEnvironment: {env}")
        for appsettings_file in APPSETTINGS_MAPPING[env]:
            update_appsettings_file(args.service, appsettings_file, args.name, set_true=True)
    
    # Process remaining environments where flag should be false
    for env in other_envs:
        print(f"\nEnvironment: {env}")
        for appsettings_file in APPSETTINGS_MAPPING[env]:
            update_appsettings_file(args.service, appsettings_file, args.name, set_true=False)

if __name__ == "__main__":
    main() 