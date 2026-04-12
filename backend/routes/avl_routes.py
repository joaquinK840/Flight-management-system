import json

from core.structures.avl_tree.tree import AVL
from core.structures.bst_tree.bst import BST
from core.structures.node.node import Node
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/avl", tags=["AVL Tree"])

# instancia global del arbol AVL
avl = AVL()
# instancia global del arbol BST para comparacion
bst = BST()


# Serializador con informacion de altura y balance
def serialize_with_info(node):

    if node is None:
        return None

    return {
        "value": node.getValue(),
        "height": avl.altura(node),
        "balance_factor": avl.obtenerFactorBalance(node),
        "left": serialize_with_info(node.getLeftChild()),
        "right": serialize_with_info(node.getRightChild())
    }


# Serializador basico
def serialize(node):

    if node is None:
        return None

    return {
        "value": node.getValue(),
        "left": serialize(node.getLeftChild()),
        "right": serialize(node.getRightChild())
    }


# -----------------------------
# INSERTAR NODO
# -----------------------------
@router.post("/insert/{value}")
def insert_value(value: int):

    node = Node(value)

    avl.insert(node)

    return {
        "message": "Nodo insertado",
        "root": avl.getRoot().getValue(),
        "tree": serialize(avl.getRoot())
    }


# -----------------------------
# OBTENER ARBOL COMPLETO
# -----------------------------
@router.get("/tree")
def get_tree():

    root = avl.getRoot()

    return {
        "tree": serialize(root)
    }


# -----------------------------
# BUSCAR VALOR
# -----------------------------
@router.get("/search/{value}")
def search_value(value: int):

    node = avl.search(value)

    if node is None:
        return {
            "found": False,
            "value": value
        }

    return {
        "found": True,
        "value": node.getValue()
    }


# -----------------------------
# REINICIAR ARBOL
# -----------------------------
@router.delete("/reset")
def reset_tree():

    global avl
    avl = AVL()

    return {
        "message": "Arbol reiniciado"
    }


# Recorrido preorden
@router.get("/pre-order")
def get_pre_order():

    result = avl.preOrden()

    return {
        "traversal": result
    }


# Recorrido inorden
@router.get("/in-order")
def get_in_order():

    result = avl.inOrden()

    return {
        "traversal": result
    }


# Recorrido postorden
@router.get("/post-order")
def get_post_order():

    result = avl.postOrden()

    return {
        "traversal": result
    }


# Recorrido por niveles (BFS)
@router.get("/breadth-first")
def get_breadth_first():

    result = avl.recorridoAnchura()

    return {
        "traversal": result
    }


# Obtener arbol con informacion de altura y balance
@router.get("/tree-info")
def get_tree_info():

    root = avl.getRoot()

    return {
        "tree": serialize_with_info(root)
    }


# Consultar nodos en rango de distancia
@router.get("/range/{x_min}/{x_max}/{y_min}/{y_max}")
def get_nodes_in_range(x_min: float, x_max: float, y_min: float, y_max: float):

    result = avl.consultarDistancia(x_min, x_max, y_min, y_max)

    return {
        "nodes": result
    }


# Obtener altura del arbol
@router.get("/height")
def get_tree_height():

    root = avl.getRoot()
    height = avl.altura(root) if root else -1

    return {
        "height": height
    }


# Obtener factor de balance de la raiz
@router.get("/balance-factor")
def get_balance_factor():

    root = avl.getRoot()
    bf = avl.obtenerFactorBalance(root) if root else 0

    return {
        "balance_factor": bf
    }


# Eliminar nodo
@router.delete("/delete/{value}")
def delete_value(value: int):

    try:
        avl.delete(value)

        return {
            "message": f"Nodo {value} eliminado correctamente",
            "tree": serialize(avl.getRoot())
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": f"No se pudo eliminar el nodo {value}"
        }


# Cancelar vuelo (eliminar subarbol)
@router.delete("/cancel-flight/{value}")
def cancel_flight(value: int):

    try:
        avl.cancelar_vuelo(value)

        return {
            "message": f"Vuelo {value} cancelado (subarbol eliminado)",
            "tree": serialize(avl.getRoot())
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": f"No se pudo cancelar el vuelo {value}"
        }


# Undo operacion
@router.post("/undo")
def undo_operation():

    success = avl.undo()

    return {
        "success": success,
        "message": "Operacion deshecha" if success else "No hay operaciones para deshacer",
        "tree": serialize(avl.getRoot())
    }


# Redo operacion
@router.post("/redo")
def redo_operation():

    success = avl.redo()

    return {
        "success": success,
        "message": "Operacion rehecha" if success else "No hay operaciones para rehacer",
        "tree": serialize(avl.getRoot())
    }


# Cargar arbol desde JSON
@router.post("/load-json")
async def load_from_json(file: UploadFile = File(...), load_type: str = "topology"):

    global avl, bst

    try:
        # Leer contenido del archivo
        content = await file.read()
        data = json.loads(content.decode("utf-8"))

        # Reiniciar arboles
        avl = AVL()
        bst = BST()

        if load_type == "topology":
            # Cargar respetando topologia del ModoTopologia.json
            def build_tree_from_topology(node_data):
                if node_data is None or not isinstance(node_data, dict):
                    return None

                # Crear nodo con el codigo como valor
                node = Node(node_data.get("codigo"))
                # Guardar todos los datos del vuelo
                node.setDatos(node_data)

                # Procesar hijo izquierdo
                if "izquierdo" in node_data and node_data["izquierdo"]:
                    left_child = build_tree_from_topology(node_data["izquierdo"])
                    if left_child:
                        node.setLeftChild(left_child)
                        left_child.setParent(node)

                # Procesar hijo derecho
                if "derecho" in node_data and node_data["derecho"]:
                    right_child = build_tree_from_topology(node_data["derecho"])
                    if right_child:
                        node.setRightChild(right_child)
                        right_child.setParent(node)

                return node

            # El archivo ModoTopologia.json tiene la estructura del arbol directamente
            avl.root = build_tree_from_topology(data)

        elif load_type == "insertion":
            # Cargar mediante insercion progresiva del ModoInsercion.json
            if "vuelos" in data:
                import asyncio

                # Extraer codigos numericos (sin "SB") y ordenarlos
                flights = []
                for flight_data in data["vuelos"]:
                    codigo_str = flight_data.get("codigo", "")
                    # Extraer solo el numero despues de "SB"
                    if codigo_str.startswith("SB"):
                        try:
                            flight_number = int(codigo_str[2:])
                            flights.append((flight_number, flight_data))
                        except ValueError:
                            continue

                # Ordenar por codigo numerico
                flights.sort(key=lambda x: x[0])

                # Insertar uno por uno con delay para visualizacion
                for flight_number, flight_data in flights:
                    # Insertar en AVL
                    node = Node(flight_number)
                    node.setDatos(flight_data)
                    avl.insert(node)

                    # Insertar en BST para comparacion
                    bst_node = Node(flight_number)
                    bst_node.setDatos(flight_data)
                    bst.insert(bst_node)

                    # Pequeno delay para visualizacion progresiva (1 segundo)
                    await asyncio.sleep(1)

        return {
            "message": f"Arbol cargado desde JSON ({load_type})",
            "load_type": load_type,
            "comparison": {
                "avl": {
                    "root": avl.get_raiz_valor(),
                    "height": avl.get_profundidad(),
                    "leaves": avl.contar_hojas()
                },
                "bst": {
                    "root": bst.getRoot().getValue() if bst.getRoot() else None,
                    "height": bst.get_height(),
                    "leaves": bst.count_leaves()
                }
            },
            "trees": {
                "avl": serialize_with_info(avl.getRoot()),
                "bst": bst.serialize()
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al cargar JSON: {str(e)}")


# Exportar arbol a JSON
@router.get("/export-json")
def export_to_json():

    def serialize_to_topology(node):
        if node is None:
            return None

        # Obtener los datos del nodo (origen, destino, etc.)
        datos = node.getDatos() or {}

        # Construir el nodo con la estructura de ModoTopologia.json
        node_data = {
            "codigo": node.getValue(),
            "origen": datos.get("origen", ""),
            "destino": datos.get("destino", ""),
            "horaSalida": datos.get("horaSalida", ""),
            "precioBase": datos.get("precioBase", 0),
            "precioFinal": datos.get("precioFinal", 0),
            "pasajeros": datos.get("pasajeros", 0),
            "promocion": datos.get("promocion", False),
            "alerta": datos.get("alerta", False),
            "altura": avl.altura(node),
            "factorEquilibrio": avl.obtenerFactorBalance(node),
            "izquierdo": serialize_to_topology(node.getLeftChild()),
            "derecho": serialize_to_topology(node.getRightChild())
        }
        return node_data

    # Exportar directamente el arbol con la estructura de topologia
    tree_data = serialize_to_topology(avl.getRoot())

    return JSONResponse(
        content=tree_data,
        headers={"Content-Disposition": "attachment; filename=avl_tree.json"}
    )


# Obtener comparacion de arboles
@router.get("/comparison")
def get_tree_comparison():

    return {
        "comparison": {
            "avl": {
                "root": avl.get_raiz_valor(),
                "height": avl.get_profundidad(),
                "leaves": avl.contar_hojas(),
                "in_order": avl.inOrden()
            },
            "bst": {
                "root": bst.getRoot().getValue() if bst.getRoot() else None,
                "height": bst.get_height(),
                "leaves": bst.count_leaves(),
                "in_order": bst.in_order_traversal()
            }
        },
        "trees": {
            "avl": serialize_with_info(avl.getRoot()),
            "bst": bst.serialize()
        }
    }
