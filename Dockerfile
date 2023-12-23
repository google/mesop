# Use the latest Ubuntu image as the base
FROM amd64/ubuntu:latest

# Install various packages
RUN apt-get update && \
    apt-get install -y git wget vim build-essential

# Clone the Mesop repository
RUN git clone https://github.com/google/mesop.git

# Set the working directory to the cloned repository
WORKDIR /mesop

# Download and install Bazelisk
RUN wget https://github.com/bazelbuild/bazelisk/releases/latest/download/bazelisk-linux-amd64 && \
    chmod +x bazelisk-linux-amd64 && \
    mv bazelisk-linux-amd64 /usr/local/bin/bazel

# Create a new user and group
RUN groupadd -r myuser && useradd -r -g myuser myuser && mkdir -p /home/myuser && chown myuser:myuser /home/myuser && chown -R myuser /mesop
USER myuser

# Expose port 32123
EXPOSE 32123

# Make sure Bazel is working
RUN bazel version

# Build the Mesop CLI
RUN bazel build //mesop/cli

# Run Mesop CLI (this will fail because it's missing required flag path)
# But if we don't do this then when we run bazel-bin/mesop/cli, we get error:
# ln: /cli.venv/include: No such file or directory
RUN bazel run //mesop/cli || true

# Remove node_modules to reduce container image size
# because it's huge (2GB+) and we don't need it at serving time
RUN rm -rf node_modules
