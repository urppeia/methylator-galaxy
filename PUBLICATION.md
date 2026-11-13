# Methylator Galaxy - Publication & Reproducibility Guide

This document provides guidelines for using methylator-galaxy in research and publishing results.

## Citation

If you use methylator-galaxy in your research, please cite:

```bibtex
@software{methylator_galaxy,
  title={Methylator: Galaxy Instance for Whole Genome Bisulfite Sequencing Analysis},
  author={Tanwar, Deepak K.},
  year={2026},
  url={https://github.com/urppeia/methylator-galaxy},
  note={Powered by Galaxy Project}
}
```

## Reproducibility Checklist

### Before Publishing

- [ ] **Document your Galaxy version**: Record the exact version used
- [ ] **Capture tool versions**: Export tool manifest from Galaxy
- [ ] **Save workflow definition**: Export `.ga` workflow files
- [ ] **Version your data**: Use Galaxy's history IDs and dataset tracking
- [ ] **Record parameters**: Galaxy automatically captures all tool parameters
- [ ] **Generate provenance report**: Export complete analysis trail

### Capturing Analysis Provenance

```bash
# Export complete workflow history as JSON
curl -H "X-Api-Key: YOUR_API_KEY" \
  http://localhost:8080/api/histories/{history_id}/contents \
  | jq '.' > analysis_provenance.json

# Export workflow definition
curl -H "X-Api-Key: YOUR_API_KEY" \
  http://localhost:8080/api/workflows/{workflow_id} \
  | jq '.' > workflow_definition.json

# Generate container configuration
docker-compose config > docker-compose-reproducible.yml
git log --oneline > git-history.txt
```

### Sharing Your Analysis

```bash
# Export Galaxy history as .tar.gz (shareable archive)
curl -H "X-Api-Key: YOUR_API_KEY" \
  -X GET "http://localhost:8080/api/histories/{history_id}/export" \
  --output analysis_export.tar.gz

# Share dataset
curl -H "X-Api-Key: YOUR_API_KEY" \
  http://localhost:8080/api/histories/{history_id}/datasets/{dataset_id}/download

# Generate Galaxy workflow link (shareable with full tool versions)
# Access via: http://localhost:8080/api/workflows/{workflow_id}/download
```

## Methods Section Template

```markdown
### Computational Methods

Data analysis was performed using Methylator, a Galaxy-based 
workflow system for whole genome bisulfite sequencing (WGBS) analysis.

#### Tools and Versions

- **Bismark**: Version {version} (BgruenBox) - Alignment and methylation calling
- **SAMtools**: Version {version} - BAM file processing
- **Sambamba**: Version {version} - BAM filtering and deduplication
- **BEDtools**: Version {version} - Genomic region analysis

#### Analysis Workflow

Data processing proceeded through the following steps:

1. **Quality Control**: FastQC analysis of raw reads
2. **Alignment**: Bismark alignment to reference genome
3. **Methylation Calling**: Extraction of methylation levels
4. **Post-Processing**: 
   - BAM deduplication using Sambamba
   - Coverage filtering using BEDtools
5. **Visualization**: Generation of coverage plots and methylation heatmaps

#### Container Environment

```
Galaxy Version: 24.1
Container: quay.io/bgruening/galaxy:24.1
Dockerfile: {commit_hash}
Build Date: {date}
```

#### Full Configuration

Complete reproducible environment available at:
{GitHub_URL}/releases/tag/{version}

All analyses are deterministic and can be reproduced by:
1. Pulling the Docker image
2. Loading the exported workflow
3. Re-running with identical parameters
```

## Data Availability Statement Template

```markdown
### Data Availability

Raw sequencing data is available in [GEO|SRA|Zenodo] under 
accession number [ACCESSION].

Processed data, analysis workflows, and complete Galaxy histories 
are available at:
- **Code**: {GitHub_URL}
- **Workflows**: {GitHub_URL}/tree/main/workflows
- **Container**: {Docker_Hub_URL}

Reproducible analysis can be performed using the provided Docker 
container and Galaxy history export:

```bash
# Pull the container
docker pull {docker_image}

# Run the analysis
docker-compose up -d
python install_methylator_tools.py

# Import shared history
curl -H "X-Api-Key: {api_key}" \
  -X POST http://localhost:8080/api/histories \
  -d '{"name": "Reproduced Analysis"}'
```
```

## Supplementary Materials

Create supplementary files for publication:

```
supplementary/
├── S1_Methods.md                    # Extended methods
├── S2_Tool_Versions.json            # Complete tool manifest
├── S3_Workflow_Definition.ga        # Exported workflow
├── S4_Parameter_Settings.yaml       # All tool parameters
├── S5_Sample_Processing.tsv         # Sample metadata
├── S6_Quality_Metrics.pdf           # QC reports
├── S7_Provenance_Report.html        # Complete analysis trail
└── Docker_Reproducible_Environment/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md
```

### Generate Supplementary Materials

```bash
# Export tool versions
docker-compose exec galaxy python3 << 'EOF'
import json
from galaxy.tools.toolbox import ToolBox
toolbox = ToolBox(None)
versions = {tool.id: tool.version for tool in toolbox.tools}
with open('tool_versions.json', 'w') as f:
    json.dump(versions, f, indent=2)
EOF

# Export workflow
curl -H "X-Api-Key: YOUR_API_KEY" \
  http://localhost:8080/api/workflows/{workflow_id} \
  --output Workflow_Definition.ga

# Generate HTML provenance report
docker-compose exec galaxy \
  python3 -m galaxy.tools.generator_util \
  --history {history_id} \
  --output provenance_report.html
```

## Publication Checklist

- [ ] Galaxy version documented (24.1)
- [ ] All tools pinned to specific versions
- [ ] Workflow exported and versioned in repo
- [ ] Docker image tagged with release version
- [ ] Methods section includes reproducibility statement
- [ ] Data availability includes container instructions
- [ ] Supplementary materials include full environment
- [ ] GitHub repository has clear README + documentation
- [ ] Docker Hub image is public (if sharing)
- [ ] Zenodo DOI generated for reproducibility archive

## Example Publications Using Galaxy

See how other researchers have published with Galaxy:
- [Galaxy-based publication examples](https://galaxyproject.org/citing-galaxy/)
- [Reproducible research in Galaxy](https://galaxyproject.org/community/best-practices/)

## API Access for Readers

Researchers reading your paper can access your Galaxy instance via:

```python
from bioblend.galaxy import GalaxyInstance

# Connect to published instance
gi = GalaxyInstance(url='http://your-server.edu', key='public-key')

# Access your history
histories = gi.histories.get_histories()
workflow_invocations = gi.invocations.get_invocations()

# Download results
for dataset in gi.histories.show_history(history_id)['contents_url']:
    dataset_contents = gi.datasets.show_dataset(dataset['id'])
```

## Making Your Galaxy Instance "AI-Ready"

For agent/AI integration (as discussed in AGENTS_SETUP.md):

1. **Enable MCP Server**: Agents can programmatically access your analyses
2. **Document Tool I/O**: Clear input/output schemas for automated workflows
3. **Version APIs**: Maintain backward compatibility
4. **Public Demo Data**: Provide sample datasets for reproducibility

```bash
# Test agent access
curl http://localhost:8080/api/version
curl -H "X-Api-Key: YOUR_API_KEY" http://localhost:8080/api/tools
curl -H "X-Api-Key: YOUR_API_KEY" http://localhost:8080/api/workflows
```

## Best Practices

✅ **DO:**
- Pin all tool versions explicitly
- Use version control for workflows and configs
- Document all parameter choices
- Test reproducibility before publishing
- Generate DOIs for code/data
- Provide clear installation instructions

❌ **DON'T:**
- Rely on "latest" versions of tools
- Use hardcoded absolute paths
- Store passwords or keys in Git
- Share API keys publicly
- Make breaking changes after publication

## Additional Resources

- [Galaxy and Reproducibility](https://galaxyproject.org/learn/best-practices/)
- [Ten Simple Rules for Reproducible Computational Research](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285)
- [FORCE11 Best Practices](https://www.force11.org/group/best-practices-scientific-computing)
- [BioBlend API Documentation](https://bioblend.readthedocs.io/)

## Support

For publication-related questions:
- Open an issue: {GitHub_URL}/issues
- Galaxy Help Forum: https://help.galaxyproject.org/
- Email: dktanwar@hotmail.com
