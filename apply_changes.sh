#!/bin/bash

echo "=========================================="
echo "APPLYING HOSTEL INFORMATION UPDATES"
echo "=========================================="
echo ""

# Check if MySQL is running
echo "Checking MySQL status..."
if ! pgrep -x "mysqld" > /dev/null && ! pgrep -x "mariadbd" > /dev/null; then
    echo "MySQL is not running. Attempting to start..."
    systemctl start mariadb 2>/dev/null || service mysql start 2>/dev/null || \
    mysqld_safe --skip-grant-tables &
    sleep 3
    echo "MySQL started"
else
    echo "MySQL is already running"
fi

echo ""
echo "Applying SQL updates..."
echo ""

# Apply the SQL updates
mysql -u root hostel_management < /home/prajwal/Programs/Hostel/UPDATE_HOSTEL_INFO.sql 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ UPDATES APPLIED SUCCESSFULLY"
    echo "=========================================="
    echo ""
    echo "Changes made:"
    echo "- Address: Zeal Chowk, Narhe, Pune"
    echo "- Phone: 7030710886"
    echo "- Email: hostelhub@work.com"
    echo ""
    echo "To see the changes:"
    echo "1. Hard refresh browser: Ctrl+Shift+R"
    echo "2. Visit /contact page"
    echo "3. Check footer on any page"
    echo "=========================================="
else
    echo ""
    echo "❌ ERROR: Failed to apply updates"
    echo "Make sure MySQL is properly installed and running"
fi
