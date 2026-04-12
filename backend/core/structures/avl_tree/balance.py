from .rotations import rotate_left, rotate_right


def get_height(node):

    if node is None:
        return -1

    leftHeight = get_height(node.getLeftChild())
    rightHeight = get_height(node.getRightChild())

    return max(leftHeight, rightHeight) + 1


def get_balance_factor(node):

    if node is None:
        return 0

    leftHeight = get_height(node.getLeftChild())
    rightHeight = get_height(node.getRightChild())

    return leftHeight - rightHeight


def check_balance(tree, node):

    while node is not None:

        bf = get_balance_factor(node)

        # LEFT HEAVY
        if bf > 1:

            if get_balance_factor(node.getLeftChild()) >= 0:
                # LL case
                tree.rotation_counts["LL"] += 1
                rotate_right(tree, node)

            else:
                # LR case
                tree.rotation_counts["LR"] += 2
                rotate_left(tree, node.getLeftChild())
                rotate_right(tree, node)

        # RIGHT HEAVY
        elif bf < -1:

            if get_balance_factor(node.getRightChild()) <= 0:
                # RR case
                tree.rotation_counts["RR"] += 1
                rotate_left(tree, node)

            else:
                # RL case
                tree.rotation_counts["RL"] += 2
                rotate_right(tree, node.getRightChild())
                rotate_left(tree, node)

        node = node.getParent()

def get_balance_case(node, bf):

    if bf > 1:

        if get_balance_factor(node.getLeftChild()) >= 0:
            return "LL"
        else:
            return "LR"

    if bf < -1:

        if get_balance_factor(node.getRightChild()) <= 0:
            return "RR"
        else:
            return "RL"