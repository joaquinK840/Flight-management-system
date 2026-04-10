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
                rotate_right(tree, node)  # LL
                tree.rotate_right += 1

            else:
                rotate_left(tree, node.getLeftChild())  # LR parte 1
                rotate_right(tree, node)               # LR parte 2
                tree.rotate_left_right += 1

        # RIGHT HEAVY
        elif bf < -1:

            if get_balance_factor(node.getRightChild()) <= 0:
                rotate_left(tree, node)  # RR
                tree.rotate_left += 1

            else:
                rotate_right(tree, node.getRightChild())  # RL parte 1
                rotate_left(tree, node)                   # RL parte 2
                tree.rotate_right_left += 1

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