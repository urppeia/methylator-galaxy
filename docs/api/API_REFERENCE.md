# Methylator Galaxy - API Reference

Complete API reference for programmatic access to methylator-galaxy via REST API and BioBlend.

## Quick Start

### 1. Get Your API Key

```bash
# Generate API key (inside container or via HTTP)
curl -X POST http://localhost:8080/api/users/admin/api_key \
  -H "Content-Type: application/json" \
  -u admin:password
```

Response:
```json
{
  "api_key": "abc123def456..."
}
```

### 2. Test Connection

```bash
# Using curl
curl -H "X-Api-Key: YOUR_API_KEY" \
  http://localhost:8080/api/version

# Using Python
from bioblend.galaxy import GalaxyInstance
gi = GalaxyInstance(url='http://localhost:8080', key='YOUR_API_KEY')
print(gi.version.get_version())
```

## REST API Endpoints

### Core Endpoints

#### 1. Version & Status

```bash
GET /api/version
  Response: {"version_major": 24, "version": "24.1", ...}

GET /api/configuration
  Response: {full Galaxy configuration}

GET /api/user_current
  Response: {current user details}
```

#### 2. Tools

```bash
# List all tools
GET /api/tools
  Query params:
    - in_panel: true|false (filter by tool panel)
    - q: search query
  Response: [{id, name, version, owner, ...}]

# Get tool details
GET /api/tools/{tool_id}
  Response: {
    "id": "bismark",
    "name": "Bismark",
    "version": "0.24.0",
    "description": "...",
    "inputs": [{name, type, required, ...}],
    "outputs": [{name, type, ...}],
    "help": "..."
  }

# Execute tool
POST /api/tools
  Body: {
    "tool_id": "bismark",
    "history_id": "abcd1234",
    "inputs": {
      "input_fastq": {"src": "hda", "id": "dataset_id"},
      "reference_genome": "hg38",
      "min_coverage": 5
    }
  }
  Response: {"outputs": [{id, name, ...}], "job_id": "..."}
```

#### 3. Workflows

```bash
# List workflows
GET /api/workflows
  Response: [{id, name, owner, published, ...}]

# Get workflow definition
GET /api/workflows/{workflow_id}
  Response: {
    "id": "wgbs_pipeline",
    "name": "WGBS Analysis",
    "steps": [{
      "id": 0,
      "tool_id": "fastqc",
      "state": "ok",
      "inputs": {...},
      "outputs": {...}
    }, ...],
    "inputs": {
      "step_0_input": {type, name, ...}
    }
  }

# Invoke (run) workflow
POST /api/workflows/{workflow_id}/invocations
  Body: {
    "history_id": "abcd1234",
    "inputs": {
      "0": {"src": "hda", "id": "dataset_id"}
    }
  }
  Response: {
    "id": "invocation_123",
    "state": "scheduled",
    "workflow_id": "wgbs_pipeline",
    "history_id": "abcd1234"
  }

# Get invocation status
GET /api/invocations/{invocation_id}
  Response: {
    "id": "invocation_123",
    "state": "running|ok|error",
    "progress": 0.5,
    "steps": [{id, state, job_id, outputs: [{...}]}]
  }

# Export workflow
GET /api/workflows/{workflow_id}/download
  Response: {.ga workflow file (JSON)}
```

#### 4. Histories (Analysis Sessions)

```bash
# List histories
GET /api/histories
  Query params:
    - limit: 10 (max results)
    - offset: 0 (pagination)
  Response: [{id, name, size, update_time, ...}]

# Get history details
GET /api/histories/{history_id}
  Response: {
    "id": "abc123",
    "name": "My Analysis",
    "update_time": "2026-11-13T11:00:00.000Z",
    "size": 5368709120,
    "contents_url": "/api/histories/abc123/contents"
  }

# Get datasets in history
GET /api/histories/{history_id}/contents
  Response: [{
    "id": "dataset_123",
    "name": "Sample_R1.fastq",
    "type": "file",
    "file_size": 1024000000,
    "state": "ok",
    "data_type": "fastqsanger",
    "download_url": "/api/datasets/dataset_123/download",
    "visualizations": [...]
  }, ...]

# Create history
POST /api/histories
  Body: {"name": "New Analysis"}
  Response: {history object}

# Delete history
DELETE /api/histories/{history_id}
  Response: 204 No Content
```

#### 5. Datasets

```bash
# Get dataset info
GET /api/datasets/{dataset_id}
  Response: {
    "id": "dataset_123",
    "name": "output.bam",
    "type": "file",
    "file_size": 2147483648,
    "state": "ok",
    "data_type": "bam",
    "metadata": {
      "bam_index": "exists",
      "lines": 10000000
    }
  }

# Download dataset
GET /api/datasets/{dataset_id}/download
  Response: Binary file content

# Upload dataset
POST /api/tools/upload
  Body: multipart/form-data with file
  Response: {dataset_id, ...}
```

#### 6. Jobs

```bash
# Get job details
GET /api/jobs/{job_id}
  Response: {
    "id": "job_123",
    "tool_id": "bismark",
    "state": "ok|error|running",
    "tool_stdout": "...",
    "tool_stderr": "...",
    "exit_code": 0,
    "create_time": "2026-11-13T11:00:00.000Z",
    "update_time": "2026-11-13T11:30:00.000Z"
  }

# List jobs
GET /api/jobs
  Query params:
    - state: ok, error, running, queued
    - limit: 10
  Response: [{job objects}]

# Get job outputs
GET /api/jobs/{job_id}/outputs
  Response: [{dataset objects}]
```

## Python API (BioBlend)

### Installation

```bash
pip install bioblend
```

### Common Patterns

#### Setup Connection

```python
from bioblend.galaxy import GalaxyInstance

# Connect to your Galaxy instance
gi = GalaxyInstance(
    url='http://localhost:8080',
    key='YOUR_API_KEY'
)
```

#### List & Search Tools

```python
# List all tools
tools = gi.tools.get_tools()
print(f"Available tools: {len(tools)}")

# Search for specific tool
bismark_tools = [t for t in tools if 'bismark' in t['name'].lower()]
print(f"Bismark tools: {[t['id'] for t in bismark_tools]}")

# Get tool details
tool = gi.tools.show_tool('bismark')
print(f"Tool ID: {tool['id']}")
print(f"Version: {tool['version']}")
print(f"Inputs: {[i['name'] for i in tool['inputs']]}")
```

#### List Workflows

```python
# List all workflows
workflows = gi.workflows.get_workflows()
for wf in workflows:
    print(f"{wf['name']} (ID: {wf['id']})")

# Get workflow details
workflow = gi.workflows.show_workflow('workflow_id')
print(f"Steps: {len(workflow['steps'])}")
for step_id, step in workflow['steps'].items():
    print(f"  {step['name']} ({step['tool_id']})")
```

#### Run Workflow

```python
# Create history
history = gi.histories.create_history(name='My WGBS Analysis')
history_id = history['id']

# Upload input dataset
file_id = gi.tools.upload_file(
    file_path='/path/to/sample.fastq',
    history_id=history_id
)

# Run workflow
inputs = {
    '0': {  # First step in workflow
        'src': 'hda',
        'id': file_id
    }
}

invocation = gi.workflows.invoke_workflow(
    workflow_id='wgbs_part1',
    history_id=history_id,
    inputs=inputs
)

print(f"Invocation ID: {invocation['id']}")
print(f"State: {invocation['state']}")
```

#### Monitor Workflow Execution

```python
import time

invocation_id = invocation['id']

# Poll for completion
while True:
    inv = gi.invocations.show_invocation(invocation_id)
    
    print(f"State: {inv['state']}")
    if 'progress' in inv:
        print(f"Progress: {inv['progress']:.1%}")
    
    if inv['state'] in ['ok', 'error']:
        break
    
    time.sleep(10)  # Check every 10 seconds

if inv['state'] == 'error':
    print("Workflow failed!")
    print(f"Error: {inv.get('messages', 'Unknown error')}")
else:
    print("Workflow completed successfully!")
    
    # Get output datasets
    for step in inv['steps']:
        print(f"Step {step['id']}: {step['state']}")
        for output in step['outputs']:
            print(f"  Output: {output['name']} (Dataset ID: {output['id']})")
```

#### Access Results

```python
# Get history contents
history_id = 'abc123'
contents = gi.histories.show_history(history_id, contents=True)

for item in contents['contents']:
    if item['state'] == 'ok':
        print(f"{item['name']} ({item['data_type']})")
        print(f"  Size: {item['file_size']:,} bytes")
        print(f"  Download: /api/datasets/{item['id']}/download")

# Download specific dataset
dataset_id = 'dataset_123'
gi.datasets.download_dataset(
    dataset_id=dataset_id,
    file_path='./output.bam'
)
```

#### Custom Script Execution

```python
# Run single tool with custom parameters
job = gi.tools.run_tool(
    tool_id='bismark',
    tool_inputs={
        'input_fastq': {
            'src': 'hda',
            'id': dataset_id
        },
        'reference_genome': 'hg38',
        'multi_hits': 'no',
        'min_coverage': 5,
        'min_identity': 0.8
    },
    history_id=history_id
)

print(f"Job ID: {job['id']}")
print(f"Outputs: {[o['id'] for o in job['outputs']]}")
```

## Advanced: Batch Processing

```python
from bioblend.galaxy import GalaxyInstance
import glob

gi = GalaxyInstance(url='http://localhost:8080', key='YOUR_API_KEY')

# Create project history
history = gi.histories.create_history(name='Batch Analysis')
history_id = history['id']

# Process multiple samples
samples = glob.glob('data/*.fastq')

for sample_file in samples:
    print(f"Processing {sample_file}...")
    
    # Upload
    dataset = gi.tools.upload_file(sample_file, history_id)
    dataset_id = dataset['outputs'][0]['id']
    
    # Run workflow
    invocation = gi.workflows.invoke_workflow(
        workflow_id='wgbs_part1',
        history_id=history_id,
        inputs={'0': {'src': 'hda', 'id': dataset_id}}
    )
    
    # Wait for completion
    while gi.invocations.show_invocation(invocation['id'])['state'] not in ['ok', 'error']:
        time.sleep(10)
    
    print(f"  → Complete!")
```

## Error Handling

```python
from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.client import ConnectionError

try:
    gi = GalaxyInstance(url='http://localhost:8080', key='invalid_key')
    tools = gi.tools.get_tools()
except ConnectionError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Rate Limiting & Pagination

```python
# Get first 100 workflows (paginated)
workflows = gi.workflows.get_workflows(limit=100, offset=0)

# Process large datasets
limit = 50
offset = 0
all_datasets = []

while True:
    datasets = gi.datasets.show_dataset(limit=limit, offset=offset)
    if not datasets:
        break
    all_datasets.extend(datasets)
    offset += limit
```

## Response Formats

All API responses are JSON. Common status codes:

| Code | Meaning |
|------|---------|
| 200 | OK - Successful request |
| 201 | Created - Resource created |
| 204 | No Content - Successful delete |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid/missing API key |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 500 | Server Error - Internal Galaxy error |

## Authentication

All requests require authentication via API key:

```bash
# Header-based (recommended)
curl -H "X-Api-Key: YOUR_API_KEY" http://localhost:8080/api/...

# URL parameter (less secure)
curl http://localhost:8080/api/...?key=YOUR_API_KEY

# HTTP Basic Auth (for key generation only)
curl -u admin:password http://localhost:8080/api/...
```

## CORS & Cross-Origin Requests

For web applications accessing from different domains:

```javascript
// JavaScript fetch example
fetch('http://localhost:8080/api/version', {
  headers: {
    'X-Api-Key': 'YOUR_API_KEY'
  }
})
.then(r => r.json())
.then(data => console.log(data))
```

## Useful Resources

- [Galaxy API Documentation](https://docs.galaxyproject.org/en/master/api/)
- [BioBlend Documentation](https://bioblend.readthedocs.io/)
- [Interactive API Documentation](http://localhost:8080/api/docs) (available when Galaxy is running)
- [Galaxy Workflow Exchange](https://myexperiment.org/) (share workflows)

## Support

- Documentation: https://docs.galaxyproject.org/
- API Issues: https://github.com/galaxyproject/galaxy/issues
- BioBlend Issues: https://github.com/galaxyproject/bioblend/issues
- Help Forum: https://help.galaxyproject.org/
