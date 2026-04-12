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

export const cancelValue = async (value) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/cancel/${value}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Error al cancelar el valor');
        }
        return await response.json();
    } catch (error) {
        console.error('Error en cancelValue:', error);
        throw error;
    }
};