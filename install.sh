#!/bin/sh

REPO_URL="https://github.com/schech1/remoteio.git"
REMOTEIO_DIR="remoteio"
INSTALL_DIR="/usr/share/remoteio"
SERVICE_DIR="/etc/systemd/system"
SCRIPT_USER="1000"
SCRIPT_GROUP="100"

echo "Cloning repository from GitHub..."
git clone "$REPO_URL"

echo "Moving files to $INSTALL_DIR."
sudo mkdir -p "$INSTALL_DIR"
sudo cp -f "$REMOTEIO_DIR/remoteio_server.py" "$INSTALL_DIR/remoteio_server.py"
sudo cp -f "$REMOTEIO_DIR/remoteio_client.py" "$INSTALL_DIR/remoteio_client.py"
echo "Moving service file to $SERVICE_DIR."
sudo cp -f "$REMOTEIO_DIR/remoteiod.service" "$SERVICE_DIR/remoteiod.service"
sudo chown "$SCRIPT_USER":"$SCRIPT_GROUP" "$INSTALL_DIR/remoteio_server.py" "$INSTALL_DIR/remoteio_client.py"

echo "Files moved successfully."
sudo rm -rf "$REMOTEIO_DIR"
echo "remoteio directory deleted"

echo "Reloading systemd daemon and enabling the service..."
sudo systemctl daemon-reload

sudo systemctl enable remoteiod
sudo systemctl restart remoteiod

echo "remoteiod service installed and restarted."
