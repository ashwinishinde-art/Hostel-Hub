#!/usr/bin/env python3
"""
Theme Visibility Audit Tool
Checks all text colors in CSS files to ensure visibility in both light and dark themes
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

# Define the project root
PROJECT_ROOT = Path(__file__).parent
CSS_DIR = PROJECT_ROOT / "static" / "css"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# Common light theme colors (text colors that might not be visible in light theme)
PROBLEMATIC_LIGHT_COLORS = {
    '#000000', '#000', 'black', 'rgb(0,0,0)', 'rgba(0,0,0',
    '#111', '#222', '#333', '#444', '#555', '#666',  # Dark grays
}

# Common dark theme colors (text colors that might not be visible in dark theme)
PROBLEMATIC_DARK_COLORS = {
    '#ffffff', '#fff', 'white', 'rgb(255,255,255)', 'rgba(255,255,255',
    '#eee', '#ddd', '#ccc', '#bbb',  # Light grays
}

def analyze_css_file(css_path):
    """Analyze a CSS file for theme visibility issues"""
    issues = []
    
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return issues
    
    # Find all color properties
    color_patterns = [
        r'color\s*:\s*([^;!]+)',  # color property
        r'background-color\s*:\s*([^;!]+)',  # background-color
        r'background\s*:\s*([^;!]+)',  # background shorthand
        r'text-shadow\s*:\s*([^;!]+)',  # text-shadow
        r'box-shadow\s*:\s*([^;!]+)',  # box-shadow
    ]
    
    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        # Skip comments
        if line.strip().startswith('//') or line.strip().startswith('/*'):
            continue
            
        # Check for color properties
        for pattern in color_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                color_value = match.group(1).strip().lower()
                
                # Check if this is a text/foreground color in light theme
                if 'color:' in line and any(c in color_value for c in PROBLEMATIC_LIGHT_COLORS):
                    # Check if not in a dark theme specific rule
                    if 'dark' not in line and '@media (prefers-color-scheme: dark)' not in content[max(0, content.find(line)-500):content.find(line)]:
                        issues.append({
                            'file': str(css_path),
                            'line': line_num,
                            'type': 'Dark text in light theme',
                            'color': color_value,
                            'line_text': line.strip()[:80]
                        })
                
                # Check if this is a text/foreground color in dark theme
                if 'color:' in line and any(c in color_value for c in PROBLEMATIC_DARK_COLORS):
                    # Check if not in a light theme specific rule
                    if 'light' not in line and '@media (prefers-color-scheme: light)' not in content[max(0, content.find(line)-500):content.find(line)]:
                        issues.append({
                            'file': str(css_path),
                            'line': line_num,
                            'type': 'Light text in dark theme',
                            'color': color_value,
                            'line_text': line.strip()[:80]
                        })
    
    return issues

def analyze_html_inline_styles(html_path):
    """Analyze HTML files for inline style color issues"""
    issues = []
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return issues
    
    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        # Find inline styles
        if 'style=' in line:
            match = re.search(r'style=["\']([^"\']+)["\']', line)
            if match:
                style_content = match.group(1).lower()
                
                # Check for problematic colors
                if 'color:' in style_content:
                    if any(c in style_content for c in PROBLEMATIC_LIGHT_COLORS):
                        issues.append({
                            'file': str(html_path),
                            'line': line_num,
                            'type': 'Dark text in light theme (inline)',
                            'line_text': line.strip()[:80]
                        })
                    elif any(c in style_content for c in PROBLEMATIC_DARK_COLORS):
                        issues.append({
                            'file': str(html_path),
                            'line': line_num,
                            'type': 'Light text in dark theme (inline)',
                            'line_text': line.strip()[:80]
                        })
    
    return issues

def main():
    print("=" * 80)
    print("THEME VISIBILITY AUDIT - Checking for Text Visibility Issues")
    print("=" * 80)
    print()
    
    all_issues = []
    
    # Analyze CSS files
    print("[1/2] Analyzing CSS files...")
    if CSS_DIR.exists():
        for css_file in CSS_DIR.glob('*.css'):
            print(f"  Checking: {css_file.name}")
            issues = analyze_css_file(css_file)
            all_issues.extend(issues)
    
    print()
    
    # Analyze HTML files
    print("[2/2] Analyzing HTML files for inline styles...")
    if TEMPLATES_DIR.exists():
        for html_file in TEMPLATES_DIR.rglob('*.html'):
            issues = analyze_html_inline_styles(html_file)
            if issues:
                print(f"  Issues found in: {html_file.relative_to(PROJECT_ROOT)}")
                all_issues.extend(issues)
    
    print()
    print("=" * 80)
    print("AUDIT RESULTS")
    print("=" * 80)
    print()
    
    if not all_issues:
        print("✅ No obvious visibility issues detected!")
        print()
        print("NOTE: This is an automated scan. Manual testing across themes is recommended.")
    else:
        print(f"⚠️  Found {len(all_issues)} potential visibility issues:\n")
        
        # Group by file
        by_file = defaultdict(list)
        for issue in all_issues:
            by_file[issue['file']].append(issue)
        
        for file_path, issues in sorted(by_file.items()):
            print(f"\n📄 {file_path}")
            print("-" * 80)
            for issue in issues:
                print(f"  Line {issue['line']}: {issue['type']}")
                if 'color' in issue:
                    print(f"    Color: {issue['color']}")
                print(f"    Code: {issue['line_text']}")
                print()
    
    # Print recommendations
    print()
    print("=" * 80)
    print("RECOMMENDATIONS FOR FIXING VISIBILITY ISSUES")
    print("=" * 80)
    print()
    print("1. Use CSS Variables for theme-specific colors")
    print("   Example:")
    print("   :root { --text-primary: #000000; --text-secondary: #666666; }")
    print("   @media (prefers-color-scheme: dark) {")
    print("     :root { --text-primary: #ffffff; --text-secondary: #cccccc; }")
    print("   }")
    print()
    print("2. Use currentColor for adaptive colors")
    print("   color: currentColor;  /* Inherits from parent */")
    print()
    print("3. Test manually in both light and dark themes:")
    print("   - Toggle theme switcher")
    print("   - Check Windows 10/11 Settings > Colors > Light/Dark")
    print("   - Use browser DevTools to simulate prefers-color-scheme")
    print()

if __name__ == '__main__':
    main()
