# Galaxy MCP Server Configuration for Agents

This configuration enables AI agents (like Orbit, Claude Code, etc.) to interact with your methylator-galaxy instance via the Model Context Protocol (MCP).

## Quick Start

### 1. Install Galaxy MCP Server

```bash
# Inside the Galaxy container
docker-compose exec galaxy pip install galaxy-mcp

# Or use the Python version
docker-compose exec galaxy pip install 'galaxy-mcp[python]'
```

### 2. Generate API Key

```bash
# Get your Galaxy API key (use in agent configuration)
curl -X POST http://localhost:8080/api/users/admin/api_key \
  -H "Content-Type: application/json" \
  -d '{"user": "admin"}' \
  -u admin:password
```

### 3. Configure Your Agent

#### For Orbit (Desktop App)
1. Download Orbit from https://galaxyproject.org/agents/orbit/
2. Launch Orbit and select "Connect to Galaxy"
3. Enter your Galaxy URL: `http://localhost:8080`
4. Enter your API key from step 2
5. Start asking questions about your data!

#### For Claude Code / Claude Desktop
```json
{
  "mcpServers": {
    "galaxy": {
      "command": "python",
      "args": ["-m", "galaxy_mcp.server"],
      "env": {
        "GALAXY_API_KEY": "your-api-key-here",
        "GALAXY_URL": "http://localhost:8080"
      }
    }
  }
}
```

#### For Other Agents
Install the galaxy-mcp package and configure with:
- **Galaxy URL**: `http://localhost:8080`
- **API Key**: From step 2
- **Server mode**: stdio (default for MCP)

## What Agents Can Do

With Galaxy Agents enabled, AI assistants can:

1. **Search & List Tools**
   - Find methylation tools available in your instance
   - List installed workflows
   - Query tool parameters and requirements

2. **Execute Workflows**
   - Run methylation analysis workflows
   - Create custom workflows on-the-fly
   - Chain tools together for complex pipelines

3. **Manage Data**
   - Upload datasets
   - Query historical analyses
   - Export results

4. **Create Custom Tools**
   - Write user-defined tools (Python/R/Bash scripts)
   - Galaxy records them as regular jobs
   - Tools become reusable in future analyses

5. **Autonomous Analysis**
   - Agent proposes analysis plan
   - You review and approve
   - Agent executes with full provenance tracking
   - Results stored in Galaxy history

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Your Agent                             │
│              (Orbit, Claude Code, etc.)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ MCP Protocol (stdio/HTTP)
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Galaxy MCP Server                              │
│          (galaxy-mcp Python/TypeScript)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ BioBlend / Galaxy API
                     │
┌────────────────────▼────────────────────────────────────────┐
│              Your Galaxy Instance                           │
│         (methylator-galaxy on localhost:8080)              │
└─────────────────────────────────────────────────────────────┘
```

## Advanced Configuration

### Enable in docker-compose.yml

Add this to your Galaxy environment variables:

```yaml
environment:
  # ... existing variables ...
  GALAXY_ENABLE_AGENTS: "true"
  GALAXY_AGENT_MCP_SERVER: "http://localhost:8888"
```

### Run MCP Server Separately

```bash
# Terminal 1: Start Galaxy
docker-compose up -d galaxy

# Terminal 2: Start MCP server inside container
docker-compose exec galaxy python -m galaxy_mcp.server \
  --galaxy-url http://localhost:8080 \
  --api-key fakekey \
  --port 8888
```

### Multiple API Keys (for Multiple Agents)

```bash
# Create additional API keys for different agents
curl -X POST http://localhost:8080/api/users/admin/api_key \
  -H "Content-Type: application/json" \
  -d '{"user": "admin"}' \
  -u admin:password

# Each agent can use a different key for audit logging
```

## Security Best Practices

⚠️ **Important for Production:**

1. **Use Strong Passwords**: Change `GALAXY_ADMIN_PASSWORD` from "password"
2. **Use HTTPS**: Set up TLS/SSL certificates
3. **API Key Rotation**: Regenerate keys periodically
4. **Network Isolation**: Don't expose Galaxy to untrusted networks
5. **Agent Approval**: Always require agent plan approval before execution
6. **Audit Logging**: Monitor agent activities via Galaxy job history

```bash
# Production docker-compose setup
export GALAXY_ADMIN_PASSWORD=$(openssl rand -base64 32)
export GALAXY_ADMIN_API_KEY=$(openssl rand -base64 32)
docker-compose up -d
```

## Troubleshooting

### "Connection refused" from Agent

```bash
# Check Galaxy is running
docker-compose ps

# Check API is responding
curl http://localhost:8080/api/version

# Check MCP server is running
docker-compose logs galaxy | grep -i mcp
```

### "Invalid API key"

```bash
# Regenerate API key
docker-compose exec galaxy python3 << 'EOF'
from galaxy.api.app import galaxy_api_app
from galaxy.config import Configuration
config = Configuration(allow_user_creation=False, database_connection="sqlite://")
# Query and regenerate admin key
EOF
```

### Agent Can't Find Tools

```bash
# Verify tools are installed
curl -s http://localhost:8080/api/tools | jq '.[] | .id' | head -20

# Check tool panel is populated
curl -s http://localhost:8080/api/tools?in_panel=true | jq '.[] | length'
```

## Example: Orbit Workflow

1. **Launch Orbit** → "Connect Galaxy" → Enter URL + API key
2. **Ask**: "What methylation patterns do we have in this dataset?"
3. **Orbit proposes**: 
   - Upload dataset
   - Run methylation analysis
   - Generate visualization
4. **You review** the proposed workflow
5. **Click approve** → Orbit executes all steps
6. **Results appear** in Galaxy history with full provenance

## Resources

- [Galaxy Agents](https://galaxyproject.org/agents/)
- [Galaxy MCP Server GitHub](https://github.com/galaxyproject/galaxy-mcp)
- [Orbit Documentation](https://galaxyproject.org/agents/orbit/)
- [Galaxy MCP Plugins](https://github.com/galaxyproject/agentic-plugins)
- [Galaxy Help Forum](https://help.galaxyproject.org/)

## Next Steps

1. Install galaxy-mcp: `docker-compose exec galaxy pip install galaxy-mcp`
2. Generate API key: See section 2 above
3. Download Orbit or configure your agent
4. Connect to `http://localhost:8080`
5. Start analyzing with your AI agent!
