# Architecture — Retail Billing System

## 1. Overview

The Retail Billing System is a desktop GUI application written in Python using the **Tkinter** standard-library toolkit. It is designed for small retail stores and supports product quantity entry across three categories, automatic price and tax calculation, bill generation, local persistence, bill search, printing, and email delivery.

The entire application is contained in a **single source file** (`main.py`) with no third-party dependencies; it relies exclusively on Python's standard library.

---

## 2. Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| GUI framework | Tkinter (stdlib) |
| Email transport | `smtplib` + Gmail SMTP (TLS, port 587) |
| Printing | `os.startfile` (Windows) / `lpr` subprocess (macOS & Linux) |
| Persistence | Local flat-file storage (`bills/` directory, `.txt` files) |
| OS detection | `platform` (stdlib) |
| Temp files | `tempfile` (stdlib) |

---

## 3. Repository Structure

```
BillingSystem/
├── main.py            # Entire application — logic + GUI
├── bills/             # Auto-created at startup; stores saved bill .txt files
│   └── <bill_number>.txt
├── icons/
│   ├── billing.ico
│   └── billing_machine.png
├── readme-images/
│   ├── Image1.png
│   ├── Image2.png
│   └── Image3.png
├── Readme.md
└── LICENSE
```

---

## 4. Application Architecture

Because the application is a single-file Tkinter script, it follows a **flat, procedural architecture** common to simple GUI desktop apps. There are no classes, modules, or packages. The file is divided into two logical sections:

1. **Function definitions** — all business logic and event-handler callbacks (lines 1–317).
2. **GUI construction + main loop** — all widget instantiation and layout using `root = Tk()` (lines 319–557).

### 4.1 High-Level Component Diagram

```
┌─────────────────────────────────────────────────────┐
│                   Tkinter Root Window                │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │          Customer Details Frame              │   │
│  │  Name | Phone | Bill Number | [SEARCH]       │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──┐ │
│  │ Cosmetics  │ │  Grocery   │ │Cold Drinks │ │  │ │
│  │   Frame    │ │   Frame    │ │   Frame    │ │B │ │
│  │ (6 items)  │ │ (6 items)  │ │ (6 items)  │ │i │ │
│  └────────────┘ └────────────┘ └────────────┘ │l │ │
│                                               │l │ │
│                                               │  │ │
│                                               │A │ │
│                                               │r │ │
│                                               │e │ │
│                                               │a │ │
│                                               └──┘ │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │               Bill Menu Frame                │   │
│  │  Cosmetic/Grocery/Drinks Price + Tax         │   │
│  │  [Total] [Bill] [Email] [Print] [Clear]      │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 5. GUI Layout

The main window (`root`) is built using **pack** and **grid** geometry managers. Three nested frames organise the interface:

| Frame | Geometry | Purpose |
|---|---|---|
| `customer_details_frame` | `pack(fill=X)` | Name, phone, bill number inputs + Search button |
| `productsFrame` | `pack()` | Container for 4 side-by-side sub-frames (3 product columns + bill area) |
| `cosmeticsFrame` | `grid(row=0, col=0)` | 6 cosmetic item quantity entries |
| `groceryFrame` | `grid(row=0, col=1)` | 6 grocery item quantity entries |
| `drinksFrame` | `grid(row=0, col=2)` | 6 cold drink quantity entries |
| `billframe` | `grid(row=0, col=3)` | Scrollable `Text` widget showing the rendered bill |
| `billmenuFrame` | `pack()` | Subtotal / tax read-only fields + action buttons |
| `buttonFrame` | inside `billmenuFrame` | Total, Bill, Email, Print, Clear buttons |

---

## 6. Core Functions (Business Logic)

### 6.1 `total()`
Calculates per-item, per-category, and overall totals.

**Flow:**
1. Read quantity from each `Entry` widget.
2. Multiply by hardcoded unit price (see §8).
3. Sum each category subtotal.
4. Apply category tax rate (see §8).
5. Write subtotals and taxes back into the read-only `Entry` widgets in the Bill Menu.
6. Store individual item prices and grand total in **global variables** for later use by `bill_area()`.

### 6.2 `bill_area()`
Generates the formatted bill text and triggers save.

**Flow:**
1. Validate that customer name, phone, and at least one product are provided.
2. Clear the `textarea` widget.
3. Write bill header (bill number, customer details).
4. Iterate through non-zero item quantities, appending formatted lines.
5. Append tax summary and grand total.
6. Call `save_bill()` automatically.

### 6.3 `save_bill()`
Persists the current bill as a plain-text file.

**Flow:**
1. Prompt user for confirmation via `messagebox.askyesno`.
2. Read the full bill text from the `textarea` widget.
3. Write to `bills/<billnumber>.txt`.
4. Generate a new random bill number (200–1000) for the next transaction.

### 6.4 `search_bill()`
Loads a previously saved bill from disk.

**Flow:**
1. Iterate over all files in the `bills/` directory.
2. Match filename stem against the value in `billnumberEntry`.
3. On match: read file contents into `textarea`.
4. On no match: show error dialog.

### 6.5 `print_bill()`
Sends the bill to the system printer in a cross-platform way.

**Flow:**
1. Write bill text to a temporary `.txt` file (`tempfile.mktemp`).
2. Detect OS via `platform.system()`:
   - **Windows** → `os.startfile(file, 'print')`
   - **macOS / Linux** → `subprocess.run(['lpr', file])`
3. Delete the temporary file.

### 6.6 `send_email()`
Sends the bill via Gmail SMTP in a modal child window.

**Flow:**
1. Open a `Toplevel` window (`root1`) with sender email, password, and recipient fields.
2. Pre-populate an editable `Text` widget with the current bill (stripping formatting characters).
3. On "SEND": authenticate with `smtplib.SMTP('smtp.gmail.com', 587)`, call `starttls()`, `login()`, `sendmail()`, then `quit()`.

### 6.7 `clear()`
Resets all `Entry` widgets to `0` and clears the `textarea`.

---

## 7. Data Flow

```
User enters quantities
        │
        ▼
   [Total button]
        │
        ▼
  total() — computes prices, taxes, grand total
  → updates subtotal/tax Entry widgets
  → stores values in global variables
        │
        ▼
   [Bill button]
        │
        ▼
  bill_area() — formats bill text → textarea
        │
        ├──► save_bill() — writes bills/<N>.txt
        │
        ▼
  User chooses action:
    ├── [Print]  → print_bill()  → lpr / os.startfile
    ├── [Email]  → send_email()  → Gmail SMTP
    └── [Clear]  → clear()       → reset all widgets
```

---

## 8. Hardcoded Pricing and Tax Rates

All prices (in GHS — Ghanaian Cedi) and tax rates are constants embedded inside `total()`.

### Cosmetics (Tax: 5%)

| Item | Unit Price (GHS) |
|---|---|
| Bath Soap | 20 |
| Face Cream | 30 |
| Face Wash | 25 |
| Hair Spray | 50 |
| Hair Gel | 40 |
| Body Lotion | 60 |

### Grocery (Tax: 6%)

| Item | Unit Price (GHS) |
|---|---|
| Rice | 70 |
| Oil | 45 |
| Coffee | 25 |
| Tea | 15 |
| Sugar | 32 |
| Wheat | 45 |

### Cold Drinks (Tax: 2%)

| Item | Unit Price (GHS) |
|---|---|
| Maaza | 5 |
| Pepsi | 7 |
| Mountain Dew | 6 |
| Fanta | 8 |
| Coca Cola | 10 |
| Sprite | 7 |

---

## 9. Data Persistence

- **Format**: Plain text (`.txt`), human-readable, tab-separated columns.
- **Location**: `bills/` directory (created automatically on startup if absent via `os.makedirs`).
- **Naming**: `<billnumber>.txt` where bill number is a random integer in the range [200, 1000].
- **Lifecycle**: A new random bill number is assigned after each successful save.
- **Search**: Linear scan of directory listing — no index or database.

---

## 10. Global State

The application uses Python **global variables** to pass computed values between functions, as Tkinter `Entry` widgets cannot directly return formatted numbers to callbacks:

| Variable | Type | Description |
|---|---|---|
| `billnumber` | `int` | Current bill number (random 200–1000) |
| `soapprice` … `spriteprice` | `int` | Per-item total price (qty × unit price) |
| `totalbill` | `float` | Grand total including all taxes |

---

## 11. Error Handling

All user-facing errors are surfaced through Tkinter `messagebox` dialogs:

| Scenario | Dialog type |
|---|---|
| Customer details missing | `showerror` |
| No products selected | `showerror` |
| Bill text area empty (print/email) | `showerror` |
| Bill number not found on search | `showerror` |
| SMTP / email failure | `showerror` |
| Printer not found (Unix) | `showerror` |
| Save confirmation | `askyesno` |
| Successful save | `showinfo` |
| Successful email send | `showinfo` |

---

## 12. Known Limitations and Design Notes

- **Single-file, procedural**: All logic and UI code is in `main.py`. There is no separation of concerns (MVC/MVP). Scaling the product catalogue or categories would require significant refactoring.
- **Hardcoded prices**: Unit prices and tax rates are literals inside `total()`. No configuration file or database is used.
- **No input validation**: Quantities are cast with `int()` without try/except; non-numeric input will crash `total()`.
- **Bill number collisions**: The random range [200, 1000] is small; bill files can be overwritten silently.
- **Email credentials**: The sender's Gmail password is entered in plaintext in the UI. Google has deprecated "less secure app" access; an App Password is required if 2FA is enabled.
- **`search_bill` bug**: The loop shows an error dialog on every non-matching file rather than only after exhausting the entire list.
- **No tests**: There is no test suite (unit, integration, or UI).
- **No CI/CD**: No build scripts, Makefiles, Dockerfiles, or pipeline configuration files are present.
