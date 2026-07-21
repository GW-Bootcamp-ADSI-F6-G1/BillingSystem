# Architecture — Retail Billing System v1.1

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Repository Structure](#3-repository-structure)
4. [Application Architecture](#4-application-architecture)
5. [GUI Layout](#5-gui-layout)
6. [Core Functions](#6-core-functions)
7. [Data Model & State Management](#7-data-model--state-management)
8. [Product Catalogue & Pricing](#8-product-catalogue--pricing)
9. [Tax Calculation](#9-tax-calculation)
10. [Data Persistence](#10-data-persistence)
11. [External Integrations](#11-external-integrations)
12. [Cross-Platform Printing](#12-cross-platform-printing)
13. [Control Flow](#13-control-flow)
14. [Known Limitations & Design Notes](#14-known-limitations--design-notes)

---

## 1. Project Overview

The **Retail Billing System** is a single-file, desktop point-of-sale (POS) application targeted at small retail stores. It provides a graphical interface for:

- Entering item quantities across three product categories (Cosmetics, Groceries, Cold Drinks)
- Computing per-category subtotals, taxes, and a grand total
- Generating and displaying a formatted bill
- Saving bills to the local filesystem
- Retrieving past bills by bill number
- Printing bills to a system printer
- Emailing bills to a recipient via Gmail SMTP

The application requires no installation beyond a standard Python 3.x environment and has no third-party dependencies.

---

## 2. Technology Stack

| Concern | Technology |
|---|---|
| Language | Python 3.x |
| GUI framework | `tkinter` (Python standard library) |
| Email delivery | `smtplib` (Python standard library) |
| Printing | `os.startfile` (Windows) / `subprocess` + `lpr` (Unix) |
| File I/O | `os`, `tempfile` (Python standard library) |
| OS detection | `platform` (Python standard library) |
| Randomisation | `random` (Python standard library) |

No third-party packages or package manager files (e.g., `requirements.txt`, `pyproject.toml`) are present.

---

## 3. Repository Structure

```
BillingSystem/
├── main.py            # Entire application — UI, logic, and entry point
├── Readme.md          # Project documentation
├── LICENSE            # MIT licence
├── bills/             # Auto-created at runtime; stores saved bill .txt files
│   └── <billnumber>.txt
├── icons/
│   ├── billing.ico            # Application icon (Windows)
│   └── billing_machine.png    # Application icon (other platforms)
└── readme-images/
    ├── Image1.png
    ├── Image2.png
    └── Image3.png
```

The entire application lives in **one file** (`main.py`). There are no modules, packages, classes, or separate configuration files.

---

## 4. Application Architecture

The application follows a **monolithic, procedural, single-file** architecture pattern:

```
main.py
├── Function definitions (business logic + UI callbacks)
│   ├── clear()
│   ├── send_email()
│   ├── print_bill()
│   ├── search_bill()
│   ├── save_bill()
│   ├── bill_area()
│   └── total()
│
└── Top-level script body (executed at run time)
    ├── Global variable declarations (billnumber, price globals)
    ├── bills/ directory bootstrap
    └── Tkinter widget tree construction + root.mainloop()
```

There is no separation of concerns between the presentation layer and the business logic layer. Tkinter widget references (e.g., `bathsoapEntry`, `textarea`) are module-level globals accessed directly by every function.

---

## 5. GUI Layout

The root window is **1350 × 820 px** with a dark theme (`bg='gray20'`, accent colour `fg='gold'`).

```
root  (Tk — "Retail Billing System v1.1")
│
├── headingLabel              Label — application title banner
│
├── customer_details_frame    LabelFrame — customer header row
│   ├── nameEntry             Entry  — customer name
│   ├── phoneEntry            Entry  — customer phone
│   ├── billnumberEntry       Entry  — bill number (read/search)
│   └── searchButton          Button → search_bill()
│
├── productsFrame             Frame — horizontal product layout (grid)
│   ├── cosmeticsFrame        LabelFrame  col 0 — 6 cosmetic item entries
│   ├── groceryFrame          LabelFrame  col 1 — 6 grocery item entries
│   ├── drinksFrame           LabelFrame  col 2 — 6 cold drink entries
│   └── billframe             Frame       col 3 — scrollable bill text area
│       └── textarea          Text (60 × 18 chars, vertical scrollbar)
│
└── billmenuFrame             LabelFrame — summary + actions
    ├── costmeticpriceEntry   Entry  — cosmetics subtotal (auto-filled)
    ├── grocerypriceEntry     Entry  — grocery subtotal (auto-filled)
    ├── drinkspriceEntry      Entry  — drinks subtotal (auto-filled)
    ├── cosmetictaxEntry      Entry  — cosmetics tax (auto-filled)
    ├── grocerytaxEntry       Entry  — grocery tax (auto-filled)
    ├── drinkstaxEntry        Entry  — drinks tax (auto-filled)
    └── buttonFrame           Frame
        ├── totalButton       Button → total()
        ├── billButton        Button → bill_area()
        ├── emailButton       Button → send_email()
        ├── printButton       Button → print_bill()
        └── clearButton       Button → clear()
```

The email dialog is rendered as a modal `Toplevel` window created dynamically inside `send_email()`.

---

## 6. Core Functions

### `total()`
Reads all product quantity entries, multiplies by hardcoded unit prices, sums each category, calculates per-category tax, and writes results back into the summary `Entry` widgets. Stores computed prices and the grand total in global variables for use by `bill_area()`.

### `bill_area()`
Validates that customer details and at least one non-zero item are present, then formats and writes the complete bill text into `textarea`. Immediately calls `save_bill()` upon successful bill generation.

### `save_bill()`
Reads the content of `textarea`, prompts the user for confirmation via `messagebox.askyesno`, then writes the bill to `bills/{billnumber}.txt`. After saving, generates a new random bill number in the range [200, 1000].

### `search_bill()`
Iterates over files in the `bills/` directory and matches the filename stem against the value in `billnumberEntry`. If found, loads the file content into `textarea`; otherwise shows an error dialog.

### `print_bill()`
Validates that `textarea` is non-empty, writes its content to a temporary file, then dispatches to the OS-appropriate print command (see [Cross-Platform Printing](#12-cross-platform-printing)). Deletes the temp file after dispatch.

### `send_email()`
Creates a modal `Toplevel` window with fields for sender email, sender password, recipient email, and a pre-populated message body (bill content with decorative characters stripped). The inner function `send_gmail()` opens a TLS connection to `smtp.gmail.com:587` and sends the message.

### `clear()`
Resets all product `Entry` widgets to `'0'` (insert-then-delete pattern), clears the summary entries, customer fields, and `textarea`.

---

## 7. Data Model & State Management

There is no database or structured data model. All state is held in **module-level global Python variables** and **Tkinter widget state**:

| Variable | Type | Description |
|---|---|---|
| `billnumber` | `int` | Current bill number (random 200–1000); regenerated after each save |
| `soapprice` … `spriteprice` | `int` | Per-item computed price (qty × unit price); set by `total()` |
| `totalbill` | `float` | Grand total including all taxes; set by `total()` |

Widget references (all module-level):

- **Product entries**: `bathsoapEntry`, `facecreamEntry`, `facewashEntry`, `hairsprayEntry`, `hairgelEntry`, `bodylotionEntry`, `riceEntry`, `oilEntry`, `coffeeEntry`, `teaEntry`, `sugarEntry`, `wheatEntry`, `maazaEntry`, `pepisEntry`, `dewEntry`, `fantaEntry`, `cokeEntry`, `spriteEntry`
- **Summary entries**: `costmeticpriceEntry`, `grocerypriceEntry`, `drinkspriceEntry`, `cosmetictaxEntry`, `grocerytaxEntry`, `drinkstaxEntry`
- **Customer entries**: `nameEntry`, `phoneEntry`, `billnumberEntry`
- **Bill display**: `textarea`

---

## 8. Product Catalogue & Pricing

All prices are **hardcoded** in `total()`. There is no external configuration file.

### Cosmetics
| Product | Unit Price (GHS) |
|---|---|
| Bath Soap | 20 |
| Face Cream | 30 |
| Face Wash | 25 |
| Hair Spray | 50 |
| Hair Gel | 40 |
| Body Lotion | 60 |

### Groceries
| Product | Unit Price (GHS) |
|---|---|
| Rice | 70 |
| Oil | 45 |
| Coffee | 25 |
| Tea | 15 |
| Sugar | 32 |
| Wheat | 45 |

### Cold Drinks
| Product | Unit Price (GHS) |
|---|---|
| Maaza | 5 |
| Pepsi | 7 |
| Mountain Dew | 6 |
| Fanta | 8 |
| Coca-Cola | 10 |
| Sprite | 7 |

---

## 9. Tax Calculation

Taxes are applied per category at fixed rates hardcoded in `total()`:

| Category | Tax Rate |
|---|---|
| Cosmetics | 5% |
| Groceries | 6% |
| Cold Drinks | 2% |

```
totalcosmeticprice  = sum(qty × unit_price for each cosmetic item)
cosmetictax         = totalcosmeticprice × 0.05

totalgroceryprice   = sum(qty × unit_price for each grocery item)
grocerytax          = totalgroceryprice × 0.06

totaldrinksprice    = sum(qty × unit_price for each drink item)
drinkstax           = totaldrinksprice × 0.02

totalbill = totalcosmeticprice + totalgroceryprice + totaldrinksprice
          + cosmetictax + grocerytax + drinkstax
```

---

## 10. Data Persistence

Bills are stored as plain-text `.txt` files on the local filesystem.

- **Directory**: `bills/` (relative to the working directory; auto-created at startup if absent via `os.mkdir`)
- **Filename**: `{billnumber}.txt`, where `billnumber` is a random integer in [200, 1000]
- **Format**: Human-readable, tab-separated bill text as rendered in `textarea`
- **No database, no serialisation format, no indexing**

Bill numbers are not guaranteed unique across sessions since they are random integers in a small range. There is no deduplication check before saving; an existing file with the same number will be overwritten.

---

## 11. External Integrations

### Gmail SMTP (Email Delivery)
- **Server**: `smtp.gmail.com`
- **Port**: `587` (STARTTLS upgrade via `ob.starttls()`)
- **Auth**: Plain username/password entered interactively at send time
- **Limitation**: Requires the sender Gmail account to permit "less secure app" access, or an App Password when 2FA is enabled.

No API keys, OAuth tokens, or environment variables are used anywhere in the codebase.

---

## 12. Cross-Platform Printing

`print_bill()` detects the operating system at runtime and dispatches accordingly:

```
platform.system()
  ├── "Windows"  → os.startfile(tmpfile, 'print')
  └── other      → subprocess.run(['lpr', tmpfile])
                     ├── Success              → bill sent to default printer
                     ├── CalledProcessError   → messagebox error dialog
                     └── FileNotFoundError    → messagebox error dialog (lpr not found)
```

A temporary file (`.txt` extension) is created via `tempfile.mktemp`, written with the bill content, dispatched to the printer, then deleted with `os.remove`.

> **Note**: The legacy Windows-only implementation of `print_bill()` is preserved in the source as a commented-out block immediately above the active cross-platform version.

---

## 13. Control Flow

A typical billing session follows this sequence:

```
1. Launch application
   └── bills/ directory created if missing
   └── Tkinter window opens; billnumber assigned a random value

2. User fills in customer details (Name, Phone Number)

3. User enters item quantities in product panels

4. User clicks [Total]
   └── total() computes subtotals and taxes
       └── Summary entries updated with computed values

5. User clicks [Bill]
   └── bill_area() validates:
       ├── Name and Phone are non-empty
       └── At least one item has a non-zero quantity
   └── Formatted bill rendered into textarea
   └── save_bill() invoked automatically:
       ├── User confirms via dialog
       ├── Bill written to bills/{billnumber}.txt
       └── New random billnumber generated

6. (Optional) User clicks [Print]
   └── print_bill() → temp file → OS print command → cleanup

7. (Optional) User clicks [Email]
   └── send_email() → modal window opens
       └── User enters sender credentials and recipient
       └── send_gmail() → Gmail SMTP → bill delivered

8. (Optional) User clicks [Clear]
   └── clear() → all entries reset to 0, textarea emptied

9. (Optional) User enters bill number + clicks [Search]
   └── search_bill() → reads bills/{n}.txt → loads into textarea
```

---

## 14. Known Limitations & Design Notes

| Area | Issue |
|---|---|
| **No separation of concerns** | Business logic, UI construction, and event handlers are all in one flat procedural file with no classes or modules. |
| **Global mutable state** | Price variables and widget references are module-level globals, making isolated testing or reuse impossible. |
| **Hardcoded prices** | Unit prices and tax rates are embedded in `total()`; changing them requires editing source code. |
| **No input validation** | `total()` calls `int(entry.get())` directly — a non-numeric or empty entry will raise an unhandled `ValueError`. |
| **Bill number collisions** | Random integers in [200, 1000] will collide; a new save silently overwrites an existing file. |
| **Plain-text password** | Gmail credentials are entered into a plain `Entry` widget (password field uses `show="#"`) and sent in memory over TLS — no secure credential storage. |
| **No undo / edit workflow** | Once a bill is generated and saved there is no edit path; the user must clear and restart. |
| **No tests** | There are no unit, integration, or UI tests anywhere in the repository. |
| **No logging** | Errors surface only through `messagebox` dialogs; nothing is written to a log file. |
| **Typos in UI strings** | Several labels contain spelling errors (e.g., "Costmetic", "Reatail Billing System", "Pepis", "Coca Cola" label on Hair Spray line). |
