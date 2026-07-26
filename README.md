# NexBank — Banking Management System (DAA Project)

A Banking Management System built for the *Design and Analysis of Algorithms* subject,
demonstrating real usage of a **Linked List, Stack, Queue, Binary Search Tree, Merge Sort,
and Binary Search** on top of a **MySQL** database, with a clean dark-themed **Streamlit** UI.

## 1. Project Structure

```
banking_project/
├── app.py                 # Streamlit UI (all pages/logic)
├── db.py                  # MySQL connection + query helper
├── data_structures.py     # Linked List, Stack, Queue, BST
├── algorithms.py          # Merge Sort, Binary Search, Linear Search
├── schema.sql             # MySQL schema (tables + indexes)
├── requirements.txt
└── .streamlit/
    └── config.toml        # Dark theme config
```

## 2. Prerequisites

- Python 3.9+
- MySQL Server 8.x running locally (or a remote instance)
- VS Code with the Python extension

## 3. Setup (VS Code)

1. **Open the folder** `banking_project` in VS Code.

2. **Create a virtual environment** (Terminal → New Terminal):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MySQL credentials.**
   Open `db.py` and update `DB_CONFIG`, or (recommended) set environment variables
   before running so you don't hardcode a password:
   ```bash
   # macOS/Linux
   export DB_HOST=localhost
   export DB_USER=root
   export DB_PASSWORD=your_mysql_password
   export DB_NAME=banking_system

   # Windows (PowerShell)
   $env:DB_HOST="localhost"
   $env:DB_USER="root"
   $env:DB_PASSWORD="your_mysql_password"
   $env:DB_NAME="banking_system"
   ```

5. **Create the database** (the app will also auto-create tables on first run via
   `schema.sql`, but you can run it manually too):
   ```bash
   mysql -u root -p < schema.sql
   ```

6. **Run the app:**
   ```bash
   streamlit run app.py
   ```
   Streamlit will open the app in your browser at `http://localhost:8501`, already
   in dark mode (set in `.streamlit/config.toml`).

## 4. How the DSA Maps to the App

| Feature                         | Data Structure / Algorithm | Where in code                     |
|----------------------------------|-----------------------------|------------------------------------|
| Customer list (add/delete)       | Linked List                | `data_structures.py: CustomerLinkedList` |
| Deposit / Withdraw balance sync  | Linked List (in-memory)    | `app.py: page_deposit / page_withdraw` |
| Transaction history (LIFO)       | Stack                      | `data_structures.py: TransactionStack` |
| Service requests (FIFO)          | Queue                      | `data_structures.py: RequestQueue` |
| Search customer by ID            | Binary Search Tree         | `data_structures.py: CustomerBST` |
| Sort customers (by balance/name) | Merge Sort                 | `algorithms.py: merge_sort` |
| Fast lookup on sorted data        | Binary Search               | `algorithms.py: binary_search` |

## 5. Notes

- Passwords are hashed with SHA-256 before storage (adequate for an academic project;
  use `bcrypt`/`argon2` for production).
- The "Search Customer" page shows a live micro-benchmark comparing BST search vs.
  linear search time, useful for the report's complexity analysis section.
- The "Reports & Visualization" page lets you re-sort customers live with merge sort
  and run a binary search against the sorted result.
