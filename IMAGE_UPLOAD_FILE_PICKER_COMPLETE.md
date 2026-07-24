# Image Upload Feature - File Manager Integration

## Overview
The gallery now includes a full-featured image upload system with device file manager integration. Users can select images directly from their device using a native file picker dialog.

## Features

### 1. File Manager Integration
- **Click to Upload**: Click the upload zone or "Browse Files" button to open device file manager
- **Drag and Drop**: Drag images from file manager or desktop directly onto the upload zone
- **Multiple Methods**: Use both methods interchangeably

### 2. File Validation
- **File Type**: Only image files allowed (PNG, JPG, GIF, WebP, etc.)
- **File Size**: Maximum 5MB per image
- **Error Messages**: Clear feedback if file doesn't meet requirements

### 3. Auto-Fill Features
- **Title Auto-Generation**: Image filename is automatically converted to a title
- **File Info Display**: Shows file name and size for reference
- **Preview Image**: Displays selected image before upload

### 4. User Experience
- **Visual Feedback**: Clear icons and instructions
- **Loading States**: Shows "Uploading..." while file is being uploaded
- **Success Messages**: Animated success notification after upload
- **Error Handling**: Detailed error messages if upload fails

## How to Use

### Method 1: Click Upload Zone
1. Navigate to `/admin/gallery`
2. In "Add New Photo" tab
3. Click on the upload zone OR click "Browse Files" button
4. Device file manager opens
5. Select an image from your device
6. Image preview appears
7. Fill in title, description, category
8. Click "Upload Image"

### Method 2: Drag and Drop
1. Open file manager on your device
2. Drag image file onto the upload zone
3. Image preview appears
4. Fill in title, description, category
5. Click "Upload Image"

### Method 3: Via Gallery Upload Page
1. Navigate to `/admin/gallery/upload`
2. Click the upload zone or drag & drop an image
3. Fill in details
4. Click "Upload Image"

### Method 4: Manual Path Entry
1. If you have an existing image path
2. In "Add New Photo" tab, click "Browse Files"
3. Select image to auto-upload
4. Or manually enter path: `/static/uploads/image.jpg`

## File Structure

### Updated Files

#### `/templates/admin/gallery.html`
- Added file picker button next to image path input
- Added JavaScript for file upload and preview
- Shows preview after file selection

#### `/templates/admin/gallery_upload.html`
- Enhanced upload zone with better visual feedback
- Added file info display
- Improved error messages with icons
- Auto-fill title from filename
- Better upload success messaging

### Key Features in Code

#### File Input (Hidden)
```html
<input type="file" id="imageInput" accept="image/*" style="display: none;">
```
- Hidden file input triggered by clicking upload zone
- Accepts only image files

#### Upload Zone
```html
<div class="upload-zone" id="uploadZone" onclick="document.getElementById('imageInput').click();">
    <!-- Click or drag/drop images here -->
</div>
```
- Styled to show it's clickable
- Responds to drag/drop events

#### File Picker Button
```html
<button type="button" class="btn btn-primary" id="galleryFilePickerBtn">
    <i class="fas fa-folder-open"></i> Browse Files
</button>
```
- Clear button to open file picker
- Positioned next to image path input

### JavaScript Functionality

#### handleFileSelect(file)
- Validates file type (must be image)
- Validates file size (max 5MB)
- Displays preview
- Auto-fills title from filename
- Shows file information

#### uploadFileToServer(file)
- Uploads selected file to server
- Shows progress feedback
- Returns image path
- Displays image preview in form
- Auto-fills image path input

#### uploadImage()
- Validates title is provided
- Creates FormData with file and metadata
- Sends to `/admin/gallery/upload` endpoint
- Shows loading spinner during upload
- Displays success message
- Auto-reloads page after 1.5 seconds

## Validation & Error Handling

### File Type Validation
```javascript
if (!file.type.startsWith('image/')) {
    alert('❌ Please select an image file...');
    return;
}
```

### File Size Validation
```javascript
if (file.size > 5 * 1024 * 1024) {
    alert('❌ File size should be less than 5MB...');
    return;
}
```

### Title Validation
```javascript
if (!imageTitle.value.trim()) {
    alert('❌ Please enter an image title');
    return;
}
```

## User Feedback

### Success Messages
✓ "File selected: photo.jpg (1.23MB)"
✓ "✓ Success! Image 'Common Room' uploaded successfully!"

### Error Messages
❌ "Please select an image file (PNG, JPG, GIF, WebP, etc.)"
❌ "File size should be less than 5MB. Your file is 6.50MB"
❌ "Please enter an image title"
❌ "Upload failed: Network error"

### Loading States
- Upload zone shows visual feedback
- Button shows "Uploading..." spinner
- Form is disabled during upload
- Clear indication of what's happening

## Browser Compatibility

✅ **Modern Browsers**
- Chrome/Chromium
- Firefox
- Safari
- Edge

✅ **Features Supported**
- File input with accept attribute
- Drag and drop
- FileReader API
- FormData API
- Fetch API
- CSS Grid and Flexbox

## File Upload Endpoint

The feature uses the existing `/admin/gallery/upload` endpoint:

```python
@admin_bp.route('/gallery/upload', methods=['POST'])
@login_required
@admin_required
def upload_gallery_image():
    """Upload gallery image via AJAX"""
    # Validates file type (PNG, JPG, GIF, WebP)
    # Validates file size (max 5MB)
    # Saves file to /static/uploads/gallery/
    # Returns JSON with success status and image path
```

## Security Features

✅ **Admin Only**
- Only logged-in admins can upload
- Route has @admin_required decorator

✅ **File Validation**
- File type checked
- File size limited to 5MB
- Filename sanitized

✅ **CSRF Protection**
- Uses Flask's form protection
- Validates session

## Performance

- **File Size Limit**: 5MB per image
- **Upload Speed**: Depends on file size and network
- **Preview Generation**: Instant (client-side)
- **Server Processing**: < 1 second for typical image

## Screenshots

### Upload Zone
```
┌─────────────────────────────────────────┐
│  ☁️ Click to upload or drag and drop    │
│  PNG, JPG, GIF up to 5MB               │
│  🖱️ Click to open file manager          │
└─────────────────────────────────────────┘
```

### After File Selection
```
┌─────────────────────────────────────────┐
│  [Image Preview]                        │
│                                         │
│  Image Details                          │
│  ┌──────────────────────────────────┐  │
│  │ Title: Common Room               │  │
│  │ Description: [optional]          │  │
│  │ Category: Facilities             │  │
│  │                                  │  │
│  │ [Upload] [Cancel]                │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Troubleshooting

### File Manager Doesn't Open
- Check if browser supports input type="file"
- Try refreshing page
- Check browser console for errors

### Upload Fails
- Check file is less than 5MB
- Verify file is a valid image format
- Check network connection
- Ensure title is not empty

### Preview Not Showing
- Verify FileReader API is supported
- Check browser console for errors
- Try a different image file

### File Manager Shows Wrong Path
- This is browser-specific behavior
- No action needed, user can navigate

## Future Enhancements

Potential improvements:
- Multiple image upload at once
- Drag and drop directly to gallery cards
- Image cropping/editing before upload
- Compression options
- Batch upload with progress bar
- Image optimization
- Metadata extraction (EXIF)

## Testing Checklist

✓ Click upload zone opens file manager
✓ File manager shows on all devices
✓ Can drag and drop images
✓ Invalid files show error
✓ Large files show error
✓ Preview displays correctly
✓ Title auto-fills from filename
✓ Upload works
✓ Success message appears
✓ Page reloads after upload
✓ New image appears in gallery

---

**Status**: ✅ COMPLETE - File manager integration fully implemented!

Users can now easily select images from their device with the native file picker.
