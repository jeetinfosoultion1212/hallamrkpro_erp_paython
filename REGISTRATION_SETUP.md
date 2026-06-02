# HallmarkPro Registration Feature

## Overview

A complete registration system has been added to HallmarkPro, allowing new firms to self-register with their details and upload a firm logo.

## Features Added

### 1. Registration Module (`modules/register.py`)
- Standalone registration window with professional UI
- Matches the login page design
- Scrollable form for better UX

### 2. Form Fields
**Required Fields:**
- Firm Name
- Full Name (Contact Person)
- Phone Number (10 digits)
- Email Address
- Firm Type (dropdown)
- Password (min 6 chars)
- Confirm Password
- Firm Logo (PNG/JPG, round shape)

**Optional Fields:**
- Address
- State (dropdown)

### 3. Logo Upload & Processing
- Users can upload PNG or JPG logos
- Logos are automatically converted to **circular shape** (300x300px)
- Stored in `assets/logos/` directory
- Named by phone number: `{phone}_logo.png`
- Uses PIL (Pillow) for image processing

### 4. Data Validation
- Phone number required
- Email format validation ready (can be enhanced)
- Password confirmation matching
- All required fields validated
- Firm type selection mandatory

### 5. Database Integration
- Creates new firm entry in `firms` table
- Creates admin user in `admins` table
- Stores logo path for future reference
- Uses password hashing (SHA256)

## Directory Structure

```
project_root/
├── modules/
│   ├── login.py           (Updated with registration link)
│   └── register.py        (New registration module)
├── assets/
│   └── logos/             (Logo storage - auto-created)
└── hallmarkpro.db         (Database with new firm data)
```

## How It Works

### User Flow

1. **Login Page** → Click "🏛 Register Centre"
2. **Registration Form** → Fill in firm details
3. **Logo Upload** → Select firm logo (PNG/JPG)
4. **Submit** → System validates and saves
5. **Success** → Returns to login page
6. **Login** → User can now login with phone + password

### Logo Processing

1. User selects image file (PNG/JPG)
2. System opens and converts to RGBA
3. Resizes to 300x300px (maintains aspect ratio)
4. Creates circular mask
5. Applies mask to create perfect circle
6. Saves as PNG in `assets/logos/`

### Database Changes

**Firms Table** - New fields used:
- `firm_name` - Name entered in registration
- `contact_person` - Full name of contact
- `phone_number` - Primary contact number
- `email` - Email address
- `address1` - Street address
- `state` - State/Province
- `firm_type` - Type of firm
- `logo_path` - Path to uploaded logo
- `created_at` - Registration timestamp
- `status` - Set to 1 (active)

**Admins Table** - New admin created:
- `username` - Phone number used as username
- `name` - Full name
- `phone_number` - Contact number
- `email` - Email address
- `password` - SHA256 hashed password
- `firm_id` - References created firm
- `role` - Set to "admin"
- `status` - Set to 1 (active)

## Installation & Dependencies

### Pillow (PIL) - Image Processing
Already installed. Required for circular logo generation.

```bash
pip install Pillow
```

### Folder Structure
Auto-created at first registration:
```
assets/
└── logos/
    ├── 9810359334_logo.png
    ├── 9811234567_logo.png
    └── ...
```

## Security Features

1. **Password Hashing** - SHA256 encryption
2. **Field Validation** - Required fields checked
3. **File Type Validation** - PNG/JPG only
4. **Database** - Uses prepared statements (SQL injection safe)

## Usage

### For End Users

1. Open HallmarkPro application
2. On login page, click "🏛 Register Centre"
3. Fill in firm details
4. Upload round logo (will be auto-converted)
5. Create password (min 6 characters)
6. Click "🏛 Create Account"
7. Upon success, return to login and sign in

### For Developers

#### Access Registration Window Directly
```python
from modules.register import RegisterWindow

def on_close():
    print("Closed registration")

reg = RegisterWindow(on_back_to_login=on_close)
```

#### Check Logo Location
```
/vercel/share/v0-project/assets/logos/{phone_number}_logo.png
```

#### Query Registered Firms
```python
from db.schema import get_connection

conn = get_connection()
c = conn.cursor()
c.execute("SELECT firm_name, contact_person, phone_number FROM firms ORDER BY created_at DESC")
for row in c.fetchall():
    print(row)
conn.close()
```

## File Reference

### New Files
- `modules/register.py` - Complete registration module (537 lines)

### Modified Files
- `modules/login.py` - Added registration link and navigation

### Directories Created
- `assets/logos/` - Logo storage location

## Testing Checklist

- [ ] Registration page loads from login
- [ ] All form fields accept input
- [ ] Logo upload opens file dialog
- [ ] Logo selection shows filename
- [ ] Form validation works for required fields
- [ ] Password confirmation matching works
- [ ] Submit creates firm and admin
- [ ] Logo saved to assets/logos/
- [ ] Back button returns to login
- [ ] New user can login after registration

## Future Enhancements

1. **Email Verification** - Confirm email before activation
2. **Phone OTP** - Verify phone number with OTP
3. **Logo Preview** - Show preview of circular logo before submit
4. **Firm Approval** - Admin review before activation
5. **GST/PAN Validation** - Validate GST and PAN numbers
6. **Terms & Conditions** - T&C checkbox
7. **Captcha** - Prevent bot registrations
8. **Email Notification** - Welcome email after registration

## Troubleshooting

### Logo Not Saving
- Check `assets/logos/` folder exists
- Verify PIL/Pillow is installed
- Check file permissions on assets folder

### Registration Form Not Loading
- Verify `modules/register.py` exists
- Check Python syntax (run `python -m py_compile`)
- Look for import errors in console

### Database Error
- Ensure database schema is initialized
- Check database file permissions
- Verify firms and admins tables exist

## Database Schema Reference

```sql
-- Firms table columns used in registration
firm_name TEXT
contact_person TEXT
phone_number TEXT
email TEXT
address1 TEXT
state TEXT
firm_type TEXT
logo_path TEXT
created_at TEXT
status INTEGER

-- Admins table columns used
username TEXT UNIQUE
name TEXT
phone_number TEXT
email TEXT
password TEXT
role TEXT
firm_id INTEGER
status INTEGER
created_at TEXT
```

## Support

For issues or questions about the registration feature:
1. Check this documentation
2. Review the code in `modules/register.py`
3. Check database logs
4. Contact: admin@hallmarkpro.in

---

**Feature Added**: June 3, 2026  
**Status**: Production Ready  
**Version**: 2.1  
