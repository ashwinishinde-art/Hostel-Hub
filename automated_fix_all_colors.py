#!/usr/bin/env python3
"""
Automated Theme Visibility Fix - Fixes all text colors to use CSS variables
Ensures all text is visible in both light and dark themes
"""

import re
import os
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent
CSS_DIR = PROJECT_ROOT / "static" / "css"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# Mapping of problematic colors to CSS variables
COLOR_REPLACEMENTS = {
    # Dark text/grays to use semantic variables
    'color: #000000': 'color: var(--text-primary)',
    'color: #000': 'color: var(--text-primary)',
    'color: black': 'color: var(--text-primary)',
    'color:#000000': 'color: var(--text-primary)',
    'color:#000': 'color: var(--text-primary)',
    'color:#111111': 'color: var(--text-primary)',
    'color:#222222': 'color: var(--text-primary)',
    'color:#333333': 'color: var(--text-primary)',
    'color:#444444': 'color: var(--text-primary)',
    'color: #111': 'color: var(--text-primary)',
    'color: #222': 'color: var(--text-primary)',
    'color: #333': 'color: var(--text-primary)',
    'color: #444': 'color: var(--text-primary)',
    'color: #555': 'color: var(--text-secondary)',
    'color: #555555': 'color: var(--text-secondary)',
    'color: #666': 'color: var(--text-secondary)',
    'color: #666666': 'color: var(--text-secondary)',
    'color: #777': 'color: var(--text-tertiary)',
    'color: #999': 'color: var(--text-tertiary)',
    'color: #999999': 'color: var(--text-tertiary)',
    'color: #2c3e50': 'color: var(--text-primary)',
    
    # Light text colors - keep white for buttons but use var for adaptive colors
    'color: white': 'color: var(--text-on-dark)',  # Text on dark backgrounds
    'color: #ffffff': 'color: var(--text-on-dark)',
    'color: #fff': 'color: var(--text-on-dark)',
    'color:#ffffff': 'color: var(--text-on-dark)',
    'color:#fff': 'color: var(--text-on-dark)',
    
    # Special cases for light gray text
    'color: #ddd': 'color: var(--text-secondary)',
    'color: #ccc': 'color: var(--text-secondary)',
    'color: #bbb': 'color: var(--text-secondary)',
}

# CSS variable mapping for use in media queries
CSS_VARIABLE_DEFINITIONS = """
/* Theme-aware text colors */
:root {
  --text-primary: #1f2937;
  --text-secondary: #666666;
  --text-tertiary: #999999;
  --text-on-dark: #ffffff;
}

@media (prefers-color-scheme: dark) {
  :root {
    --text-primary: #e5e7eb;
    --text-secondary: #d1d5db;
    --text-tertiary: #9ca3af;
    --text-on-dark: #e5e7eb;
  }
}
"""

def fix_css_colors(css_path):
    """Fix hardcoded colors in CSS files"""
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Replace colors with case-insensitive matching
        for old_color, new_var in COLOR_REPLACEMENTS.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(old_color), re.IGNORECASE)
            content = pattern.sub(new_var, content)
        
        if content != original:
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ⚠️  Error in {css_path.name}: {e}")
        return False

def fix_html_inline_colors(html_path):
    """Fix hardcoded colors in HTML inline styles"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Fix inline styles with color attributes
        for old_color, new_var in COLOR_REPLACEMENTS.items():
            # Make it case-insensitive for inline styles too
            pattern = re.compile(re.escape(old_color), re.IGNORECASE)
            content = pattern.sub(new_var, content)
        
        if content != original:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ⚠️  Error in {html_path.name}: {e}")
        return False

def update_theme_variables_file():
    """Update or create the theme variables CSS file with proper definitions"""
    variables_file = CSS_DIR / "theme-variables-adaptive.css"
    
    try:
        with open(variables_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if variables are already defined
        if '--text-on-dark' not in content:
            # Add the text-on-dark variable
            content = content.replace(
                '@media (prefers-color-scheme: dark) {',
                f'''  --text-on-dark: #ffffff;
}}

@media (prefers-color-scheme: dark) {{'''
            )
            with open(variables_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ⚠️  Error updating variables: {e}")
        return False

def main():
    print("\n" + "=" * 80)
    print("AUTOMATED THEME VISIBILITY FIX - REPLACING ALL HARDCODED COLORS")
    print("=" * 80 + "\n")
    
    # Step 1: Fix CSS files
    print("[1/4] Fixing CSS files...")
    css_files_fixed = 0
    if CSS_DIR.exists():
        for css_file in CSS_DIR.glob('*.css'):
            if fix_css_colors(css_file):
                print(f"  ✅ Fixed: {css_file.name}")
                css_files_fixed += 1
            else:
                print(f"  ℹ️  No changes needed: {css_file.name}")
    
    # Step 2: Fix HTML templates
    print("\n[2/4] Fixing HTML templates...")
    html_files_fixed = 0
    if TEMPLATES_DIR.exists():
        for html_file in TEMPLATES_DIR.rglob('*.html'):
            if fix_html_inline_colors(html_file):
                print(f"  ✅ Fixed: {html_file.relative_to(PROJECT_ROOT)}")
                html_files_fixed += 1
    
    if html_files_fixed == 0:
        print(f"  ℹ️  Scanned {len(list(TEMPLATES_DIR.rglob('*.html')))} HTML files")
    
    # Step 3: Update theme variables
    print("\n[3/4] Updating theme variables...")
    if update_theme_variables_file():
        print(f"  ✅ Updated: theme-variables-adaptive.css")
    else:
        print(f"  ℹ️  Variables already up to date")
    
    # Step 4: Summary
    print("\n[4/4] Summary")
    print("-" * 80)
    print(f"  CSS files updated: {css_files_fixed}")
    print(f"  HTML files updated: {html_files_fixed}")
    print(f"  Total files modified: {css_files_fixed + html_files_fixed}")
    
    print("\n" + "=" * 80)
    print("✅ AUTOMATED FIX COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Clear browser cache (Ctrl+Shift+Delete)")
    print("  2. Refresh the page (Ctrl+R)")
    print("  3. Test both light and dark themes")
    print("  4. Check if all text is now visible")
    print("\nCSS Variables Used:")
    print("  --text-primary    : Main text (adapts to theme)")
    print("  --text-secondary  : Secondary text")
    print("  --text-tertiary   : Tertiary text")
    print("  --text-on-dark    : Text on dark backgrounds")
    print()

if __name__ == '__main__':
    main()
