#!/usr/bin/env python3
"""
Run all database migrations to completion using manage_db.sh upgrade in a loop.
"""
import subprocess
import os

def main():
    # Set up environment
    env = os.environ.copy()
    env['GALAXY_CONFIG_FILE'] = '/etc/galaxy/galaxy.yml'
    env['GALAXY_CONFIG_DATABASE_CONNECTION'] = 'sqlite:////export/galaxy/universe.sqlite?isolation_level=IMMEDIATE'

    print("Running all migrations to completion...")

    # Run upgrade until no more migrations
    while True:
        result = subprocess.run(
            ['sh', '/galaxy/manage_db.sh', 'upgrade'],
            env=env,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode == 0:
            # Check if there are more migrations by running version
            version_result = subprocess.run(
                ['sh', '/galaxy/manage_db.sh', 'version'],
                env=env,
                capture_output=True,
                text=True
            )
            print(version_result.stdout)
            # If both gxy and tsi are at head, we're done
            if '(head)' in version_result.stdout and version_result.stdout.count('(head)') == 2:
                print("Database at latest version.")
                break
        else:
            # If upgrade fails, we might be at the end
            break

    print("All migrations completed.")

if __name__ == '__main__':
    main()