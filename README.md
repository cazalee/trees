B-Tree Implementation in Python
🔍 Fully Explained, ASCII Illustrated, Commented, and Ready to Run
📘 What is a B-Tree?

A B-Tree is a self-balancing search tree used in databases, file systems, and indexing systems.
It keeps data sorted and allows fast search, insertion, and deletion — all in O(log n) time.

🧠 Why B-Tree?

Unlike a Binary Search Tree (BST):

Each node stores multiple keys.

Tree height stays small and balanced.

Fewer disk accesses (in databases or file systems).

Always sorted and height-balanced.

⚙️ B-Tree Rules
Rule	Meaning
Minimum degree = t	Each node can have max 2t − 1 keys and min t − 1.
Root node	Can have fewer than t − 1 keys.
Children	A node with n keys has n + 1 children.
Sorted order	Keys inside a node are always sorted.
Balance	All leaves are at the same level.
🧩 B-Tree Node Structure
class BTreeNode:
    def __init__(self, t, leaf=True):
        self.t = t                 # Minimum degree
        self.keys = []             # Keys stored here
        self.children = []         # Child pointers
        self.leaf = leaf           # True if leaf node

🧱 B-Tree Example (ASCII)
            [20]
           /    \
       [10]     [30, 40]


✅ 3 nodes:

Root has one key 20.

Two children: left [10] and right [30, 40].

🧩 B-Tree Class Overview
class BTree:
    ├── insert()
    ├── insertNonFull()
    ├── splitChild()
    ├── delete()
    ├── deleteFromNode()
    ├── get_predecessor()
    ├── get_successor()
    ├── merge_children()
    ├── borrowFromPrev()
    ├── borrowFromNext()
    ├── search()
    └── inorder()

⚙️ 1️⃣ Insertion — Explained with ASCII

When inserting a key:

If the root is full, split it → tree grows taller.

Find the correct child and insert recursively.

If child full, split it before going down.

Insert in sorted order.

Example: Insert keys [10, 20, 5, 6, 12, 30, 7, 17]

Step by Step:

Insert 10 → [10]
Insert 20 → [10, 20]
Insert 5  → [5, 10, 20]
Insert 6  → [5, 6, 10, 20]
Insert 12 → [5, 6, 10, 12, 20]  ← full (for t=3)

Split at 10 (middle key):
          [10]
         /    \
     [5,6]   [12,20]


Now continue inserting → new splits handled automatically.

✅ Maintains balance after every insert.

⚙️ 2️⃣ Search

Search moves top-down like binary search but through multiple keys per node.

def search(self, node, key):
    i = 0
    while i < len(node.keys) and key > node.keys[i]:
        i += 1
    if i < len(node.keys) and node.keys[i] == key:
        return (node, i)
    elif node.leaf:
        return (None, -1)
    else:
        return self.search(node.children[i], key)

Example Search Flow

Search for 12:

          [10, 20]
         /    |    \
     [5,6] [12,17] [30]


1️⃣ Compare with 10 → 12 > 10, move right
2️⃣ Compare with 20 → 12 < 20, go to middle child
3️⃣ Found 12 ✅

⚙️ 3️⃣ Inorder Traversal (Sorted Print)
def inorder(self, node):
    if node:
        for i in range(len(node.keys)):
            if not node.leaf:
                self.inorder(node.children[i])   # Left subtree
            print(node.keys[i], end=" ")        # Node key
        if not node.leaf:
            self.inorder(node.children[-1])     # Rightmost child

Why the last child?

A node with n keys has n + 1 children → last child comes after all keys.

ASCII Flow
           [10, 20]
          /    |    \
     [5,7]  [12,17]  [30,40]


Steps:
1️⃣ Visit [5,7] → print 5 7
2️⃣ Print 10
3️⃣ Visit [12,17] → print 12 17
4️⃣ Print 20
5️⃣ Visit [30,40] → print 30 40

✅ Output: 5 7 10 12 17 20 30 40

⚙️ 4️⃣ Get Predecessor and Successor
Predecessor → largest key in left subtree
def get_predecessor(self, node):
    while not node.leaf:
        node = node.children[-1]   # go rightmost child
    return node.keys[-1]

Successor → smallest key in right subtree
def get_successor(self, node):
    while not node.leaf:
        node = node.children[0]    # go leftmost child
    return node.keys[0]

ASCII Example:
           [20]
          /    \
     [10,15]  [25,30]


Predecessor(20) = 15
Successor(20) = 25

⚙️ 5️⃣ Borrow from Previous Sibling

Used when a child has too few keys during deletion.

def borrowFromPrev(self, parent, idx):
    child = parent.children[idx]
    sibling = parent.children[idx - 1]

    child.keys.insert(0, parent.keys[idx - 1])     # Bring parent's key down
    parent.keys[idx - 1] = sibling.keys.pop(-1)    # Move sibling's last key up
    if not sibling.leaf:
        child.children.insert(0, sibling.children.pop(-1))  # Move last child too

ASCII Illustration

Before Borrow:

Parent: [20]
         /   \
   [5]        [25]


Borrow from left:

Move parent’s 20 ↓ right child

Move left’s 5 ↑ to parent

After Borrow:

Parent: [5]
         /   \
   []        [20,25]

⚙️ 6️⃣ Borrow from Next Sibling
def borrowFromNext(self, parent, idx):
    child = parent.children[idx]
    sibling = parent.children[idx + 1]

    child.keys.append(parent.keys[idx])         # Bring parent's key down
    parent.keys[idx] = sibling.keys.pop(0)      # Move sibling's first key up
    if not sibling.leaf:
        child.children.append(sibling.children.pop(0))  # Move first child

ASCII Illustration

Before Borrow:

Parent: [20]
         /   \
   [10]       [25,30]


Borrow from right:

Bring down parent’s 20 → left child

Move sibling’s 25 → up to parent

After Borrow:

Parent: [25]
         /   \
   [10,20]    [30]

⚙️ 7️⃣ Merge Children

Used when both children of a parent key have minimal keys (t − 1).

def merge_children(self, parent, idx):
    child = parent.children[idx]
    sibling = parent.children[idx + 1]

    child.keys.append(parent.keys[idx])        # Pull parent key down
    child.keys.extend(sibling.keys)            # Merge sibling's keys
    if not child.leaf:
        child.children.extend(sibling.children)  # Merge their children
    parent.keys.pop(idx)                       # Remove key from parent
    parent.children.pop(idx + 1)               # Remove merged sibling

ASCII Flow

Before Merge:

Parent: [30]
         /   \
   [10,20]    [40,50]


After Merge:

[10,20,30,40,50]


✅ Height reduces, balance preserved.

⚙️ 8️⃣ Deletion Overview (Simplified)
Cases:

1️⃣ Delete from leaf → direct removal.
2️⃣ Delete from internal node →
  replace with predecessor/successor, then delete recursively.
3️⃣ If child lacks keys →
  borrow from sibling or merge, then continue deletion.

ASCII Flow (Deletion Example)
         [30]
        /    \
   [10,20]   [40,50]


Delete 30:

Cannot stay in parent.

Merge both children → [10,20,30,40,50]

Root reduces height.

✅ Tree remains balanced.

⚙️ 9️⃣ Full Inorder Driver Code Example
if __name__ == "__main__":
    btree = BTree(t=3)  # Minimum degree

    # Insert values
    for k in [10, 20, 5, 6, 12, 30, 7, 17]:
        btree.insert(k)

    print("Inorder traversal after insertion:")
    btree.inorder(btree.root)
    print("\n")

    # Search demo
    print("Searching for 6:", btree.search(btree.root, 6))
    print("Searching for 15:", btree.search(btree.root, 15))

    # Deletion demo
    btree.delete(6)
    print("\nInorder after deleting 6:")
    btree.inorder(btree.root)
    print()

    btree.delete(7)
    print("\nInorder after deleting 7:")
    btree.inorder(btree.root)
    print()

Output:
Inorder traversal after insertion:
5 6 7 10 12 17 20 30

Searching for 6: (<BTreeNode>, 1)
Searching for 15: (None, -1)

Inorder after deleting 6:
5 7 10 12 17 20 30

Inorder after deleting 7:
5 10 12 17 20 30

🧮 Time & Space Complexity
Operation	Time	Space
Search	O(log n)	O(1)
Insert	O(log n)	O(1)
Delete	O(log n)	O(1)
🧾 Summary Diagram
   Root → [K1, K2, K3]
          /    |    |    \
      C0    C1   C2   C3


Each subtree holds values in sorted ranges:

C0 < K1 < C1 < K2 < C2 < K3 < C3

💡 Mnemonics for Quick Recall

Split → Node overflow → divide.

Merge → Node underflow → combine.

Borrow → Take one key from sibling.

Predecessor/Successor → replace during delete.

Inorder → sorted output.

🧠 Visual Summary
           [M]
         /     \
   [L smaller]  [R larger]


✅ Always balanced
✅ Always sorted
✅ O(log n) guaranteed performance



So you can learn, debug, and teach directly from this repo.

End of README ✅
