# Repository Organization Guide

This document explains the new repository structure and rationale.

## 📁 Directory Structure

```
methylator-galaxy/
│
├── README.md                          # Project overview
├── CONTRIBUTING.md                    # Contribution guidelines (NEW)
├── .gitignore                         # Git ignore rules (NEW)
│
├── docs/                              # 📚 DOCUMENTATION (NEW)
│   ├── INDEX.md                       Navigation guide
│   ├── SETUP_SUMMARY.md               Implementation summary
│   ├── CHANGES.md                     Feature list
│   │
│   ├── guides/                        How-to guides
│   │   ├── QUICKSTART.md             5-minute setup
│   │   └── AGENTS_SETUP.md           AI agent integration
│   │
│   ├── api/                          API reference
│   │   └── API_REFERENCE.md          REST API + examples
│   │
│   ├── architecture/                 System design
│   │   └── ARCHITECTURE.md           System architecture
│   │
│   ├── publishing/                   Publishing guidelines
│   │   └── PUBLICATION.md            Citation, reproducibility
│   │
│   └── development/                  Developer resources
│       └── BUILD_OPTIMIZATION.md     Performance tuning
│
├── config/                            # ⚙️ CONFIGURATION (NEW)
│   ├── docker/                        Docker configuration
│   │   ├── Dockerfile                Container definition (UPDATED: 26.1)
│   │   ├── docker-compose.yml        Container orchestration (UPDATED: paths)
│   │   ├── .dockerignore             Build optimization
│   │   └── .env.example              Environment variables
│   │
│   └── methylator_tool_list.yaml      Tool definitions (MOVED)
│
├── scripts/                           # 🔧 SCRIPTS (NEW)
│   ├── install_methylator_tools.py   Tool installation (MOVED)
│   └── install_tools.sh              Shell script (MOVED)
│
├── workflows/                         # 🔬 WORKFLOWS (EXISTING)
│   ├── wgbs_part1.ga                 WGBS analysis part 1
│   └── wgbs_part2.ga                 WGBS analysis part 2
│
├── .github/                           # 🚀 CI/CD (ENHANCED)
│   ├── workflows/                     GitHub Actions
│   │   ├── build-docker.yml          Docker build & push (NEW)
│   │   ├── tests.yml                 Validation & linting (NEW)
│   │   ├── release.yml               Release automation (NEW)
│   │   └── docker-build.yml          Original workflow (kept)
│   │
│   └── yamllint-config.yml            YAML linting config (NEW)
│
└── build/                             # (placeholder for future artifacts)
```

## 🎯 Organization Rationale

### Why Reorganize?

**Before:**
```
(messy root with 9 markdown files)
├── PUBLICATION.md
├── ARCHITECTURE.md
├── API_REFERENCE.md
├── AGENTS_SETUP.md
├── BUILD_OPTIMIZATION.md
├── QUICKSTART.md
├── SETUP_SUMMARY.md
├── CHANGES.md
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── install_methylator_tools.py
├── install_tools.sh
└── methylator_tool_list.yaml
```

**After:**
```
(organized with clear structure)
docs/          (all documentation)
config/        (all configuration)
scripts/       (all scripts)
workflows/     (analysis workflows)
.github/       (CI/CD automation)
```

### Benefits

✅ **Clear Navigation** - Easy to find docs by type (guides, API, architecture, etc.)  
✅ **Scalability** - Easy to add new docs, scripts, or configurations  
✅ **Professional** - Structure suitable for publication & collaboration  
✅ **CI/CD Ready** - Automated tests, linting, releases  
✅ **Maintainability** - Logical grouping reduces clutter  

## 📚 Documentation Organization

### docs/guides/
**Purpose**: Step-by-step guides and tutorials  
**Contents**:
- QUICKSTART.md - 5-minute setup
- AGENTS_SETUP.md - AI agent integration
- (Future: troubleshooting, advanced workflows, etc.)

### docs/api/
**Purpose**: API reference and integration guides  
**Contents**:
- API_REFERENCE.md - REST API + 100+ examples
- (Future: SDK documentation, webhook guides, etc.)

### docs/architecture/
**Purpose**: System design and technical deep-dives  
**Contents**:
- ARCHITECTURE.md - System design, tech stack, security
- (Future: deployment guides, scaling strategies, etc.)

### docs/publishing/
**Purpose**: Research publication support  
**Contents**:
- PUBLICATION.md - Citation, reproducibility, methods
- (Future: journal-specific guides, data sharing, etc.)

### docs/development/
**Purpose**: Developer and DevOps resources  
**Contents**:
- BUILD_OPTIMIZATION.md - Performance tuning
- (Future: release procedures, debugging, maintenance, etc.)

## ⚙️ Configuration Organization

### config/docker/
**Purpose**: All Docker/container related files  
**Contents**:
- Dockerfile - Container definition
- docker-compose.yml - Orchestration
- .dockerignore - Build optimization
- .env.example - Configuration template

**Why**: Easy to find all container setup in one place

### config/
**Purpose**: Application configuration  
**Contents**:
- methylator_tool_list.yaml - Galaxy tools

**Why**: Separates application config from infrastructure config

## 🔧 Scripts Organization

### scripts/
**Purpose**: Installation and utility scripts  
**Contents**:
- install_methylator_tools.py - Tool installer
- install_tools.sh - Shell wrapper

**Why**: Keeps scripts organized and away from root clutter

## 🚀 GitHub Actions Workflow

### build-docker.yml
**Triggers**: Push to main, tags, workflow_dispatch  
**Actions**:
- Builds Docker image with BuildKit
- Validates configuration
- Pushes to Docker Hub & Quay.io
- Caches layers for speed

### tests.yml
**Triggers**: Push/PR to main, workflow_dispatch  
**Actions**:
- Lints YAML (yamllint)
- Lints Markdown
- Validates Docker configuration
- Validates Python scripts
- Checks documentation completeness
- Tests configuration files

### release.yml
**Triggers**: Tag push (format: 20*), workflow_dispatch  
**Actions**:
- Creates GitHub Release
- Generates release notes
- Publishes Docker image
- Adds artifacts to release

### Why Multiple Workflows?

✅ **Separation of Concerns** - Each workflow has a single purpose  
✅ **Clear Status** - Easy to see which part succeeded/failed  
✅ **Optimization** - Workflows run in parallel  
✅ **Flexibility** - Can trigger individually if needed  

## 📝 Using the New Structure

### For Users
```bash
# Access documentation
open docs/INDEX.md

# Follow guides
cd docs/guides/
cat QUICKSTART.md

# Check API
cat docs/api/API_REFERENCE.md

# Build from config/docker
cd config/docker
docker-compose build
```

### For Developers
```bash
# Edit scripts
vim scripts/install_methylator_tools.py

# Update documentation
vim docs/guides/QUICKSTART.md

# Modify Docker config
vim config/docker/docker-compose.yml

# View CI/CD status
open .github/workflows/
```

### For Maintainers
```bash
# Tag a release
git tag -a 2026.02 -m "Release 2026.02"
git push origin 2026.02

# GitHub Actions will:
# 1. Run tests (tests.yml)
# 2. Create release (release.yml)
# 3. Build & push Docker (build-docker.yml)
# 4. Publish to Docker Hub
```

## 🔄 Migration from Old Structure

### Old Path → New Path

| Old | New |
|-----|-----|
| `PUBLICATION.md` | `docs/publishing/PUBLICATION.md` |
| `ARCHITECTURE.md` | `docs/architecture/ARCHITECTURE.md` |
| `API_REFERENCE.md` | `docs/api/API_REFERENCE.md` |
| `AGENTS_SETUP.md` | `docs/guides/AGENTS_SETUP.md` |
| `BUILD_OPTIMIZATION.md` | `docs/development/BUILD_OPTIMIZATION.md` |
| `QUICKSTART.md` | `docs/guides/QUICKSTART.md` |
| `Dockerfile` | `config/docker/Dockerfile` |
| `docker-compose.yml` | `config/docker/docker-compose.yml` |
| `install_methylator_tools.py` | `scripts/install_methylator_tools.py` |
| `methylator_tool_list.yaml` | `config/methylator_tool_list.yaml` |

### Updated Commands

```bash
# Build (was: docker build -t methylator-galaxy .)
# Now:
cd config/docker
docker-compose build

# Start (was: docker run -d -p 8080:80 ...)
# Now:
docker-compose up -d

# Access config (was: cat .env.example)
# Now:
cat .env.example

# Access docs (was: open QUICKSTART.md)
# Now:
open docs/guides/QUICKSTART.md
```

## 🎁 Future Extensibility

### Easy to Add

```
docs/
├── guides/
│   ├── QUICKSTART.md
│   ├── AGENTS_SETUP.md
│   ├── TROUBLESHOOTING.md        (NEW)
│   └── ADVANCED_WORKFLOWS.md     (NEW)
│
├── api/
│   ├── API_REFERENCE.md
│   └── SDK_GUIDE.md              (NEW)
│
└── deployment/                    (NEW)
    ├── KUBERNETES.md
    ├── SLURM_CLUSTER.md
    └── AWS_DEPLOYMENT.md
```

### Easy to Add Workflows

```
workflows/
├── wgbs_part1.ga
├── wgbs_part2.ga
├── advanced_methylation.ga       (NEW)
└── machine_learning.ga           (NEW)
```

### Easy to Add CI/CD

```
.github/workflows/
├── build-docker.yml
├── tests.yml
├── release.yml
├── security-scan.yml             (NEW)
└── performance-bench.yml         (NEW)
```

## ✅ Checklist for Contributors

- [ ] Documentation in `docs/` organized by type
- [ ] Configuration in `config/` separated by concern
- [ ] Scripts in `scripts/` not in root
- [ ] Updated paths in documentation links
- [ ] Updated Dockerfile context paths
- [ ] Updated docker-compose.yml build context
- [ ] Tests pass (GitHub Actions)
- [ ] No files left in root except essentials

## 🎓 References

- [docs/INDEX.md](../docs/INDEX.md) - Documentation navigation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [docs/guides/QUICKSTART.md](../docs/guides/QUICKSTART.md) - Quick start
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

**This organization makes methylator-galaxy professional, scalable, and easy to maintain!** 🎉
