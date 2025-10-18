

class BTreeNode: 
    def __init__(self, t, leaf=False):
        self.t = t                  # Minimum degree (defines range for keys)
        self.keys = []              # List of keys in the node
        self.children = []          # References to child nodes
        self.leaf = leaf            # True if node is a leaf (no children)
        
class BTree: 
    def __init__(self, t):
        self.t = t
        self.root = BTreeNode(t, leaf=True)   # Root starts empty and is a leaf
        
    # ---------------- INSERT ----------------
    def insert(self, key):
        root = self.root
        # If root is full, split it and grow tree height
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(self.t, leaf=False)  # New root (not leaf)
            new_root.children.append(self.root)       # Old root becomes child
            self.splitChild(new_root, 0)              # Split old root
            self.root = new_root                      # Update root
            self.insertNonFull(new_root, key)         # Insert into new root
        else: 
            # If root not full, normal insertion
            self.insertNonFull(root, key)
            
    def insertNonFull(self, Node, key): 
        if Node.leaf: 
            # Insert key into leaf → just add and sort
            Node.keys.append(key)
            Node.keys.sort()
        else: 
            # If internal node, go down to the correct child
            i = len(Node.keys) - 1
            while i >= 0 and key < Node.keys[i]:
                i -= 1
            i += 1
            # If child is full, split it first
            if len(Node.children[i].keys) == 2 * self.t - 1:
                self.splitChild(Node, i)
                # After split, decide which of the two children to go into
                if key > Node.keys[i]:
                    i += 1
            # Recurse into the correct child
            self.insertNonFull(Node.children[i], key)
            
    def splitChild(self, parent, i): 
        t = self.t
        full = parent.children[i]            # The child to split
        right = BTreeNode(t, leaf=full.leaf) # New right child
        
        # Move middle key up to parent
        parent.keys.insert(i, full.keys[t-1])
        # Add new right child to parent
        parent.children.insert(i+1, right)
        
        # Split keys between left (full) and right (new)
        right.keys = full.keys[t:]     # Right half
        full.keys = full.keys[:t-1]    # Left half
        
        # If not leaf, also split children
        if not full.leaf: 
            right.children = full.children[t:]   # Right half children
            full.children = full.children[:t]    # Left half children
            
    # ---------------- DELETE ----------------
    def delete(self, key): 
        self.deleteFromNode(self.root, key)  # Call recursive delete
        # If root becomes empty and has children → shrink tree height
        if not self.root.leaf and len(self.root.keys) == 0:
            self.root = self.root.children[0]
            
    def deleteFromNode(self, Node, key): 
        t = self.t
        i = 0 
        # Step 1: Find position of key in node
        while i < len(Node.keys) and key > Node.keys[i]: 
            i += 1
        
        # Case 1: Key found in this node
        if i < len(Node.keys) and Node.keys[i] == key: 
            if Node.leaf: 
                # 1a: If leaf → remove directly
                Node.keys.pop(i)
            else: 
                # 1b: If internal node
                if len(Node.children[i].keys) >= t: 
                    # Borrow predecessor from left child
                    pred = self.get_predecessor(Node.children[i])
                    Node.keys[i] = pred
                    self.deleteFromNode(Node.children[i], pred)
                elif len(Node.children[i+1].keys) >= t:
                    # Borrow successor from right child
                    succ = self.get_successor(Node.children[i+1])
                    Node.keys[i] = succ
                    self.deleteFromNode(Node.children[i+1], succ)
                else: 
                    # Both children have min keys → merge and delete
                    self.merge_children(Node, i)
                    self.deleteFromNode(Node.children[i], key)
            return 
        
        # Case 2: Key not found in this node
        if Node.leaf: 
            return  # Key not in tree → stop
        child = Node.children[i]
        
        # Ensure child has at least t keys before recursing
        if len(child.keys) < t: 
            if i > 0 and len(Node.children[i-1].keys) >= t: 
                self.borrowFromprev(Node, i)     # Borrow from left sibling
            elif i < len(Node.children)-1 and len(Node.children[i+1].keys) >= t: 
                self.borrowFromNext(Node, i)     # Borrow from right sibling
            else: 
                # If no borrowing possible, merge
                if i < len(Node.children)-1:
                    self.merge_children(Node, i)
                else: 
                    self.merge_children(Node, i-1)
                    i -= 1
        # Recurse into child (after fixing size)
        self.deleteFromNode(Node.children[i], key)
            
    # ---------------- SEARCH ----------------
    def search(self, key): 
        Node = self.root
        while True: 
            i = 0 
            # Find first key ≥ search key
            while i < len(Node.keys) and key > Node.keys[i]: 
                i += 1
            if i < len(Node.keys) and Node.keys[i] == key: 
                return (Node, i)  # Found
            if Node.leaf:
                return (None, -1) # Not found
            Node = Node.children[i]  # Move down
            
    # ---------------- INORDER TRAVERSAL ----------------
    def inorder(self, Node):
        if Node:
            for i in range(len(Node.keys)):
                if not Node.leaf:
                    self.inorder(Node.children[i])   # Visit left child
                print(Node.keys[i], end=" ")         # Print current key
            if not Node.leaf:
                self.inorder(Node.children[-1])      # Visit rightmost child
                    
    # ---------------- HELPERS ----------------
    def get_predecessor(self, Node):
        # Go down to rightmost leaf of subtree
        while not Node.leaf:
            Node = Node.children[-1]
        return Node.keys[-1]

    def get_successor(self, Node):
        # Go down to leftmost leaf of subtree
        while not Node.leaf:
            Node = Node.children[0]
        return Node.keys[0]

    def merge_children(self, parent, idx):
        # Merge children[idx] and children[idx+1]
        child = parent.children[idx]
        sibling = parent.children[idx + 1]
        child.keys.append(parent.keys[idx])       # Pull parent key down
        child.keys.extend(sibling.keys)           # Add sibling’s keys
        if not child.leaf:
            child.children.extend(sibling.children) # Add sibling’s children
        parent.keys.pop(idx)                      # Remove key from parent
        parent.children.pop(idx + 1)              # Remove sibling from parent

    def borrowFromprev(self, parent, idx):
        # Borrow from left sibling
        child = parent.children[idx]
        sibling = parent.children[idx - 1]
        child.keys.insert(0, parent.keys[idx - 1])  # Parent key → child
        parent.keys[idx - 1] = sibling.keys.pop(-1) # Sibling last → parent
        if not sibling.leaf:
            child.children.insert(0, sibling.children.pop(-1))

    def borrowFromNext(self, parent, idx):
        # Borrow from right sibling
        child = parent.children[idx]
        sibling = parent.children[idx + 1]
        child.keys.append(parent.keys[idx])        # Parent key → child
        parent.keys[idx] = sibling.keys.pop(0)     # Sibling first → parent
        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))


# ---------------- DRIVER CODE ----------------
if __name__ == "__main__":
    btree = BTree(t=3)  # Minimum degree = 3

    # Insert keys
    for k in [10, 20, 5, 6, 12, 30, 7, 17]:
        btree.insert(k)

    print("Inorder traversal after insertion:")
    btree.inorder(btree.root)
    print("\n")                    
    
    # Search keys
    print("Searching for 6:", btree.search(6))
    print("Searching for 15:", btree.search(15))

    # Delete keys
    btree.delete(6)
    print("\nInorder traversal after deleting 6:")
    btree.inorder(btree.root)
    print("\n")

    btree.delete(13)  # Non-existent
    print("\nInorder traversal after deleting 13 (non-existent):")
    btree.inorder(btree.root)
    print("\n")

    btree.delete(7)
    print("\nInorder traversal after deleting 7:")
    btree.inorder(btree.root)
    print()
