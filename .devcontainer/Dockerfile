FROM mcr.microsoft.com/devcontainers/python:3.11

WORKDIR /workspace

# Avoid apt key errors; install Chromium for Selenium + OpenSSH server
RUN rm -f /etc/apt/sources.list.d/yarn.list /etc/apt/sources.list.d/*yarn* 2>/dev/null; \
    apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    chromium \
    chromium-driver \
    openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /run/sshd

# Copy requirements and install Python deps
COPY requirements.txt* ./
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || true

COPY . .

# Start SSH server then keep container running (connect with ssh root@localhost when port 22 is forwarded)
CMD ["sh", "-c", "/usr/sbin/sshd && exec sleep infinity"]
