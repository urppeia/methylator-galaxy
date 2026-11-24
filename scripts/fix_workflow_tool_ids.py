#!/usr/bin/env python3
"""
Fix workflow tool IDs to match Galaxy's installed tool IDs.
The workflow .ga files use full ToolShed IDs with version strings,
but Galaxy loads tools with short IDs from the XML files.
"""

import json
import sys
from pathlib import Path

# Mapping from workflow tool_id to Galaxy's actual tool_id
TOOL_ID_MAP = {
    # WGBS Part 1
    "toolshed.g2.bx.psu.edu/repos/devteam/fastqc/fastqc/0.74+galaxy1": "rgFastQC",
    "toolshed.g2.bx.psu.edu/repos/bgruening/trim_galore/trim_galore/0.6.10+galaxy0": "trim_galore",
    "toolshed.g2.bx.psu.edu/repos/jobucher/bbtools_clumpify/clumpify/0.1.0+galaxy0": "clumpify",
    "toolshed.g2.bx.psu.edu/repos/bgruening/bismark/bismark_bowtie2/0.22.1+galaxy4": "bismark_bowtie2",
    "toolshed.g2.bx.psu.edu/repos/bgruening/bismark/bismark_methylation_extractor/0.22.1+galaxy1": "bismark_methylation_extractor",
    # WGBS Part 2
    "toolshed.g2.bx.psu.edu/repos/bgruening/bismark/bismark_methylation_extractor/0.22.1+galaxy1": "bismark_methylation_extractor",
    "toolshed.g2.bx.psu.edu/repos/jobucher/dmrseq/dmrseq/1.22.0+galaxy1": "dmrseq",
    "toolshed.g2.bx.psu.edu/repos/rnateam/methylkit/methylkit/0.99.2": "methylkit",
    "toolshed.g2.bx.psu.edu/repos/jobucher/rgreat/rgreat/2.4.0+galaxy1": "rgreat",
    "toolshed.g2.bx.psu.edu/repos/jobucher/monalisa/monaLisa/1.8.0+galaxy2": "monalisa",
}

def fix_workflow(workflow_path):
    """Fix tool IDs in a workflow file."""
    with open(workflow_path, 'r') as f:
        workflow = json.load(f)

    steps = workflow.get('steps', {})
    fixed_count = 0

    # Also track which short IDs we're mapping to
    TARGET_IDS = set(TOOL_ID_MAP.values())

    for step_id, step in steps.items():
        if step.get('type') == 'tool':
            old_tool_id = step.get('tool_id')
            if old_tool_id in TOOL_ID_MAP:
                new_tool_id = TOOL_ID_MAP[old_tool_id]
                step['tool_id'] = new_tool_id
                step['content_id'] = new_tool_id
                # Remove tool_shed_repository so Galaxy uses tool_id directly
                if 'tool_shed_repository' in step:
                    del step['tool_shed_repository']
                # Clear tool_version so Galaxy doesn't reconstruct ToolShed ID
                step['tool_version'] = None
                print(f"  Fixed step {step_id}: {old_tool_id} -> {new_tool_id}")
                fixed_count += 1
            elif old_tool_id in TARGET_IDS:
                # Already has correct tool_id but still has tool_shed_repository
                if 'tool_shed_repository' in step:
                    del step['tool_shed_repository']
                    print(f"  Removed tool_shed_repository from step {step_id} (tool_id: {old_tool_id})")
                    fixed_count += 1
                # Also clear tool_version so Galaxy doesn't reconstruct ToolShed ID
                if 'tool_version' in step:
                    step['tool_version'] = None
                    print(f"  Cleared tool_version from step {step_id}")
            elif old_tool_id:
                # Check if it's a ToolShed ID we don't have in map
                if old_tool_id.startswith('toolshed.g2.bx.psu.edu'):
                    print(f"  WARNING: Unmapped tool_id in step {step_id}: {old_tool_id}")

    if fixed_count > 0:
        with open(workflow_path, 'w') as f:
            json.dump(workflow, f, indent=2)
        print(f"✓ Fixed {fixed_count} tool IDs in {workflow_path.name}")
    else:
        print(f"No changes needed for {workflow_path.name}")

    return fixed_count

def main():
    workflows_dir = Path("/Users/detanw/Desktop/methylator-galaxy/workflows")

    for workflow_file in workflows_dir.glob("*.ga"):
        print(f"\nProcessing {workflow_file.name}...")
        fix_workflow(workflow_file)

if __name__ == "__main__":
    main()