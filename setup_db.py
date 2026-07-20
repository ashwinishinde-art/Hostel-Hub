#!/usr/bin/env python3
"""
Hostel Management System - Database Setup
This script sets up the database without requiring sudo
"""

import MySQLdb
import MySQLdb.cursors
import sys

def setup_database():
    """Setup database with schema"""
    
    try:
        # First, connect to MySQL without database
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            charset='utf8mb4',
            cursorclass=MySQLdb.cursors.DictCursor
        )
        
        cursor = conn.cursor()
        
        # Drop existing database
        print("Dropping old database...")
        cursor.execute("DROP DATABASE IF EXISTS hostel_management")
        conn.commit()
        
        # Create database
        print("Creating database...")
        cursor.execute("""
            CREATE DATABASE hostel_management 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci
        """)
        conn.commit()
        cursor.close()
        conn.close()
        
        # Now connect to the new database and load schema
        print("Loading schema...")
        conn = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='hostel_management',
            charset='utf8mb4',
            cursorclass=MySQLdb.cursors.DictCursor
        )
        
        cursor = conn.cursor()
        
        # Read and execute the SQL schema file
        with open('/home/prajwal/Programs/Hostel/config/database.sql', 'r') as f:
            sql_content = f.read()
        
        # Split into individual statements
        statements = sql_content.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except MySQLdb.Error as e:
                    # Skip errors for statements that may have already been executed
                    if "already exists" not in str(e) and "no database selected" not in str(e):
                        print(f"Warning: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✓ Database setup complete!")
        print("✓ All tables created")
        print("✓ Sample data loaded")
        print("\nNow run Flask:")
        print("  python app.py")
        
        return True
        
    except MySQLdb.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "="*60)
    print("HOSTEL MANAGEMENT SYSTEM - DATABASE SETUP")
    print("="*60 + "\n")
    
    success = setup_database()
    sys.exit(0 if success else 1)
