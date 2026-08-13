# Simple POS System

A Flask-based desktop application for tracking daily transactions and expenses — built as a digital replacement for paper-based financial record-keeping. Generates printable PDF receipts and runs as a standalone Windows desktop app.

## 📌 Overview

A local-first point-of-sale / expense tracking system: no internet dependency, no external database server — everything runs and persists on the user's own machine.

**Status:** Feature-complete. Core functionality, PDF receipts, and desktop packaging are all working end to end.

## 🛠️ Tech Stack

- **Flask** (Application Factory pattern + Blueprints)
- **Flask-SQLAlchemy** — ORM
- **SQLite** — database, managed via **Flask-Migrate**
- **pdfkit + wkhtmltopdf** — PDF receipt generation
- **pywebview** — desktop window shell
- Vanilla JS, Jinja2, plain CSS (no frontend framework)

## ✨ Features

- Add / edit / delete transactions (name, phone, items/services, price, discount, amount paid)
- Server-computed pricing and outstanding/overpaid balance (`remain_amount = paid_amount - (price - discount)`)
- Dashboard showing today's transactions
- Full data page with:
  - Server-side filters (date range, name, item/category, outstanding/overpaid)
  - Instant client-side quick-search by name (filters visible rows as you type)
- Settings page to manage the list of available items/services and their prices
- CSV export respecting all active filters
- Printable PDF receipts per transaction (RTL Arabic support), auto-filed under `instance/reports/<year>/<month>/`
- Runs as a native Windows desktop app (no browser required)
- Separate module for tracking incoming bills/invoices from suppliers (company name, category, amount, paid/remaining balance), with its own filtered list view and printable PDF receipts
- Automatic local database backup on each app launch

## 📂 Project Structure

    Simple-POS-System/
    ├── app.py                 # Application factory (create_app)
    ├── config.py              # Centralized path config (dev vs. packaged/frozen mode)
    ├── extensions.py          # Shared SQLAlchemy instance
    ├── launcher.py            # Desktop entry point (Flask thread + pywebview window)
    ├── bin/                   # Bundled wkhtmltopdf.exe + dependencies
    ├── migrations/            # Flask-Migrate schema history
    ├── models/                # Expense, Test, Bils
    ├── routes/                # index, add, edit, delete, data, settings, export, receipt, bils
    ├── services/              # item lookup, date parsing, receipt generation, port selection, backup
    ├── templates/             # base, index, data, settings, receipt, bils
    └── static/
        ├── css/               # theme.css (variables) + style.css (layout/components)
        └── js/

## ⚙️ Running Locally (development mode)

```bash
git clone https://github.com/MahmoudAlQataa/Simple-POS-System
cd Simple-POS-System

python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

pip install -r requirements.txt

flask db upgrade   # apply database migrations
flask run
```

This runs the app as a regular Flask server, accessible from a browser at `http://127.0.0.1:5000`.

### Running in a desktop window (webview)

To run the app inside a native desktop window instead of a browser tab, use:

```bash
python launcher.py
```

This requires `pywebview` to be installed on your machine (included in `requirements.txt`).

PDF receipt generation requires `wkhtmltopdf` — a copy is bundled in `bin/`, or set the path in `config.py`.

## 📄 License

No license has been chosen yet.