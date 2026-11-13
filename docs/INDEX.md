# Documentation Index

Welcome! This directory contains all methylator-galaxy documentation organized by topic.

## 🎯 Quick Navigation

### 🚀 Getting Started
- **[QUICKSTART.md](guides/QUICKSTART.md)** - 5-minute setup guide
- **[README.md](../README.md)** - Project overview (in root)

### 📚 For Researchers & Publishing
- **[PUBLICATION.md](publishing/PUBLICATION.md)** - Citation formats, reproducibility, publishing guidelines
- **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Implementation overview
- **[CHANGES.md](CHANGES.md)** - Complete feature list

### 🤖 For AI & Automation
- **[AGENTS_SETUP.md](guides/AGENTS_SETUP.md)** - Galaxy Agents (Orbit) integration guide
- **[API_REFERENCE.md](api/API_REFERENCE.md)** - Complete REST API + 100+ Python examples

### 🏗️ For Developers & Architects
- **[ARCHITECTURE.md](architecture/ARCHITECTURE.md)** - System design, tech stack, security model
- **[BUILD_OPTIMIZATION.md](development/BUILD_OPTIMIZATION.md)** - Performance tuning guide

---

## 📂 Directory Structure

```
docs/
├── INDEX.md                          (this file)
├── SETUP_SUMMARY.md                  Overview of all improvements
├── CHANGES.md                        Complete feature list
│
├── guides/                           How-to guides & tutorials
│   ├── QUICKSTART.md                Getting started in 5 minutes
│   └── AGENTS_SETUP.md              Integrate AI agents (Orbit)
│
├── api/                             API reference
│   └── API_REFERENCE.md             REST API + BioBlend examples
│
├── architecture/                    System design
│   └── ARCHITECTURE.md              Complete system architecture
│
├── publishing/                      For research & publication
│   └── PUBLICATION.md               Citation, reproducibility, methods
│
└── development/                     For developers & DevOps
    └── BUILD_OPTIMIZATION.md        Build performance tuning
```

---

## 🎓 Choose Your Path

### "I want to publish my research"
→ Start with **[PUBLICATION.md](publishing/PUBLICATION.md)**
- Citation formats (BibTeX, APA, etc.)
- Reproducibility checklist
- Methods section template
- Data availability statement template
- Supplementary materials guide

### "I want to use Galaxy Agents (Orbit)"
→ Start with **[AGENTS_SETUP.md](guides/AGENTS_SETUP.md)**
- Galaxy Agents configuration
- MCP Server setup
- API key generation
- Orbit installation & connection
- Security best practices

### "I want to develop/integrate with the API"
→ Start with **[API_REFERENCE.md](api/API_REFERENCE.md)**
- Complete REST API reference
- 50+ Python BioBlend examples
- Error handling patterns
- Batch processing guide
- Advanced use cases

### "I need to understand the system"
→ Start with **[ARCHITECTURE.md](architecture/ARCHITECTURE.md)**
- System overview & diagrams
- Component design
- Data flow
- Tech stack details
- Database schema
- Performance characteristics

### "I want to optimize builds & performance"
→ Start with **[BUILD_OPTIMIZATION.md](development/BUILD_OPTIMIZATION.md)**
- BuildKit optimization
- Layer caching strategy
- Performance benchmarks
- Troubleshooting guide

### "I want a quick 5-minute setup"
→ Start with **[QUICKSTART.md](guides/QUICKSTART.md)**
- Prerequisites
- Build & start
- Install tools
- Access Galaxy
- Run first analysis

---

## 📊 Documentation Statistics

| Document | Lines | Purpose |
|----------|-------|---------|
| PUBLICATION.md | 271 | Citation, reproducibility, publishing |
| ARCHITECTURE.md | 407 | System design & technical details |
| API_REFERENCE.md | 531 | REST API reference + examples |
| AGENTS_SETUP.md | 230 | AI agent integration |
| BUILD_OPTIMIZATION.md | 122 | Performance tuning |
| QUICKSTART.md | 150 | Getting started |
| SETUP_SUMMARY.md | 325 | Implementation overview |
| CHANGES.md | 325 | Feature list |
| **TOTAL** | **2,361** | **Comprehensive documentation** |

---

## 🔍 Quick Reference

### Most Useful Commands

```bash
# Build Docker image (optimized)
export DOCKER_BUILDKIT=1
docker-compose -f config/docker/docker-compose.yml build --progress=plain

# Start Galaxy
docker-compose -f config/docker/docker-compose.yml up -d

# Install methylator tools
docker-compose -f config/docker/docker-compose.yml exec galaxy \
  python /galaxy/install_methylator_tools.py

# View logs
docker-compose -f config/docker/docker-compose.yml logs -f galaxy

# Check Galaxy API
curl http://localhost:8080/api/version
```

### Key Features

- ✅ Publication-ready (citation, methods templates)
- ✅ AI-friendly (Orbit, MCP Server, REST API)
- ✅ Performance-optimized (6-8x faster builds)
- ✅ Comprehensively documented (2,300+ lines)
- ✅ Production-ready (docker-compose, PostgreSQL)

---

## 📚 Learning Paths

### Path 1: Researcher Publishing
1. README.md (overview)
2. QUICKSTART.md (setup)
3. PUBLICATION.md (publishing)
4. Run analysis → Export provenance → Submit

### Path 2: AI Integration
1. README.md (overview)
2. QUICKSTART.md (setup)
3. AGENTS_SETUP.md (AI config)
4. Download Orbit → Connect → Analyze

### Path 3: Developer
1. README.md (overview)
2. QUICKSTART.md (setup)
3. API_REFERENCE.md (API guide)
4. Write scripts → Integrate → Deploy

### Path 4: System Admin
1. README.md (overview)
2. ARCHITECTURE.md (system design)
3. BUILD_OPTIMIZATION.md (performance)
4. Deploy → Monitor → Scale

### Path 5: Quick Setup
1. QUICKSTART.md (5 minutes)
2. Done! Start analyzing

---

## 🔗 External Resources

- [Galaxy Project](https://galaxyproject.org/)
- [Galaxy Agents](https://galaxyproject.org/agents/)
- [Galaxy API Docs](https://docs.galaxyproject.org/en/master/api/)
- [BioBlend Documentation](https://bioblend.readthedocs.io/)
- [Orbit Documentation](https://galaxyproject.org/agents/orbit/)

---

## 💬 Questions or Issues?

- Check relevant documentation above
- Review [ARCHITECTURE.md](architecture/ARCHITECTURE.md) for system design
- See [API_REFERENCE.md](api/API_REFERENCE.md) for integration help
- Read [PUBLICATION.md](publishing/PUBLICATION.md) for publishing guidance
- Open a GitHub issue for bugs or feature requests

---

**Happy analyzing! 🚀**

*Last updated: November 2026*
*Version: 2026.01*
