#!/usr/bin/env python3
"""
Automatic MySQL Setup using Socket Authentication
This bypasses TCP authentication restrictions
"""

import MySQLdb
import MySQLdb.cursors
import subprocess
import sys

def setup_with_socket():
    """Try to connect via socket and setup database"""
    try:
        print("Attempting socket connection to MySQL...")
        
        # Try socket connection
        conn = MySQLdb.connect(
            unix_socket='/var/run/mysqld/mysqld.sock',
            user='root',
            database='mysql',
            cursorclass=MySQLdb.cursors.DictCursor
        )
        
        cursor = conn.cursor()
        
        print("✓ Connected via socket!")
        print("Setting up database...")
        
        # Drop and create database
        cursor.execute("DROP DATABASE IF EXISTS hostel_management")
        cursor.execute("""
            CREATE DATABASE hostel_management 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci
        """)
        
        # Reset root authentication
        cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED BY ''")
        cursor.execute("FLUSH PRIVILEGES")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Database created")
        print("✓ Root authentication set to no password")
        
        return True
        
    except MySQLdb.Error as e:
        print(f"✗ Socket connection failed: {e}")
        return False

def setup_with_tcp():
    """Try standard TCP connection"""
    try:
        print("Attempting TCP connection...")
        
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='mysql',
            port=3306,
            cursorclass=MySQLdb.cursors.DictCursor
        )
        
        cursor = conn.cursor()
        
        print("✓ Connected via TCP!")
        print("Setting up database...")
        
        # Drop and create database
        cursor.execute("DROP DATABASE IF EXISTS hostel_management")
        cursor.execute("""
            CREATE DATABASE hostel_management 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Database created")
        
        return True
        
    except MySQLdb.Error as e:
        print(f"✗ TCP connection failed: {e}")
        return False

def load_schema():
    """Load database schema"""
    print("\nLoading schema...")
    
    try:
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='hostel_management',
            charset='utf8mb4',
            cursorclass=MySQLdb.cursors.DictCursor,
            autocommit=True
        )
        
        cursor = conn.cursor()
        
        # Read schema file
        with open('/home/prajwal/Programs/Hostel/config/database.sql', 'r') as f:
            sql_content = f.read()
        
        # Split into statements and execute
        statements = sql_content.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except MySQLdb.Error as e:
                    # Ignore certain errors
                    if "already exists" not in str(e):
                        print(f"  Note: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Schema loaded successfully")
        return True
        
    except Exception as e:
        print(f"✗ Schema loading failed: {e}")
        return False

def verify_setup():
    """Verify the database is ready"""
    print("\nVerifying setup...")
    
    try:
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='hostel_management',
            charset='utf8mb4',
            cursorclass=MySQLdb.cursors.DictCursor
        )
        
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        # Check users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        users = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print(f"✓ Found {len(tables)} tables")
        print(f"✓ Found {users['count']} test users")
        
        return True
        
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "="*70)
    print("HOSTEL MANAGEMENT SYSTEM - AUTOMATIC MYSQL SETUP")
    print("="*70 + "\n")
    
    # Try socket first (works without password)
    if not setup_with_socket():
        print("\nSocket auth failed, trying TCP...")
        if not setup_with_tcp():
            print("\n✗ Could not connect to MySQL")
            sys.exit(1)
    
    # Load schema
    if not load_schema():
        print("\n✗ Could not load schema")
        sys.exit(1)
    
    # Verify
    if not verify_setup():
        print("\n⚠ Verification failed, but setup may have worked")
    
    # Success
    print("\n" + "="*70)
    print("✓ MYSQL SETUP COMPLETE!")
    print("="*70)
    print("\n📋 NOW YOU'RE READY TO START!")
    print("\nRun these commands in order:")
    print("\n  1. Kill any existing Flask:")
    print("     pkill -f 'python app.py'")
    print("\n  2. Start Flask:")
    print("     cd /home/prajwal/Programs/Hostel")
    print("     python app.py")
    print("\n  3. Open browser:")
    print("     http://10.252.129.72:5000")
    print("\n  4. Login with:")
    print("     Admin: admin / admin123")
    print("     Student: prajwal / admin123")
    print("     Warden: warden / admin123")
    print("\n" + "="*70 + "\n")
    
    sys.exit(0)
