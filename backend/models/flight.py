class Flight:
    """
    Model representing a flight with all its associated data.

    Attributes:
        codigo: Flight identifier (numeric)
        prioridad: Priority level (default: 0 for topology mode)
        origen: Origin city
        destino: Destination city
        horaSalida: Departure time
        precioBase: Base price of the flight
        precioFinal: Final price after penalties/discounts
        pasajeros: Number of passengers
        promocion: Whether flight has a promotion
        alerta: Alert flag
    """

    def __init__(self, codigo, origen="", destino="", horaSalida="",
                 precioBase=0, pasajeros=0, prioridad=0, promocion=False,
                 alerta=False, precioFinal=None):
        self.codigo = codigo
        self.prioridad = prioridad
        self.origen = origen
        self.destino = destino
        self.horaSalida = horaSalida
        self.precioBase = precioBase
        self.precioFinal = precioFinal if precioFinal is not None else precioBase
        self.pasajeros = pasajeros
        self.promocion = promocion
        self.alerta = alerta

    @classmethod
    def from_dict(cls, data):
        """
        Create a Flight instance from a dictionary.

        Args:
            data: Dictionary containing flight information

        Returns:
            Flight instance
        """
        if data is None:
            return None

        # Extract code from 'codigo' field, removing 'SB' prefix if present
        codigo = data.get('codigo')
        if isinstance(codigo, str) and codigo.startswith('SB'):
            try:
                codigo = int(codigo[2:])
            except ValueError:
                codigo = int(codigo) if codigo.isdigit() else codigo
        else:
            codigo = int(codigo) if isinstance(codigo, (int, str)) else codigo

        return cls(
            codigo=codigo,
            prioridad=data.get('prioridad', 0),
            origen=data.get('origen', ''),
            destino=data.get('destino', ''),
            horaSalida=data.get('horaSalida', ''),
            precioBase=data.get('precioBase', 0),
            precioFinal=data.get('precioFinal', data.get('precioBase', 0)),
            pasajeros=data.get('pasajeros', 0),
            promocion=data.get('promocion', False),
            alerta=data.get('alerta', False)
        )

    def to_dict(self):
        """
        Convert Flight instance to dictionary.

        Returns:
            Dictionary representation of the flight
        """
        return {
            'codigo': self.codigo,
            'prioridad': self.prioridad,
            'origen': self.origen,
            'destino': self.destino,
            'horaSalida': self.horaSalida,
            'precioBase': self.precioBase,
            'precioFinal': self.precioFinal,
            'pasajeros': self.pasajeros,
            'promocion': self.promocion,
            'alerta': self.alerta
        }

    def __repr__(self):
        return f"Flight({self.codigo}, {self.origen}->{self.destino}, ${self.precioFinal})"
