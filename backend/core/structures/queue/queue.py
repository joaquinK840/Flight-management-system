"""
Queue (Cola) - Estructura FIFO.
First In, First Out: el primer elemento agregado es el primero en ser extraído.
"""


class Queue:
    """Cola FIFO simple."""
    
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """
        Agregar un elemento a la cola (al final).
        
        Args:
            item: Elemento a agregar
        """
        self.items.append(item)
    
    def dequeue(self):
        """
        Extraer el primer elemento de la cola.
        
        Returns:
            El elemento al frente de la cola
            
        Raises:
            IndexError: Si la cola está vacía
        """
        if len(self.items) == 0:
            raise IndexError("Cola vacía")
        return self.items.pop(0)
    
    def peek(self):
        """
        Ver el primer elemento sin extraerlo.
        
        Returns:
            El elemento al frente de la cola
            
        Raises:
            IndexError: Si la cola está vacía
        """
        if len(self.items) == 0:
            raise IndexError("Cola vacía")
        return self.items[0]
    
    def is_empty(self):
        """
        Verificar si la cola está vacía.
        
        Returns:
            bool: True si está vacía
        """
        return len(self.items) == 0
    
    def size(self):
        """
        Obtener el tamaño de la cola.
        
        Returns:
            int: Cantidad de elementos en la cola
        """
        return len(self.items)
    
    def clear(self):
        """Vaciar la cola."""
        self.items = []
    
    def get_all(self):
        """
        Obtener todos los elementos sin modificar la cola.
        
        Returns:
            list: Copia de los elementos en la cola
        """
        return self.items.copy()
