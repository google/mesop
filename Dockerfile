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

# Build the Optic CLI
RUN bazel build //optic:cli

# Run Optic CLI (this will fail because it's missing required flag path)
# But if we don't do this then when we run bazel-bin/optic/cli, we get error:
# ln: /cli.venv/include: No such file or directory
RUN bazel run //optic:cli || true