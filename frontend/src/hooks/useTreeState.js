import { useCallback, useState } from 'react'
import { getTree } from '../services/avlService'

const normalizeTreePayload = (data) => {
    if (!data) return null
    if (data.root !== undefined) return data.root
    return data
}

export const useTreeState = () => {
    const [tree, setTree] = useState(null)
    const [bstTree, setBstTree] = useState(null)
    const [treeHeight, setTreeHeight] = useState(0)
    const [balanceFactor, setBalanceFactor] = useState(0)

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
