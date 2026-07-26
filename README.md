## 🏦 NexBank — Banking Management System
## Design and Analysis of Algorithms (DAA) Project

## 📌 About the Project
Banks deal with thousands of customer accounts, deposits, withdrawals, fund transfers,
and transaction records every day. Managing all these operations manually is
time-consuming and increases the chances of errors.
This project automates banking activities using appropriate Data Structures and
Algorithms learned in the Design and Analysis of Algorithms subject. The system is
built using Python and Streamlit with a MySQL database backend.
The project demonstrates how choosing the right data structure drastically improves
the efficiency of banking operations. For example, using a Binary Search Tree for
customer search gives O(log n) time compared to O(n) for a simple linear search.
Using a Stack for transaction history gives instant access to the most recent
transaction, and a Queue ensures service requests are handled fairly in order.

## ❗ Problem Statement
Traditional banking systems manage a large amount of customer and transaction data.
Without efficient data structures and algorithms, tasks like searching records,
updating customer details, deposits, withdrawals, fund transfers, and maintaining
transaction history become slow as the number of customers increases.
This project solves these challenges by using Linked Lists, Stacks, Queues, Binary
Search Trees, and efficient searching and sorting algorithms.

## ✅ Problem Solution
The proposed Banking Management System allows users to:
Create and manage customer accounts with Savings or Current account types
Deposit, withdraw, and transfer funds between accounts
View account details and complete transaction history
Filter transactions by date range
Search customer records quickly using a Binary Search Tree
Sort customer data efficiently using Merge Sort
Process customer service requests using a Queue
Compare BST search speed vs Linear search speed in real time
View reports and charts for data analysis
Close accounts and manage passwords securely

## 🎯 Objectives
-Develop a banking management system using DAA concepts
-Store and manage customer records efficiently using a Linked List
-Perform banking transactions securely and accurately
-Implement searching algorithms — Linear Search and Binary Search
-Implement a sorting algorithm — Merge Sort
-Use a Stack for LIFO transaction history management
-Use a Queue for FIFO customer request processing
-Use a BST for fast O(log n) customer search
-Improve execution speed and optimize memory usage
-Provide visual reports and charts for analysis
-Demonstrate time complexity differences between algorithms

## 🧱 Data Structures Used
-Linked List
-Stores and manages all customer records in memory
-New customers are added at the front in O(1) time
-Deletion traverses the list in O(n) time
-Balance is updated in O(n) time by traversing to the node
-Stack (LIFO — Last In First Out)
-Maintains transaction history
-Every deposit, withdrawal, and transfer is pushed onto the stack
-The most recent transaction is always on top
-Push and Pop operations are both O(1)
-Queue (FIFO — First In First Out)
-Manages customer service requests
-Requests like cheque book, card block, and address update are enqueued
-Requests are processed in the order they were submitted
-Enqueue and Dequeue operations are both O(1)
-Binary Search Tree
-Searches customers by Customer ID
-Faster than linear search — O(log n) average time complexity
-Customers are inserted based on ID for balanced searching
-In-order traversal returns customers sorted by ID

## ⚙️ Algorithms Used
.Merge Sort — O(n log n)
.Sorts customers by balance, name, or ID
.Stable sorting algorithm — maintains relative order of equal elements
.Divide-and-conquer approach splits the list and merges sorted halves
.Used on the Reports page and All Customers page
.Binary Search — O(log n)
.Works on a sorted list of customers
.Finds a customer much faster than linear search
.Used on the Reports page with a live demo
.Linear Search — O(n)
.Used as a baseline comparison against BST search
.Traverses the Linked List from head to tail
.The Search Customer page shows timing of both BST and Linear Search

## 🗂️ Modules of the System
- ✅ User Authentication (Register / Login / Logout)
- ✅ Account Details (View / Update / Close)
- ✅ Change Password
- ✅ Deposit / Withdraw / Transfer Funds
- ✅ Transaction History with Date Filter (Stack)
- ✅ Search Customer — BST vs Linear Search with timing
- ✅ Display All Customers (Linked List + Merge Sort)
- ✅ Delete Customer Record
- ✅ Service Requests Queue (FIFO)
- ✅ Reports & Visualization (4 Plotly Charts)
- ✅ Time Complexity Reference Table
- ✅ Savings & Current Account Types
- ✅ Jupyter Notebook version with interactive menu


## 💻 Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python 3.9+ |
| UI | Streamlit (Dark Theme) |
| Database | MySQL 8.0 |
| Visualization | Plotly, Matplotlib, Seaborn |
| Data Processing | Pandas, NumPy |

---

## 📁 Project Structure
banking-management-system/
├── app.py                  # Streamlit UI — all pages and logic
├── db.py                   # MySQL connection and query helper
├── data_structures.py      # Linked List, Stack, Queue, BST
├── algorithms.py           # Merge Sort, Binary Search, Linear Search
├── schema.sql              # MySQL database schema
├── requirements.txt        # Python dependencies
├── banking_system_DAA.ipynb # Jupyter Notebook version
└── .streamlit/
    └── config.toml         # Dark theme configuration


---

## ⏱️ Time Complexity Analysis
| Operation | Data Structure | Complexity |
|---|---|---|
| Add customer | Linked List | O(1) |
| Delete customer | Linked List | O(n) |
| Search customer | BST | O(log n) |
| Deposit | Linked List | O(1) |
| Withdraw | Linked List | O(1) |
| Push transaction | Stack | O(1) |
| Pop transaction | Stack | O(1) |
| Add request | Queue | O(1) |
| Remove request | Queue | O(1) |
| Sort customers | Merge Sort | O(n log n) |
| Binary search | Sorted Array | O(log n) |

---


## ⚙️ Prerequisites
Python 3.9+
MySQL Server 8.x running locally (or a remote instance)
VS Code with the Python extension

## 🔮 Future Enhancements
Internet Banking and Mobile Banking application
OTP-based login for extra security
QR code payments
Real-time notifications
Cloud storage and deployment
AI-based analytics and fraud detection
Loan management module
Fixed Deposit and Recurring Deposit features

## 📊 Expected Outcome
The system efficiently manages customer records, performs banking transactions
accurately, reduces processing time using appropriate data structures and algorithms,
and provides a practical understanding of Design and Analysis of Algorithms through
a real working application.


## 👨‍💻 Developed By
Yashi Mishra
DAA Project — Banking Management System
Subject: Design and Analysis of Algorithms

## 📜 License
This project is licensed under the MIT License.
