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
        const response = await fetch(`${API_BASE_URL}/avl/export`);
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

export const loadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
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
            throw new Error('Error al insertar vuelo');
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