class Stack:
    """
    Estructura de datos Stack (LIFO - Last In First Out).
    Utilizada para implementar la pila de undo en el repositorio de arboles.
    """

    def __init__(self):
        self.items = []

    def push(self, item):
        """
        Agrega un elemento al tope de la pila.

        Args:
            item: Elemento a agregar
        """
        self.items.append(item)

    def pop(self):
        """
        Extrae y retorna el elemento del tope de la pila.

        Returns:
            El elemento del tope, o None si la pila esta vacia

        Raises:
            IndexError: Si la pila esta vacia
        """
        if len(self.items) == 0:
            raise IndexError("Pop from empty stack")
        return self.items.pop()

    def peek(self):
        """
        Retorna el elemento del tope sin extraerlo.

        Returns:
            El elemento del tope, o None si la pila esta vacia
        """
        if len(self.items) == 0:
            return None
        return self.items[-1]

    def is_empty(self):
        """
        Verifica si la pila esta vacia.

        Returns:
            bool: True si no hay elementos, False en caso contrario
        """
        return len(self.items) == 0

    def size(self):
        """
        Retorna la cantidad de elementos en la pila.

        Returns:
            int: Numero de elementos
        """
        return len(self.items)

    def clear(self):
        """
        Vacia completamente la pila.
        """
        self.items = []

    def __str__(self):
        return f"Stack({self.items})"

    def __repr__(self):
        return self.__str__()
