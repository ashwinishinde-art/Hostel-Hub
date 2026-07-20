#!/usr/bin/env python3
"""
Setup MySQL/MariaDB for Hostel Management System
This script uses mysql_config_editor to create credentials
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a shell command and report result"""
    print(f"\n{description}...", end=" ")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓")
            return True
        else:
            print(f"✗\n  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗\n  Error: {e}")
        return False

def setup_mysql():
    """Setup MySQL database and user"""
    
    print("\n" + "="*70)
    print("HOSTEL MANAGEMENT SYSTEM - MYSQL SETUP")
    print("="*70)
    
    # Step 1: Connect to MySQL and setup database
    print("\n[1/3] Setting up MySQL database...")
    
    # Create SQL commands
    sql_commands = [
        "DROP DATABASE IF EXISTS hostel_management;",
        "CREATE DATABASE hostel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
        "USE hostel_management;",
    ]
    
    sql_string = " ".join(sql_commands)
    
    # Try to execute as root
    cmd = f"mysql -u root -e \"{sql_string}\""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"✗ Could not create database")
        print(f"  Error: {result.stderr}")
        print("\nTrying alternative approach...")
        
        # Try with socket
        cmd = f"mysql -u root --socket=/var/run/mysqld/mysqld.sock -e \"{sql_string}\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"✗ Socket connection also failed")
            return False
    
    print("✓ Database created successfully")
    
    # Step 2: Load schema
    print("\n[2/3] Loading database schema...")
    
    schema_file = "/home/prajwal/Programs/Hostel/config/database.sql"
    if not os.path.exists(schema_file):
        print(f"✗ Schema file not found: {schema_file}")
        return False
    
    cmd = f"mysql -u root hostel_management < {schema_file}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"✗ Could not load schema")
        print(f"  Error: {result.stderr}")
        return False
    
    print("✓ Schema loaded successfully")
    
    # Step 3: Verify
    print("\n[3/3] Verifying database setup...")
    
    cmd = "mysql -u root hostel_management -e \"SHOW TABLES;\" | wc -l"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    try:
        table_count = int(result.stdout.strip())
        if table_count > 0:
            print(f"✓ Database verified with {table_count} tables")
        else:
            print("✗ No tables found")
            return False
    except:
        print("✗ Could not verify tables")
        return False
    
    return True

def test_connection():
    """Test if Python can connect to MySQL"""
    print("\n[4/4] Testing application connection...")
    
    try:
        import MySQLdb
        
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='hostel_management',
            charset='utf8mb4',
            cursorclass=MySQLdb.cursors.DictCursor
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        
        print(f"✓ Application can connect to MySQL")
        print(f"  Found {result['count']} test users in database")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Application connection test failed: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "="*70)
    print("MYSQL SETUP FOR HOSTEL MANAGEMENT SYSTEM")
    print("="*70)
    
    # Setup database
    if not setup_mysql():
        print("\n✗ Database setup failed")
        sys.exit(1)
    
    # Test connection
    if not test_connection():
        print("\n✗ Connection test failed")
        print("  But database setup was successful")
        sys.exit(1)
    
    # Success!
    print("\n" + "="*70)
    print("✓ MYSQL SETUP COMPLETE!")
    print("="*70)
    print("\n📋 Next Steps:")
    print("   1. python app.py         (Start Flask application)")
    print("   2. Visit: http://10.252.129.72:5000")
    print("   3. Login with:")
    print("      - Admin: admin / admin123")
    print("      - Student: prajwal / admin123")
    print("      - Warden: warden / admin123")
    print("\n" + "="*70 + "\n")
    
    sys.exit(0)
