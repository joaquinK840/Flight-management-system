"""
Binary tree node structure.

This module defines the Node class, which represents a node in a binary tree
with support for AVL balancing and associated flight data.
"""

class Node:
    """
    Binary tree node with AVL balancing support.

    Manages tree structure and associated flight data. Follows single responsibility
    principle by handling only structural operations, not business logic.

    Attributes:
        value: Numeric value of the node (search key)
        height: Node height for AVL balancing
        datos: Associated flight data dictionary
        parent: Parent node reference
        leftChild: Left child node
        rightChild: Right child node
    """

    def __init__(self, value, datos=None):
        """
        Initialize a node with value and optional flight data.

        Args:
            value (int): Numeric value of the node (search key)
            datos (dict, optional): Flight data dictionary containing:
                - codigo: Flight code
                - origen: Origin city
                - destino: Destination city
                - horaSalida: Departure time
                - precioBase: Base price
                - precioFinal: Final price
                - pasajeros: Number of passengers
                - promocion: Promotion flag
                - alerta: Alert status
                - prioridad: Priority level
        """
        self.value = value
        self.height = 1
        self.datos = datos
        self.parent = None
        self.leftChild = None
        self.rightChild = None

    def getValue(self):
        """
        Get the node's value.

        Returns:
            int: The node's numeric value
        """
        return self.value

    def getHeight(self):
        """
        Get the node's height for AVL balancing.

        Returns:
            int: The node's height
        """
        return self.height

    def setHeight(self, h):
        """
        Set the node's height.

        Args:
            h (int): New height value
        """
        self.height = h

    def getDatos(self):
        """
        Get the associated flight data.

        Returns:
            dict: Flight data dictionary or None
        """
        return self.datos

    def setDatos(self, d):
        """
        Set the associated flight data.

        Args:
            d (dict): Flight data dictionary
        """
        self.datos = d

    def getLeftChild(self):
        """
        Get the left child node.

        Returns:
            Node or None: The left child node
        """
        return self.leftChild

    def setLeftChild(self, node):
        """
        Set the left child node.

        Args:
            node (Node): The node to set as left child
        """
        self.leftChild = node

    def getRightChild(self):
        """
        Get the right child node.

        Returns:
            Node or None: The right child node
        """
        return self.rightChild

    def setRightChild(self, node):
        """
        Set the right child node.

        Args:
            node (Node): The node to set as right child
        """
        self.rightChild = node

    def getParent(self):
        """
        Get the parent node.

        Returns:
            Node or None: The parent node
        """
        return self.parent

    def setParent(self, node):
        """
        Set the parent node.

        Args:
            node (Node): The node to set as parent
        """
        self.parent = node