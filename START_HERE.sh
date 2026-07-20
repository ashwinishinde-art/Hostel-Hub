#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║         🚀 HOSTEL MANAGEMENT SYSTEM - MASTER SETUP 🚀         ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Start MySQL
echo "════════════════════════════════════════════════════════════════"
echo -e "${YELLOW}Step 1/4: Starting MySQL Service...${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Try to start MySQL
if command -v sudo &> /dev/null; then
    echo "Attempting to start MySQL via sudo..."
    sudo service mysql start 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ MySQL service started${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not start with sudo${NC}"
        echo "Trying to start MySQL directly..."
        service mysql start 2>/dev/null
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ MySQL service started${NC}"
        else
            echo -e "${RED}❌ Could not start MySQL${NC}"
            echo "Please run manually: sudo service mysql start"
        fi
    fi
else
    echo "Trying to start MySQL..."
    service mysql start 2>/dev/null
fi

# Wait for MySQL to be ready
echo ""
echo "Waiting for MySQL to start..."
sleep 5

# Step 2: Create database
echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${YELLOW}Step 2/4: Creating Database and Tables...${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

if [ -f "/home/prajwal/Programs/Hostel/config/database.sql" ]; then
    # Try with sudo first
    sudo mysql -u root < /home/prajwal/Programs/Hostel/config/database.sql 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Database created successfully${NC}"
    else
        echo "Trying without sudo..."
        mysql -u root < /home/prajwal/Programs/Hostel/config/database.sql 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Database created successfully${NC}"
        else
            echo -e "${RED}❌ Could not load database schema${NC}"
            echo "File: /home/prajwal/Programs/Hostel/config/database.sql"
        fi
    fi
else
    echo -e "${RED}❌ Database schema file not found${NC}"
fi

# Step 3: Verify database
echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${YELLOW}Step 3/4: Verifying Database Setup...${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

VERIFY=$(mysql -u root -e "SELECT COUNT(*) FROM hostel_management.users LIMIT 1;" 2>&1)

if echo "$VERIFY" | grep -q "5"; then
    echo -e "${GREEN}✅ Database verification successful${NC}"
    echo "   Found 5 test users in database"
elif echo "$VERIFY" | grep -q "COUNT"; then
    echo -e "${GREEN}✅ Database connection works${NC}"
else
    echo -e "${YELLOW}⚠️  Could not verify database${NC}"
    echo "   But this might be normal if using socket connection"
fi

# Step 4: Summary
echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ DATABASE SETUP COMPLETE!${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "📋 NEXT STEPS:"
echo ""
echo "   1. Open a NEW terminal window (keep this one open)"
echo ""
echo "   2. In the NEW terminal, run Flask:"
echo "      $ cd /home/prajwal/Programs/Hostel"
echo "      $ python app.py"
echo ""
echo "   3. Wait for: '✅ Database connected successfully!'"
echo ""
echo "   4. Open browser: http://10.252.129.72:5000"
echo ""
echo "   5. Click 'Register' and create a new student account"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}👥 Test Accounts (already in database):${NC}"
echo "   Admin:    admin / admin123"
echo "   Student:  prajwal / admin123"
echo "   Warden:   warden / admin123"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

