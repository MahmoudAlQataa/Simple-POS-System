# Expense Tracker

A simple Flask project for tracking daily expenses. Still under development 🚧

## 📌 Overview

A system for recording and tracking personal expenses, built with Flask and SQLAlchemy. The current goal is to build a basic working version, with plans to expand later (e.g., turning it into a simple daily financial ledger for a small shop).

## 🛠️ Tech Stack

- **Flask** — core web framework
- **SQLAlchemy** — database ORM
- **SQLite** — database (development stage)

## 🚧 Project Status

This project is still in progress.

### ✅ Done so far
- Basic project structure set up
- Database connection configured via SQLAlchemy
- Base templates set up (base.html, index.html)

### 📝 In progress / TODO
- [ ] Build the Models
- [ ] Build the Routes
- [ ] Build the Services
- [ ] Complete the frontend/UI
- [ ] User authentication system
- [ ] Expense reports/analytics (charts, summaries)
- [ ] Full documentation

## ⚙️ Running Locally

```bash
git clone https://github.com/MahmoudAlQataa/Expense-Tracker.git
cd Expense-Tracker

python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

pip install -r requirements.txt

flask run
```

## 📂 Project Structure
```
Expense-Tracker/
├── static/
│ ├── css/
│ └── js/
├── templates/
│ ├── base.html
│ └── index.html
├── instance/
│ └── expenses.db       # auto-created when the app runs (not tracked in Git)
├── app.py
├── requirements.txt
└── .gitignore
```

> Note: The `models/`, `routes/`, and `services/` folders are planned but currently empty — they'll appear in the structure once code is added to them.

## 📄 License

No license has been chosen yet.

---

> ⚠️ Note: This project is in its early stages and is actively changing. Feedback and suggestions are welcome.
