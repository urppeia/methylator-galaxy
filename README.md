# methylator-galaxy
Galaxy related code for Methylator

## Docker Image

This repository includes a `Dockerfile` to create a Docker image for `methylator`. This allows for a consistent and isolated environment to run `methylator` and its associated tools.

### Building the Docker Image

To build the Docker image, navigate to the root of this repository and run the following command:

```bash
docker build -t methylator-galaxy .
```

This command will build an image named `methylator-galaxy` with the tag `latest`.

### Running the Docker Image

To run Galaxy with Methylator tools, use:

```bash
docker run -d -p 8080:80 --name methylator methylator-galaxy
```

This starts the Galaxy server in the background:
- Access Galaxy at `http://localhost:8080`
- Default admin user: `admin`
- Default admin password: `password`

To mount your data directory:

```bash
docker run -d -p 8080:80 -v /path/to/your/data:/data --name methylator methylator-galaxy
```

### Installing Tools

The Methylator tools are configured in `methylator_tool_list.yaml` and need to be installed after the container starts.

**Option 1: Using the Python installation script (recommended)**

```bash
# Wait for Galaxy to fully start (first-run may take 2-5 minutes)
docker exec methylator bash -c "
  echo 'Waiting for Galaxy to be ready...'
  for i in {1..60}; do
    if curl -s http://localhost:8080/api/version > /dev/null 2>&1; then
      echo '✓ Galaxy is ready!'
      break
    fi
    sleep 5
  done
"

# Install tools using the Python script
docker exec methylator python3 /galaxy/install_methylator_tools.py \
  /galaxy/tools.yaml \
  http://localhost:8080 \
  admin
```

**Option 2: Manual installation via Galaxy UI**

1. Access Galaxy at `http://localhost:8080`
2. Go to Admin (top menu) → Manage tools
3. Search for and install each tool from the Tool Shed individually

**Option 3: Using ephemeris command-line (if tools are installed)**

```bash
docker exec methylator bash -c "
  # First, ensure Galaxy is running
  sleep 30
  
  # Then install tools
  install-tools /galaxy/tools.yaml
"
```

Note: This method can take 15-30+ minutes depending on tool size and network speed.

### Installing Workflows

Once Galaxy is running and tools are installed, you can import the workflows:

```bash
CONTAINER_ID=$(docker ps | grep methylator-galaxy | awk '{print $1}')

docker exec $CONTAINER_ID bash -c "
  workflow-install \
    --workflow_path /home/galaxy/workflows/ \
    -g http://localhost:8080 \
    -u admin \
    -p password
"
```

### Available Workflows

- `wgbs_part1.ga` - WGBS analysis part 1
- `wgbs_part2.ga` - WGBS analysis part 2

### Troubleshooting

**Galaxy is slow to start on first run**
- The first startup can take 2-5 minutes as Galaxy initializes the database
- Use `docker logs methylator` to monitor startup progress

**"Connection refused" when trying to install tools**
- Make sure Galaxy is fully started: `docker exec methylator curl http://localhost:8080/api/version`
- Wait a few more seconds and retry

**Tools installation is very slow**
- Tool installation can take 15-30 minutes or more
- Don't interrupt the process; let it run to completion
- Use `docker logs methylator` to monitor progress

**Container won't start or exits immediately**
- Check logs: `docker logs methylator`
- Ensure port 8080 is not already in use
- Try removing and recreating the container

### Adding Custom Branding

To add custom branding (logo, welcome page), uncomment these lines in the Dockerfile:
```dockerfile
ADD assets/img/full_logo.png $GALAXY_CONFIG_DIR/web/welcome_image.png
ADD welcome.html $GALAXY_CONFIG_DIR/web/welcome.html
```

Then rebuild the image with `docker build -t methylator-galaxy .`

### References

- [Galaxy Project](https://galaxyproject.org/)
- [BioBlend Documentation](https://bioblend.readthedocs.io/)
- [Ephemeris Tool Installation](https://ephemeris.readthedocs.io/)

