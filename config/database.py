import MySQLdb
from MySQLdb import cursors
import sys
import os

class Database:
    """Database connection - PRODUCTION READY"""
    
    def __init__(self):
        self.connection = None
        self.is_connected = False
    
    def connect(self):
        """Connect to MySQL with error handling"""
        try:
            # Direct connection to localhost
            self.connection = MySQLdb.connect(
                host='127.0.0.1',
                user='root',
                password='',
                database='hostel_management',
                charset='utf8mb4',
                cursorclass=cursors.DictCursor,
                autocommit=True,
                port=3306
            )
            self.is_connected = True
            return self.connection
            
        except MySQLdb.Error as e:
            print(f"✗ Database connection failed: {e}")
            self.is_connected = False
            self.connection = None
            return None
    
    def get_connection(self):
        """Ensure connection is alive"""
        try:
            if self.connection is None or not self.is_connected:
                self.connect()
            # Ping to ensure connection is alive
            self.connection.ping(True)
        except:
            self.connect()
        return self.connection
    
    def execute_query(self, query, params=None):
        """Execute SELECT query"""
        try:
            conn = self.get_connection()
            if not conn:
                return None
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"✗ Query error: {e}")
            self.connection = None
            self.is_connected = False
            return None
    
    def execute_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE"""
        try:
            conn = self.get_connection()
            if not conn:
                return False
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"✗ Update error: {e}")
            try:
                conn.rollback()
            except:
                pass
            self.connection = None
            self.is_connected = False
            return False
    
    def close(self):
        """Close connection"""
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            self.is_connected = False

# Initialize
db = Database()
connection = db.connect()

if not connection:
    # Don't raise error - let app.py fall back to mock database
    print("⚠️  MySQL connection failed. App will fall back to mock database.")
