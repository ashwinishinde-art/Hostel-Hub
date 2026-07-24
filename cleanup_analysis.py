#!/usr/bin/env python3
"""
Website Folder Cleanup Tool - Identifies and removes unnecessary files
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Files NECESSARY for the website to function
NECESSARY_FILES = {
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
    
    # Templates (all)
    # Static files (all)
    # Data directory (if exists)
    
    # Scripts to keep (startup/tunnel)
    'start_tunnel.sh',
    'start_tunnel.ps1',
    'START_TUNNEL.bat',
    'START_TUNNEL.desktop',
    'automated_fix_all_colors.py',  # Latest theme fix
}

# Files that can be safely deleted (debug, test, fix scripts)
DELETABLE_FILES = {
    # Old fix scripts and debugging files
    'apply_all_changes_flask.py',
    'apply_database_fixes.py',
    'apply_hostel_info.py',
    'apply_updates_now.py',
    'apply_via_flask.py',
    'apply_via_http.py',
    'audit_theme_visibility.py',  # Replaced by automated_fix_all_colors.py
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
    'fix_theme_visibility.py',  # Replaced by automated_fix_all_colors.py
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
    
    # Old documentation/notes (hundreds of these)
    # Keep only: README.md, THEME_VISIBILITY_*, AUTOMATED_FIX_COMPLETE.txt
}

# Documentation to keep (essential for understanding the system)
KEEP_DOCUMENTATION = {
    'README.md',
    'AUTOMATED_FIX_COMPLETE.txt',
    'QUICK_START_THEME_TESTING.txt',
    'THEME_VISIBILITY_SUMMARY.txt',
    'THEME_VISIBILITY_TEST_CHECKLIST.md',
    'THEME_VISIBILITY_FIX_GUIDE.md',
    'THEME_VISIBILITY_INDEX.md',
    '00_START_HERE.txt',
}

# All other MD/TXT files are documentation that can be deleted
def analyze_files():
    """Analyze files to categorize them"""
    
    py_files = list(PROJECT_ROOT.glob('*.py'))
    md_files = list(PROJECT_ROOT.glob('*.md'))
    txt_files = list(PROJECT_ROOT.glob('*.txt'))
    other_files = list(PROJECT_ROOT.glob('*.sql')) + list(PROJECT_ROOT.glob('*.log'))
    
    necessary_py = []
    deletable_py = []
    uncertain_py = []
    
    deletable_md = []
    deletable_txt = []
    
    # Categorize Python files
    for py in py_files:
        name = py.name
        if name in NECESSARY_FILES:
            necessary_py.append(name)
        elif name in DELETABLE_FILES:
            deletable_py.append(name)
        else:
            uncertain_py.append(name)
    
    # Categorize documentation
    for md in md_files:
        if md.name not in KEEP_DOCUMENTATION:
            deletable_md.append(md.name)
    
    for txt in txt_files:
        if txt.name not in KEEP_DOCUMENTATION:
            deletable_txt.append(txt.name)
    
    return {
        'necessary_py': necessary_py,
        'deletable_py': deletable_py,
        'uncertain_py': uncertain_py,
        'deletable_md': deletable_md,
        'deletable_txt': deletable_txt,
        'other': other_files,
    }

def main():
    print("\n" + "=" * 80)
    print("WEBSITE FOLDER CLEANUP ANALYSIS")
    print("=" * 80 + "\n")
    
    analysis = analyze_files()
    
    print("NECESSARY FILES TO KEEP")
    print("-" * 80)
    print(f"Python scripts ({len(analysis['necessary_py'])}):")
    for f in sorted(analysis['necessary_py']):
        print(f"  ✅ {f}")
    
    print(f"\nDocumentation to keep ({len(KEEP_DOCUMENTATION)}):")
    for f in sorted(KEEP_DOCUMENTATION):
        print(f"  ✅ {f}")
    
    print("\n" + "=" * 80)
    print("FILES SAFE TO DELETE")
    print("=" * 80 + "\n")
    
    total_deletable = len(analysis['deletable_py']) + len(analysis['deletable_md']) + len(analysis['deletable_txt'])
    
    print(f"Python scripts to delete ({len(analysis['deletable_py'])}):")
    for f in sorted(analysis['deletable_py']):
        print(f"  ❌ {f}")
    
    print(f"\nMarkdown files to delete ({len(analysis['deletable_md'])}):")
    for f in sorted(analysis['deletable_md'])[:10]:  # Show first 10
        print(f"  ❌ {f}")
    if len(analysis['deletable_md']) > 10:
        print(f"  ... and {len(analysis['deletable_md']) - 10} more markdown files")
    
    print(f"\nText files to delete ({len(analysis['deletable_txt'])}):")
    for f in sorted(analysis['deletable_txt'])[:10]:  # Show first 10
        print(f"  ❌ {f}")
    if len(analysis['deletable_txt']) > 10:
        print(f"  ... and {len(analysis['deletable_txt']) - 10} more text files")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY: {total_deletable} files can be safely deleted")
    print("=" * 80)
    
    print(f"\nPython scripts: {len(analysis['deletable_py'])} deletable out of {len(analysis['necessary_py']) + len(analysis['deletable_py']) + len(analysis['uncertain_py'])}")
    print(f"Documentation: {len(analysis['deletable_md']) + len(analysis['deletable_txt'])} deletable files")
    
    return analysis

if __name__ == '__main__':
    main()
