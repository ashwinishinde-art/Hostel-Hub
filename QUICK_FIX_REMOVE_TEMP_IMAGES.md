# Quick Fix - Remove Temporary Images from Gallery

## Problem
Your gallery has images titled "temp" or "test" that were auto-added accidentally.

## Solution - 3 Simple Steps

### Step 1: Go to Gallery Management
```
URL: /admin/gallery
```

### Step 2: Click "Manage Photos" Tab
You'll see all images in the gallery including the temporary ones.

### Step 3: Delete Temp Images
For each image with title "temp" or "test":
1. Find the image card
2. Click the red **"Delete"** button
3. Confirm deletion in the popup
4. Image is removed

## What to Look For

### Temporary Images
- Title: "temp"
- Title: "test"
- Title: "Lights" (if uploaded without proper title)
- Recently added (at the top of the list)

### How to Identify
```
Gallery card:
┌─────────────────┐
│ [Image Preview] │
│ Title: "temp"   │ ← DELETE THIS
│ Category: ...   │
│ [Edit] [Delete] │ ← Click Delete
└─────────────────┘
```

## Step-by-Step Instructions

### 1. Log in as Admin
- Go to `/admin/gallery`

### 2. Click "Manage Photos"
```
┌──────────────────┐
│ Gallery Manage   │
├──────────────────┤
│ Add New Photo │ Manage Photos ← Click here
└──────────────────┘
```

### 3. Find Temporary Images
Look for images with these titles:
- "temp"
- "test"
- "Lights"
- Any obviously incomplete titles

### 4. Delete Each One
For each temporary image:
```
Image Card:
┌────────────────┐
│ [Preview]      │
│ Title: "temp"  │
│ Category:      │
│ [Edit][Delete] │ ← Click Delete button (red)
└────────────────┘
         ↓
Delete Confirmation:
┌────────────────────────┐
│ Are you sure you       │
│ want to delete this?   │
│                        │
│ [Cancel] [Delete]      │ ← Click Delete to confirm
└────────────────────────┘
```

### 5. Confirm Deletion
- Click **"Delete"** button in confirmation dialog
- Image is removed
- Repeat for other temp images

## Result
```
BEFORE:
Gallery has temp/test images ❌

AFTER:
Gallery has only real images ✓
```

## How to Prevent This Happening Again

The code is now fixed! Going forward:
- ✓ Select image with "Browse Files"
- ✓ Image preview shows
- ✓ Enter proper title
- ✓ Click "Add Photo"
- ✓ Image uploaded with correct title
- ✗ No more "temp" images!

## Need Help?

**Can't find Delete button?**
- Make sure you're in "Manage Photos" tab
- Not "Add New Photo" tab

**Delete button not working?**
- Refresh the page
- Try a different browser
- Check internet connection

**More temp images keep appearing?**
- The issue is now fixed
- Only new images won't have this problem
- Clean up existing ones with this guide

---

## Quick Cleanup Checklist

```
□ Go to /admin/gallery
□ Click "Manage Photos" tab
□ Find images with "temp" title
□ Click Delete button
□ Confirm deletion
□ Repeat for other temp images
□ Check gallery is clean
✓ Done!
```

**Time Needed**: 2-5 minutes

**Difficulty**: Very Easy

---

**That's it! Your gallery is now clean. 🎉**
