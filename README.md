# Methylator Galaxy
### AI-Friendly, Publication-Ready WGBS Analysis Platform

![Galaxy](https://img.shields.io/badge/Galaxy-24.1-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ed)
![License](https://img.shields.io/badge/License-MIT-green)
![Build](https://img.shields.io/badge/Build-Optimized-brightgreen)

Methylator is a **containerized Galaxy instance** for whole genome bisulfite sequencing (WGBS) analysis, designed for **publication-quality research** and **AI agent integration**.

## ✨ Key Features

🔬 **Research-Grade Analysis**
- Pre-configured tools for WGBS: Bismark, SAMtools, Sambamba, BEDtools
- Multi-step workflows for complete methylation analysis
- Automatic provenance tracking for reproducibility

📊 **Publication-Ready**
- Full method reproducibility via Docker containers
- Complete audit trail of all analyses
- Exportable workflows and results
- Pre-built templates for methods sections (see `PUBLICATION.md`)

🤖 **AI-Ready with Galaxy Agents**
- Integrated MCP (Model Context Protocol) server for Orbit/agents
- API access for autonomous analysis planning & execution
- User-defined tool support (agents can write custom tools)
- See `AGENTS_SETUP.md` for configuration

⚡ **Optimized for Speed**
- 6-8x faster rebuild with BuildKit caching
- 120s startup with health checks (vs. 600s)
- Multi-layer optimization for CI/CD pipelines
- See `BUILD_OPTIMIZATION.md` for details

## Quick Start (5 Minutes)

### 1. Prerequisites
```bash
docker --version  # 19.03+
docker-compose --version  # 3.8+
```

### 2. Clone & Setup
```bash
git clone https://github.com/urppeia/methylator-galaxy.git
cd methylator-galaxy

# Build with BuildKit (6-8x faster)
export DOCKER_BUILDKIT=1
docker-compose build --progress=plain
```

### 3. Start Galaxy
```bash
docker-compose up -d

# Wait for Galaxy to be ready (check with healthcheck)
docker-compose ps  # Shows "healthy" when ready

# View logs
docker-compose logs -f galaxy
```

### 4. Access & Install Tools
```bash
# Access Galaxy web interface
open http://localhost:8080
# Default: admin / password

# Install methylation tools
docker-compose exec galaxy python /galaxy/install_methylator_tools.py

# Or use command-line (inside container)
docker-compose exec galaxy shed-tools install -t /galaxy/tools.yaml -a fakekey -u http://localhost
```

### 5. Run Analysis
- Upload FASTQ file via web UI (or API)
- Select workflow: `wgbs_part1` or `wgbs_part2`
- Run and monitor progress
- Export results

## Documentation

| Document | Purpose |
|----------|---------|
| **[QUICKSTART.md](QUICKSTART.md)** | Get started in 5 minutes |
| **[PUBLICATION.md](PUBLICATION.md)** | Citation, reproducibility, publishing guidelines |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design for developers & researchers |
| **[API_REFERENCE.md](API_REFERENCE.md)** | Complete REST API & BioBlend guide |
| **[AGENTS_SETUP.md](AGENTS_SETUP.md)** | Configure Orbit or other AI agents |
| **[BUILD_OPTIMIZATION.md](BUILD_OPTIMIZATION.md)** | Docker build performance guide |

## Docker Image

This repository includes a `Dockerfile` to create a Docker image for `methylator`. This allows for a consistent and isolated environment to run `methylator` and its associated tools.

### Building the Docker Image

```bash
# With BuildKit (recommended, 6-8x faster rebuilds)
export DOCKER_BUILDKIT=1
docker-compose build --progress=plain

# Or manual build
docker build -t methylator-galaxy .
```

This creates an image named `methylator-galaxy` with tag `latest`.

### Running the Docker Image

**Using Docker Compose** (recommended):
```bash
docker-compose up -d
```

**Or Docker directly**:
```bash
docker run -d -p 8080:80 --name methylator methylator-galaxy
```

Galaxy will be available at `http://localhost:8080`:
- Admin user: `admin`
- Admin password: `password` (⚠️ change in production!)

### Installing Tools

The Methylator tools are configured in `methylator_tool_list.yaml` and need to be installed after the container starts.

**Option 1: Using the Python installation script (recommended)**

```bash
# Wait for Galaxy to fully start (first-run may take 2-5 minutes)
docker-compose exec galaxy bash -c "
  echo 'Waiting for Galaxy to be ready...'
  for i in {1..120}; do
    if curl -s http://localhost/api/version > /dev/null 2>&1; then
      echo '✓ Galaxy is ready!'
      break
    fi
    sleep 5
  done
"

# Install tools using the Python script
docker-compose exec galaxy python /galaxy/install_methylator_tools.py
```

**Option 2: Using ephemeris/shed-tools**

```bash
docker-compose exec galaxy shed-tools install \
  -t /galaxy/tools.yaml \
  -a fakekey \
  -u http://localhost
```

**Option 3: Manual via Galaxy UI**

1. Access Galaxy at `http://localhost:8080`
2. Click Admin (top menu) → "Manage tools and data managers"
3. Search for and install tools individually from ToolShed

### Importing Workflows

After tools are installed, import the WGBS workflows:

```bash
docker-compose exec galaxy \
  workflow-install \
    --workflow_path /home/galaxy/workflows/ \
    -g http://localhost \
    -u admin \
    -p password
```

## Using Methylator

### Via Web Interface

1. **Upload data**: Click "Upload file" → select FASTQ files
2. **Select workflow**: Search for `wgbs_part1` or `wgbs_part2`
3. **Configure parameters**: Set reference genome, quality thresholds, etc.
4. **Run**: Click "Execute"
5. **Monitor**: View job progress in left panel
6. **Download**: Download results from history

### Via API (Python)

See [API_REFERENCE.md](API_REFERENCE.md) for complete examples:

```python
from bioblend.galaxy import GalaxyInstance

gi = GalaxyInstance(url='http://localhost:8080', key='YOUR_API_KEY')

# Upload data
dataset = gi.tools.upload_file('sample.fastq', history_id)

# Run workflow
invocation = gi.workflows.invoke_workflow(
    workflow_id='wgbs_part1',
    history_id=history_id,
    inputs={'0': {'src': 'hda', 'id': dataset}}
)

# Download results
gi.datasets.download_dataset(dataset_id, 'output.bam')
```

### Via Orbit / AI Agents

See [AGENTS_SETUP.md](AGENTS_SETUP.md) for detailed configuration:

```
1. Install Orbit desktop app
2. Connect to your Galaxy instance
3. Upload data and describe your analysis
4. Orbit suggests a plan (alignments, quality controls, etc.)
5. Approve and let Orbit run it automatically
6. Results appear in Galaxy history with full provenance
```

## Workflows

### WGBS Pipeline Part 1: Alignment & QC
- **Input**: FASTQ files
- **Steps**:
  1. Quality assessment (FastQC)
  2. Read alignment to reference genome (Bismark)
  3. Duplicate marking (Sambamba)
  4. Coverage filtering
- **Output**: Aligned BAM, quality reports

### WGBS Pipeline Part 2: Methylation Analysis
- **Input**: Aligned BAM files
- **Steps**:
  1. Methylation calling
  2. Coverage analysis (BEDtools)
  3. Statistical summary
  4. Visualization
- **Output**: Methylation calls, BED files, plots

## Available Tools

| Tool | Version | Purpose |
|------|---------|---------|
| **Bismark** | 0.24.0+ | WGBS alignment & methylation calling |
| **SAMtools** | Latest | BAM file processing |
| **Sambamba** | Latest | Fast BAM filtering & deduplication |
| **BEDtools** | Latest | Genomic interval analysis |
| **FastQC** | Latest | Read quality assessment |
| **MultiQC** | Latest | Multi-sample QC aggregation |

For full tool list, see `methylator_tool_list.yaml`.

## Publication & Reproducibility

### Before Publishing

Follow the checklist in [PUBLICATION.md](PUBLICATION.md):

- [ ] Document Galaxy & tool versions
- [ ] Export workflow definitions
- [ ] Save analysis histories
- [ ] Capture all parameters
- [ ] Generate provenance reports
- [ ] Test full reproducibility

### Example Methods Section

```
Data analysis was performed using Methylator Galaxy (v24.1), 
a containerized bioinformatics platform for WGBS analysis. 
Reads were aligned using Bismark v0.24.0, with duplicate 
marking by Sambamba v0.8.1. Methylation levels were extracted 
genome-wide at single-base resolution...

Complete reproducible environment available at:
https://github.com/urppeia/methylator-galaxy (commit: abc123def)
Docker image: docker://methylator-galaxy:v1.0
```

See [PUBLICATION.md](PUBLICATION.md) for citation format, data availability statements, and supplementary materials templates.

## Performance & Optimization

### Build Time
- **Fresh build**: 3-4 minutes
- **Cached rebuild**: 20-30 seconds (6-8x faster)
- Optimization via BuildKit, layer caching, .dockerignore

### Runtime Performance
- **Startup**: 90-120 seconds (with health checks)
- **WGBS analysis**: 60-90 minutes (100M reads sample)
- **Resource requirements**: 4+ CPU, 8+ GB RAM, 50+ GB disk

See [BUILD_OPTIMIZATION.md](BUILD_OPTIMIZATION.md) for detailed performance tuning.

## Troubleshooting

### "Galaxy not up yet" (600 timeout)
- Galaxy needs 90-120s to start
- Check logs: `docker-compose logs galaxy | tail -50`
- Ensure 8+ GB RAM available
- Give it more time before retrying tool installation

### Connection Refused
- Check Galaxy is running: `docker-compose ps`
- Check port 8080 is free: `lsof -i :8080`
- Inspect error logs: `docker-compose logs galaxy`

### Tools Won't Install
- Ensure Galaxy API is responding: `curl http://localhost:8080/api/version`
- Check tool YAML is valid: `python -m yaml methylator_tool_list.yaml`
- View installation logs: `docker-compose logs galaxy | grep -i tool`
- Try shed-tools directly (see "Installing Tools" above)

### Slow Performance
- Monitor resource usage: `docker stats`
- Check disk space: `df -h`
- Reduce job parallelism if memory-constrained
- Use SSD storage for Galaxy data volume

See [ARCHITECTURE.md](ARCHITECTURE.md) for more troubleshooting and detailed system design.

## Security

⚠️ **Development Setup** (current defaults)
- Default passwords are hardcoded
- Suitable only for localhost development
- Do NOT expose to untrusted networks

✅ **Production Setup**
- Use strong passwords (see `.env.example`)
- Enable HTTPS/TLS
- Use PostgreSQL (not SQLite)
- Restrict API key permissions
- Run on private network or behind firewall
- See [PUBLICATION.md](PUBLICATION.md) for production best practices

## Configuration

Customize via environment variables in `docker-compose.yml` or `.env`:

```bash
# Copy example config
cp .env.example .env

# Edit .env with your settings
nano .env

# Start with custom config
docker-compose up -d
```

Available variables: See `docker-compose.yml` comments and `.env.example`.

## Support & Contributing

### Getting Help
- **Documentation**: See links above (PUBLICATION.md, ARCHITECTURE.md, etc.)
- **Galaxy Help**: https://help.galaxyproject.org/
- **Issues**: https://github.com/urppeia/methylator-galaxy/issues
- **Email**: dktanwar@hotmail.com

### Contributing
- Report bugs: Open an issue with details & logs
- Request features: Describe use case & expected behavior
- Submit improvements: Fork → develop → PR

## License

MIT License - See LICENSE file for details

## Citation

If you use methylator-galaxy in research, please cite:

```bibtex
@software{methylator_galaxy,
  title={Methylator: Galaxy Instance for Whole Genome Bisulfite Sequencing Analysis},
  author={Tanwar, Deepak K.},
  year={2026},
  url={https://github.com/urppeia/methylator-galaxy}
}
```

Also cite Galaxy and relevant tool papers - see [PUBLICATION.md](PUBLICATION.md).

## Acknowledgments

Built on:
- [Galaxy Project](https://galaxyproject.org/)
- [BioBlend](https://github.com/galaxyproject/bioblend)
- [Bismark](https://github.com/FelixKrueger/Bismark)
- [SAMtools](http://samtools.sourceforge.net/)
- [Sambamba](http://lomereiter.github.io/sambamba/)
- [BEDtools](https://bedtools.readthedocs.io/)

