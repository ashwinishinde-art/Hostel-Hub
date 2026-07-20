#!/bin/bash

# Hostel Management System - MySQL Startup Script

echo "🚀 Starting Hostel Management System MySQL..."
echo "=================================================="

# Check if MySQL is already running
if ps aux | grep -q '[m]ysqld'; then
    echo "✓ MySQL is already running"
else
    echo "Starting MySQL service..."
    
    # Try different methods to start MySQL
    if command -v service &> /dev/null; then
        echo "Attempting: sudo service mysql start"
        sudo service mysql start
    elif command -v systemctl &> /dev/null; then
        echo "Attempting: sudo systemctl start mysql"
        sudo systemctl start mysql
    elif command -v /etc/init.d/mysql &> /dev/null; then
        echo "Attempting: sudo /etc/init.d/mysql start"
        sudo /etc/init.d/mysql start
    else
        echo "❌ Could not find MySQL start command"
        echo "Please start MySQL manually and try again"
        exit 1
    fi
fi

# Verify MySQL is running
sleep 2
if ps aux | grep -q '[m]ysqld'; then
    echo "✓ MySQL is now running"
    echo ""
    echo "To start the Flask application, run:"
    echo "  python3 app.py"
else
    echo "❌ Failed to start MySQL"
    echo "Please check your MySQL installation and try again"
    exit 1
fi
