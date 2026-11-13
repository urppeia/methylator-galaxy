# Methylator Galaxy - Architecture & Design

Technical overview of the methylator-galaxy system for researchers, developers, and AI agents.

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                   Methylator Galaxy Instance                    │
│                   (quay.io/bgruening/galaxy:24.1)              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Galaxy Web Interface (Port 8080)                        │  │
│  │  - History Management                                    │  │
│  │  - Workflow Execution                                    │  │
│  │  - Tool Management & Configuration                       │  │
│  │  - Data Upload/Download                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Galaxy MCP Server (Port 8888) - AI/Agent Interface     │  │
│  │  - Tool discovery & execution                            │  │
│  │  - Workflow management                                   │  │
│  │  - History & dataset access                             │  │
│  │  - User-defined tool support                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Tool Panel (Installed Tools)                           │  │
│  │  ├─ Bismark (WGBS alignment)                            │  │
│  │  ├─ SAMtools (BAM processing)                           │  │
│  │  ├─ Sambamba (BAM filtering)                            │  │
│  │  ├─ BEDtools (Genomic regions)                          │  │
│  │  └─ Quality Control Tools                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Workflow Engine                                        │  │
│  │  - Bismark-based WGBS pipeline                          │  │
│  │  - Custom multi-step workflows                          │  │
│  │  - Parameterized analysis                               │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Job Execution Engine                                  │  │
│  │  - Async job processing                                │  │
│  │  - Resource scheduling                                 │  │
│  │  - Error handling & retry logic                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Data Management                                       │  │
│  │  - Galaxy Data Library                                 │  │
│  │  - History tracking (versioning)                       │  │
│  │  - Dataset metadata                                    │  │
│  │  - Persistent storage (/galaxy-data volume)            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         ▲            ▲            ▲            ▲
         │            │            │            │
         │            │            │            │
    Web UI       Python API    Orbit/Agents   BioBlend
    (Human)      (Scripts)     (AI Tools)     (Tools)
```

## Component Details

### 1. Galaxy Core (quay.io/bgruening/galaxy:24.1)

**Role**: Central workflow execution and data management platform

**Features**:
- Web-based interface for data upload, tool execution, workflow management
- RESTful API for programmatic access (used by BioBlend, agents, scripts)
- PostgreSQL database (configurable via `docker-compose.yml`)
- Built-in job scheduling and monitoring

**Volumes**:
```
galaxy-data:/home/galaxy/galaxy_storage  # Persistent data
    ├── databases/                       # SQLite or PostgreSQL
    ├── jobs/                           # Job execution logs
    ├── datasets/                       # Uploaded & generated files
    ├── workflows/                      # Exported workflow definitions
    └── histories/                      # Analysis histories
```

### 2. Methylator Tool Suite

**Installed Tools** (via `methylator_tool_list.yaml`):

```yaml
WGBS Analysis:
  - bismark              # Align reads to reference, call methylation
  - bismark_local        # Local version with custom parameters
  - samtools_merge       # Merge BAM files
  
BAM Processing:
  - sambamba_markdup     # Mark duplicates
  - sambamba_filter      # Filter reads by criteria
  - sambamba_merge       # Merge BAM files
  - sambamba_flagstat    # Generate alignment statistics
  
Genomic Analysis:
  - bedtools             # Intersection, coverage, range operations

Quality Control:
  - fastqc               # Read quality assessment
  - multiqc              # Multi-sample QC aggregation
```

**Tool Sources**:
- **ToolShed**: toolshed.g2.bx.psu.edu (community-curated)
- **Versions**: Pinned to specific revisions for reproducibility
- **Installation**: `install_methylator_tools.py` or `docker-compose exec galaxy shed-tools install ...`

### 3. Workflows

**Available Workflows** (`workflows/` directory):

- `wgbs_part1.ga` - Read QC → Alignment → Duplicate marking
- `wgbs_part2.ga` - Methylation calling → Coverage analysis → Visualization

**Workflow Structure**:
```
Input (FASTQ)
  ↓
[FastQC: Quality assessment]
  ↓
[Bismark: Align & call methylation]
  ↓
[Sambamba: Mark duplicates & filter]
  ↓
[BEDtools: Coverage analysis]
  ↓
[Visualization: Heatmaps, plots]
  ↓
Output (BAM, BED, VCF, Plots)
```

**Workflow Format**: Galaxy Workflow Archive (`.ga` JSON format)
- Portable across Galaxy instances
- Includes tool versions and parameters
- Can be imported/exported via API

### 4. Data Flow

```
User Input (FASTQ files)
    ↓
[Upload via Web UI or API]
    ↓
Galaxy History (versioned dataset collection)
    ↓
[Select Workflow]
    ↓
[Set Parameters]
    ↓
[Execute]
    ↓
Job Queue (async processing)
    ↓
Tool Containers (each tool runs in isolated environment)
    ↓
Output Datasets
    ↓
[View, download, visualize]
    ↓
Results (BAM, VCF, plots, reports)
```

### 5. API Access

**RESTful API** (via Galaxy Backend):

```bash
# Authentication
curl -H "X-Api-Key: YOUR_API_KEY" http://localhost:8080/api/

# Core Endpoints
/api/version              # Galaxy version info
/api/tools                # List installed tools
/api/workflows            # List available workflows
/api/histories            # Manage analysis histories
/api/jobs                 # Monitor job execution
/api/datasets             # Access data files
/api/invocations          # Workflow invocations
```

**Client Libraries**:
- **BioBlend** (Python): `pip install bioblend`
- **bioblend-rs** (Rust): Compiled bindings
- **Custom**: Any HTTP client with JSON handling

**Usage Example** (Python):
```python
from bioblend.galaxy import GalaxyInstance

gi = GalaxyInstance(url='http://localhost:8080', key='fakekey')

# Get tool list
tools = gi.tools.get_tools()
print([t['id'] for t in tools])

# Run workflow
workflow = gi.workflows.show_workflow('workflow-id')
invocation = gi.workflows.invoke_workflow('workflow-id', {
    'step_0': {'src': 'hda', 'id': 'dataset-id'}
})

# Monitor
while True:
    inv = gi.invocations.show_invocation(invocation['id'])
    if inv['state'] == 'scheduled':
        print(f"Progress: {inv['progress']}")
    elif inv['state'] == 'error':
        print("Failed")
        break
    elif inv['state'] == 'ok':
        print("Complete!")
        break
```

### 6. Container Architecture

**Build Process** (via `Dockerfile`):

```dockerfile
FROM quay.io/bgruening/galaxy:24.1
  ├─ Base Galaxy image (bioconda, preinstalled packages)
  ├─ Python 3.10+
  ├─ Conda environment
  ├─ PostgreSQL client
  └─ BioBlend, ephemeris libraries

ADD Tools & Configurations
  ├─ methylator_tool_list.yaml
  ├─ install_methylator_tools.py
  ├─ workflows/ directory
  └─ Visualizations (dotplot, dbgraph)

Environment Variables
  ├─ GALAXY_CONFIG_BRAND=Methylator
  ├─ GALAXY_ENABLE_AGENTS=true
  └─ Tool installation flags
```

**Optimization** (BuildKit caching):

Layer ordering (cheap → expensive):
```
1. Base image pull (cached by Docker)
2. Install MCP server & libraries (cached, rarely changes)
3. Setup directories (cached)
4. Download visualizations (cached between builds)
5. Add tool list YAML (invalidated when tool versions change)
6. Add Python installer script (invalidated when script changes)
7. Add workflow definitions (invalidated frequently)
```

**Result**: 
- Fresh build: 3-4 min
- Cached rebuild: 20-30 sec (6-8x faster)

### 7. Database Schema

**SQLite (Development)**: Single file at `galaxy-data/galaxy.db`

**PostgreSQL (Production)**: 
```
Database: galaxy
Tables:
  - users              # User accounts & permissions
  - histories          # Analysis sessions
  - datasets           # Data files (metadata)
  - jobs               # Job execution records
  - tool_dependencies  # Tool version tracking
  - workflows          # Workflow definitions
  - invocations        # Workflow run instances
```

### 8. Security Model

**Authentication**:
- Galaxy user accounts (username/password)
- API keys (for programmatic access)
- Role-based access control (RBAC)

**Data Privacy**:
- User data isolated by history/account
- Public/shared histories via explicit sharing
- API key scoping (future: fine-grained permissions)

**Container Security** (Production):
- Run as non-root user
- Read-only filesystems where possible
- Network isolation via Docker bridge
- Secrets via environment variables (.env)

### 9. Performance Characteristics

**Typical Workflow Execution** (WGBS pipeline):

| Step | Tool | Time | Input | Output |
|------|------|------|-------|--------|
| QC | FastQC | 2-5 min | 100 M reads | Reports |
| Align | Bismark | 30-60 min | 100 M reads | BAM (2-5 GB) |
| Dedup | Sambamba | 5-10 min | BAM 2-5 GB | BAM 1-2 GB |
| Filter | Sambamba | 2-5 min | BAM 1-2 GB | BAM (filtered) |
| Coverage | BEDtools | 5-10 min | BAM | BED |
| Visualization | Custom | 2-5 min | BED | Plots |
| **Total** | | **60-90 min** | | |

**Resource Requirements**:
- CPU: 4+ cores recommended
- Memory: 8 GB minimum, 16 GB recommended
- Disk: 50 GB for single large sample, 100+ GB for multiple
- Network: Adequate for tool downloads (first run: 2-5 min)

### 10. AI/Agent Integration Points

**MCP Server** (Port 8888):

```
Agent (Orbit, Claude Code, etc.)
    ↓ (stdio/HTTP)
Galaxy MCP Server
    ↓ (BioBlend)
Galaxy REST API
    ↓
Galaxy Core
```

**Capabilities Exposed to Agents**:
1. **Tool Discovery**: List & search available tools
2. **Workflow Execution**: Run workflows with parameters
3. **History Management**: Access previous analyses
4. **Data Upload/Download**: Transfer datasets
5. **Job Monitoring**: Track execution progress
6. **User-Defined Tools**: Write and execute custom scripts

**Example Agent Workflow**:

```
1. Agent asks: "Analyze this WGBS dataset"
2. System responds: "Available tools: bismark, sambamba, bedtools..."
3. Agent proposes: "Align → Dedup → Analyze coverage"
4. User approves plan
5. Agent invokes workflow with dataset
6. Agent monitors job: "50% complete..."
7. Agent processes results: "Found 12,345 methylated sites"
8. Results stored in Galaxy history (shareable, reproducible)
```

## Deployment Models

### Development (Docker Compose)
- Single container
- SQLite database
- Local storage
- Suitable for: Prototyping, testing, small teams

### Production (Recommended)
- Galaxy container + PostgreSQL container
- Persistent volumes
- Network-attached storage
- SSL/TLS certificates
- Dedicated server resources

### Cluster Deployment (Advanced)
- Galaxy with cluster job runner (Slurm, HTCondor)
- Distributed database (PostgreSQL on separate server)
- Shared filesystem (NFS, CEPH)
- Load balancer
- Suitable for: Large teams, high throughput

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Container Runtime | Docker | 19.03+ |
| Orchestration | Docker Compose | 3.8+ |
| Web Framework | Galaxy | 24.1 |
| Language | Python | 3.10+ |
| Database | PostgreSQL / SQLite | 15+ / 3.x |
| API Framework | REST/JSON | JSON API spec |
| Agent Protocol | MCP (Model Context Protocol) | 1.0+ |
| Package Manager | Conda/pip | Latest |

## Future Enhancements

- [ ] Kubernetes deployment configuration
- [ ] Advanced workflow visualization
- [ ] Real-time collaboration features
- [ ] Machine learning model integration
- [ ] Expanded AI agent support
- [ ] Advanced user-defined tool sandboxing
- [ ] Performance monitoring & auto-scaling

## References

- [Galaxy Project Architecture](https://galaxyproject.org/admin/)
- [Galaxy API Documentation](https://docs.galaxyproject.org/en/master/api/)
- [BioBlend Documentation](https://bioblend.readthedocs.io/)
- [Galaxy Best Practices](https://galaxyproject.org/community/best-practices/)
