# Flagizer

A tool for managing feature flags across different environments in NESY services.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/aras-digital/flagizer.git
cd flagizer
```

2. Install required packages:
```bash
pip install python-dotenv
```

3. Make the script executable and add it to your PATH:
```bash
# Make the script executable
chmod +x flagizer.py

# Create a symlink in a directory that's in your PATH
# For macOS/Linux:
sudo ln -s "$(pwd)/flagizer.py" /usr/local/bin/flagizer

# For Windows:
# Add the directory containing flagizer.py to your PATH environment variable
```

## Usage

After adding to PATH, you can run the script from anywhere:

```bash
# From any directory
flagizer --name IsMyFeatureEnabled --service integration --env sps,hr
```

Or run it directly from the script location:

```bash
python flagizer.py --name IsMyFeatureEnabled --service integration --env sps,hr
```

The script will look for appsettings files in the following order:
1. If `PROJECT_PATH` is set in `.env`, it will look in `$PROJECT_PATH/ServiceName/appsettings.*.json`
2. If `PROJECT_PATH` is not set, it will look in:
   - Current directory: `./appsettings.*.json`
   - Service subdirectory: `./ServiceName/appsettings.*.json`

### Available Options

- `--name`: Name of the feature flag (required)
- `--service`: Service to configure the flag for (required)
  - You can use simplified names like 'integration' instead of 'IntegrationWebAPI'
- `--env`: Comma-separated list of environments where the flag should be true (required)
  - Available environments: hr, si, sps, az

### Environment Variables

- `PROJECT_PATH`: Optional. Base path to the services directory. 
  - Example: If your services are in `/path/to/services`, set `PROJECT_PATH=/path/to/services`
  - If not set, the script will look in the current directory and service subdirectories

### Examples

```bash
# Example 1: Using PROJECT_PATH
echo "PROJECT_PATH=/path/to/services" > .env
flagizer --name IsNewFeatureEnabled --service shipment --env sps
# This will look in /path/to/services/ShipmentWebAPI/appsettings.*.json

# Example 2: Without PROJECT_PATH (running from any directory)
cd /path/to/your/project
flagizer --name IsAnotherFeatureEnabled --service integration --env hr,si
# This will look in:
# - ./appsettings.*.json
# - ./IntegrationWebAPI/appsettings.*.json

# The feature will be set to false for all unspecified environments
```

### Uninstalling

To remove the script from your PATH:
```bash
# For macOS/Linux:
sudo rm /usr/local/bin/flagizer

# For Windows:
# Remove the directory from your PATH environment variable
```

## Development

To contribute to Flagizer:

1. Clone the repository
2. Install in development mode:
   ```bash
   pip install -e .
   ```
3. Make your changes
4. Test the changes locally 