import { API_BASE_URL } from '../config/api'

export const insertValue = async (value) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/insert/${value}`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error al insertar el valor');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en insertValue:', error);
        throw error;
    }
};

export const getTree = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/tree`);
        if (!response.ok) {
            throw new Error('Error al obtener el árbol');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getTree:', error);
        throw error;
    }
};

export const getTreeWithInfo = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/tree-info`);
        if (!response.ok) {
            throw new Error('Error al obtener el árbol con información');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getTreeWithInfo:', error);
        throw error;
    }
};

export const searchValue = async (value) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/search/${value}`);
        if (!response.ok) {
            throw new Error('Error al buscar el valor');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en searchValue:', error);
        throw error;
    }
};

export const resetTree = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/reset`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Error al reiniciar el árbol');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en resetTree:', error);
        throw error;
    }
};

export const getPreOrder = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/pre-order`);
        if (!response.ok) {
            throw new Error('Error al obtener recorrido preorden');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getPreOrder:', error);
        throw error;
    }
};

export const getInOrder = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/in-order`);
        if (!response.ok) {
            throw new Error('Error al obtener recorrido inorden');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getInOrder:', error);
        throw error;
    }
};

export const getPostOrder = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/post-order`);
        if (!response.ok) {
            throw new Error('Error al obtener recorrido postorden');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getPostOrder:', error);
        throw error;
    }
};

export const getBreadthFirst = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/breadth-first`);
        if (!response.ok) {
            throw new Error('Error al obtener recorrido por niveles');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getBreadthFirst:', error);
        throw error;
    }
};

export const getNodesInRange = async (xMin, xMax, yMin, yMax) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/range/${xMin}/${xMax}/${yMin}/${yMax}`);
        if (!response.ok) {
            throw new Error('Error al consultar nodos en rango');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getNodesInRange:', error);
        throw error;
    }
};

export const getTreeHeight = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/height`);
        if (!response.ok) {
            throw new Error('Error al obtener altura del árbol');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getTreeHeight:', error);
        throw error;
    }
};

export const getBalanceFactor = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/balance-factor`);
        if (!response.ok) {
            throw new Error('Error al obtener factor de balance');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getBalanceFactor:', error);
        throw error;
    }
};

export const deleteValue = async (value) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/delete/${value}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Error al eliminar el valor');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en deleteValue:', error);
        throw error;
    }
};

export const cancelFlight = async (value) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/cancel-flight/${value}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Error al cancelar vuelo');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en cancelFlight:', error);
        throw error;
    }
};

export const undoOperation = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/undo`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error al deshacer operación');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en undoOperation:', error);
        throw error;
    }
};

export const redoOperation = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/redo`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error al rehacer operación');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en redoOperation:', error);
        throw error;
    }
};

export const loadFromJSON = async (file, loadType = 'topology', onProgress = null) => {
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('load_type', loadType);

        const response = await fetch(`${API_BASE_URL}/avl/load-json`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Error al cargar desde JSON');
        }

        const result = await response.json();

        // Si hay callback de progreso y es modo inserción, actualizar en tiempo real
        if (onProgress && loadType === 'insertion') {
            // Para modo inserción, podríamos implementar polling aquí si es necesario
            // Por ahora, devolver el resultado final
        }

        return result;
    } catch (error) {
        console.error('Error en loadFromJSON:', error);
        throw error;
    }
};

export const exportToJSON = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/export-json`);
        if (!response.ok) {
            throw new Error('Error al exportar a JSON');
        }
        return await response.blob();
    } catch (error) {
        console.error('Error en exportToJSON:', error);
        throw error;
    }
};

export const getTreeComparison = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/comparison`);
        if (!response.ok) {
            throw new Error('Error al obtener comparación');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getTreeComparison:', error);
        throw error;
    }
};