#!/usr/bin/env python3
"""
Hostel Management System - Pre-flight Check
Verifies all dependencies before starting the application
"""

import sys
import subprocess
import MySQLdb
from pathlib import Path

def print_status(message, status=None):
    """Print formatted status message"""
    if status is None:
        print(f"\n{message}")
    elif status is True:
        print(f"✓ {message}")
    elif status is False:
        print(f"✗ {message}")
    else:
        print(f"⚠ {message}")

def check_python_dependencies():
    """Check if required Python packages are installed"""
    print_status("Checking Python Dependencies")
    required_packages = {
        'flask': 'Flask',
        'flask_login': 'Flask-Login',
        'MySQLdb': 'MySQLdb',
        'bcrypt': 'bcrypt',
    }
    
    all_good = True
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print_status(f"{package_name}", True)
        except ImportError:
            print_status(f"{package_name} - Not installed", False)
            all_good = False
    
    return all_good

def check_mysql_running():
    """Check if MySQL daemon is running"""
    print_status("Checking MySQL Status")
    try:
        result = subprocess.run(['pgrep', '-f', 'mysqld'], capture_output=True)
        if result.returncode == 0:
            print_status("MySQL daemon is running", True)
            return True
        else:
            print_status("MySQL daemon is NOT running", False)
            return False
    except Exception as e:
        print_status(f"Could not check MySQL status: {e}", None)
        return False

def check_mysql_connection():
    """Check if we can connect to MySQL"""
    print_status("Checking MySQL Connection")
    try:
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            port=3306
        )
        conn.close()
        print_status("Connected to MySQL server", True)
        return True
    except MySQLdb.Error as e:
        print_status(f"Cannot connect to MySQL: {e.args[1] if len(e.args) > 1 else e}", False)
        return False

def check_database_exists():
    """Check if hostel_management database exists"""
    print_status("Checking Database")
    try:
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            port=3306
        )
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES LIKE 'hostel_management'")
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        
        if exists:
            print_status("Database 'hostel_management' exists", True)
            return True
        else:
            print_status("Database 'hostel_management' NOT found", False)
            return False
    except Exception as e:
        print_status(f"Error checking database: {e}", False)
        return False

def check_database_tables():
    """Check if main tables exist"""
    print_status("Checking Database Tables")
    try:
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='hostel_management',
            port=3306
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = 'hostel_management'
        """)
        table_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        if table_count > 0:
            print_status(f"Found {table_count} tables", True)
            return True
        else:
            print_status("No tables found in database", False)
            return False
    except Exception as e:
        print_status(f"Error checking tables: {e}", False)
        return False

def check_user_data():
    """Check if sample users exist"""
    print_status("Checking User Data")
    try:
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='hostel_management',
            port=3306,
            cursorclass=MySQLdb.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        user_count = result['count'] if result else 0
        cursor.close()
        conn.close()
        
        if user_count > 0:
            print_status(f"Found {user_count} users in database", True)
            return True
        else:
            print_status("No users found in database", False)
            return False
    except Exception as e:
        print_status(f"Error checking users: {e}", False)
        return False

def check_config_files():
    """Check if required config files exist"""
    print_status("Checking Configuration Files")
    required_files = [
        'app.py',
        'config/config.py',
        'config/database.py',
        'templates/login.html',
    ]
    
    all_good = True
    for file_path in required_files:
        if Path(file_path).exists():
            print_status(f"{file_path}", True)
        else:
            print_status(f"{file_path} - NOT FOUND", False)
            all_good = False
    
    return all_good

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("🔍 Hostel Management System - Pre-flight Check")
    print("="*60)
    
    checks = [
        ("Python Dependencies", check_python_dependencies),
        ("Configuration Files", check_config_files),
        ("MySQL Running", check_mysql_running),
        ("MySQL Connection", check_mysql_connection),
        ("Database Exists", check_database_exists),
        ("Database Tables", check_database_tables),
        ("User Data", check_user_data),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print_status(f"Check '{check_name}' failed with error: {e}", False)
            results[check_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    failed_checks = [name for name, result in results.items() if not result]
    
    if not failed_checks:
        print("✓ All checks passed! Ready to start the application.")
        print("\nRun: python3 app.py")
        return 0
    else:
        print(f"✗ {len(failed_checks)} check(s) failed:")
        for check in failed_checks:
            print(f"  - {check}")
        print("\nPlease fix the issues above before starting the application.")
        print("\nFor help, see: LOGIN_TROUBLESHOOTING.md")
        return 1

if __name__ == '__main__':
    sys.exit(main())
