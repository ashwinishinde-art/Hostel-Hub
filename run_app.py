#!/usr/bin/env python3
"""Run Flask app with debug output"""

import sys
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

if __name__ == '__main__':
    from app import app
    
    print("=" * 70)
    print("Starting Hostel Hub Flask App")
    print("=" * 70)
    print("\nApp running on: http://localhost:5000")
    print("Login page: http://localhost:5000/login")
    print("\nTest account:")
    print("  Username: prajwal")
    print("  Password: admin123")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
