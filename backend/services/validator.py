"""
AVL property validator. Delegates to stress_mode_service.audit_tree().
"""
from services.stress_mode_service import audit_tree as _audit_tree


def validate_avl_property(avl) -> dict:
	"""Validate AVL balance and height invariants for every node."""
	return _audit_tree(avl)
