# Theme Visibility Test Checklist

## What Was Fixed
✅ Created `theme-variables-adaptive.css` with adaptive color variables
✅ Updated `base.html` to include the new adaptive theme variables
✅ Added CSS variables for text colors that automatically adapt to the active theme

## How to Test

### Step 1: Start the Application
```bash
cd ~/Desktop/Hostel-Hub
./start_tunnel.sh
```

### Step 2: Open in Browser
Visit: http://localhost:5000 (or the Cloudflare tunnel URL)

### Step 3: Test Light Theme
Look for the theme toggle in your app (usually a sun/moon icon)
1. Click to switch to **Light Theme**
2. Navigate through each page
3. Check if ALL text is visible and readable

**Pages to check:**
- [ ] Login page
- [ ] Register page
- [ ] Forgot Password page
- [ ] Admin Dashboard
- [ ] Admin Rooms
- [ ] Admin Students
- [ ] Admin Complaints
- [ ] Admin Notices
- [ ] Admin Gallery
- [ ] Admin Fees
- [ ] Admin Visitors
- [ ] Student Dashboard
- [ ] Student Room
- [ ] Student Fees
- [ ] Student Notices
- [ ] Student Complaints
- [ ] Student Visitors
- [ ] Student Profile
- [ ] Warden Dashboard
- [ ] Warden Rooms
- [ ] Warden Students
- [ ] Warden Complaints
- [ ] Warden Notices
- [ ] Warden Visitors

### Step 4: Test Dark Theme
1. Click to switch to **Dark Theme**
2. Repeat checking all pages from Step 3
3. Verify all text is still visible and readable

### Step 5: System Theme Preference (Optional)

**Windows 10/11:**
1. Settings → Personalization → Colors
2. Switch between Light and Dark mode
3. Refresh your browser
4. Verify theme changes accordingly

**macOS:**
1. System Preferences → General
2. Switch between Light and Dark appearance
3. Refresh your browser
4. Verify theme changes

**Chrome DevTools Method:**
1. Open DevTools (F12)
2. Click ⋮ → More Tools → Rendering
3. Scroll to "Emulate CSS media feature prefers-color-scheme"
4. Toggle between light and dark
5. Verify text visibility in real-time

## What to Look For

### ✅ GOOD - Text is visible:
- Black text on white background
- White text on dark background
- Any text that contrasts with its background

### ❌ BAD - Text is NOT visible:
- Black text on dark background
- White text on white background
- Gray text that blends with background
- Any text that's the same color as its background

## Common Problem Areas to Check

### 1. Dashboard Cards
- Check if card titles are visible
- Check if descriptions are readable
- Check if numbers/data inside cards are clear

### 2. Table Data
- Check if table text is readable
- Check if header row is distinguishable
- Check if borders are visible

### 3. Form Elements
- Check if labels are visible
- Check if input fields have visible borders
- Check if placeholder text is visible
- Check if error messages are readable

### 4. Buttons
- Check if button text is visible
- Check if disabled buttons are distinguishable
- Check if hover/active states are clear

### 5. Modals/Dialogs
- Check if headers are visible
- Check if body text is readable
- Check if buttons in modals are visible

### 6. Navigation/Menus
- Check if menu items are visible
- Check if active menu items are distinguishable
- Check if hover states are clear

## Report Issues

If you find text that's NOT visible in either theme, note:

1. **Page name:** (e.g., "Admin Dashboard")
2. **Theme:** (Light or Dark)
3. **Element:** (e.g., "Dashboard card title", "Table row text")
4. **Description:** (e.g., "Black text on dark background")
5. **Screenshot:** (optional but helpful)

## Quick Fix for Issues

If you find a visibility issue, search for the element and update the style to use CSS variables:

**Search in templates for:** `style="color: #555"` or similar

**Replace with:** `style="color: var(--text-secondary)"`

**Replace Black text with:** `color: var(--text-primary)`
**Replace Dark gray with:** `color: var(--text-secondary)`
**Replace Light text with:** Keep as white or use `color: white` in buttons

## CSS Variables Available

```css
--text-primary       /* Main text color - adapts to theme */
--text-secondary     /* Secondary text - slightly lighter */
--text-tertiary      /* Tertiary text - even lighter */
--bg-primary         /* Main background - adapts to theme */
--bg-secondary       /* Secondary background */
--bg-tertiary        /* Tertiary background */
--border-color       /* Border colors - adapts to theme */
--primary            /* Primary accent color */
--success            /* Green for success */
--warning            /* Orange for warnings */
--danger             /* Red for errors */
--info               /* Blue for info */
```

## Success Criteria

✅ All text is readable in Light Theme
✅ All text is readable in Dark Theme
✅ No text "disappears" when switching themes
✅ All form fields and labels are visible
✅ All buttons and links are visible
✅ Tables and data are clearly readable
✅ Navigation menus are clear and usable
✅ Modal dialogs display properly
✅ System theme preference changes are detected

---

**Status:** Theme visibility audit and fixes applied ✅
**Test with:** ./start_tunnel.sh then http://localhost:5000
**Report issues to:** Prajwal
