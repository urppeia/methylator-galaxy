#!/usr/bin/env python3
"""
Install Methylator tools into a running Galaxy instance using the Bioblend API.
"""

import sys
import time
from pathlib import Path
import yaml

try:
    from bioblend.galaxy import GalaxyInstance
    from bioblend.galaxy.toolshed import ToolShedClient
except ImportError:
    print("Error: bioblend not installed. Install with: pip install bioblend")
    sys.exit(1)

def load_tools_yaml(yaml_file):
    """Load tools from YAML configuration file."""
    with open(yaml_file, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('tools', [])

def install_tools(galaxy_url, api_key, tools_list, timeout=600):
    """Install tools from Tool Shed into Galaxy."""
    
    print(f"Connecting to Galaxy at {galaxy_url}")
    gi = GalaxyInstance(url=galaxy_url, key=api_key)
    
    # Verify connection
    try:
        version = gi.gi.make_get_request(gi.gi.url + "/api/version")
        print(f"✓ Connected to Galaxy version {version.get('version_major')}.{version.get('version_minor')}")
    except Exception as e:
        print(f"✗ Failed to connect to Galaxy: {e}")
        return False
    
    # Install tools
    tc = ToolShedClient(gi)
    installed_count = 0
    failed_tools = []
    
    for i, tool in enumerate(tools_list, 1):
        print(f"\n[{i}/{len(tools_list)}] Installing {tool['name']} from {tool['owner']}...")
        
        try:
            # Install each revision
            for revision in tool.get('revisions', []):
                install_params = {
                    'tool_shed_url': tool.get('tool_shed_url', 'toolshed.g2.bx.psu.edu'),
                    'repository_name': tool['name'],
                    'repository_owner': tool['owner'],
                    'changeset_revision': revision,
                    'install_tool_dependencies': True,
                    'install_repository_dependencies': True,
                    'tool_panel_section_label': tool.get('tool_panel_section_label', 'Tools'),
                }
                
                result = tc.install_repository_revision(**install_params)
                print(f"  ✓ Installed revision {revision}")
                installed_count += 1
                
                # Small delay between installations
                time.sleep(2)
                
        except Exception as e:
            print(f"  ✗ Error installing {tool['name']}: {e}")
            failed_tools.append(tool['name'])
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Installation Summary:")
    print(f"  Successfully installed: {installed_count} revisions")
    print(f"  Failed tools: {len(failed_tools)}")
    if failed_tools:
        print(f"  Failed: {', '.join(failed_tools)}")
    print(f"{'='*60}")
    
    return len(failed_tools) == 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: install_methylator_tools.py <tools.yaml> [galaxy_url] [api_key]")
        print("Example: install_methylator_tools.py /galaxy/tools.yaml http://localhost:8080 my-api-key")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    galaxy_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8080"
    api_key = sys.argv[3] if len(sys.argv) > 3 else "admin"
    
    if not Path(yaml_file).exists():
        print(f"Error: {yaml_file} not found")
        sys.exit(1)
    
    tools = load_tools_yaml(yaml_file)
    print(f"Found {len(tools)} tools to install")
    
    success = install_tools(galaxy_url, api_key, tools)
    sys.exit(0 if success else 1)
