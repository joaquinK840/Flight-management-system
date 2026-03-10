def search_node(currentRoot, value):

    if currentRoot.getValue() == value:
        return currentRoot

    elif value > currentRoot.getValue():

        if currentRoot.getRightChild() is None:
            return None

        return search_node(currentRoot.getRightChild(), value)

    else:

        if currentRoot.getLeftChild() is None:
            return None

        return search_node(currentRoot.getLeftChild(), value)