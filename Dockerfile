# Use the latest Ubuntu image as the base
FROM amd64/ubuntu:latest

# Install various packages
RUN apt-get update && \
    apt-get install -y git wget vim build-essential

# Clone the Optic repository
RUN git clone https://github.com/google/optic.git

# Set the working directory to the cloned repository
WORKDIR /optic

# Download and install Bazelisk
RUN wget https://github.com/bazelbuild/bazelisk/releases/latest/download/bazelisk-linux-amd64 && \
    chmod +x bazelisk-linux-amd64 && \
    mv bazelisk-linux-amd64 /usr/local/bin/bazel

# Create a new user and group
RUN groupadd -r myuser && useradd -r -g myuser myuser && mkdir -p /home/myuser && chown myuser:myuser /home/myuser && chown -R myuser /optic
USER myuser

# Expose port 8080
EXPOSE 8080

# Make sure Bazel is working
RUN bazel version

# Trim out Angular section to avoid NPM dependencies which take a long time to install
RUN sed -i '/# Angular-related/,/# Optic/d' WORKSPACE

# Run the following Bazel command manually inside the container
# after creating the image because it takes forever during the build step.
# Afterwards, commit the container into an image and deploy that image.

# RUN bazel build //optic:cli
