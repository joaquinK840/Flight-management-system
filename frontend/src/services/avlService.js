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