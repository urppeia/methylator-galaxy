#!/usr/bin/env python3
"""
Import and publish workflows from directory into Galaxy instance.
Automatically runs on container startup.
"""

import os
import sys
import json
import time
import requests
from pathlib import Path

GALAXY_URL = os.environ.get("GALAXY_URL", "http://localhost:80")
GALAXY_API_KEY = os.environ.get("GALAXY_ADMIN_API_KEY", "fakekey")
WORKFLOWS_DIR = os.environ.get("WORKFLOWS_DIR", "/home/galaxy/workflows")

def wait_for_galaxy(timeout=300, retries=60):
    """Wait for Galaxy to be ready."""
    print(f"Waiting for Galaxy at {GALAXY_URL}...")
    for attempt in range(retries):
        try:
            response = requests.get(f"{GALAXY_URL}/api/version", timeout=5)
            if response.status_code == 200:
                print(f"✓ Galaxy is ready after {attempt * 5}s")
                return True
        except Exception as e:
            if attempt % 6 == 0:  # Log every 30s
                print(f"  Waiting... ({attempt * 5}s elapsed)")
        time.sleep(5)
    print("✗ Galaxy did not become ready within timeout")
    return False

def get_user_id(headers):
    """Get the current user's ID."""
    try:
        response = requests.get(f"{GALAXY_URL}/api/users/current", headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("id")
    except:
        pass
    return None

def import_workflow(workflow_file, headers):
    """Import a single workflow file."""
    try:
        with open(workflow_file, 'r') as f:
            workflow_data = json.load(f)
    except Exception as e:
        print(f"✗ Failed to read {Path(workflow_file).name}: {e}")
        return None
    
    workflow_name = workflow_data.get("name", Path(workflow_file).stem)
    
    files = {
        "workflow_name": (None, workflow_name),
        "workflow_data": (Path(workflow_file).name, json.dumps(workflow_data))
    }
    
    try:
        response = requests.post(
            f"{GALAXY_URL}/api/workflows",
            headers=headers,
            files=files,
            timeout=30
        )
        
        if response.status_code in (200, 201):
            result = response.json()
            workflow_id = result.get("id")
            print(f"✓ Imported: {workflow_name} (ID: {workflow_id})")
            return workflow_id
        else:
            print(f"✗ Failed to import {workflow_name}: {response.status_code}")
            if response.text:
                print(f"  Response: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"✗ Error importing {workflow_name}: {e}")
        return None

def publish_workflow(workflow_id, headers):
    """Publish a workflow to make it visible to all users."""
    try:
        payload = {"published": True}
        response = requests.put(
            f"{GALAXY_URL}/api/workflows/{workflow_id}",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code in (200, 204):
            print(f"  ✓ Published workflow {workflow_id}")
            return True
        else:
            print(f"  ✗ Failed to publish workflow {workflow_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error publishing workflow {workflow_id}: {e}")
        return False

def main():
    if not wait_for_galaxy():
        print("\nNote: Galaxy may still be initializing. Workflows can be manually imported later.")
        return 1
    
    headers = {"X-Galaxy-Authorization": GALAXY_API_KEY}
    
    # Verify authentication
    user_id = get_user_id(headers)
    if not user_id:
        print("✗ Failed to authenticate with Galaxy")
        return 1
    
    print(f"✓ Authenticated as user {user_id}\n")
    
    if not os.path.isdir(WORKFLOWS_DIR):
        print(f"✗ Workflows directory not found: {WORKFLOWS_DIR}")
        return 1
    
    workflow_files = sorted(Path(WORKFLOWS_DIR).glob("*.ga"))
    
    if not workflow_files:
        print("No workflows found to import")
        return 0
    
    print(f"Found {len(workflow_files)} workflow(s) to import and publish\n")
    
    imported = 0
    published = 0
    
    for workflow_file in workflow_files:
        workflow_id = import_workflow(str(workflow_file), headers)
        if workflow_id:
            imported += 1
            if publish_workflow(workflow_id, headers):
                published += 1
        time.sleep(1)  # Rate limiting
    
    print(f"\nSummary: Imported {imported}/{len(workflow_files)}, Published {published}/{imported}")
    return 0 if imported == len(workflow_files) else 1

if __name__ == "__main__":
    sys.exit(main())

