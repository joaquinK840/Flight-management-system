from fastapi import HTTPException

from services.avl_service import AVLService


class TreeController:
	def __init__(self, avl_service: AVLService):
		self.avl_service = avl_service

	def insert_value(self, value: int) -> dict:
		try:
			return self.avl_service.insert_value(value)
		except Exception as exc:
			raise HTTPException(status_code=500, detail=str(exc))

	def get_tree(self) -> dict:
		try:
			return self.avl_service.get_tree()
		except Exception as exc:
			raise HTTPException(status_code=500, detail=str(exc))

	def search_value(self, value: int) -> dict:
		try:
			return self.avl_service.search_value(value)
		except Exception as exc:
			raise HTTPException(status_code=500, detail=str(exc))

	def cancel_value(self, value: int) -> dict:
		try:
			return self.avl_service.cancel_value(value)
		except ValueError as exc:
			raise HTTPException(status_code=404, detail=str(exc))
		except Exception as exc:
			raise HTTPException(status_code=500, detail=str(exc))

	def delete_value(self, value: int) -> dict:
		try:
			return self.avl_service.delete_value(value)
		except ValueError as exc:
			raise HTTPException(status_code=404, detail=str(exc))
		except Exception as exc:
			raise HTTPException(status_code=500, detail=str(exc))

	def reset_tree(self) -> dict:
		try:
			return self.avl_service.reset_tree()
		except Exception as exc:
			raise HTTPException(status_code=500, detail=str(exc))


tree_controller = TreeController(AVLService())

