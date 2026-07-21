# Architecture Documentation - Retail Billing System

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Style](#architecture-style)
3. [Technology Stack](#technology-stack)
4. [System Components](#system-components)
5. [Data Flow](#data-flow)
6. [UI Architecture](#ui-architecture)
7. [Feature Modules](#feature-modules)
8. [Storage Architecture](#storage-architecture)
9. [Integration Points](#integration-points)
10. [Design Patterns](#design-patterns)
11. [Security Considerations](#security-considerations)
12. [Future Improvements](#future-improvements)

---

## System Overview

The Retail Billing System is a desktop point-of-sale (POS) application designed for small retail stores. It provides a comprehensive solution for managing customer transactions, calculating bills with taxes, and handling bill-related operations including saving, searching, printing, and emailing receipts.

**Version**: 1.1  
**Primary Language**: Python 3.x  
**UI Framework**: Tkinter  
**Architecture Type**: Monolithic Desktop Application

### Key Capabilities
- Multi-category product billing (Cosmetics, Groceries, Cold Drinks)
- Automated tax calculation
- Bill generation and persistence
- Cross-platform printing support
- Email delivery via SMTP
- Historical bill search and retrieval

---

## Architecture Style

### Monolithic Architecture
The application follows a **monolithic architecture** pattern with all functionality consolidated in a single `main.py` file (~557 lines). This approach is characterized by:

- **Single-tier deployment**: Runs entirely on the client machine
- **Tight coupling**: All components share the same runtime environment
- **Direct function calls**: No service boundaries or APIs
- **State management**: Global and local variables for state handling

### Event-Driven GUI Pattern
Built on Tkinter's event-driven model where user interactions trigger callback functions:
```
User Action → Event → Handler Function → UI Update
```

---

## Technology Stack

### Core Technologies
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.x | Core application logic |
| **GUI Framework** | Tkinter | User interface rendering |
| **Email** | smtplib | SMTP email delivery |
| **System Operations** | os, tempfile | File management |
| **Cross-platform** | platform, subprocess | OS detection & printing |

### Standard Library Dependencies
- `tkinter`: GUI components and layout management
- `smtplib`: Gmail SMTP integration
- `platform`: OS identification for cross-platform features
- `subprocess`: Command execution (printing on Unix-like systems)
- `random`: Bill number generation
- `os`: Directory and file operations
- `tempfile`: Temporary file creation for printing
- `messagebox`: User notifications and dialogs

---

## System Components

### Component Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                     Main Window (Tkinter)                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         Customer Details Frame                      │    │
│  │  [Name] [Phone] [Bill Number] [Search Button]      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌─────────────┬─────────────┬─────────────┬───────────┐   │
│  │  Cosmetics  │   Grocery   │ Cold Drinks │ Bill Area │   │
│  │   Frame     │   Frame     │   Frame     │  (Text)   │   │
│  │             │             │             │           │   │
│  │ 6 Products  │ 6 Products  │ 6 Products  │ Receipt   │   │
│  │ (Entry)     │ (Entry)     │ (Entry)     │ Display   │   │
│  └─────────────┴─────────────┴─────────────┴───────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Bill Menu Frame                        │    │
│  │  Prices & Taxes    │    Action Buttons             │    │
│  │  [3 Prices]        │  [Total] [Bill] [Email]       │    │
│  │  [3 Taxes]         │  [Print] [Clear]              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Functional Components

#### 1. **Input Layer**
- **Purpose**: Capture user input for products and customer details
- **Components**: 
  - 18 Entry widgets (6 per category)
  - Customer information fields (name, phone)
  - Bill number field for search

#### 2. **Business Logic Layer**
- **Purpose**: Process calculations and business rules
- **Functions**:
  - `total()`: Calculate prices and taxes
  - `bill_area()`: Generate formatted bill
  - `save_bill()`: Persist bill to filesystem
  - `search_bill()`: Retrieve historical bills

#### 3. **Output Layer**
- **Purpose**: Display and export results
- **Components**:
  - Text widget for bill display
  - Print functionality
  - Email delivery system
  - File storage

---

## Data Flow

### Primary Data Flow Sequence

```
┌──────────────┐
│ User Input   │
│ (Quantities) │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Calculate Total  │  ← total()
│ - Product Prices │
│ - Category Taxes │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Generate Bill    │  ← bill_area()
│ - Format Receipt │
│ - Display Text   │
└──────┬───────────┘
       │
       ├─────────────┐─────────────┐─────────────┐
       ▼             ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Save    │  │  Print   │  │  Email   │  │  Clear   │
│  File    │  │  Output  │  │  Send    │  │  Reset   │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

### Data Types and Structures

#### Product Categories
```python
# Cosmetics (6 items)
- Bath Soap (20 GHS)
- Face Cream (30 GHS)
- Face Wash (25 GHS)
- Hair Spray (50 GHS)
- Hair Gel (40 GHS)
- Body Lotion (60 GHS)
Tax Rate: 5%

# Grocery (6 items)
- Rice (70 GHS)
- Oil (45 GHS)
- Coffee (25 GHS)
- Tea (15 GHS)
- Sugar (32 GHS)
- Wheat (45 GHS)
Tax Rate: 6%

# Cold Drinks (6 items)
- Maaza (5 GHS)
- Pepsi (7 GHS)
- Dew (6 GHS)
- Fanta (8 GHS)
- Coca Cola (10 GHS)
- Sprite (7 GHS)
Tax Rate: 2%
```

#### Global State Variables
```python
billnumber          # Random number (200-1000)
soapprice, facecreamprice, ...  # Individual product totals
totalbill           # Grand total with taxes
```

---

## UI Architecture

### Layout Hierarchy

```
Root Window (1350x820)
│
├── Heading Label
│   └── "Retail Billing System v1.1"
│
├── Customer Details Frame (LabelFrame)
│   ├── Name Entry
│   ├── Phone Entry
│   ├── Bill Number Entry
│   └── Search Button
│
├── Products Frame (Frame)
│   ├── Cosmetics Frame (LabelFrame)
│   │   └── 6 × [Label + Entry]
│   ├── Grocery Frame (LabelFrame)
│   │   └── 6 × [Label + Entry]
│   ├── Drinks Frame (LabelFrame)
│   │   └── 6 × [Label + Entry]
│   └── Bill Frame
│       ├── Bill Area Label
│       ├── Scrollbar
│       └── Text Widget (18 rows × 60 cols)
│
└── Bill Menu Frame (LabelFrame)
    ├── Price/Tax Entries (6 fields)
    └── Button Frame
        ├── Total Button
        ├── Bill Button
        ├── Email Button
        ├── Print Button
        └── Clear Button
```

### Visual Design
- **Color Scheme**: Gray20 background, Gold text on labels
- **Fonts**: Times New Roman (headers), Arial (inputs/buttons)
- **Relief**: GROOVE effect for frames
- **Border**: Consistent 7-12 pixel borders

---

## Feature Modules

### 1. Clear Module
**Function**: `clear()`  
**Purpose**: Reset all input fields to initial state

**Algorithm**:
```
1. Insert '0' into all 18 product entries
2. Delete all content from entries (0 to END)
3. Clear tax and price display fields
4. Clear customer detail fields
5. Clear bill text area
```

**Complexity**: O(n) where n = number of input fields

---

### 2. Total Calculation Module
**Function**: `total()`  
**Purpose**: Calculate category totals and taxes

**Calculation Logic**:
```python
# For each category:
1. Product Price = Quantity × Unit Price
2. Category Total = Sum of all product prices
3. Category Tax = Category Total × Tax Rate
4. Grand Total = Sum(All Category Totals + All Taxes)
```

**Tax Rates**:
- Cosmetics: 5% (0.05)
- Grocery: 6% (0.06)
- Cold Drinks: 2% (0.02)

---

### 3. Bill Generation Module
**Function**: `bill_area()`  
**Purpose**: Create formatted receipt

**Validation Rules**:
1. Customer name and phone required
2. At least one product must have quantity > 0
3. At least one category must have non-zero total

**Bill Format**:
```
     WELCOME CUSTOMER
Bill Number: [RANDOM]
Customer Name: [NAME]
Customer Phone Number: [PHONE]
=========================
Product    QTY    Price
=========================
[Items with QTY > 0]
*************************
[Tax Lines]
Total Bill: [AMOUNT]
*************************
```

**Auto-Save**: Automatically calls `save_bill()` after generation

---

### 4. Save/Load Module

#### Save Function: `save_bill()`
**Storage Format**: Plain text files  
**Location**: `bills/` directory  
**Naming**: `{billnumber}.txt`  
**Behavior**: Creates confirmation dialog before saving

#### Search Function: `search_bill()`
**Search Method**: Exact match on bill number  
**Algorithm**:
```
1. List all files in bills/ directory
2. Split filename by '.' to get bill number
3. Compare with search query
4. If match: Load and display in text area
5. If no match: Show error dialog
```

---

### 5. Print Module
**Function**: `print_bill()`  
**Cross-Platform Support**:

| OS | Method | Command |
|----|--------|---------|
| Windows | `os.startfile()` | Built-in print dialog |
| macOS/Linux | `subprocess.run()` | `lpr` command |

**Process**:
```
1. Validate bill is not empty
2. Create temporary file with .txt extension
3. Write bill content to temp file
4. Detect operating system
5. Execute platform-specific print command
6. Clean up temporary file
```

**Error Handling**:
- No printer found
- Print command not available
- Subprocess execution failure

---

### 6. Email Module
**Function**: `send_email()`  
**Protocol**: SMTP via Gmail (smtp.gmail.com:587)

**UI Flow**:
```
1. Validate bill is not empty
2. Create modal window (Toplevel)
3. Display sender/recipient forms
4. Pre-fill message with bill content
5. Connect to Gmail SMTP server
6. Authenticate with credentials
7. Send email
8. Close modal on success
```

**Security**: Uses STARTTLS for encrypted connection

**Email Content Transformation**:
- Removes '=' characters
- Removes '*' characters
- Adjusts tab spacing for email formatting

---

## Storage Architecture

### Directory Structure
```
/project-root/
│
├── main.py                 # Application entry point
├── Readme.md               # Documentation
├── LICENSE                 # MIT License
│
├── bills/                  # Bill storage directory
│   ├── 914.txt
│   └── [billnumber].txt
│
├── icons/                  # UI assets
│   ├── billing.ico
│   └── billing_machine.png
│
└── readme-images/          # Documentation images
    ├── Image1.png
    ├── Image2.png
    └── Image3.png
```

### File Format Specification

#### Bill Text File (.txt)
- **Encoding**: UTF-8 (default)
- **Format**: Plain text with tab-separated columns
- **Line Ending**: Platform-specific (CRLF on Windows, LF on Unix)
- **Fields**:
  - Header: Customer info, bill number
  - Body: Product list with quantities and prices
  - Footer: Taxes and total

**Example Structure**:
```
\t\t\tWELCOME CUSTOMER
Bill Number: [INT]
Customer Name: [STRING]
Customer Phone Number: [STRING]

==========================================================
Product\t\t\tQTY\t\t\tPrice
==========================================================
[Product Name]\t\t\t[Quantity]\t\t\t[Price]GHS
...
*************************************************
[Tax Line]
Total Bill\t\t[Amount]
*************************************************
```

---

## Integration Points

### 1. Email Integration (SMTP)
**Service**: Gmail SMTP Server  
**Endpoint**: smtp.gmail.com:587  
**Authentication**: Username/Password  
**Protocol**: SMTP with STARTTLS

**Configuration Requirements**:
- Gmail account with "Less secure apps" enabled OR
- App-specific password for 2FA-enabled accounts

**Error Scenarios**:
- Invalid credentials
- Network connectivity issues
- SMTP server unavailable

---

### 2. Print System Integration

#### Windows Integration
- **API**: Win32 API via `os.startfile()`
- **Behavior**: Opens default system print dialog
- **Requirements**: Configured default printer

#### Unix-like Systems (macOS, Linux)
- **Command**: `lpr` (Line Printer)
- **Dependencies**: CUPS (Common Unix Printing System)
- **Fallback**: Error message if lpr not found

---

### 3. File System Integration
**Operations**:
- **Directory Creation**: `os.mkdir('bills')` on startup
- **File Write**: Text mode, UTF-8 encoding
- **File Read**: Text mode for bill search
- **Temporary Files**: `tempfile.mktemp()` for printing

**Permissions Required**:
- Read/write access to application directory
- Execute permissions for print commands (Unix)

---

## Design Patterns

### 1. Event-Driven Pattern
- **Implementation**: Tkinter event loop
- **Usage**: Button clicks trigger callback functions
- **Benefits**: Responsive UI, clear separation of concerns

### 2. Global State Pattern
- **Usage**: Global variables for prices and bill number
- **Drawback**: Tight coupling, difficult to test
- **Alternatives**: Consider class-based state management

### 3. Direct Function Invocation
- **Pattern**: Inline event handlers
- **Example**: `command=total` in Button widgets
- **Pro**: Simple, straightforward
- **Con**: Hard to extend or mock

### 4. Validation Guard Pattern
```python
if nameEntry.get() == '' or phoneEntry.get() == '':
    messagebox.showerror('Error', 'Customer Details Required')
    return
```
- **Purpose**: Input validation before processing
- **Implementation**: Early return on validation failure

---

## Security Considerations

### Current Vulnerabilities

#### 1. Email Credentials
- **Issue**: Credentials entered in plain text
- **Risk**: Password exposure through UI
- **Mitigation**: Uses password masking (show="#")
- **Improvement Needed**: Secure credential storage

#### 2. File System Access
- **Issue**: No path sanitization
- **Risk**: Directory traversal in bill search
- **Current State**: Limited to bills/ directory
- **Recommendation**: Validate bill numbers (numeric only)

#### 3. Bill Storage
- **Issue**: Bills stored as plain text
- **Risk**: No encryption for sensitive customer data
- **Compliance**: May not meet data protection regulations

### Security Best Practices (Recommendations)
1. Implement encrypted storage for customer data
2. Use environment variables or keyring for email credentials
3. Add input sanitization for all user inputs
4. Implement access controls for bill files
5. Add audit logging for sensitive operations

---

## Future Improvements

### Architecture Enhancements

#### 1. Modularization
**Current**: Monolithic single-file structure  
**Proposed**: Multi-module architecture
```
/app/
├── main.py              # Entry point
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── email_dialog.py
│   └── widgets.py
├── business/
│   ├── __init__.py
│   ├── calculator.py
│   └── bill_generator.py
├── data/
│   ├── __init__.py
│   ├── storage.py
│   └── models.py
└── config/
    ├── __init__.py
    └── settings.py
```

#### 2. MVC Pattern Implementation
```
Model (Data Layer)
  └── Product, Bill, Customer classes

View (UI Layer)
  └── Tkinter widgets and layouts

Controller (Logic Layer)
  └── Event handlers and business logic
```

### Feature Enhancements

#### 1. Database Integration
- **Current**: File-based storage
- **Proposed**: SQLite/PostgreSQL
- **Benefits**:
  - Advanced search capabilities
  - Data integrity constraints
  - Transaction support
  - Better concurrent access

**Schema Proposal**:
```sql
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE bills (
    id INTEGER PRIMARY KEY,
    bill_number INTEGER UNIQUE,
    customer_id INTEGER,
    date_created DATETIME,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE bill_items (
    id INTEGER PRIMARY KEY,
    bill_id INTEGER,
    product_name TEXT,
    quantity INTEGER,
    price DECIMAL(10,2),
    FOREIGN KEY (bill_id) REFERENCES bills(id)
);
```

#### 2. Configuration Management
- **Externalize**: Prices, tax rates, SMTP settings
- **Format**: JSON or YAML configuration files
- **Benefit**: No code changes for price updates

#### 3. Reporting Module
- **Daily Sales Reports**
- **Product Performance Analytics**
- **Customer Purchase History**
- **Tax Summary Reports**

#### 4. Barcode Integration
- **Scanner Support**: USB barcode scanner
- **Product Database**: Map barcodes to products
- **Auto-Fill**: Automatic quantity increment

#### 5. Multi-User Support
- **User Authentication**: Login system
- **Role-Based Access**: Cashier, Manager, Admin
- **Audit Trail**: Track who created each bill

#### 6. Receipt Printer Integration
- **Thermal Printer Support**: ESC/POS protocol
- **Faster Printing**: Direct hardware access
- **Professional Receipts**: Logo, formatting

### Technical Debt

#### 1. Error Handling
**Current**: Basic try-catch in email function only  
**Needed**: Comprehensive exception handling across all modules

#### 2. Input Validation
**Current**: Minimal validation (empty checks)  
**Needed**: 
- Phone number format validation
- Numeric input validation for quantities
- Email format validation

#### 3. Testing
**Current**: No automated tests  
**Needed**:
- Unit tests for calculation logic
- Integration tests for file operations
- UI tests for user workflows

#### 4. Code Quality
**Issues**:
- Magic numbers (prices hardcoded)
- Duplicated code in clear() function
- Long function bodies
- No docstrings

**Improvements**:
- Extract constants to configuration
- DRY principle application
- Function decomposition
- Add comprehensive documentation

### Performance Optimizations

#### 1. UI Responsiveness
- **Issue**: Blocking operations on main thread
- **Solution**: Threading for email/print operations

#### 2. Large Bill History
- **Issue**: Linear search through all bill files
- **Solution**: Index file or database with indexing

#### 3. Startup Time
- **Current**: GUI initialization all at once
- **Optimization**: Lazy loading for heavy widgets

---

## Conclusion

The Retail Billing System demonstrates a functional monolithic desktop application suitable for small retail operations. While the current architecture is simple and effective for its scope, the identified improvements would enhance scalability, maintainability, and security for production use.

### Architecture Strengths
- Simple, understandable structure
- Cross-platform compatibility
- No external dependencies beyond standard library
- Complete feature set for basic billing operations

### Architecture Weaknesses
- Monolithic structure limits scalability
- Global state management complicates testing
- File-based storage lacks robustness
- Security considerations need addressing

### Recommended Next Steps
1. Implement database backend (SQLite as first step)
2. Extract configuration to external files
3. Add comprehensive error handling
4. Refactor to MVC pattern
5. Implement automated testing suite
6. Add user authentication system

---

**Document Version**: 1.0  
**Last Updated**: July 2026  
**Maintainer**: Development Team
