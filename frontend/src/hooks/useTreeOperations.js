import { useCallback } from 'react'
import {
    cancelValue,
    deleteValue,
    insertValue,
    resetTree,
    searchValue,
} from '../services/avlService'

export const useTreeOperations = ({ loadTree } = {}) => {
    const insert = useCallback(async (value) => {
        const result = await insertValue(value)
        if (loadTree) await loadTree()
        return result
    }, [loadTree])

    const deleteNode = useCallback(async (value) => {
        const result = await deleteValue(value)
        if (loadTree) await loadTree()
        return result
    }, [loadTree])

    const cancel = useCallback(async (value) => {
        const result = await cancelValue(value)
        if (loadTree) await loadTree()
        return result
    }, [loadTree])

    const search = useCallback(async (value) => {
        return searchValue(value)
    }, [])

    const reset = useCallback(async () => {
        const result = await resetTree()
        if (loadTree) await loadTree()
        return result
    }, [loadTree])

    const undo = useCallback(async () => {
        return { supported: false, message: 'Undo no disponible' }
    }, [])

    const redo = useCallback(async () => {
        return { supported: false, message: 'Redo no disponible' }
    }, [])

    return {
        insert,
        delete: deleteNode,
        cancel,
        search,
        undo,
        redo,
        reset,
    }
}
