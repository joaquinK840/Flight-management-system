import { useCallback, useState } from 'react'
import { getTree } from '../services/avlService'

/**
 * Normalize tree data from API response.
 * Handles different response formats from backend.
 * If data has 'root' property, returns root node. Otherwise returns data as-is.
 * @param {any} data - Raw tree data from API
 * @returns {Object|null} Normalized tree root node or null
 */
const normalizeTreePayload = (data) => {
    if (!data) return null
    if (data.root !== undefined) return data.root
    return data
}

/**
 * Custom React hook for managing simple tree state.
 * 
 * Provides lightweight state management for tree structure and metrics.
 * Primarily used for tree loading and caching.
 * 
 * @returns {Object} Hook state and functions:
 *   - tree: Current AVL tree root node
 *   - bstTree: BST tree root for comparison
 *   - treeHeight: Height of the tree
 *   - balanceFactor: Balance factor of root node
 *   - loadTree: Async function to load tree from backend
 */
export const useTreeState = () => {
    const [tree, setTree] = useState(null)
    const [bstTree, setBstTree] = useState(null)
    const [treeHeight, setTreeHeight] = useState(0)
    const [balanceFactor, setBalanceFactor] = useState(0)

    /**
     * Load tree from backend API.
     * Fetches AVL tree structure and normalizes response.
     * Updates all tree-related state variables.
     * @returns {Promise<Object>} Complete tree data from API
     */
    const loadTree = useCallback(async () => {
        const data = await getTree()
        const treePayload = normalizeTreePayload(data?.tree)
        setTree(treePayload)
        setBstTree(data?.bstTree ?? null)
        setTreeHeight(data?.treeHeight ?? 0)
        setBalanceFactor(data?.balanceFactor ?? 0)
        return data
    }, [])

    return {
        tree,
        bstTree,
        treeHeight,
        balanceFactor,
        loadTree,
    }
}
