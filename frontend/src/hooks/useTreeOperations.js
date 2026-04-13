import { useCallback } from 'react'
import {
    cancelValue,
    deleteValue,
    insertValue,
    resetTree,
    searchValue,
} from '../services/avlService'

/**
 * Custom ReactHook for tree operations with optional auto-refresh.
 * 
 * Provides memoized async functions for common AVL tree operations.
 * Each operation that modifies the tree (insert, delete, cancel, reset)
 * optionally calls loadTree to refresh state after completion.
 * 
 * @param {Object} options - Configuration options
 *   - loadTree: Optional callback to refresh tree state after mutations
 * @returns {Object} Operation functions:
 *   - insert: Add a value to the tree
 *   - delete: Remove a value from the tree
 *   - cancel: Cancel a value and its subtree
 *   - search: Search for a value
 *   - reset: Clear the tree
 *   - undo: Undo operation (not supported)
 *   - redo: Redo operation (not supported)
 */
export const useTreeOperations = ({ loadTree } = {}) => {
    /**
     * Insert a value into the tree.
     * Automatically refreshes tree state after insertion.
     * @param {number} value - Value to insert
     * @returns {Promise<Object>} Insert operation result from backend
     */
    const insert = useCallback(async (value) => {
        const result = await insertValue(value)
        if (loadTree) await loadTree()
        return result
    }, [loadTree])

    /**
     * Delete a value from the tree.
     * Automatically refreshes tree state after deletion.
     * @param {number} value - Value to delete
     * @returns {Promise<Object>} Delete operation result from backend
     */
    const deleteNode = useCallback(async (value) => {
        const result = await deleteValue(value)
        if (loadTree) await loadTree()
        return result
    }, [loadTree])

    /**
     * Cancel a value and its entire subtree.
     * Automatically refreshes tree state after cancellation.
     * @param {number} value - Root value of subtree to cancel
     * @returns {Promise<Object>} Cancel operation result from backend
     */
    const cancel = useCallback(async (value) => {
        const result = await cancelValue(value)
        if (loadTree) await loadTree()
        return result
    }, [loadTree])

    /**
     * Search for a value in the tree.
     * Does not modify tree or reload state.
     * @param {number} value - Value to search for
     * @returns {Promise<Object>} Search result with found status
     */
    const search = useCallback(async (value) => {
        return searchValue(value)
    }, [])

    /**
     * Reset tree to empty state.
     * Automatically refreshes tree state after reset.
     * @returns {Promise<Object>} Reset operation confirmation
     */
    const reset = useCallback(async () => {
        const result = await resetTree()
        if (loadTree) await loadTree()
        return result
    }, [loadTree])

    /**
     * Undo operation (not supported in current implementation).
     * Placeholder function returning unsupported message.
     * @returns {Promise<Object>} Object with supported=false
     */
    const undo = useCallback(async () => {
        return { supported: false, message: 'Undo not available' }
    }, [])

    /**
     * Redo operation (not supported in current implementation).
     * Placeholder function returning unsupported message.
     * @returns {Promise<Object>} Object with supported=false
     */
    const redo = useCallback(async () => {
        return { supported: false, message: 'Redo not available' }
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
