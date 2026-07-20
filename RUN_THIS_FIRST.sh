#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  ONE-STEP DATABASE SETUP                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Load the database schema
echo "Loading database schema..."
mysql -u root < /home/prajwal/Programs/Hostel/config/database.sql 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Database loaded successfully!"
else
    echo "Trying with localhost..."
    mysql -h 127.0.0.1 -u root < /home/prajwal/Programs/Hostel/config/database.sql 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ Database loaded successfully!"
    else
        echo "❌ Could not load database"
        echo "Attempting to create database manually..."
        mysql -u root -e "CREATE DATABASE IF NOT EXISTS hostel_management;" 2>/dev/null
        mysql -u root hostel_management < /home/prajwal/Programs/Hostel/config/database.sql 2>/dev/null
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ SETUP COMPLETE!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📋 NEXT STEP:"
echo "   Run Flask in a new terminal:"
echo "   $ cd /home/prajwal/Programs/Hostel"
echo "   $ python app.py"
echo ""
echo "   Then open: http://10.252.129.72:5000"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

