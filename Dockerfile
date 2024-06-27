FROM python:3.10-alpine

# Expose VNC port to access the GUI
EXPOSE 5900

# Copy the Python dependencies file
COPY ./requirements.txt /tmp/requirements.txt

# Install necessary packages including the community repository for xorg-xdpyinfo
RUN apk update && apk upgrade && \
    apk add --no-cache --virtual .build-deps \
    alpine-sdk \
    curl \
    wget \
    unzip \
    gnupg && \
    apk add --no-cache \
    xvfb \
    x11vnc \
    fluxbox \
    xterm \
    libffi-dev \
    openssl-dev \
    openssl \
    zlib-dev \
    bzip2-dev \
    readline-dev \
    sqlite-dev \
    git \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    chromium \
    chromium-chromedriver \
    xdpyinfo \
    nss-tools

# Set up VNC server password
RUN mkdir ~/.vnc && \
    x11vnc -storepasswd 123123 ~/.vnc/passwd

# Create the NSS database
RUN mkdir -p /root/.pki/nssdb && \
    modutil -create -dbdir sql:/root/.pki/nssdb -force

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Copy scripts and certs into the container
COPY ./scripts /scripts
COPY ./certs /certs

# Add the policy setup in Dockerfile
RUN mkdir -p /etc/chromium/policies/managed
COPY ./policies /etc/chromium/policies/managed

# Set the work directory to where scripts are stored
WORKDIR /scripts

# Make scripts executable
RUN chmod +x *.py

# Environment variables
ENV PATH="/scripts:$PATH"
ENV DISPLAY=:0

# Delete temporary dependencies to reduce image size
RUN apk del .build-deps

# Entry point script to start the X server and services
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
