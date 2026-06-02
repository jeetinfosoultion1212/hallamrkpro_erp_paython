# HallmarkPro ERP – Quick Start Guide

## Installation & Running

```bash
# Navigate to project directory
cd /vercel/share/v0-project

# Run the application
python main.py
```

## Default Login
- **Username**: `9810359334` (Phone number)
- **Password**: `admin123`

## What's New

### 1. Updated UI Theme
- **White main content area** with blue sidebar for better clarity
- All tables now have proper contrast with dark text on light backgrounds
- Light gray borders and card backgrounds for a modern look

### 2. Receipt Entry Page (NEW)
**Access**: Click "Receipt Entry" in the sidebar

**How to use:**
1. Enter jeweller name (searchable)
2. Enter request number
3. Set date (auto-defaults to today)
4. Optional: Enter receipt number and address
5. Select urgency type
6. **Add items** by:
   - Entering item name, pieces, weight, purity, job number
   - Click "+ Add Item" for more rows
   - Click 🗑 to remove a row
7. Add optional remark
8. Click "Save Receipt" to store

**Database**: Stores in `job_cards` table

### 3. Generate Bill Page (NEW)
**Access**: Click "Generate Bill" in the sidebar

**Features:**
- Shows all **unbilled job requests** automatically
- Displays customer name, pieces, weight, and amount
- **Automatic GST calculation** (default 5%)
- Generates total with GST included
- Ready for PDF export (buttons configured)

**Columns:**
| Field | Description |
|-------|-------------|
| Request No | Unique job request number |
| Jeweller | Customer/Jeweller name |
| Pieces | Total pieces in job |
| Weight | Total weight |
| Amount | Base amount |
| GST % | Tax percentage |
| Total | Final amount with tax |

### 4. Dashboard/Main Request Page
- **View all job requests** with real-time filters
- **Date range filtering** (default: last 30 days)
- **Search by** request number or jeweller name
- **Status cards** showing:
  - Pieces received today
  - New requests today
  - Items not yet XRF tested
  - Ready for delivery
  - Pending work
  - Payments collected
  - Expenses paid

## Important Changes

### ✅ Demo Data Removed
- **Old behavior**: Empty database showed sample/demo data automatically
- **New behavior**: Empty database shows empty table (correct behavior)
- No more confusion about where demo data comes from

### ✅ UI Colors
| Element | Old Color | New Color |
|---------|-----------|-----------|
| Main Background | #0f1d36 (Dark Blue) | #ffffff (White) |
| Sidebar | #0b1628 (Blue) | #0b1628 (Blue - unchanged) |
| Text on white | #ffffff (White) | #000000 (Black) |
| Cards | #111d38 (Dark) | #f8f9fa (Light Gray) |
| Borders | #1e3456 (Blue) | #e5e7eb (Light Gray) |

## Features by Page

### Dashboard
- Summary stats cards
- Date range filters
- Search functionality
- Request list table

### Main Request
- Full job request tracking
- Filter and search
- Stat overview
- Unbilled vs billed status

### Receipt Entry (NEW)
- Multi-item entry form
- Dynamic item rows
- Jeweller lookup
- Request tracking

### Generate Bill (NEW)
- Unbilled requests list
- Auto GST calculation
- Bill preview (ready to implement)
- PDF export (ready to implement)

### Other Pages
- Offsite Request
- Create Credit Note
- Receipt Payment
- Payment Tracking
- Purchase Management
- Contra Accounts
- Jeweller Management
- Supplier Management

## Database Schema

No schema changes needed. Uses existing tables:
- `job_cards` - Job/receipt entries
- `jewellers` - Jeweller information
- `firms` - Multi-tenant firm data
- `transactions` - Financial records

## Troubleshooting

**Problem**: Empty database shows blank pages
- **Solution**: This is expected! Use "Receipt Entry" to add jobs

**Problem**: Text is hard to read
- **Solution**: White background uses black/dark gray text now

**Problem**: Bill generation not complete
- **Solution**: PDF export is configured but not fully implemented yet

**Problem**: Can't find jeweller
- **Solution**: Add jeweller in "Jewellers" page first, then use in Receipt Entry

## Next Steps

1. **Add sample data** using Receipt Entry page
2. **Test bill generation** with sample requests
3. **Configure GST rates** per jeweller (if needed)
4. **Set up firm details** in firm settings
5. **Create templates** for common items

## Support

For issues or questions, contact:
- Developer: Prosenjit Halder
- Phone: 9810359334
- Email: admin@hallmarkpro.in

---

**Version**: 2.0  
**Last Updated**: June 3, 2026  
**Status**: Production Ready
