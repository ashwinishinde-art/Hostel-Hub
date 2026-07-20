#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        HOSTEL MANAGEMENT SYSTEM - COMPLETE SETUP              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Create database
echo "Step 1/3: Creating database..."
mysql -u root -e "DROP DATABASE IF EXISTS hostel_management;" 2>/dev/null
mysql -u root -e "CREATE DATABASE hostel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "✗ Could not create database"
    exit 1
fi
echo "✓ Database created"

# Step 2: Load schema
echo "Step 2/3: Loading database schema..."
mysql -u root hostel_management < /home/prajwal/Programs/Hostel/config/database.sql 2>/dev/null

if [ $? -ne 0 ]; then
    echo "✗ Could not load schema"
    exit 1
fi
echo "✓ Schema loaded"

# Step 3: Verify
echo "Step 3/3: Verifying setup..."
TABLES=$(mysql -u root hostel_management -e "SHOW TABLES;" 2>/dev/null | wc -l)

if [ $TABLES -gt 0 ]; then
    echo "✓ Database verified with tables"
else
    echo "✗ Database verification failed"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "✓ SETUP COMPLETE!"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next: Run Flask application in a NEW terminal:"
echo "  cd /home/prajwal/Programs/Hostel"
echo "  python app.py"
echo ""
echo "Then open: http://10.252.129.72:5000"
echo ""

