#!/bin/bash

# This script updates the password hashes in your existing database
# Run this AFTER starting MySQL

echo "Hostel Management System - Database Password Hash Update"
echo "========================================================="
echo ""
echo "This script will update all user passwords to the correct bcrypt hashes"
echo "for the password: admin123"
echo ""
echo "Updating database..."
echo ""

mysql -u root -D hostel_management << EOF
UPDATE users SET password_hash = '\$2b\$12\$V6W/ACX8nu4cn2NB6yFLxOt50FONybRDJvqcoG.HteYCk9V2nk6aK' WHERE username IN ('admin', 'warden', 'prajwal', 'rajdeep', 'rutuja');
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Database updated successfully!"
    echo ""
    echo "You can now login with:"
    echo "  - Username: admin, prajwal, rajdeep, rutuja, or warden"
    echo "  - Password: admin123"
else
    echo ""
    echo "✗ Error updating database. Make sure MySQL is running:"
    echo "  sudo service mysql start"
fi
