import hashlib

def compute_hash(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()

class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

def build_tree(data):
    if len(data) == 1:
        return Node(compute_hash(data[0]))

    left_data = data[:len(data) // 2]
    right_data = data[len(data) // 2:]

    left_subtree = build_tree(left_data)
    right_subtree = build_tree(right_data)

    return Node(compute_hash(left_subtree.data + right_subtree.data), left_subtree, right_subtree)

def verify_tree(root):
    if root.left is None and root.right is None:
        return True

    left_is_valid = verify_tree(root.left)
    right_is_valid = verify_tree(root.right)

    computed_hash = compute_hash(root.left.data + root.right.data)

    if computed_hash != root.data:
        return False

    return left_is_valid and right_is_valid

def hash_in_tree(root, data_hash):
    if root.left is None and root.right is None:
        return root.data == data_hash

    left_result = hash_in_tree(root.left, data_hash)
    right_result = hash_in_tree(root.right, data_hash)

    return left_result or right_result

def insert_data(root, data):
    data_hash = compute_hash(data)

    if root.left is None and root.right is None:
        return Node(compute_hash(root.data + data_hash), root, Node(data_hash))

    if root.left.left is None and root.left.right is None:
        root.left = insert_data(root.left, data)
    elif root.right.left is None and root.right.right is None:
        root.right = insert_data(root.right, data)

    root.data = compute_hash(root.left.data + root.right.data)

    return root

def get_node_hash(root, index):
    if root.left is None and root.right is None:
        if index == 0:
            return root.data

        return None

    if index % 2 == 0 and root.left is not None:
        return get_node_hash(root.left, index // 2)
    elif index % 2 == 1 and root.right is not None:
        return get_node_hash(root.right, index // 2)

    return None

def insert_data_at_index(root, index, data):
    data_hash = compute_hash(data)
    if root.left is None and root.right is None:
        if index == 0:
            root.data = data_hash
            return root

    if index % 2 == 0 and root.left is not None:
        return insert_data_at_index(root.left, index // 2, data)
    elif index % 2 == 1 and root.right is not None:
        return insert_data_at_index(root.right, index // 2, data)

    if index % 2 == 0 and root.left is None:
        left_child = Node(compute_hash(b"default data hash"))
        right_child = Node(root.data)
        root.left = left_child
        root.right = right_child
        root.data = compute_hash(left_child.data + right_child.data)
        return insert_data_at_index(root.left, index // 2, data)
    elif index % 2 == 1 and root.right is None:
        left_child = Node(root.data)
        right_child = Node(compute_hash(b"default data hash"))
        root.left = left_child
        root.right = right_child
        root.data = compute_hash(left_child.data + right_child.data)
        return insert_data_at_index(root.right, index // 2, data)

def recalculate_hashes(root):
    if root.left is None and root.right is None:
        return

    recalculate_hashes(root.left)
    recalculate_hashes(root.right)

    root.data = compute_hash(root.left.data + root.right.data)

def get_index(root, data):
    data_hash = compute_hash(data)
    if root.left is None and root.right is None:
        if root.data == data_hash:
            return 0

    index = None
    if root.left is not None:
        index = get_index(root.left, data)
        if index is not None:
            return 2 * index
    if root.right is not None:
        index = get_index(root.right, data)
        if index is not None:
            return 2 * index + 1

    return None


