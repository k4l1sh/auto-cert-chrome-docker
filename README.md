# Containerized Undetected Chromedriver with Automated Certificate Import

This repository provides a boilerplate for a containerized application of Undetected Chromedriver, which loads a certificate into Chrome and configures it for automatic selection. This allows the certificate to be used seamlessly in Chrome browser automation.

## Installation

To build the Docker image, run the following command:

```bash
docker build -t auto_cert_chrome:latest .
```

## Usage

```bash
docker run -p 5900:5900 --rm auto_cert_chrome:latest python example.py -c example_certificate -p 123123
```

The default password for the [certificate](./certs) used as example is 123123.

## Accessing with VNC

To check the container running, you can access it via VNC. Use a VNC viewer to connect to the container.

1. Open your VNC viewer
2. Connect to `localhost:5900`
3. When prompted, enter the default password `123123` (it is recommended to change this password inside the Dockerfile)

You will be able to see the Chrome browser running inside the container, allowing you to manually inspect and verify the certificate installation.

![VNC viewer](https://i.imgur.com/SbX0jR4.png)

## Configuring for Development

The `example.py` script automates the process of loading a certificate into the Chrome browser. It installs the certificate into the NSS database, creates a Chrome profile and downloads folder, and verifies the installation by navigating to `chrome://settings/certificates`.

To run the script with a different certificate or password, use the following command:

```bash
docker run -p 5900:5900 --rm auto_cert_chrome:latest python example.py -c your_certificate_name -p your_certificate_password
```

Ensure that your certificate file is placed in the certs directory and named appropriately.