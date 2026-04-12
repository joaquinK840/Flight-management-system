class Node:
    """
    Nodo para arbol binario. Gestiona estructura de arbol y datos asociados.
    Single Responsibility: Solo maneja estructura, no logica de negocio.
    """

    def __init__(self, value, datos=None):
        """
        Inicializa un nodo con valor y datos opcionales de vuelo.

        Args:
            value (int): Valor numerico del nodo (clave de busqueda)
            datos (dict, optional): Datos del vuelo. Puede contener:
                - codigo: str
                - origen: str
                - destino: str
                - horaSalida: str
                - precioBase: float
                - precioFinal: float
                - pasajeros: int
                - promocion: bool
                - alerta: str
                - prioridad: int
        """
        self.value = value
        self.height = 1
        self.datos = datos
        self.parent = None
        self.leftChild = None
        self.rightChild = None

    # Metodos para gestion de valor
    def getValue(self):
        return self.value

    # Metodos para gestion de altura (AVL)
    def getHeight(self):
        return self.height

    def setHeight(self, h):
        self.height = h

    # Metodos para gestion de datos de vuelo
    def getDatos(self):
        return self.datos

    def setDatos(self, d):
        self.datos = d

    # Metodos para gestion de children
    def setRightChild(self, node):
        self.rightChild = node

    def getRightChild(self):
        return self.rightChild

    def setLeftChild(self, node):
        self.leftChild = node

    def getLeftChild(self):
        return self.leftChild

    # Metodos para gestion de parent
    def setParent(self, node):
        self.parent = node

    def getParent(self):
        return self.parent
