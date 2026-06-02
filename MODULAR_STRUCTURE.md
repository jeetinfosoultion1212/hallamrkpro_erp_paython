# HallmarkPro ERP - Modular Architecture

## Project Structure (Refactored)

After refactoring, the project now follows a clean **modular design pattern** with separate files for each functional page.

```
modules/
├── dashboard.py          # Main dashboard controller & page routing
├── receipt_entry.py      # Receipt Entry page (NEW)
├── generate_bill.py      # Generate Bill page (NEW)
├── login.py              # Login page
└── [other pages]         # Other module pages
```

## Why Modular?

✅ **Better Organization**
- Each page has its own dedicated file
- Easier to locate and modify specific functionality
- Cleaner separation of concerns

✅ **Improved Maintainability**
- Smaller files = easier to understand
- Less cognitive load when working on a page
- Reduced risk of unintended side effects

✅ **Scalability**
- Adding new pages is straightforward
- Team members can work on different pages simultaneously
- Less merge conflicts in version control

✅ **Code Reusability**
- Page classes can be imported and reused
- Common patterns extracted into shared modules
- Easier to create variations of existing pages

✅ **Testing**
- Each page can be tested independently
- Isolated unit tests are simpler to write
- Better test coverage possible

## Module Descriptions

### 1. `dashboard.py` (555 lines)
**Purpose**: Main application controller and page routing

**Responsibilities**:
- Application window setup and styling
- Sidebar navigation menu
- Page routing/switching logic
- Main request dashboard (request list, stats, filters)
- Dashboard statistics loading
- Color scheme and theme definitions

**Key Classes**:
- `Dashboard` - Main application class

**Imports from**:
- `receipt_entry.ReceiptEntryPage`
- `generate_bill.GenerateBillPage`
- `db.schema.get_connection`

### 2. `receipt_entry.py` (252 lines) - NEW
**Purpose**: Jewelry receipt entry functionality

**Responsibilities**:
- Receipt entry form UI
- Dynamic item row management
- Form validation
- Database insertion
- User feedback (success/error messages)

**Key Classes**:
- `ReceiptEntryPage` - Receipt entry page handler

**Features**:
- Jeweller field (searchable)
- Request number field
- Date picker
- Receipt number (optional)
- Address auto-fill
- Urgency type selector
- Dynamic items table with add/remove
- Remark field
- Save & Reset buttons

**Database Operations**:
- INSERT into `job_cards` table
- Reads from `jewellers` table (for lookup)

### 3. `generate_bill.py` (176 lines) - NEW
**Purpose**: Bill generation from unbilled requests

**Responsibilities**:
- Unbilled request listing
- Bill generation logic
- GST calculations
- PDF export handling
- Preview functionality

**Key Classes**:
- `GenerateBillPage` - Bill generation page handler

**Features**:
- Table of unbilled requests
- Request selection
- GST rate calculation (5% default)
- Total calculation with tax
- Generate bills button
- Preview button
- Export as PDF button

**Database Operations**:
- SELECT from `job_cards` (unbilled)
- SELECT from `jewellers` (for name mapping)
- UPDATE `job_cards` (mark as billed)

## How Page Routing Works

### In `dashboard.py` - `_show_page()` method:

```python
def _show_page(self, key):
    for w in self.content_frame.winfo_children():
        w.destroy()
    
    if key == "main_request":
        self._build_main_request(self.content_frame)
    elif key == "dashboard":
        self._build_dashboard_page(self.content_frame)
    elif key == "receipt_entry":
        ReceiptEntryPage(self.content_frame, self.admin)  # Instantiate module
    elif key == "generate_bill":
        GenerateBillPage(self.content_frame, self.admin)  # Instantiate module
    else:
        self._build_placeholder(self.content_frame, key)
```

### How It Works:

1. **Sidebar clicked** → triggers `_show_page(key)` with page key
2. **Clear previous page** → destroy all widgets in `content_frame`
3. **Route to correct page**:
   - If built-in → call `_build_*` method
   - If modular → instantiate page class
4. **Page loads** → page class constructor builds UI in provided frame

## Adding a New Modular Page

### Step 1: Create new module file
Create `modules/my_new_page.py`:

```python
import tkinter as tk
from tkinter import ttk

class MyNewPage:
    def __init__(self, parent, admin):
        self.parent = parent
        self.admin = admin
        self.build()
    
    def build(self):
        """Build the page UI"""
        # Your UI code here
        tk.Label(self.parent, text="My New Page",
                font=("Segoe UI", 18, "bold")).pack()
```

### Step 2: Import in dashboard.py
```python
from .my_new_page import MyNewPage
```

### Step 3: Add to page router
```python
elif key == "my_new_page":
    MyNewPage(self.content_frame, self.admin)
```

### Step 4: Add to sidebar menu (optional)
In `SIDEBAR_SECTIONS` dictionary in `dashboard.py`:
```python
("my_new_page", "My New Page", "icon"),
```

That's it! Your new page is now integrated.

## Shared Resources

### Color Palette
Each module defines its own color constants to be self-contained:
```python
BG_MAIN      = "#ffffff"
BG_CARD      = "#f8f9fa"
TEXT_BLACK   = "#000000"
ACCENT_BLUE  = "#4361ee"
```

### Database Connection
All modules import from `db.schema`:
```python
from db.schema import get_connection

conn = get_connection()
c = conn.cursor()
# ... query execution
```

### Admin Data
Admin information is passed to each page:
```python
ReceiptEntryPage(parent_frame, admin_dict)
# admin_dict contains: {"id": 1, "firm_id": 1, "name": "...", etc}
```

## Benefits of This Structure

| Aspect | Before | After |
|--------|--------|-------|
| Largest file | 870+ lines | 555 lines |
| Page isolation | Mixed together | Separate files |
| Testing | Difficult | Easy per-page |
| Maintenance | Hard to find code | Clear organization |
| Team collaboration | Many conflicts | Independent work |
| Code reuse | Low | High |
| Scalability | Limited | Excellent |

## File Statistics

```
dashboard.py:      555 lines (down from 870)
receipt_entry.py:  252 lines (new)
generate_bill.py:  176 lines (new)
─────────────────────────────
Total:             983 lines (organized into modules)
```

## Next Steps

### If adding more pages:
1. Create `modules/page_name.py` with `PageNameClass`
2. Add import in `dashboard.py`
3. Add route in `_show_page()` method
4. Add sidebar menu item (optional)

### If extending existing pages:
- Edit the specific module file
- No need to touch other pages
- Self-contained changes

### For testing:
- Import and test each page class independently
- Mock the `admin` parameter
- No need to initialize full Dashboard

## Conclusion

The refactored structure makes HallmarkPro ERP more **professional**, **maintainable**, and **scalable**. Each module is self-contained, easy to understand, and can be developed/tested independently.

---

**Last Updated**: June 3, 2026  
**Version**: 2.0 (Modular)  
**Status**: Production Ready
