# Contributing to Methylator Galaxy

Thank you for your interest in contributing! This document provides guidelines for contributing to methylator-galaxy.

## Code of Conduct

This project adheres to the Galaxy Project's Code of Conduct. By participating, you're expected to uphold this code.

## Ways to Contribute

### 1. Report Bugs
- Check if the bug has already been reported in [Issues](../../issues)
- Include:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs. actual behavior
  - System info (OS, Docker version, etc.)
  - Relevant logs

### 2. Suggest Enhancements
- Check if the enhancement has been suggested in [Issues](../../issues)
- Describe the use case and expected benefit
- Provide examples if possible

### 3. Submit Pull Requests
- Fork the repository
- Create a feature branch: `git checkout -b feature/your-feature`
- Make your changes
- Test locally
- Commit with clear messages
- Push to your fork
- Open a Pull Request with description

### 4. Improve Documentation
- Fix typos or unclear sections
- Add examples or clarifications
- Improve organization
- All in [docs/](docs/) directory

### 5. Share Workflows
- Create WGBS analysis workflows
- Document in [workflows/](workflows/) directory
- Include parameter descriptions
- Add usage examples

## Development Setup

```bash
# Clone repo
git clone https://github.com/urppeia/methylator-galaxy.git
cd methylator-galaxy

# Enable BuildKit for fast builds
export DOCKER_BUILDKIT=1

# Build
cd config/docker
docker-compose build --progress=plain

# Start
docker-compose up -d

# Install tools
docker-compose exec galaxy python /galaxy/install_methylator_tools.py

# Check Galaxy is running
docker-compose logs -f galaxy
```

## Making Changes

### Directory Structure

```
methylator-galaxy/
├── config/               # Configuration files
│   ├── docker/          # Docker configuration
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── .env.example
│   └── methylator_tool_list.yaml
├── scripts/             # Python/shell scripts
├── docs/                # Documentation (organized by type)
│   ├── guides/          # How-to guides
│   ├── api/             # API reference
│   ├── architecture/    # System design
│   ├── publishing/      # Publishing guidelines
│   └── development/     # Development docs
├── workflows/           # Galaxy workflows
├── .github/
│   └── workflows/       # GitHub Actions
├── README.md
└── .gitignore
```

### Workflow for Changes

1. **Documentation changes**: Edit files in `docs/` directory
2. **Code changes**: Edit scripts in `scripts/` directory
3. **Configuration**: Edit files in `config/` directory
4. **Workflows**: Add `.ga` files to `workflows/` directory
5. **GitHub Actions**: Edit `.yml` files in `.github/workflows/`

## Code Standards

### Python
- Follow PEP 8
- Use clear variable names
- Add docstrings for functions
- Test before submitting

### YAML
- Use 2-space indentation
- Validate with `yamllint`
- Comment complex configurations

### Markdown
- Use clear headers
- Include code examples
- Link to related docs
- Keep line length under 100 chars

### Docker
- Use specific base image versions
- Pin tool versions
- Add comments for complex RUN commands
- Test locally with BuildKit

## Testing

Before submitting:

```bash
# Validate configs
python3 -c "import yaml; yaml.safe_load(open('config/docker/docker-compose.yml'))"

# Lint Python
flake8 scripts/*.py

# Test build
export DOCKER_BUILDKIT=1
cd config/docker
docker-compose build --progress=plain

# Test startup
docker-compose up -d
docker-compose ps  # Should show "healthy"
docker-compose down

# Verify docs
ls docs/INDEX.md  # Should exist
```

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add support for XYZ feature
- Added new capability
- Updated documentation
- Added tests

fix: Fix bug with ABC
- Corrected behavior
- Tested fix

docs: Update installation guide
- Clarified steps
- Added examples

chore: Update Galaxy to 26.1
- Upgraded base image
- Updated documentation
```

## Pull Request Process

1. Ensure all tests pass (GitHub Actions will check)
2. Update relevant documentation
3. Add/update tests if applicable
4. Reference related issues
5. Provide clear description
6. Be open to feedback

### PR Title Format

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `chore:` Maintenance
- `test:` Test improvements
- `refactor:` Code refactoring

### PR Description Template

```markdown
## Description
Clear description of changes.

## Related Issues
Fixes #123
Related to #456

## Changes Made
- Bullet point 1
- Bullet point 2

## How to Test
Steps to test the changes.

## Documentation
- [ ] Updated relevant docs
- [ ] Added examples if applicable

## Checklist
- [ ] Tests pass
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] No breaking changes
```

## Release Process

Maintainers will:
1. Review and merge pull requests
2. Create release tags: `YYYY.MM` (e.g., `2026.01`)
3. GitHub Actions will:
   - Build Docker image
   - Create GitHub Release
   - Publish to Docker Hub
   - Generate release notes

## Getting Help

- Check [docs/INDEX.md](docs/INDEX.md) for documentation
- Review existing [Issues](../../issues)
- Read [GitHub Discussions](../../discussions)
- Ask in Galaxy Help Forum

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes
- Project documentation

---

Thank you for contributing to methylator-galaxy! 🎉
