# BANKING-MANAGEMENT-SYSTEM
Banking Management System using Data Structure and Algorithm- - DAA Project

---

## 📌 About the Project

Bank deal with thousands of customer accounts, deposits, withdrawls, fund transfer, and transaction management every day. Managing all these operations manually is time-consuming and increasing the chances of error.

This project automates banking activities by using appropriate data structure and algorithms subject. The system is built using python and straemlit with a MySQL database backend.The project demonstrates how choosing the right data structure drastically improves the efficiency of banking operations. For example, using a Binary Search Tree for customer search gives O(log n) time compared to O(n) for a simple linear search. Using a Stack for transaction history gives instant access to the most recent transaction, and a Queue ensures service requests are handled fairly in order.



---

## 🧱 Data Structures Used

- Linked List — Store and manage customer records — Add O(1), Delete O(n)
- Stack — Transaction history LIFO — Push/Pop O(1)
- Queue — Service requests FIFO — Enqueue/Dequeue O(1)
- Binary Search Tree — Search customer by ID — O(log n) average

---

## ⚙️ Algorithms Used

- Merge Sort — Sort customers by balance or name — O(n log n)
- Binary Search — Search on sorted customer data — O(log n)
- Linear Search — Baseline comparison with BST — O(n)

---

## 🗂️ Modules

- User Authentication — Register, Login, Logout
- Account Details — View, Update, Close Account
- Change Password
- Deposit, Withdraw, Transfer Funds
- Transaction History with Date Filter using Stack
- Search Customer using BST vs Linear Search with timing comparison
- Display All Customers using Linked List and Merge Sort
- Delete Customer Record
- Service Requests using Queue FIFO
- Reports and Visualization with Charts
- Time Complexity Reference Table
- Savings and Current Account Types
- Jupyter Notebook version with interactive menu

---

## 💻 Tech Stack

- Backend — Python 3.9+
- UI — Streamlit Dark Theme
- Database — MySQL 8.0
- Visualization — Plotly, Matplotlib, Seaborn
- Data Processing — Pandas, NumPy

---

## 📁 Project Structure

- app.py — Streamlit UI, all pages and logic
- db.py — MySQL connection and query helper
- data_structures.py — Linked List, Stack, Queue, BST
- algorithms.py — Merge Sort, Binary Search, Linear Search
- schema.sql — MySQL database schema
- requirements.txt — Python dependencies
- banking_system_DAA.ipynb — Jupyter Notebook version
- .streamlit/config.toml — Dark theme configuration

---

## ⏱️ Time Complexity Analysis

- Add customer — Linked List — O(1)
- Delete customer — Linked List — O(n)
- Search customer — BST — O(log n)
- Deposit — Linked List — O(1)
- Withdraw — Linked List — O(1)
- Push transaction — Stack — O(1)
- Pop transaction — Stack — O(1)
- Add request — Queue — O(1)
- Remove request — Queue — O(1)
- Sort customers — Merge Sort — O(n log n)
- Binary search — Sorted Array — O(log n)

---

## 👨‍💻 Developed By

Yashi Mishra
DAA Project — Banking Management System
Subject — Design and Analysis of Algorithms

---

## 📜 License

This project is licensed under the MIT License.

