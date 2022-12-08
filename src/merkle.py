import hashlib

def compute_hash(data):
    h = hashlib.sha256()

    h.update(data)

    return h.hexdigest()

class Node:
    def __init__(self, data):
        self.data = data

        self.hash = compute_hash(data)

        self.left = None
        self.right = None

class MerkleTree:
    def __init__(self, data_blocks):
        self.leaves = [Node(block) for block in data_blocks]

        self.parents = []

        while len(self.leaves) > 1:
            left_hash = self.leaves[0].hash
            right_hash = self.leaves[1].hash

            parent = Node(left_hash + right_hash)

            parent.left = self.leaves[0]
            parent.right = self.leaves[1]

            self.parents.append(parent)

            self.leaves = self.leaves[2:]

        if len(self.leaves) == 1:
            self.root = self.leaves[0]

        else:
            self.root = None

    def insert(self, data_block):
        leaf = Node(data_block)

        self.leaves.append(leaf)

        while len(self.leaves) > 1:
            left_hash = self.leaves[0].hash
            right_hash = self.leaves[1].hash

            parent = Node(left_hash + right_hash)

            parent.left = self.leaves[0]
            parent.right = self.leaves[1]

            self.parents.append(parent)

            self.leaves = self.leaves[2:]

        if len(self.leaves) == 1:
            self.root = self.leaves[0]


def verify(tree, data_block):
    if tree.root is None:
        return False

    current_node = tree.root

    while current_node.left is not None:
        if current_node.left.hash == compute_hash(current_node.data[:len(current_node.data) // 2]):
            current_node = current_node.left

        else:
            current_node = current_node.right

    return current_node.hash == compute_hash(data_block)

