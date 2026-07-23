#!/bin/bash

# Try to start MariaDB using sudo with NOPASSWD (if configured)
# Or try to connect to test if it's already running

echo "Attempting to start MariaDB..."

# Test if MariaDB is already running
mysql -u root -e "SELECT 1" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ MariaDB is already running"
    exit 0
fi

# Try using sudo to start
echo "MariaDB not running. Attempting to start with sudo..."
sudo systemctl start mariadb

# Test again
sleep 2
mysql -u root -e "SELECT 1" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ MariaDB started successfully"
    exit 0
else
    echo "✗ Failed to start MariaDB"
    echo "You may need to run: sudo systemctl start mariadb"
    exit 1
fi
