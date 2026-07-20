#!/bin/bash

echo "════════════════════════════════════════════════════════════════"
echo "🚀 HOSTEL MANAGEMENT SYSTEM - FINAL SETUP"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Step 1: Start MySQL
echo "1️⃣  Starting MySQL Service..."
sudo service mysql start
sleep 3

echo "✅ MySQL Started"
echo ""

# Step 2: Load database schema
echo "2️⃣  Setting Up Database..."
echo "   Creating database and tables..."
sudo mysql -u root < /home/prajwal/Programs/Hostel/config/database.sql

if [ $? -eq 0 ]; then
    echo "✅ Database Setup Complete"
else
    echo "❌ Database setup failed"
    exit 1
fi

echo ""

# Step 3: Verify
echo "3️⃣  Verifying Setup..."
RESULT=$(sudo mysql -u root -e "SELECT COUNT(*) as count FROM hostel_management.users;" 2>&1 | grep -c "5")

if [ $RESULT -gt 0 ]; then
    echo "✅ Verification Successful - 5 users found"
else
    echo "⚠️  Warning: Could not verify users"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ SETUP COMPLETE!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Next Steps:"
echo "1. Open a new terminal"
echo "2. Run: cd /home/prajwal/Programs/Hostel && python app.py"
echo "3. Open browser: http://10.252.129.72:5000"
echo "4. Click Register and create a new student account"
echo ""
echo "Test Credentials:"
echo "  Admin:    admin / admin123"
echo "  Student:  prajwal / admin123"
echo ""
echo "════════════════════════════════════════════════════════════════"

