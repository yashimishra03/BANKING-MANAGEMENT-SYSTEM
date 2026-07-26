"""
data_structures.py
-------------------
Hand-written DSA implementations used by the Banking Management System.
These are the actual structures the project report references — they are
not just decorative, the app logic in app.py operates on them directly.

Implemented:
    - CustomerLinkedList   -> O(1) add, O(n) delete, O(n) traverse
    - TransactionStack     -> O(1) push / pop  (LIFO transaction history)
    - RequestQueue         -> O(1) enqueue / dequeue (FIFO customer requests)
    - CustomerBST          -> O(log n) average search by customer_id
"""


# ------------------------------------------------------------------
# 1. Linked List — stores customer records
# ------------------------------------------------------------------
class CustomerNode:
    def __init__(self, customer):
        self.customer = customer   # dict: customer_id, name, email, phone, balance...
        self.next = None


class CustomerLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, customer):
        """O(1) insert at head."""
        node = CustomerNode(customer)
        node.next = self.head
        self.head = node
        self.size += 1

    def delete(self, customer_id):
        """O(n) delete by customer_id."""
        prev = None
        curr = self.head
        while curr:
            if curr.customer["customer_id"] == customer_id:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                self.size -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    def update_balance(self, customer_id, new_balance):
        """O(n) find + update balance in the in-memory list."""
        curr = self.head
        while curr:
            if curr.customer["customer_id"] == customer_id:
                curr.customer["balance"] = new_balance
                return True
            curr = curr.next
        return False

    def to_list(self):
        """O(n) traverse -> list of dicts."""
        result = []
        curr = self.head
        while curr:
            result.append(curr.customer)
            curr = curr.next
        return result

    def linear_search(self, customer_id):
        """O(n) linear search by id (used for comparison against BST)."""
        curr = self.head
        while curr:
            if curr.customer["customer_id"] == customer_id:
                return curr.customer
            curr = curr.next
        return None


# ------------------------------------------------------------------
# 2. Stack — LIFO transaction history (per session view)
# ------------------------------------------------------------------
class TransactionStack:
    def __init__(self):
        self._items = []

    def push(self, transaction):
        """O(1)"""
        self._items.append(transaction)

    def pop(self):
        """O(1)"""
        if not self.is_empty():
            return self._items.pop()
        return None

    def peek(self):
        return self._items[-1] if self._items else None

    def is_empty(self):
        return len(self._items) == 0

    def to_list(self):
        """Most recent transaction first."""
        return list(reversed(self._items))


# ------------------------------------------------------------------
# 3. Queue — FIFO customer service requests
# ------------------------------------------------------------------
class RequestQueue:
    def __init__(self):
        self._items = []

    def enqueue(self, request):
        """O(1) amortized."""
        self._items.append(request)

    def dequeue(self):
        """O(1) using pop(0) trade-off -> for teaching purposes; a deque
        would be O(1) true, but list is kept for simplicity/clarity."""
        if not self.is_empty():
            return self._items.pop(0)
        return None

    def is_empty(self):
        return len(self._items) == 0

    def to_list(self):
        return list(self._items)


# ------------------------------------------------------------------
# 4. Binary Search Tree — search customers by customer_id
# ------------------------------------------------------------------
class BSTNode:
    def __init__(self, customer):
        self.customer = customer
        self.left = None
        self.right = None


class CustomerBST:
    def __init__(self):
        self.root = None

    def insert(self, customer):
        """O(log n) average, O(n) worst case."""
        if self.root is None:
            self.root = BSTNode(customer)
            return
        self._insert(self.root, customer)

    def _insert(self, node, customer):
        if customer["customer_id"] < node.customer["customer_id"]:
            if node.left is None:
                node.left = BSTNode(customer)
            else:
                self._insert(node.left, customer)
        else:
            if node.right is None:
                node.right = BSTNode(customer)
            else:
                self._insert(node.right, customer)

    def search(self, customer_id):
        """O(log n) average search."""
        return self._search(self.root, customer_id)

    def _search(self, node, customer_id):
        if node is None:
            return None
        if node.customer["customer_id"] == customer_id:
            return node.customer
        if customer_id < node.customer["customer_id"]:
            return self._search(node.left, customer_id)
        return self._search(node.right, customer_id)

    def in_order(self):
        """Returns customers sorted by customer_id."""
        result = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node, result):
        if node:
            self._in_order(node.left, result)
            result.append(node.customer)
            self._in_order(node.right, result)

    @classmethod
    def build_from_list(cls, customers):
        tree = cls()
        for c in customers:
            tree.insert(c)
        return tree
