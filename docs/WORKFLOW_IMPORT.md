# Importing and Managing Workflows in Methylator Galaxy

This guide explains how to import, publish, and manage WGBS workflows in your Methylator Galaxy instance.

## Available Workflows

Methylator comes with two pre-built workflows for complete WGBS analysis:

- **`wgbs_part1.ga`** - Initial QC and alignment pipeline
  - Quality control on raw FASTQ files
  - Trimming with Trimgalore
  - Bismark alignment to reference genome
  
- **`wgbs_part2.ga`** - Methylation analysis and quantification
  - Methylation calling from BAM files
  - Coverage analysis and reporting
  - Export results for downstream analysis

## Method 1: Import via Web Interface (Recommended)

### Step 1: Access Galaxy
1. Open **http://localhost:8080** in your browser
2. Login with:
   - **Username**: admin
   - **Password**: password

### Step 2: Import Workflow
1. Click **"Workflows"** in the top menu
2. Click the **"Import"** button (top right)
3. Click **"Browse"** or drag-and-drop
4. Navigate to your repository and select:
   - `workflows/wgbs_part1.ga`
   - `workflows/wgbs_part2.ga` (import separately)
5. Click **"Import"**

### Step 3: Publish Workflow (Optional)
To make workflows visible in the "Published Workflows" list:

1. Go to **"Workflows"** menu
2. Click on your imported workflow
3. Click the **workflow settings icon** (three dots)
4. Select **"Make published"** or **"Share"**
5. Check **"Make this workflow public"** if desired

The workflow will now appear in:
- **"My Workflows"** - Your personal workflows
- **"Published Workflows"** - Visible to all users (if made public)

## Method 2: Import via File Browser

Galaxy also allows importing from local files:

1. Go to **"Workflows"** > **"Import"**
2. Select **"From Local File"** tab
3. The `/home/galaxy/workflows/` directory is accessible
4. Select `wgbs_part1.ga` or `wgbs_part2.ga`
5. Click **"Import"**

## Method 3: Import via API (Advanced)

For automated imports or integration with CI/CD:

```bash
#!/bin/bash
GALAXY_URL="http://localhost:8080"
API_KEY="your-api-key-here"  # From Galaxy user preferences

for workflow in workflows/*.ga; do
    workflow_name=$(basename "$workflow" .ga)
    
    curl -X POST "$GALAXY_URL/api/workflows" \
        -H "X-Galaxy-Authorization: $API_KEY" \
        -F "workflow_name=$workflow_name" \
        -F "workflow_data=@$workflow"
done
```

**Note**: API authentication requires setting up an API key in Galaxy user preferences.

## Running a Workflow

After importing, you can run workflows:

1. Go to **"Workflows"** in the top menu
2. Click on your workflow name
3. Click **"Run"** button
4. Set input parameters:
   - **Input Dataset**: Select your FASTQ file(s)
   - **Reference Genome**: Choose your reference (e.g., hg38, mm10)
   - **Other Parameters**: Configure as needed
5. Click **"Run Workflow"**
6. Monitor progress in the **History** panel on the right
7. View results as they complete

## Sharing Workflows

### Make Public
1. Click the workflow
2. **Workflow Options** > **Make published**
3. Toggle **"Make this workflow public"**

### Share with Specific Users
1. Click the workflow
2. **Workflow Options** > **Share**
3. Enter usernames or emails to share with

### Export Workflow
1. Click the workflow  
2. **Workflow Options** > **Download**
3. Save the `.ga` file for archival or sharing

## Troubleshooting

### Workflow Import Fails
- **Symptom**: "API authentication required" error
- **Solution**: Use the web UI import instead (Method 1)

### Workflow Not Showing in List
- **Symptom**: Imported workflow doesn't appear in "My Workflows"
- **Solution**: 
  - Refresh the page (Cmd+R or Ctrl+R)
  - Check the import status in Galaxy logs
  - Try re-importing the file

### "File Not Found" When Running
- **Symptom**: Workflow fails because input file is missing
- **Solution**:
  - Upload your FASTQ file first via **"Get Data"** > **"Upload File"**
  - Select the uploaded file as input

### Workflow Runs but Produces No Output
- **Symptom**: Workflow completes but no result files
- **Solution**:
  - Check job logs for errors
  - Verify reference genome is correctly specified
  - Check tool parameter settings in workflow

## Workflow Structure

Both workflows follow this structure:

```
Input (FASTQ files)
  ↓
QC & Trimming
  ↓
Alignment
  ↓
Methylation Calling
  ↓
Analysis & Reports
  ↓
Output (BAM, coverage, methylation calls)
```

For detailed workflow specifications, see `docs/guides/WORKFLOWS.md`.

## Command Line (Docker)

If you prefer command-line access:

```bash
# Access Galaxy container
docker-compose exec galaxy bash

# View workflows in container
ls /home/galaxy/workflows/

# Check Galaxy database
docker-compose exec galaxy python3 /galaxy/import_workflows.py
```

## Next Steps

1. **Run your first analysis**: Use `wgbs_part1` to process FASTQ files
2. **Chain workflows**: Run Part 2 on Part 1 outputs for complete analysis
3. **Customize workflows**: Edit workflows to add custom tools or parameters
4. **Export results**: Download methylation calls and coverage files for publication

## See Also

- [Galaxy Workflows Documentation](https://docs.galaxyproject.org/en/latest/user_guide/workflows.html)
- [Bismark Documentation](https://www.felix.ac.uk/bismark_docs/)
- [Publication Guide](../publishing/PUBLICATION.md)
