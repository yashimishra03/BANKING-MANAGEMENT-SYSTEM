"""
app.py
------
Banking Management System Using Data Structures and Algorithms
Streamlit front-end (dark theme) + MySQL backend.

Run:
    streamlit run app.py
"""

import hashlib
import time
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from db import run_query, init_db
from data_structures import CustomerLinkedList, TransactionStack, RequestQueue, CustomerBST
from algorithms import merge_sort, binary_search, linear_search


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="NexBank | Banking Management System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS — dark, clean, minimal card-based UI
# =========================================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    html, body, [class*="css"]  {
        font-family: 'Segoe UI', -apple-system, sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161B22, #1C2128);
        border: 1px solid #262C36;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25);
    }
    div[data-testid="stMetricLabel"] { color: #9AA4B2; }

    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        border: 1px solid #2B3542;
        background: linear-gradient(145deg, #5B8CFF, #3E6FE0);
        color: white;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        transition: all 0.15s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(91,140,255,0.35);
        border-color: #5B8CFF;
    }

    /* Section headers */
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        color: #F0F2F5;
    }
    .section-sub {
        color: #8B93A1;
        margin-bottom: 1.2rem;
        font-size: 0.9rem;
    }

    /* Card-like container */
    .nb-card {
        background: #161B22;
        border: 1px solid #262C36;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    hr { border-color: #262C36; }

    [data-testid="stSidebar"] {
        background-color: #10141A;
        border-right: 1px solid #262C36;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE INIT
# =========================================================
def init_session():
    defaults = {
        "logged_in": False,
        "customer": None,
        "linked_list": CustomerLinkedList(),
        "bst": CustomerBST(),
        "txn_stack": TransactionStack(),
        "req_queue": RequestQueue(),
        "db_ready": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session()


# =========================================================
# DB BOOTSTRAP
# =========================================================
def ensure_db():
    if not st.session_state.db_ready:
        try:
            init_db()
            st.session_state.db_ready = True
        except Exception as e:
            st.error(f"Could not connect to / initialize MySQL database: {e}")
            st.info("Check your credentials in db.py (or set DB_HOST / DB_USER / "
                     "DB_PASSWORD / DB_NAME environment variables) and that "
                     "MySQL is running, then rerun the app.")
            st.stop()


def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


# =========================================================
# DATA LOADERS — populate the in-memory DS from MySQL
# =========================================================
def load_all_customers():
    rows = run_query("SELECT * FROM customers", fetch=True) or []
    ll = CustomerLinkedList()
    bst = CustomerBST()
    for r in rows:
        r["balance"] = float(r["balance"])
        ll.add_front(r)
        bst.insert(r)
    st.session_state.linked_list = ll
    st.session_state.bst = bst
    return rows


def load_customer_transactions(customer_id):
    rows = run_query(
        "SELECT * FROM transactions WHERE customer_id=%s ORDER BY created_at ASC",
        (customer_id,), fetch=True
    ) or []
    stack = TransactionStack()
    for r in rows:
        stack.push(r)
    st.session_state.txn_stack = stack


def load_pending_requests(customer_id=None):
    if customer_id:
        rows = run_query(
            "SELECT * FROM requests WHERE customer_id=%s AND status='pending' ORDER BY created_at ASC",
            (customer_id,), fetch=True
        ) or []
    else:
        rows = run_query(
            "SELECT * FROM requests WHERE status='pending' ORDER BY created_at ASC",
            fetch=True
        ) or []
    q = RequestQueue()
    for r in rows:
        q.enqueue(r)
    st.session_state.req_queue = q


# =========================================================
# AUTH PAGES
# =========================================================
def page_login_signup():
    st.markdown('<div class="section-title">🏦 NexBank — Banking Management System</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Design & Analysis of Algorithms Project · Linked List · Stack · Queue · BST · Merge Sort · Binary Search</div>', unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["🔐 Login", "🆕 Create Account"])

    with tab_login:
        with st.container():
            st.markdown('<div class="nb-card">', unsafe_allow_html=True)
            email = st.text_input("Email", key="login_email")
            pw = st.text_input("Password", type="password", key="login_pw")
            if st.button("Login", key="login_btn"):
                user = run_query(
                    "SELECT * FROM customers WHERE email=%s", (email,), fetchone=True
                )
                if user and user["password_hash"] == hash_password(pw):
                    user["balance"] = float(user["balance"])
                    st.session_state.logged_in = True
                    st.session_state.customer = user
                    load_all_customers()
                    load_customer_transactions(user["customer_id"])
                    load_pending_requests(user["customer_id"])
                    st.success(f"Welcome back, {user['name']}!")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_signup:
        with st.container():
            st.markdown('<div class="nb-card">', unsafe_allow_html=True)
            name = st.text_input("Full Name")
            email_s = st.text_input("Email", key="signup_email")
            phone = st.text_input("Phone")
            pw_s = st.text_input("Password", type="password", key="signup_pw")
            opening = st.number_input("Opening Deposit", min_value=0.0, step=100.0)
            if st.button("Create Account", key="signup_btn"):
                if not (name and email_s and phone and pw_s):
                    st.warning("Please fill in all fields.")
                else:
                    try:
                        cid = run_query(
                            """INSERT INTO customers (name, email, phone, password_hash, balance)
                               VALUES (%s,%s,%s,%s,%s)""",
                            (name, email_s, phone, hash_password(pw_s), opening),
                            commit=True
                        )
                        if opening > 0:
                            run_query(
                                """INSERT INTO transactions (customer_id, type, amount, balance_after)
                                   VALUES (%s,'deposit',%s,%s)""",
                                (cid, opening, opening), commit=True
                            )
                        st.success("Account created! You can now log in.")
                    except Exception as e:
                        st.error(f"Could not create account: {e}")
            st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# DASHBOARD
# =========================================================
def page_dashboard():
    cust = st.session_state.customer
    fresh = run_query("SELECT * FROM customers WHERE customer_id=%s",
                       (cust["customer_id"],), fetchone=True)
    fresh["balance"] = float(fresh["balance"])
    st.session_state.customer = fresh

    st.markdown(f'<div class="section-title">Welcome, {fresh["name"]} 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Here\'s your account overview</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Current Balance", f"₹ {fresh['balance']:,.2f}")

    txn_count = run_query("SELECT COUNT(*) AS c FROM transactions WHERE customer_id=%s",
                           (fresh["customer_id"],), fetchone=True)["c"]
    c2.metric("Total Transactions", txn_count)

    pending = run_query("SELECT COUNT(*) AS c FROM requests WHERE customer_id=%s AND status='pending'",
                         (fresh["customer_id"],), fetchone=True)["c"]
    c3.metric("Pending Requests", pending)

    st.markdown("<br>", unsafe_allow_html=True)

    # Recent transactions chart
    rows = run_query(
        "SELECT * FROM transactions WHERE customer_id=%s ORDER BY created_at ASC",
        (fresh["customer_id"],), fetch=True
    ) or []
    if rows:
        df = pd.DataFrame(rows)
        df["amount"] = df["amount"].astype(float)
        df["balance_after"] = df["balance_after"].astype(float)
        fig = px.line(df, x="created_at", y="balance_after", markers=True,
                       title="Balance Over Time")
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
            font_color="#E6E6E6", height=380,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No transactions yet — make a deposit to get started.")


# =========================================================
# DEPOSIT / WITHDRAW / TRANSFER
# =========================================================
def record_transaction(customer_id, ttype, amount, balance_after, related_id=None):
    tid = run_query(
        """INSERT INTO transactions (customer_id, type, amount, balance_after, related_customer_id)
           VALUES (%s,%s,%s,%s,%s)""",
        (customer_id, ttype, amount, balance_after, related_id), commit=True
    )
    txn = run_query("SELECT * FROM transactions WHERE transaction_id=%s", (tid,), fetchone=True)
    st.session_state.txn_stack.push(txn)   # O(1) push onto in-memory stack


def page_deposit():
    st.markdown('<div class="section-title">💰 Deposit Money</div>', unsafe_allow_html=True)
    cust = st.session_state.customer
    with st.container():
        st.markdown('<div class="nb-card">', unsafe_allow_html=True)
        amount = st.number_input("Amount to deposit", min_value=0.0, step=100.0)
        if st.button("Deposit"):
            if amount <= 0:
                st.warning("Enter a valid amount.")
            else:
                new_balance = cust["balance"] + amount
                run_query("UPDATE customers SET balance=%s WHERE customer_id=%s",
                          (new_balance, cust["customer_id"]), commit=True)
                record_transaction(cust["customer_id"], "deposit", amount, new_balance)
                st.session_state.linked_list.update_balance(cust["customer_id"], new_balance)
                cust["balance"] = new_balance
                st.success(f"Deposited ₹{amount:,.2f}. New balance: ₹{new_balance:,.2f}")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def page_withdraw():
    st.markdown('<div class="section-title">🏧 Withdraw Money</div>', unsafe_allow_html=True)
    cust = st.session_state.customer
    with st.container():
        st.markdown('<div class="nb-card">', unsafe_allow_html=True)
        st.write(f"Available balance: **₹{cust['balance']:,.2f}**")
        amount = st.number_input("Amount to withdraw", min_value=0.0, step=100.0)
        if st.button("Withdraw"):
            if amount <= 0:
                st.warning("Enter a valid amount.")
            elif amount > cust["balance"]:
                st.error("Insufficient balance.")
            else:
                new_balance = cust["balance"] - amount
                run_query("UPDATE customers SET balance=%s WHERE customer_id=%s",
                          (new_balance, cust["customer_id"]), commit=True)
                record_transaction(cust["customer_id"], "withdraw", amount, new_balance)
                st.session_state.linked_list.update_balance(cust["customer_id"], new_balance)
                cust["balance"] = new_balance
                st.success(f"Withdrew ₹{amount:,.2f}. New balance: ₹{new_balance:,.2f}")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def page_transfer():
    st.markdown('<div class="section-title">🔁 Transfer Funds</div>', unsafe_allow_html=True)
    cust = st.session_state.customer
    with st.container():
        st.markdown('<div class="nb-card">', unsafe_allow_html=True)
        st.write(f"Available balance: **₹{cust['balance']:,.2f}**")
        target_email = st.text_input("Recipient's email")
        amount = st.number_input("Amount to transfer", min_value=0.0, step=100.0)
        if st.button("Transfer"):
            recipient = run_query("SELECT * FROM customers WHERE email=%s",
                                   (target_email,), fetchone=True)
            if not recipient:
                st.error("Recipient not found.")
            elif recipient["customer_id"] == cust["customer_id"]:
                st.warning("You cannot transfer to yourself.")
            elif amount <= 0:
                st.warning("Enter a valid amount.")
            elif amount > cust["balance"]:
                st.error("Insufficient balance.")
            else:
                sender_new = cust["balance"] - amount
                recipient_new = float(recipient["balance"]) + amount

                run_query("UPDATE customers SET balance=%s WHERE customer_id=%s",
                          (sender_new, cust["customer_id"]), commit=True)
                run_query("UPDATE customers SET balance=%s WHERE customer_id=%s",
                          (recipient_new, recipient["customer_id"]), commit=True)

                record_transaction(cust["customer_id"], "transfer_out", amount,
                                    sender_new, related_id=recipient["customer_id"])
                run_query(
                    """INSERT INTO transactions (customer_id, type, amount, balance_after, related_customer_id)
                       VALUES (%s,'transfer_in',%s,%s,%s)""",
                    (recipient["customer_id"], amount, recipient_new, cust["customer_id"]),
                    commit=True
                )

                st.session_state.linked_list.update_balance(cust["customer_id"], sender_new)
                cust["balance"] = sender_new
                st.success(f"Transferred ₹{amount:,.2f} to {recipient['name']}.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# TRANSACTION HISTORY (Stack demo — pop shows most recent first)
# =========================================================
def page_history():
    st.markdown('<div class="section-title">📜 Transaction History</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Backed by a Stack — most recent transaction on top (LIFO)</div>', unsafe_allow_html=True)

    cust = st.session_state.customer
    load_customer_transactions(cust["customer_id"])
    txns = st.session_state.txn_stack.to_list()  # already most-recent-first

    if not txns:
        st.info("No transactions yet.")
        return

    df = pd.DataFrame(txns)
    df["amount"] = df["amount"].astype(float)
    df["balance_after"] = df["balance_after"].astype(float)
    df = df[["transaction_id", "type", "amount", "balance_after", "created_at"]]
    df.columns = ["ID", "Type", "Amount", "Balance After", "Date"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    fig = px.pie(pd.DataFrame(txns), names="type", title="Transaction Type Breakdown", hole=0.5)
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0E1117",
                       font_color="#E6E6E6", height=380)
    st.plotly_chart(fig, use_container_width=True)


# =========================================================
# SEARCH CUSTOMER (BST demo)
# =========================================================
def page_search():
    st.markdown('<div class="section-title">🔍 Search Customer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Search by Customer ID using a Binary Search Tree — O(log n) average</div>', unsafe_allow_html=True)

    load_all_customers()
    with st.container():
        st.markdown('<div class="nb-card">', unsafe_allow_html=True)
        cid = st.number_input("Customer ID", min_value=1, step=1)
        if st.button("Search"):
            start = time.perf_counter()
            result_bst = st.session_state.bst.search(int(cid))
            bst_time = time.perf_counter() - start

            start = time.perf_counter()
            result_ll = st.session_state.linked_list.linear_search(int(cid))
            ll_time = time.perf_counter() - start

            if result_bst:
                st.success(f"Found: {result_bst['name']} | {result_bst['email']} | "
                           f"Balance: ₹{result_bst['balance']:,.2f}")
            else:
                st.error("Customer not found.")

            c1, c2 = st.columns(2)
            c1.metric("BST Search Time", f"{bst_time*1e6:.1f} µs")
            c2.metric("Linear Search Time", f"{ll_time*1e6:.1f} µs")
        st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# REQUESTS (Queue demo)
# =========================================================
def page_requests():
    st.markdown('<div class="section-title">🗂️ Service Requests</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Backed by a Queue — processed First-In-First-Out</div>', unsafe_allow_html=True)

    cust = st.session_state.customer

    with st.container():
        st.markdown('<div class="nb-card">', unsafe_allow_html=True)
        req_type = st.selectbox("Request Type", ["Cheque Book", "Statement", "Card Block", "Address Update"])
        if st.button("Submit Request"):
            run_query(
                "INSERT INTO requests (customer_id, request_type) VALUES (%s,%s)",
                (cust["customer_id"], req_type), commit=True
            )
            st.success("Request submitted.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    load_pending_requests(cust["customer_id"])
    pending = st.session_state.req_queue.to_list()

    st.write("**Pending requests (queue order):**")
    if not pending:
        st.info("No pending requests.")
    else:
        for i, r in enumerate(pending, 1):
            st.write(f"{i}. {r['request_type']} — submitted {r['created_at']}")


# =========================================================
# REPORTS (Merge Sort + Binary Search + Visualizations)
# =========================================================
def page_reports():
    st.markdown('<div class="section-title">📊 Reports & Visualization</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">All customers sorted with Merge Sort · O(n log n)</div>', unsafe_allow_html=True)

    customers = load_all_customers()
    if not customers:
        st.info("No customer data available.")
        return

    sort_key = st.selectbox("Sort by", ["balance", "name", "customer_id"])
    sorted_customers = merge_sort(customers, sort_key)

    df = pd.DataFrame(sorted_customers)[["customer_id", "name", "email", "balance"]]
    df.columns = ["ID", "Name", "Email", "Balance"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(df, x="Name", y="Balance", title="Customer Balances", color="Balance",
                     color_continuous_scale="Blues")
        fig.update_layout(template="plotly_dark", paper_bgcolor="#0E1117",
                           font_color="#E6E6E6", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        all_txns = run_query("SELECT type, amount, created_at FROM transactions", fetch=True) or []
        if all_txns:
            tdf = pd.DataFrame(all_txns)
            tdf["amount"] = tdf["amount"].astype(float)
            fig2 = px.histogram(tdf, x="type", y="amount", title="Total Volume by Transaction Type",
                                 color="type")
            fig2.update_layout(template="plotly_dark", paper_bgcolor="#0E1117",
                                font_color="#E6E6E6", height=400)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No transaction data yet.")

    st.markdown("---")
    st.write("**Binary Search on sorted-by-balance data**")
    target_id = st.number_input("Find Customer ID (after sorting by balance)", min_value=1, step=1, key="bsearch")
    if st.button("Run Binary Search"):
        by_id_sorted = merge_sort(customers, "customer_id")
        result = binary_search(by_id_sorted, "customer_id", int(target_id))
        if result:
            st.success(f"Found via Binary Search: {result['name']} — ₹{result['balance']:,.2f}")
        else:
            st.error("Not found.")


# =========================================================
# COMPLEXITY REFERENCE PAGE
# =========================================================
def page_complexity():
    st.markdown('<div class="section-title">⚙️ Data Structures & Complexity</div>', unsafe_allow_html=True)
    data = [
        ("Add customer", "Linked List", "O(1)"),
        ("Delete customer", "Linked List", "O(n)"),
        ("Search customer", "Binary Search Tree", "O(log n)"),
        ("Deposit", "Linked List", "O(1)"),
        ("Withdraw", "Linked List", "O(1)"),
        ("Push transaction", "Stack", "O(1)"),
        ("Pop transaction", "Stack", "O(1)"),
        ("Add request", "Queue", "O(1)"),
        ("Remove request", "Queue", "O(1)"),
        ("Sort customers", "Merge Sort", "O(n log n)"),
        ("Search sorted list", "Binary Search", "O(log n)"),
    ]
    df = pd.DataFrame(data, columns=["Operation", "Data Structure / Algorithm", "Time Complexity"])
    st.dataframe(df, use_container_width=True, hide_index=True)


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
def sidebar_nav():
    with st.sidebar:
        st.markdown("## 🏦 NexBank")
        if st.session_state.logged_in:
            st.markdown(f"**{st.session_state.customer['name']}**")
            st.caption(st.session_state.customer["email"])
            st.markdown("---")
            page = st.radio("Navigate", [
                "Dashboard", "Deposit", "Withdraw", "Transfer",
                "Transaction History", "Search Customer",
                "Service Requests", "Reports & Visualization",
                "Complexity Reference"
            ], label_visibility="collapsed")
            st.markdown("---")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.customer = None
                st.rerun()
            return page
        else:
            st.caption("Design & Analysis of Algorithms Project")
            return None


# =========================================================
# MAIN
# =========================================================
def main():
    ensure_db()

    if not st.session_state.logged_in:
        page_login_signup()
        return

    page = sidebar_nav()

    if page == "Dashboard":
        page_dashboard()
    elif page == "Deposit":
        page_deposit()
    elif page == "Withdraw":
        page_withdraw()
    elif page == "Transfer":
        page_transfer()
    elif page == "Transaction History":
        page_history()
    elif page == "Search Customer":
        page_search()
    elif page == "Service Requests":
        page_requests()
    elif page == "Reports & Visualization":
        page_reports()
    elif page == "Complexity Reference":
        page_complexity()


if __name__ == "__main__":
    main()
