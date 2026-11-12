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

To run `methylator` with your data, you will typically need to mount your data directory into the container. Replace `/path/to/your/data` with the actual path to your data on your host machine:

```bash
docker run -d -p 8080:80 -v /path/to/your/data:/data methylator-galaxy
```

This starts the Galaxy server in the background and mounts your data directory.

Access Galaxy at `http://localhost:8080`

### Installing Tools

The Methylator tools are configured in `methylator_tool_list.yaml` but need to be installed after the container starts, as the `install-tools` command requires a running Galaxy instance.

**Option 1: Install tools via docker exec (recommended)**

```bash
# Get the container ID
CONTAINER_ID=$(docker ps | grep methylator-galaxy | awk '{print $1}')

# Install tools
docker exec $CONTAINER_ID install-tools /galaxy/tools.yaml
```

**Option 2: Install tools manually via Galaxy UI**

1. Access Galaxy at `http://localhost:8080`
2. Go to Admin panel → Manage tools
3. Import tools from the Tool Shed manually

### Installing Workflows

Once Galaxy is running, you can install the workflows:

```bash
docker exec <container_id> workflow-install \
  --workflow_path /home/galaxy/workflows/ \
  -g http://localhost:8080 \
  -u admin \
  -p admin
```

Replace `admin` with your Galaxy admin password if different.

### Available Workflows

- `wgbs_part1.ga` - WGBS analysis part 1
- `wgbs_part2.ga` - WGBS analysis part 2

### Adding Custom Branding

To add custom branding (logo, welcome page), uncomment these lines in the Dockerfile:
```dockerfile
ADD assets/img/full_logo.png $GALAXY_CONFIG_DIR/web/welcome_image.png
ADD welcome.html $GALAXY_CONFIG_DIR/web/welcome.html
```

Then rebuild the image.

