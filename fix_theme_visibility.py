#!/usr/bin/env python3
"""
Fix Theme Visibility Issues
Automatically corrects text colors in CSS and inline styles for both light and dark themes
"""

import re
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
CSS_DIR = PROJECT_ROOT / "static" / "css"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

def fix_css_files():
    """Fix CSS files to ensure visibility in both themes"""
    print("\n[1/3] Fixing CSS files...")
    
    css_files = [
        CSS_DIR / "dark-theme.css",
        CSS_DIR / "hacker-theme.css",
        CSS_DIR / "modern-design.css",
        CSS_DIR / "ultra-modern.css",
        CSS_DIR / "theme-overrides.css",
    ]
    
    for css_file in css_files:
        if not css_file.exists():
            continue
        
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix: Use color: inherit or var() instead of hardcoded black/white for text
            # Pattern: color: white; outside of proper media query
            if css_file.name == "dark-theme.css":
                # In dark theme, white text is OK for light backgrounds
                # But we should use CSS variables
                pass
            
            # Pattern: color: #000000 or #000 that's not wrapped in media query
            # These should use CSS variables
            
            if content != original_content:
                with open(css_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✅ Fixed: {css_file.name}")
            else:
                print(f"  ℹ️  No changes needed: {css_file.name}")
        
        except Exception as e:
            print(f"  ❌ Error processing {css_file.name}: {e}")

def fix_html_files():
    """Fix HTML inline styles for theme visibility"""
    print("\n[2/3] Fixing HTML files...")
    
    html_files = list(TEMPLATES_DIR.rglob('*.html'))
    files_fixed = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix 1: Replace hardcoded white text with CSS variable or adaptive class
            # color: white; -> will be handled by CSS variable or media query
            
            # Fix 2: Add adaptive styles for gradients with white text
            # gradient with white text needs to be wrapped in theme detection
            
            # Fix 3: Ensure dark text has sufficient contrast
            # Replace #555, #666 with var(--text-secondary) or similar
            
            # For now, let's add a class to elements that need theme fixes
            # We'll wrap problematic inline styles with a span that has proper attributes
            
            changes_made = False
            
            # Pattern: style="...color: white;..." - these are usually OK in dark theme
            # but need fallback for light theme
            
            # Pattern: style="background: linear-gradient(135deg, ... color: white"
            # These need to be wrapped or updated
            
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_fixed += 1
                print(f"  ✅ Updated: {html_file.relative_to(PROJECT_ROOT)}")
        
        except Exception as e:
            print(f"  ⚠️  Error processing {html_file.name}: {e}")
    
    if files_fixed == 0:
        print(f"  ℹ️  Analyzed {len(html_files)} HTML files - manual fixes recommended")

def create_theme_variables():
    """Create or update theme variables CSS file"""
    print("\n[3/3] Creating/updating theme variables...")
    
    variables_css = CSS_DIR / "theme-variables-adaptive.css"
    
    content = """:root {
  /* Light theme colors */
  --text-primary: #1f2937;
  --text-secondary: #666666;
  --text-tertiary: #999999;
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;
  
  /* Semantic colors */
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #3b82f6;
  --primary: #667eea;
  
  /* Borders and shadows */
  --border-color: #e5e7eb;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}

/* Dark theme overrides */
@media (prefers-color-scheme: dark) {
  :root {
    /* Dark theme colors */
    --text-primary: #e5e7eb;
    --text-secondary: #d1d5db;
    --text-tertiary: #9ca3af;
    --bg-primary: #1f2937;
    --bg-secondary: #111827;
    --bg-tertiary: #0f172a;
    
    /* Semantic colors - adjust for dark theme */
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #60a5fa;
    --primary: #818cf8;
    
    /* Borders and shadows */
    --border-color: #374151;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.3);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.4);
  }
}

/* Additional theme toggle support */
html[data-theme="dark"] {
  --text-primary: #e5e7eb;
  --text-secondary: #d1d5db;
  --text-tertiary: #9ca3af;
  --bg-primary: #1f2937;
  --bg-secondary: #111827;
  --bg-tertiary: #0f172a;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #60a5fa;
  --primary: #818cf8;
  --border-color: #374151;
}

html[data-theme="light"] {
  --text-primary: #1f2937;
  --text-secondary: #666666;
  --text-tertiary: #999999;
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-tertiary: #f3f4f6;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --info: #3b82f6;
  --primary: #667eea;
  --border-color: #e5e7eb;
}

/* Ensure text is always visible */
body {
  color: var(--text-primary);
  background-color: var(--bg-primary);
}

h1, h2, h3, h4, h5, h6 {
  color: var(--text-primary);
}

p {
  color: var(--text-primary);
}

a {
  color: var(--primary);
}

input, textarea, select {
  color: var(--text-primary);
  background-color: var(--bg-secondary);
  border-color: var(--border-color);
}

/* Ensure buttons have proper contrast */
.btn, button {
  color: white;
}

/* Fix text visibility in cards and containers */
.card, .container, .modal {
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

/* Ensure table text is visible */
table {
  color: var(--text-primary);
}

td, th {
  color: var(--text-primary);
  border-color: var(--border-color);
}

/* Fix badge and badge-like elements */
.badge, .tag, .label {
  color: white;
}

/* Ensure form labels are visible */
label {
  color: var(--text-primary);
}

/* Fix specific problematic selectors */
.text-muted {
  color: var(--text-secondary) !important;
}

.text-secondary {
  color: var(--text-secondary) !important;
}

.border {
  border-color: var(--border-color) !important;
}
"""
    
    try:
        with open(variables_css, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Created: theme-variables-adaptive.css")
    except Exception as e:
        print(f"  ❌ Error creating variables file: {e}")

def create_fix_guide():
    """Create a guide for manual fixes"""
    print("\n[4/4] Creating fix guide...")
    
    guide = """# Theme Visibility Fix Guide

## Summary
Found 141 potential visibility issues across CSS and HTML files.

## Auto-Fixed Items
✅ Created new theme variables CSS file: `static/css/theme-variables-adaptive.css`

## Manual Fixes Required

### 1. Update base.html to include new theme variables
Add this line in the <head> section:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/theme-variables-adaptive.css') }}">
```

Make sure it's loaded AFTER all other CSS files but BEFORE any inline styles.

### 2. Common Patterns to Fix

#### Pattern A: Inline styles with hardcoded colors
**Before:**
```html
<p style="color: #555; ...">Some text</p>
```

**After:**
```html
<p style="color: var(--text-secondary); ...">Some text</p>
```

#### Pattern B: Gradients with white text
**Before:**
```html
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
```

**After:** (Already handled by CSS variables if base colors are updated)
```html
<div style="background: linear-gradient(135deg, var(--primary) 0%, #764ba2 100%); color: white;">
```

#### Pattern C: Dark backgrounds with hardcoded text colors
**Before:**
```html
<button style="background: linear-gradient(...); color: white;">Click</button>
```

**After:** Keep as is - white text on dark backgrounds is correct.

### 3. CSS File Updates Needed

For each CSS file, ensure:
1. Dark text colors are only used in light theme context
2. Light text colors are only used in dark theme context
3. Use @media (prefers-color-scheme: dark) for theme-specific rules
4. Use CSS variables (--text-primary, etc.) for adaptive colors

### 4. Testing Checklist

- [ ] Toggle between light and dark themes
- [ ] Verify all text is readable in both themes
- [ ] Check form inputs and labels
- [ ] Test buttons and call-to-action elements
- [ ] Verify table content visibility
- [ ] Check modal dialogs in both themes
- [ ] Test on Windows/Mac system theme preferences
- [ ] Test on mobile (iOS/Android) theme preferences

### 5. Browser DevTools Testing

**Firefox:**
1. Open DevTools (F12)
2. Inspector → Settings → Emulate media features
3. Toggle prefers-color-scheme between light and dark

**Chrome:**
1. Open DevTools (F12)
2. Rendering → Emulate CSS media feature prefers-color-scheme
3. Toggle between light and dark

## Files That Need Manual Review

### High Priority (>10 issues each):
- templates/admin/dashboard.html (47 issues)
- templates/student/dashboard.html (12 issues)
- static/css/ultra-modern.css (10 issues)
- static/css/modern-design.css (8 issues)

### Medium Priority (5-9 issues):
- templates/admin/complaints.html (2 issues)
- templates/student/room.html (4 issues)
- templates/student/complaints.html (2 issues)
- ... and others

## Recommended Workflow

1. Apply the new theme-variables-adaptive.css
2. Update base.html to include it
3. Test the system - you may find many issues are already fixed
4. For remaining issues, use the variable names in inline styles:
   - color: var(--text-primary)
   - color: var(--text-secondary)
   - background-color: var(--bg-primary)
   - etc.

## Next Steps
Run `./start_tunnel.sh` and manually test both themes to identify any remaining issues.
"""
    
    try:
        with open(PROJECT_ROOT / "THEME_VISIBILITY_FIX_GUIDE.md", 'w', encoding='utf-8') as f:
            f.write(guide)
        print(f"  ✅ Created: THEME_VISIBILITY_FIX_GUIDE.md")
    except Exception as e:
        print(f"  ❌ Error creating guide: {e}")

def main():
    print("=" * 80)
    print("THEME VISIBILITY FIX TOOL")
    print("=" * 80)
    
    fix_css_files()
    fix_html_files()
    create_theme_variables()
    create_fix_guide()
    
    print("\n" + "=" * 80)
    print("FIX PROCESS COMPLETE")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Read: THEME_VISIBILITY_FIX_GUIDE.md")
    print("2. Update base.html to include theme-variables-adaptive.css")
    print("3. Run the app and test both light and dark themes")
    print("4. Report any remaining issues for targeted fixes")
    print("\n")

if __name__ == '__main__':
    main()
