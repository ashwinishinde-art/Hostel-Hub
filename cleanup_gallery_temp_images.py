#!/usr/bin/env python3
"""
Clean up temporary and test images from the gallery
Removes 'temp' and 'test' titled images that were auto-added
"""

import sys
import os

# Add project to path
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

from config.database import db
import mysql.connector

def cleanup_gallery():
    """Remove temp and test images from gallery"""
    
    if not db.connection or not db.is_connected:
        print("❌ Could not connect to database")
        return False
    
    cursor = db.connection.cursor()
    
    try:
        # Find all gallery images with 'temp' or 'test' titles
        cursor.execute("""
            SELECT id, title, image_path FROM gallery 
            WHERE title IN ('temp', 'test') 
            OR title LIKE '%temp%'
            OR title LIKE '%test%'
            ORDER BY id
        """)
        
        images_to_delete = cursor.fetchall()
        
        if not images_to_delete:
            print("✓ No temporary or test images found")
            cursor.close()
            return True
        
        print(f"Found {len(images_to_delete)} temporary/test image(s):")
        
        for img_id, title, image_path in images_to_delete:
            print(f"  - ID: {img_id}, Title: '{title}', Path: {image_path}")
        
        print("\nDeleting temporary/test images...")
        
        # Delete from database
        for img_id, title, image_path in images_to_delete:
            cursor.execute("DELETE FROM gallery WHERE id = %s", (img_id,))
            
            # Try to delete file from disk
            if image_path:
                file_path = image_path.lstrip('/')
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        print(f"  ✓ Deleted database entry and file: {file_path}")
                    except Exception as e:
                        print(f"  ⚠️  Deleted database entry but couldn't delete file: {str(e)}")
                else:
                    print(f"  ✓ Deleted database entry (file not found: {file_path})")
        
        db.connection.commit()
        cursor.close()
        
        print(f"\n✅ Successfully cleaned up {len(images_to_delete)} temporary image(s)")
        return True
        
    except Exception as e:
        db.connection.rollback()
        cursor.close()
        print(f"❌ Error during cleanup: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("GALLERY CLEANUP - Remove Temporary Images")
    print("=" * 60)
    print()
    
    success = cleanup_gallery()
    
    print()
    if success:
        print("✅ Cleanup complete!")
    else:
        print("❌ Cleanup failed!")
    
    sys.exit(0 if success else 1)
