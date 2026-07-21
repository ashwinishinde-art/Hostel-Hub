"""
Database Helper - Provides safe database access for all routes
Handles both MySQL and mock database transparently
"""

def get_db():
    """Get the appropriate database instance (MySQL or mock)"""
    try:
        from config.database import db as real_db
        # Check if MySQL connection is actually available
        if real_db.connection is None or not real_db.is_connected:
            from config.database_mock import db as mock_db
            return mock_db
        return real_db
    except:
        from config.database_mock import db as mock_db
        return mock_db


def get_cursor():
    """Get a database cursor safely"""
    db = get_db()
    try:
        if db.connection is None:
            return None
        return db.connection.cursor()
    except:
        return None


def safe_execute(query, params=None):
    """Execute a query safely and return results"""
    cursor = get_cursor()
    if cursor is None:
        return []
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Database query error: {e}")
        return []


def safe_execute_one(query, params=None):
    """Execute a query safely and return first result"""
    cursor = get_cursor()
    if cursor is None:
        return None
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        print(f"Database query error: {e}")
        return None


def safe_execute_update(query, params=None):
    """Execute an update/insert/delete query safely"""
    cursor = get_cursor()
    if cursor is None:
        return False
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Commit if it's a real MySQL connection
        if hasattr(cursor, 'connection') and hasattr(cursor.connection, 'commit'):
            cursor.connection.commit()
        
        cursor.close()
        return True
    except Exception as e:
        print(f"Database update error: {e}")
        try:
            if hasattr(cursor, 'connection') and hasattr(cursor.connection, 'rollback'):
                cursor.connection.rollback()
        except:
            pass
        return False
