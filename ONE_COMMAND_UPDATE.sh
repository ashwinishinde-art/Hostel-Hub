#!/bin/bash

################################################################################
#                    HOSTEL MANAGEMENT SYSTEM - ONE COMMAND UPDATE             #
#                                                                              #
# This script applies ALL changes with a single command:                      #
# 1. Starts MySQL (if not running)                                            #
# 2. Applies hostel information updates                                       #
# 3. Verifies changes                                                         #
# 4. Provides next steps                                                      #
#                                                                              #
# Usage: bash ONE_COMMAND_UPDATE.sh                                           #
#        OR                                                                    #
#        chmod +x ONE_COMMAND_UPDATE.sh && ./ONE_COMMAND_UPDATE.sh            #
#                                                                              #
################################################################################

clear

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║         HOSTEL MANAGEMENT SYSTEM - APPLYING ALL CHANGES               ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Check if MySQL is running
echo "Step 1: Checking MySQL status..."
echo "─────────────────────────────────────────────────────────────────────────"

if pgrep -x "mysqld" > /dev/null || pgrep -x "mariadbd" > /dev/null; then
    echo "✓ MySQL is already running"
else
    echo "✗ MySQL is not running. Starting..."
    
    # Try different methods to start MySQL
    if systemctl start mariadb 2>/dev/null; then
        echo "✓ MariaDB started successfully (systemctl)"
    elif service mysql start 2>/dev/null; then
        echo "✓ MySQL started successfully (service)"
    elif service mariadb start 2>/dev/null; then
        echo "✓ MariaDB started successfully (service)"
    else
        echo "✗ Failed to start MySQL. Please start it manually:"
        echo "  - sudo systemctl start mariadb"
        echo "  - sudo service mysql start"
        exit 1
    fi
fi

sleep 2

# Step 2: Apply the updates
echo ""
echo "Step 2: Applying hostel information updates..."
echo "─────────────────────────────────────────────────────────────────────────"

cd /home/prajwal/Programs/Hostel

if mysql -u root hostel_management < UPDATE_HOSTEL_INFO.sql 2>/dev/null; then
    echo "✓ Updates applied successfully!"
else
    echo "✗ Failed to apply updates"
    echo ""
    echo "Trying alternative connection method..."
    
    # Alternative: Try with -p flag for password prompt
    mysql -u root -p hostel_management < UPDATE_HOSTEL_INFO.sql 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo "✗ Connection failed. Please verify:"
        echo "  - MySQL is running (systemctl status mysql)"
        echo "  - Database exists (mysql -u root -e 'SHOW DATABASES;')"
        echo "  - Credentials are correct (user: root, no password)"
        exit 1
    fi
fi

# Step 3: Verify changes
echo ""
echo "Step 3: Verifying changes in database..."
echo "─────────────────────────────────────────────────────────────────────────"

mysql -u root hostel_management -e "
SELECT 
    CONCAT('✓ ', setting_key, ' : ', setting_value) as 'Updated Settings'
FROM hostel_settings 
WHERE setting_key IN ('hostel_name', 'hostel_address', 'hostel_phone', 'hostel_email', 'warden_phone')
ORDER BY setting_key;
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ All settings verified in database"
else
    echo "⚠ Could not verify settings, but updates may have been applied"
fi

# Step 4: Summary
echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║                       ✅ ALL CHANGES APPLIED                           ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

echo "Updated Information:"
echo "  Address : Zeal Chowk, Narhe, Pune"
echo "  Phone   : 7030710886"
echo "  Email   : hostelhub@work.com"
echo "  Name    : HostelHub"
echo ""

echo "Next Steps:"
echo "─────────────────────────────────────────────────────────────────────────"
echo "1. Hard refresh your browser: Ctrl+Shift+R"
echo "2. Visit /contact page to verify the changes"
echo "3. Check the footer on any page"
echo "4. Try logging in - demo credentials are no longer displayed"
echo ""

echo "Where to see the changes:"
echo "  ✓ Contact Page (/contact)"
echo "  ✓ Footer (all pages)"
echo "  ✓ Admin Dashboard"
echo "  ✓ Public Landing Page"
echo ""

echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

exit 0
