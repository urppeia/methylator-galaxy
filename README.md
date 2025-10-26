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
docker run -v /path/to/your/data:/data methylator-galaxy methylator <your_methylator_commands_here>
```

Inside the container, your data will be accessible under the `/data` directory.

