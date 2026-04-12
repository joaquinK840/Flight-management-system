class Node:
    """
    Nodo para árbol binario. Gestiona estructura de árbol y datos asociados.
    Single Responsibility: Solo maneja estructura, no lógica de negocio.
    """

    def __init__(self, value, datos=None):
        """
        Inicializa un nodo con valor y datos opcionales de vuelo.
        
        Args:
            value (int): Valor numérico del nodo (clave de búsqueda)
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

    # Métodos para gestión de valor
    def getValue(self):
        return self.value

    # Métodos para gestión de altura (AVL)
    def getHeight(self):
        return self.height

    def setHeight(self, h):
        self.height = h

    # Métodos para gestión de datos de vuelo
    def getDatos(self):
        return self.datos

    def setDatos(self, d):
        self.datos = d

    # Métodos para gestión de children
    def setRightChild(self, node):
        self.rightChild = node

    def getRightChild(self):
        return self.rightChild

    def setLeftChild(self, node):
        self.leftChild = node

    def getLeftChild(self):
        return self.leftChild

    # Métodos para gestión de parent
    def setParent(self, node):
        self.parent = node

    def getParent(self):
        return self.parent