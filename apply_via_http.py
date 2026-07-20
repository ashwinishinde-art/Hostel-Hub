#!/usr/bin/env python3
"""
Apply updates by making HTTP requests to the Flask app
The Flask app has access to the database connection
"""

import requests
import json
import time

def apply_via_http():
    """Apply updates via Flask HTTP endpoint"""
    
    print("\n" + "="*70)
    print("HOSTEL MANAGEMENT SYSTEM - APPLYING ALL CHANGES VIA FLASK APP")
    print("="*70 + "\n")
    
    # Check if Flask app is running
    print("Checking if Flask app is running on http://localhost:5000...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        print("✓ Flask app is running\n")
    except:
        print("✗ Flask app is not running")
        print("  Please start it: python app.py")
        return False
    
    # Call the update endpoint
    print("Calling update endpoint...")
    print("-"*70 + "\n")
    
    try:
        # Make POST request to update endpoint
        response = requests.post(
            'http://localhost:5000/admin/update-hostel-info',
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✓ Update successful!")
            result = response.json()
            print(f"  Message: {result.get('message', 'Update completed')}\n")
        elif response.status_code == 302:  # Redirect (not authenticated)
            print("⚠ Need authentication to access admin endpoint")
            print("  This endpoint requires admin login")
            return False
        else:
            print(f"✗ Error: Status {response.status_code}")
            print(f"  Response: {response.text}\n")
            return False
            
    except Exception as e:
        print(f"✗ Error making request: {e}\n")
        return False
    
    return True

if __name__ == '__main__':
    import sys
    success = apply_via_http()
    sys.exit(0 if success else 1)
