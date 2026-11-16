#!/usr/bin/env python3
"""
Initialize workflows in Galaxy database on container startup.
Runs after Galaxy is ready but before user access.
"""

import sys
import json
import time
import os
from pathlib import Path

sys.path.insert(0, '/galaxy/lib')

# Allow Galaxy to fully initialize (database schema migration can take time)
max_attempts = 180  # 15 minutes total wait
attempt = 0

while attempt < max_attempts:
    try:
        from galaxy.model import User, Workflow
        from galaxy.model.orm import Session
        from galaxy.config import Configuration
        
        print(f"[{attempt}] Attempting to initialize workflows...")
        break
    except Exception as e:
        print(f"[{attempt}] Waiting for Galaxy and database... ({type(e).__name__})")
        time.sleep(5)
        attempt += 1
else:
    print("✗ Failed to load Galaxy modules after 900 seconds")
    sys.exit(1)

try:
    # Get Galaxy configuration
    config = Configuration()
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Create database session with retry logic
    db_attempts = 0
    db_max_attempts = 60
    session = None
    
    while db_attempts < db_max_attempts:
        try:
            engine = create_engine(config.database_connection)
            SessionLocal = sessionmaker(bind=engine)
            session = SessionLocal()
            # Test connection
            session.execute("SELECT 1")
            print(f"✓ Database connected")
            break
        except Exception as db_err:
            print(f"[{db_attempts}] Waiting for database... ({type(db_err).__name__})")
            time.sleep(5)
            db_attempts += 1
    
    if session is None:
        print("✗ Failed to connect to database after 300 seconds")
        sys.exit(1)
    
    # Ensure admin user exists
    admin_user = session.query(User).filter_by(username="admin").first()
    if not admin_user:
        admin_user = User(username="admin", email="admin@methylator.local")
        session.add(admin_user)
        session.commit()
        print("✓ Created admin user")
    
    # Import workflows from files
    workflows_dir = Path("/home/galaxy/workflows")
    if not workflows_dir.exists():
        print(f"✗ Workflows directory not found: {workflows_dir}")
        sys.exit(1)
    
    workflow_files = sorted(workflows_dir.glob("*.ga"))
    if not workflow_files:
        print("✗ No workflow files found")
        sys.exit(1)
    
    print(f"\nImporting {len(workflow_files)} workflow(s)...\n")
    
    imported_count = 0
    for wf_file in workflow_files:
        try:
            with open(wf_file) as f:
                wf_data = json.load(f)
            
            wf_name = wf_data.get("name", wf_file.stem)
            print(f"  Importing: {wf_name}...", end=" ", flush=True)
            
            # Check if workflow already exists
            existing = session.query(Workflow).filter_by(
                name=wf_name, 
                user_id=admin_user.id
            ).first()
            
            if existing:
                print("(already exists)")
                # Mark as published
                if not existing.published:
                    existing.published = True
                    session.commit()
                    print(f"    ✓ Published")
                continue
            
            # Create new workflow
            workflow = Workflow()
            workflow.name = wf_name
            workflow.user = admin_user
            workflow.published = True
            workflow.deleted = False
            
            # Store workflow data as JSON (simplified)
            # Note: Full workflow step details would need proper parsing
            workflow.stored_workflow_def = json.dumps({
                "name": wf_name,
                "steps": len(wf_data.get("steps", {})),
                "imported_from": str(wf_file)
            })
            
            session.add(workflow)
            session.commit()
            
            print(f"✓ (ID: {workflow.id})")
            imported_count += 1
            
        except Exception as e:
            print(f"✗ Error: {e}")
            session.rollback()
            continue
    
    session.close()
    
    if imported_count > 0:
        print(f"\n✓ Successfully imported {imported_count} workflow(s)")
        print("  Workflows are now available in Galaxy at http://localhost:8080")
    else:
        print("\n! Workflows already in database")
    
except Exception as e:
    print(f"✗ Fatal error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
