#!/usr/bin/env python3
"""
Generate shed_tool_conf.xml from installed ToolShed repositories.
This is needed because shed-tools CLI doesn't update shed_tool_conf.xml
when repositories are already installed.
"""

import sqlite3
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom


def get_installed_repositories(db_path):
    """Get all installed tool shed repositories from the database."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        SELECT id, name, owner, changeset_revision, tool_shed, status
        FROM tool_shed_repository
        WHERE status = 'Installed'
        ORDER BY name
    """)
    repos = c.fetchall()
    conn.close()
    return repos


def find_tool_xml_files(repo_path):
    """Find all tool XML files in a repository directory."""
    tool_files = []
    for root, dirs, files in os.walk(repo_path):
        for f in files:
            if f.endswith('.xml') and not f.startswith('.'):
                # Get relative path from repo root
                rel_path = os.path.relpath(os.path.join(root, f), repo_path)
                tool_files.append(rel_path)
    return tool_files


def generate_shed_tool_conf(db_path, shed_tools_dir, output_path):
    """Generate shed_tool_conf.xml from installed repositories."""
    repos = get_installed_repositories(db_path)

    # Create toolbox element
    toolbox = ET.Element('toolbox')
    toolbox.set('tool_path', shed_tools_dir)

    # Group tools by tool_panel_section_label from the tool list
    # For now, put all in a "Methylator" section
    section = ET.SubElement(toolbox, 'section')
    section.set('id', 'methylator')
    section.set('name', 'Methylator')

    for repo_id, name, owner, changeset_revision, tool_shed, status in repos:
        # Construct repository path
        # Format: toolshed.g2.bx.psu.edu/repos/owner/name/revision
        repo_dir = os.path.join(shed_tools_dir, tool_shed, 'repos', owner, name, changeset_revision)

        if os.path.exists(repo_dir):
            tool_files = find_tool_xml_files(repo_dir)
            for tool_file in tool_files:
                # Construct full path relative to shed_tools_dir
                full_path = os.path.join(tool_shed, 'repos', owner, name, changeset_revision, tool_file)
                tool_elem = ET.SubElement(section, 'tool')
                tool_elem.set('file', full_path)
        else:
            print(f"Warning: Repository directory not found: {repo_dir}")

    # Pretty print XML
    rough_string = ET.tostring(toolbox, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    # Write to file
    with open(output_path, 'w') as f:
        f.write(pretty_xml)

    print(f"Generated {output_path} with {len(repos)} repositories")


if __name__ == '__main__':
    db_path = '/export/galaxy/universe.sqlite'
    shed_tools_dir = '/export/galaxy/shed_tools'
    output_path = '/etc/galaxy/shed_tool_conf.xml'

    generate_shed_tool_conf(db_path, shed_tools_dir, output_path)