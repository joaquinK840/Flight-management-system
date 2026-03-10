from .balance import check_balance


def insert_node(tree, currentRoot, node):

    if node.getValue() == currentRoot.getValue():
        print(f"El valor {node.getValue()} ya existe.")

    elif node.getValue() > currentRoot.getValue():

        if currentRoot.getRightChild() is None:

            currentRoot.setRightChild(node)
            node.setParent(currentRoot)

            check_balance(tree, currentRoot)

        else:

            insert_node(tree, currentRoot.getRightChild(), node)

    else:

        if currentRoot.getLeftChild() is None:

            currentRoot.setLeftChild(node)
            node.setParent(currentRoot)

            check_balance(tree, currentRoot)

        else:

            insert_node(tree, currentRoot.getLeftChild(), node)