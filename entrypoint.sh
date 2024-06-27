#!/bin/sh

# Remove potential lock files that could prevent Xvfb from starting
rm -f /tmp/.X0-lock /tmp/.X11-unix/X0

# Start the virtual framebuffer in the background, suppress output
Xvfb :0 -screen 0 1280x720x16 >/dev/null 2>&1 &

# Start the window manager, suppress output
fluxbox -display :0 >/dev/null 2>&1 &

# Start the VNC server, suppress output
x11vnc -display :0 -forever -usepw  >/dev/null 2>&1 &

# Initialize a counter for the loop
counter=0

# Check for Xvfb readiness with a maximum wait time of 10 seconds
while ! xdpyinfo -display :0 >/dev/null 2>&1; do
    sleep 1
    counter=$((counter+1))
    if [ "$counter" -ge 15 ]; then
        echo "Timeout waiting for Xvfb to be ready."
        break
    fi
done

# Execute the command passed to the docker run (such as running a Python script)
exec "$@"