# Quick Start Guide - Methylator Galaxy

## TL;DR - Get running in 5 minutes

### 1. Build the image
```bash
docker build -t methylator-galaxy .
```

### 2. Run the container
```bash
docker run -d -p 8080:80 --name methylator methylator-galaxy
```

### 3. Wait for Galaxy to start (2-5 minutes on first run)
```bash
docker exec methylator bash -c "
  for i in {1..60}; do
    if curl -s http://localhost:8080/api/version > /dev/null 2>&1; then
      echo '✓ Galaxy is ready!'
      break
    fi
    echo "Waiting... ($i/60)"
    sleep 5
  done
"
```

### 4. Install Methylator tools
```bash
docker exec methylator python3 /galaxy/install_methylator_tools.py \
  /galaxy/tools.yaml \
  http://localhost:8080 \
  admin
```

### 5. Access Galaxy
Open your browser: http://localhost:8080
- User: `admin`
- Password: `password`

---

## Full Installation Steps

### Prerequisites
- Docker (version 20+)
- At least 4GB free disk space
- ~30-60 minutes for full tool installation

### Build

```bash
cd methylator-galaxy
docker build -t methylator-galaxy .
```

**Expected output:**
```
#12 naming to docker.io/library/methylator-galaxy:latest done
#12 DONE 0.1s
```

### Run

```bash
docker run -d \
  -p 8080:80 \
  --name methylator \
  methylator-galaxy
```

**Check status:**
```bash
docker ps | grep methylator
```

### Install Tools

**Option A: Python Script (Recommended)**
```bash
docker exec methylator python3 /galaxy/install_methylator_tools.py \
  /galaxy/tools.yaml \
  http://localhost:8080 \
  admin
```

**Option B: Via Galaxy Web UI**
1. Go to `http://localhost:8080`
2. Click `Admin` (top menu)
3. Click `Manage tools`
4. Search for and install tools manually

**Option C: Ephemeris (Takes longer, ~30 min)**
```bash
docker exec methylator bash -c "
  sleep 30  # Let Galaxy settle
  install-tools /galaxy/tools.yaml
"
```

### Verify Installation

Check if tools are installed:
```bash
curl -s http://localhost:8080/api/tools | grep -o '"name":"[^"]*' | head -10
```

---

## Useful Commands

### View logs
```bash
docker logs methylator -f
```

### Stop container
```bash
docker stop methylator
```

### Restart container
```bash
docker start methylator
```

### Remove container
```bash
docker rm methylator
```

### Access container shell
```bash
docker exec -it methylator /bin/bash
```

### Mount data directory
```bash
docker run -d \
  -p 8080:80 \
  -v /path/to/your/data:/data \
  --name methylator \
  methylator-galaxy
```

### Check Galaxy logs from container
```bash
docker exec methylator tail -f /galaxy/main.log
```

---

## Troubleshooting

### "Connection refused" errors
**Problem:** Can't connect to Galaxy when installing tools  
**Solution:** Galaxy takes time to start on first run. Wait 2-5 minutes.
```bash
# Keep checking until it responds
watch -n 2 'curl -s http://localhost:8080/api/version && echo "Ready!" || echo "Waiting..."'
```

### Port 8080 already in use
**Problem:** `Error response from daemon: driver failed programming external connectivity on endpoint`  
**Solution:** Use a different port
```bash
docker run -d -p 9000:80 --name methylator methylator-galaxy
# Access at http://localhost:9000
```

### Tool installation hangs
**Problem:** Installation seems to hang or shows no progress  
**Solution:** This is normal! Tool installation can take 15-30 minutes. Monitor with:
```bash
docker logs methylator -f
```

### Container exits immediately
**Problem:** Container starts but exits right away  
**Solution:** Check logs for errors
```bash
docker logs methylator
```
Common causes: port conflict, disk space, permissions

### Tools not appearing in Galaxy
**Problem:** Installed tools but can't see them in Galaxy UI  
**Solution:** 
1. Refresh the Galaxy page (Ctrl+F5 or Cmd+Shift+R)
2. Check installation logs: `docker logs methylator`
3. Restart Galaxy: `docker restart methylator`

---

## Next Steps

### Import Workflows
```bash
docker exec methylator bash -c "
  workflow-install \
    --workflow_path /home/galaxy/workflows/ \
    -g http://localhost:8080 \
    -u admin \
    -p password
"
```

### Run an Example Analysis
1. Go to Galaxy UI (http://localhost:8080)
2. Create a new history
3. Upload or import data
4. Run a tool from the Methylator section

### Customize Galaxy
- Edit Galaxy config: `docker exec -it methylator nano /galaxy/config/galaxy.yml`
- Restart: `docker restart methylator`

### Backup Data
```bash
# Backup Galaxy database and data
docker cp methylator:/export ./backup-methylator
```

---

## More Help

- **Galaxy Documentation:** https://docs.galaxyproject.org/
- **Methylator Repository:** https://github.com/urppeia/Methylator
- **BioBlend API:** https://bioblend.readthedocs.io/
- **Tool Shed:** https://toolshed.g2.bx.psu.edu/

---

## Version Info
- Base Image: Galaxy 24.1 (quay.io/bgruening/galaxy:24.1)
- Python: 3.10
- Maintained by: Deepak K. Tanwar (dktanwar@hotmail.com)
