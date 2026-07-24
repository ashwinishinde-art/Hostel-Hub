# Theme Visibility Fix Guide

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
