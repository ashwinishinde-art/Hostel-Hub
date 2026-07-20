# 🔧 TROUBLESHOOTING - ROOM COLUMN NOT SHOWING

## Step 1: Hard Refresh Browser
This is the most common cause. Do ONE of the following:

**Option A: Hard Refresh (All Browsers)**
- Press: `Ctrl + Shift + R` (Windows/Linux)
- Press: `Cmd + Shift + R` (Mac)

**Option B: Clear Cache**
- Chrome: `Ctrl + Shift + Del` → Clear browsing data
- Firefox: `Ctrl + Shift + Del` → Clear Recent History
- Safari: Develop → Empty Caches

**Option C: New Incognito Window**
- Open Incognito/Private browsing window
- Visit the page again
- This bypasses cache completely

---

## Step 2: Check Browser Console for Errors
1. Press `F12` to open Developer Tools
2. Click the "Console" tab
3. Look for any red error messages
4. Note any errors and report them

---

## Step 3: Verify Login & Navigation
1. Log out of admin dashboard
2. Log back in as admin
3. Navigate to **Admin → Student Management**
4. The page should now show the **Room No** column

---

## Step 4: Verify Changes Were Applied

### Check Template File
The file should have the Room No column header and display logic.

**Expected in template:**
```html
<th><i class="fas fa-door-open"></i> Room No</th>
```

And:
```html
{% if student.room_number %}
    <span style="...">{{ student.room_number }}</span>
{% else %}
    <span>Not Assigned</span>
{% endif %}
```

### Check Backend Query
The students route should fetch room_number from the database.

**Expected in code:**
```python
LEFT JOIN room_occupancy ro ON u.id = ro.student_id AND ro.status = 'Active'
LEFT JOIN rooms r ON ro.room_id = r.id
```

---

## Step 5: If Still Not Working

### Restart Flask Application
If Flask is still running, it might be using cached code:

1. **Stop Flask:**
   - If running in terminal: Press `Ctrl + C`

2. **Restart Flask:**
   ```bash
   python app.py
   ```

3. **Hard Refresh Browser:** `Ctrl + Shift + R`

---

## Expected Result

After these steps, you should see:

### Student List Table Headers
```
Name | Roll No | Branch | Semester | Room No | Email | Phone | Status
```

### Room Column Display

**For students WITH rooms:**
```
[101] ← styled blue badge with room number
```

**For students WITHOUT rooms:**
```
Not Assigned ← light text
```

---

## Quick Checklist

- [ ] Hard refreshed browser (Ctrl+Shift+R)
- [ ] Checked for errors in browser console (F12)
- [ ] Logged out and back in
- [ ] Restarted Flask application
- [ ] Can see "Room No" column header
- [ ] Can see room numbers or "Not Assigned" in cells

---

## If You Still Don't See It

Please check and report:

1. **Browser Console Error:** Any red errors? Copy and paste them
2. **Flask Terminal:** Any error messages when accessing the page?
3. **Room Number in Database:** Are students actually assigned to rooms?
   - Check by looking at allocated rooms in Room Management
4. **Browser Type:** Which browser are you using?
5. **Screenshot:** Can you take a screenshot of the Student Management page?

---

## Common Issues & Solutions

### Issue: Column added but shows only "Not Assigned"
**Solution:** Students need to be allocated to rooms first. Go to Admin → Allocate Room and assign students to rooms.

### Issue: Page shows old data
**Solution:** Clear browser cache completely (Incognito window) or restart Flask.

### Issue: Column header missing but some content shows
**Solution:** Hard refresh browser and restart Flask application.

### Issue: "Room No" text but no values
**Solution:** Check if students have active room allocations. If not, assign rooms first.

---

**Please try these steps and let me know if the Room No column is now visible!**
