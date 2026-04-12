from dataclasses import dataclass


@dataclass
class Flight:
	codigo: int
	origen: str
	destino: str
	hora_salida: str
	precio_base: float
	precio_final: float
	pasajeros: int
	prioridad: int = 0
	promocion: bool = False
	alerta: bool = False
	penalizacion: float = 0.0
	nodo_critico: bool = False

	@classmethod
	def from_dict(cls, data: dict) -> "Flight":
		"""Build a Flight from a raw dict (handles both topology and insertion JSON formats)."""
		codigo_raw = data.get("codigo", 0)
		# Handle "SB400" format from insertion JSON
		if isinstance(codigo_raw, str) and codigo_raw.startswith("SB"):
			codigo = int(codigo_raw[2:])
		else:
			codigo = int(codigo_raw)
		return cls(
			codigo=codigo,
			origen=data.get("origen", ""),
			destino=data.get("destino", ""),
			hora_salida=data.get("horaSalida", ""),
			precio_base=float(data.get("precioBase", 0)),
			precio_final=float(data.get("precioFinal", data.get("precioBase", 0))),
			pasajeros=int(data.get("pasajeros", 0)),
			prioridad=int(data.get("prioridad", 0)),
			promocion=bool(data.get("promocion", False)),
			alerta=bool(data.get("alerta", False)),
		)

	def to_dict(self) -> dict:
		return {
			"codigo": self.codigo,
			"origen": self.origen,
			"destino": self.destino,
			"horaSalida": self.hora_salida,
			"precioBase": self.precio_base,
			"precioFinal": self.precio_final,
			"pasajeros": self.pasajeros,
			"prioridad": self.prioridad,
			"promocion": self.promocion,
			"alerta": self.alerta,
			"penalizacion": self.penalizacion,
			"nodoCritico": self.nodo_critico,
		}
