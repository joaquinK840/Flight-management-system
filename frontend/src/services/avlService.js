const API_BASE_URL = 'http://localhost:8000'; // Ajusta si el backend corre en otro puerto

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

export const getMetrics = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/metrics`);
        if (!response.ok) {
            throw new Error('Error al obtener las métricas');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getMetrics:', error);
        throw error;
    }
};

export const eliminateLeastProfitable = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/eliminate-least-profitable`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Error al eliminar vuelo de menor rentabilidad');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en eliminateLeastProfitable:', error);
        throw error;
    }
};

export const exportTree = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/export-json`);
        if (!response.ok) {
            throw new Error('Error al exportar el árbol');
        }
        
        // Obtener el blob (archivo)
        const blob = await response.blob();
        
        // Crear URL temporal
        const url = window.URL.createObjectURL(blob);
        
        // Crear link temporal
        const link = document.createElement('a');
        link.href = url;
        link.download = 'skybalance_avl.json';
        
        // Simular clic para descargar
        document.body.appendChild(link);
        link.click();
        
        // Limpiar
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        
        return true;
    } catch (error) {
        console.error('Error en exportTree:', error);
        throw error;
    }
};

export const loadFile = async (file, loadType) => {
    const formData = new FormData();
    formData.append('file', file);
    if (loadType) {
        formData.append('load_type', loadType);
    }
    const response = await fetch(`${API_BASE_URL}/avl/load-file`, {
        method: 'POST',
        body: formData  // NO poner Content-Type header, fetch lo setea solo
    });
    if (!response.ok) throw new Error(await response.text());
    return response.json();
};

export const insertFlight = async (flightData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/insert`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(flightData),
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error HTTP ${response.status}`)
        }
        return await response.json();
    } catch (error) {
        console.error('Error en insertFlight:', error);
        throw error;
    }
};

export const deleteFlight = async (codigo) => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/delete/${codigo}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Error al eliminar vuelo');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en deleteFlight:', error);
        throw error;
    }
};

export const cancelFlight = async (codigo) => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/cancel/${codigo}`, {
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
        const response = await fetch(`${API_BASE_URL}/flights/undo`, {
            method: 'POST',
        });
        if (!response.ok) {
            const error = new Error('Error al deshacer');
            error.status = response.status;
            throw error;
        }
        return await response.json();
    } catch (error) {
        console.error('Error en undoOperation:', error);
        throw error;
    }
};

export const redoOperation = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/redo`, {
            method: 'POST',
        });
        if (!response.ok) {
            const error = new Error('Error al rehacer');
            error.status = response.status;
            throw error;
        }
        return await response.json();
    } catch (error) {
        console.error('Error en redoOperation:', error);
        throw error;
    }
};

export const getTraversal = async (mode) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/traversal/${mode}`, {
            method: 'GET',
        });
        if (!response.ok) {
            throw new Error('Error obteniendo recorrido');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getTraversal:', error);
        throw error;
    }
};

export const updateDepthLimit = async (limit) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/config/depth-limit`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ limit }),
        });
        if (!response.ok) {
            throw new Error(await response.text());
        }
        return await response.json();
    } catch (error) {
        console.error('Error en updateDepthLimit:', error);
        throw error;
    }
};

export const enableStressMode = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/stress-mode/enable`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error al habilitar modo estrés');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en enableStressMode:', error);
        throw error;
    }
};

export const disableStressMode = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/stress-mode/disable`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error al deshabilitar modo estrés');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en disableStressMode:', error);
        throw error;
    }
};

export const rebalanceTree = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/rebalance`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error al rebalancear');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en rebalanceTree:', error);
        throw error;
    }
};

export const auditTree = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/audit`);
        if (!response.ok) {
            throw new Error('Error en auditoría');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en auditTree:', error);
        throw error;
    }
};

export const listVersions = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/versions/list`);
        if (!response.ok) {
            throw new Error('Error listando versiones');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en listVersions:', error);
        throw error;
    }
};

export const saveVersion = async (name) => {
    try {
        const response = await fetch(`${API_BASE_URL}/versions/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name }),
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error guardando versión');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en saveVersion:', error);
        throw error;
    }
};

export const restoreVersion = async (name) => {
    try {
        // Codificar el nombre para URL (espacios, caracteres especiales, etc)
        const encodedName = encodeURIComponent(name);
        const response = await fetch(`${API_BASE_URL}/versions/restore/${encodedName}`, {
            method: 'POST',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error restaurando versión');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en restoreVersion:', error);
        throw error;
    }
};

export const deleteVersion = async (name) => {
    try {
        // Codificar el nombre para URL
        const encodedName = encodeURIComponent(name);
        const response = await fetch(`${API_BASE_URL}/versions/${encodedName}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error eliminando versión');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en deleteVersion:', error);
        throw error;
    }
};

export const addToQueue = async (flightData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/queue/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(flightData),
        });
        if (!response.ok) {
            throw new Error('Error agregando vuelo a la cola');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en addToQueue:', error);
        throw error;
    }
};

export const getPendingQueue = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/queue/pending`);
        if (!response.ok) {
            throw new Error('Error obteniendo cola pendiente');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en getPendingQueue:', error);
        throw error;
    }
};

export const processOneFromQueue = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/queue/process-one`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error procesando vuelo de la cola');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en processOneFromQueue:', error);
        throw error;
    }
};

export const processAllFromQueue = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/queue/process-all`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error procesando cola completa');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en processAllFromQueue:', error);
        throw error;
    }
};

export const clearQueue = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/queue/clear`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Error limpiando la cola');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en clearQueue:', error);
        throw error;
    }
};