#!/usr/bin/env python3
"""
Website Cleanup Script - Removes unnecessary files from the project
"""

import os
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Files to KEEP - absolutely necessary for the website
KEEP_FILES = {
    # Main application
    'app.py',
    'requirements.txt',
    
    # Configuration
    'config/config.py',
    'config/database.py',
    'config/socketio_manager.py',
    'config/__init__.py',
    
    # Routes
    'routes/admin_routes.py',
    'routes/student_routes.py',
    'routes/warden_routes.py',
    'routes/__init__.py',
    
    # Utilities
    'utils/db_helper.py',
    'utils/otp_manager.py',
    
    # Startup scripts
    'start_tunnel.sh',
    'start_tunnel.ps1',
    'START_TUNNEL.bat',
    'START_TUNNEL.desktop',
    
    # Latest theme fix tool
    'automated_fix_all_colors.py',
    
    # Essential documentation
    'README.md',
    '00_START_HERE.txt',
    'AUTOMATED_FIX_COMPLETE.txt',
    'QUICK_START_THEME_TESTING.txt',
    'THEME_VISIBILITY_SUMMARY.txt',
    'THEME_VISIBILITY_TEST_CHECKLIST.md',
    'THEME_VISIBILITY_FIX_GUIDE.md',
    'THEME_VISIBILITY_INDEX.md',
}

# Files/Directories to DELETE
DELETE_FILES = {
    # Old fix and setup scripts
    'apply_all_changes_flask.py',
    'apply_database_fixes.py',
    'apply_hostel_info.py',
    'apply_updates_now.py',
    'apply_via_flask.py',
    'apply_via_http.py',
    'audit_theme_visibility.py',
    'auto_setup_mysql.py',
    'check_room106.py',
    'check_setup.py',
    'cleanup_gallery_temp_images.py',
    'cleanup_student_list.py',
    'comprehensive_bug_analysis.py',
    'comprehensive_test_suite.py',
    'detailed_code_audit.py',
    'diagnose_500_error.py',
    'direct_update_hostel_info.py',
    'fix_admin_warden_roles.py',
    'fix_allocations.py',
    'fix_mysql.py',
    'fix_roles_flask.py',
    'fix_room_capacity.py',
    'fix_rooms_direct.py',
    'fix_theme_visibility.py',
    'run_app.py',
    'run_setup_now.py',
    'setup_db.py',
    'setup_hostel_rooms.py',
    'setup_rooms_direct.py',
    'setup_rooms_subprocess.py',
    'setup_via_flask.py',
    'simulate_alloc.py',
    'test_app_login.py',
    'test_bugs_comprehensive.py',
    'test_forgot_password.py',
    'test_gender_fix.py',
    'test_login_debug.py',
    'test_regression_suite.py',
    'test_room_numbering.py',
    'unallocate_students.py',
    'update_hostel_info.py',
    'validate_room_capacity.py',
    'verify_room_numbering.py',
    'verify_rooms.py',
    'verify_settings.py',
    
    # Old bash scripts
    'ONE_COMMAND_UPDATE.sh',
    'RUN_THIS_FIRST.sh',
    'START_HERE.sh',
    'SETUP_AND_RUN.sh',
    'FINAL_SETUP.sh',
    'EXECUTE_SETUP.sh',
    'start_mariadb.sh',
    'UPDATE_DATABASE.sh',
    'start_mysql.sh',
    
    # Old SQL files
    'unallocate_students.sql',
    'UPDATE_HOSTEL_INFO.sql',
    'FIX_ADMIN_WARDEN.sql',
    
    # Test files
    'test_room_type.html',
    'Testing sheet.xlsx',
    '.~lock.start_tunnel.ps1#',
    
    # Old documentation files - over 130 files
    # All .md and .txt files except the ones in KEEP_FILES
}

def delete_files():
    """Delete unnecessary files"""
    
    print("\n" + "=" * 80)
    print("CLEANING UP WEBSITE FOLDER")
    print("=" * 80 + "\n")
    
    deleted_count = 0
    failed_count = 0
    
    # Get all root level Python, MD, TXT files
    root_files = (
        list(PROJECT_ROOT.glob('*.py')) +
        list(PROJECT_ROOT.glob('*.md')) +
        list(PROJECT_ROOT.glob('*.txt')) +
        list(PROJECT_ROOT.glob('*.sh')) +
        list(PROJECT_ROOT.glob('*.sql')) +
        list(PROJECT_ROOT.glob('*.xlsx')) +
        list(PROJECT_ROOT.glob('*.html')) +
        list(PROJECT_ROOT.glob('.*#'))
    )
    
    # Delete files not in KEEP_FILES
    for file_path in sorted(root_files):
        file_name = file_path.name
        
        if file_name not in KEEP_FILES and file_name not in ['cleanup_analysis.py', 'cleanup_website.py']:
            try:
                if file_path.is_file():
                    os.remove(file_path)
                    print(f"  ✅ Deleted: {file_name}")
                    deleted_count += 1
            except Exception as e:
                print(f"  ⚠️  Failed to delete {file_name}: {e}")
                failed_count += 1
    
    # Delete old log files
    for log_file in PROJECT_ROOT.glob('*.log'):
        try:
            os.remove(log_file)
            print(f"  ✅ Deleted: {log_file.name}")
            deleted_count += 1
        except Exception as e:
            print(f"  ⚠️  Failed to delete {log_file.name}: {e}")
            failed_count += 1
    
    # Delete old lnk files
    for lnk_file in PROJECT_ROOT.glob('*.lnk'):
        try:
            os.remove(lnk_file)
            print(f"  ✅ Deleted: {lnk_file.name}")
            deleted_count += 1
        except Exception as e:
            print(f"  ⚠️  Failed to delete {lnk_file.name}: {e}")
            failed_count += 1
    
    print("\n" + "=" * 80)
    print(f"CLEANUP COMPLETE: {deleted_count} files deleted, {failed_count} failed")
    print("=" * 80 + "\n")
    
    # Show remaining necessary files
    print("ESSENTIAL FILES REMAINING:")
    print("-" * 80)
    
    print("\nPython Scripts:")
    for f in sorted(KEEP_FILES):
        if f.endswith('.py'):
            full_path = PROJECT_ROOT / f
            if full_path.exists():
                print(f"  ✅ {f}")
    
    print("\nConfiguration:")
    print(f"  ✅ config/ (directory)")
    print(f"  ✅ routes/ (directory)")
    print(f"  ✅ utils/ (directory)")
    print(f"  ✅ templates/ (directory)")
    print(f"  ✅ static/ (directory)")
    print(f"  ✅ data/ (directory)")
    
    print("\nDocumentation:")
    for f in sorted(KEEP_FILES):
        if f.endswith(('.md', '.txt')):
            full_path = PROJECT_ROOT / f
            if full_path.exists():
                print(f"  ✅ {f}")
    
    print("\nStartup Scripts:")
    for f in sorted(KEEP_FILES):
        if f.endswith(('.sh', '.ps1', '.bat', '.desktop')):
            full_path = PROJECT_ROOT / f
            if full_path.exists():
                print(f"  ✅ {f}")
    
    print("\n" + "=" * 80)
    print("✅ CLEANUP COMPLETE")
    print("=" * 80 + "\n")

def show_final_structure():
    """Show the final project structure"""
    
    print("FINAL PROJECT STRUCTURE:")
    print("-" * 80)
    print("""
    Hostel-Hub/
    ├── app.py                           (Main Flask application)
    ├── requirements.txt                 (Dependencies)
    ├── README.md                        (Project documentation)
    │
    ├── config/
    │   ├── config.py                   (Configuration)
    │   ├── database.py                 (Database setup)
    │   └── socketio_manager.py         (Real-time updates)
    │
    ├── routes/
    │   ├── admin_routes.py             (Admin functionality)
    │   ├── student_routes.py           (Student functionality)
    │   └── warden_routes.py            (Warden functionality)
    │
    ├── utils/
    │   ├── db_helper.py                (Database utilities)
    │   └── otp_manager.py              (OTP functionality)
    │
    ├── templates/                       (All HTML templates)
    │   ├── base.html
    │   ├── login.html
    │   ├── register.html
    │   ├── admin/
    │   ├── student/
    │   └── warden/
    │
    ├── static/                          (CSS, JS, Images)
    │   ├── css/
    │   ├── js/
    │   └── uploads/
    │
    ├── data/                            (Database files)
    │
    └── Documentation:
        ├── 00_START_HERE.txt
        ├── AUTOMATED_FIX_COMPLETE.txt
        ├── QUICK_START_THEME_TESTING.txt
        ├── THEME_VISIBILITY_*.md
        └── THEME_VISIBILITY_*.txt
    """)
    print("-" * 80)

if __name__ == '__main__':
    print("\n⚠️  THIS SCRIPT WILL DELETE 200+ UNNECESSARY FILES")
    print("=" * 80)
    print("\nFiles to be deleted:")
    print("  • 45 old fix/test Python scripts")
    print("  • 135 old documentation markdown files")
    print("  • 21 old status/summary text files")
    print("  • Old shell scripts and SQL files")
    print("\nFiles that will be KEPT:")
    print("  • app.py (main application)")
    print("  • config/ routes/ utils/ (essential code)")
    print("  • templates/ static/ data/ (website content)")
    print("  • 8 essential documentation files")
    print("\n" + "=" * 80)
    
    response = input("\n❓ Do you want to proceed with cleanup? (yes/no): ").strip().lower()
    
    if response == 'yes':
        delete_files()
        show_final_structure()
        print("\n✅ Your website is now clean and optimized!")
        print("   All unnecessary files have been removed.")
        print("   Only essential application files remain.")
    else:
        print("\n❌ Cleanup cancelled. No files were deleted.")
