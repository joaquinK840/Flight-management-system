import { useState, useEffect } from 'react'
import { getTree, searchValue, resetTree, getMetrics, eliminateLeastProfitable, exportTree, loadFile, insertFlight, deleteValue, cancelValue, undoOperation, redoOperation, getTraversal, updateDepthLimit, enableStressMode, disableStressMode, rebalanceTree, auditTree } from '../services/avlService'

/**
 * Custom React hook for managing AVL tree state and operations.
 * 
 * This hook provides a complete interface for tree manipulation including:
 * - Tree state management (tree structure, metrics, depth limit)
 * - Search, insert, delete, and cancel operations
 * - Undo/redo functionality
 * - Tree traversals (inorder, preorder, postorder, BFS)
 * - File import/export and tree comparison
 * - Stress mode testing and audit reports
 * - Tree comparison with BST equivalents
 * 
 * @returns {Object} Hook state and handler functions:
 *   - tree: Current AVL tree root node
 *   - bstTree: BST tree root for comparison
 *   - value: Current input value for operations
 *   - setValue: Function to update current input value
 *   - searchResult: Last search operation result
 *   - treeHeight: Calculated height of AVL tree
 *   - balanceFactor: Balance factor of root node
 *   - traversalMode: Last traversal mode used
 *   - traversalResult: Result of last traversal operation
 *   - comparisonData: AVL vs BST comparison metrics
 *   - showComparison: Flag to display comparison panel
 *   - metrics: Current tree metrics (height, nodes, rotations, etc)
 *   - stressMode: Flag indicating if stress mode is active
 *   - auditReport: Audit report from stress mode analysis
 *   - bstNote: Descriptive note about BST construction
 *   - depthLimit: Current depth limit for price penalties
 *   - Handler functions for all tree operations...
 */
const useAvlTree = () => {
  const [tree, setTree] = useState(null)
  const [bstTree, setBstTree] = useState(null)
  const [value, setValue] = useState('')
  const [searchResult, setSearchResult] = useState(null)
  const [treeHeight, setTreeHeight] = useState(0)
  const [balanceFactor, setBalanceFactor] = useState(0)
  const [traversalMode, setTraversalMode] = useState(null)
  const [traversalResult, setTraversalResult] = useState(null)
  const [comparisonData, setComparisonData] = useState(null)
  const [showComparison, setShowComparison] = useState(false)
  const [metrics, setMetrics] = useState(null)
  const [stressMode, setStressMode] = useState(false)
  const [depthLimit, setDepthLimit] = useState(3)
  const [auditReport, setAuditReport] = useState(null)
  const [bstNote, setBstNote] = useState('')

  useEffect(() => {
    refreshTree()
  }, [])

  /**
   * Load/reload the tree from backend.
   * @returns {Promise<void>}
   */
  const loadTree = async () => {
    await refreshTree()
  }

  /**
   * Refresh tree structure and metrics from backend.
   * Fetches the current AVL tree root and metrics in parallel.
   * Updates local state with tree structure and depth limit.
   * @returns {Promise<void>}
   */
  const refreshTree = async () => {
    try {
      const [treeData, metricsData] = await Promise.all([
        getTree(),
        getMetrics()
      ])
      // Backend returns { root, depth_limit, rotations, metrics }
      setTree(treeData.root)
      setBalanceFactor(treeData.root?.balance_factor ?? 0)
      if (typeof treeData.depth_limit === 'number') {
        setDepthLimit(treeData.depth_limit)
      }
      setMetrics(metricsData)
    } catch (err) {
      console.error('Error loading tree:', err)
    }
  }

  /**
   * Refresh only the tree metrics without reloading tree structure.
   * Useful for quick updates after operations that don't change structure.
   * @returns {Promise<void>}
   */
  const refreshMetrics = async () => {
    try {
      const metricsData = await getMetrics()
      setMetrics(metricsData)
    } catch (err) {
      console.error('Error loading metrics:', err)
    }
  }

  /**
   * Calculate height of a subtree recursively.
   * Returns 0 for null nodes, otherwise 1 + max(left height, right height).
   * @param {Object} node - Tree node to calculate height for
   * @returns {number} Height of the subtree
   */
  const calculateHeight = (node) => {
    if (!node) return 0
    return 1 + Math.max(calculateHeight(node.left), calculateHeight(node.right))
  }

  /**
   * Count total nodes in a subtree recursively.
   * @param {Object} node - Tree node to count from
   * @returns {number} Total node count in subtree
   */
  const countNodes = (node) => {
    if (!node) return 0
    return 1 + countNodes(node.left) + countNodes(node.right)
  }

  /**
   * Load tree from JSON file (topology or insertion mode).
   * Supports two modes:
   *   - "topology": Load tree structure directly, build equivalent BST
   *   - "insertion": Insert flights sequentially to build both AVL and BST
   * Updates comparison data with metrics from both trees.
   * @param {File} file - JSON file to load
   * @param {string} loadType - Load mode "topology" or "insertion"
   * @returns {Promise<void>}
   */
  const handleFileLoad = async (file, loadType) => {
    if (!file) return
    try {
      const data = await loadFile(file, loadType)
      
      // Update both trees
      setTree(data.avl.tree)
      setBstTree(data.bst.tree)
      if (data.load_type === 'topology') {
        setBstNote('BST built by inserting same flights in-order — no automatic balancing')
      } else {
        setBstNote('')
      }
      
      // Store comparison data with real server metrics
      if (data.avl.metrics && data.bst.metrics) {
        setComparisonData({
          avl: {
            height: data.avl.metrics.height,
            nodes: data.avl.metrics.total_nodes,
            leaves: data.avl.metrics.leaves,
            rotations: data.avl.metrics.total_rotations,
            rotationDetail: data.avl.metrics.rotations
          },
          bst: {
            height: data.bst.metrics.height,
            nodes: data.bst.metrics.total_nodes,
            leaves: data.bst.metrics.leaves
          },
          comparison: data.comparison
        })
        setShowComparison(true)
      }
      
      await refreshMetrics()
    } catch (err) {
      console.error('Error loading file:', err)
      alert(`❌ Error loading file: ${err.message}`)
    }
  }

  /**
   * Insert a flight into the AVL tree.
   * Validates and normalizes flight data (codigo, origin, destination, etc).
   * Updates tree structure and metrics.
   * @param {Object} flightData - Flight object with codigo, origen, destino, etc
   * @returns {Promise<void>}
   */
  const handleInsert = async (flightData) => {
    if (!flightData) return
    try {
      const codigo = parseInt(flightData.codigo, 10)
      if (Number.isNaN(codigo)) {
        alert('❌ Invalid value')
        return
      }
      const payload = {
        codigo,
        origen: String(flightData.origen || '').trim(),
        destino: String(flightData.destino || '').trim(),
        horaSalida: String(flightData.horaSalida || '00:00').trim(),
        precioBase: parseFloat(flightData.precioBase || 0),
        pasajeros: parseInt(flightData.pasajeros || 0, 10),
        prioridad: parseInt(flightData.prioridad || 1, 10),
        promocion: Boolean(flightData.promocion)
      }
      const result = await insertFlight(payload)
      setTree(result.tree.root)
      await refreshMetrics()
    } catch (err) {
      console.error('Error inserting flight:', err)
      alert(`❌ Error inserting flight: ${err.message}`)
    }
  }

  /**
   * Delete a flight by its codigo from the tree.
   * Uses simple deletion (not subtree cancellation).
   * Clears input value and refreshes metrics.
   * @returns {Promise<void>}
   */
  const handleDelete = async () => {
    if (!value) return
    try {
      const codigo = parseInt(value)
      const result = await deleteValue(codigo)
      setTree(result.tree)
      setValue('')
      await refreshMetrics()
    } catch (err) {
      console.error('Error deleting flight:', err)
      alert(`❌ Error deleting flight: ${err.message}`)
    }
  }

  /**
   * Cancel a flight and its entire subtree.
   * Performs mass cancellation of all descendant nodes.
   * Clears input and shows success alert.
   * @returns {Promise<void>}
   */
  const handleCancelFlight = async () => {
    if (!value) return
    try {
      const codigo = parseInt(value)
      const result = await cancelValue(codigo)
      setTree(result.tree)
      alert(`✅ Vuelo ${codigo} cancelado!`)
      setValue('')
      await refreshMetrics()
    } catch (err) {
      console.error('Error cancelando vuelo:', err)
      alert(`❌ Error cancelando vuelo: ${err.message}`)
    }
  }

  const handleSearch = async () => {
    if (!value) return
    try {
      const result = await searchValue(parseInt(value))
      setSearchResult(result)
    } catch (err) {
      console.error('Error buscando:', err)
    }
  }

  const handleUndo = async () => {
    try {
      const result = await undoOperation()
      setTree(result.tree.root)
      await refreshMetrics()
    } catch (err) {
      if (err.status === 400) {
        alert('No hay operaciones para deshacer')
      } else {
        console.error('Error deshaciendo:', err)
        alert(`❌ Error deshaciendo: ${err.message}`)
      }
    }
  }

  const handleRedo = async () => {
    try {
      const result = await redoOperation()
      setTree(result.tree.root)
      await refreshMetrics()
    } catch (err) {
      if (err.status === 400) {
        alert('No hay operaciones para rehacer')
      } else {
        console.error('Error rehaciendo:', err)
        alert(`❌ Error rehaciendo: ${err.message}`)
      }
    }
  }

  const handleReset = async () => {
    try {
      await resetTree()
      setTree(null)
      setSearchResult(null)
      await loadTree()
    } catch (err) {
      console.error('Error reiniciando:', err)
    }
  }

  const handleTraversal = async (mode) => {
    try {
      const data = await getTraversal(mode)
      setTraversalMode(data.mode)
      setTraversalResult(data.result)
    } catch (err) {
      console.error('Error en recorrido:', err)
      alert(`❌ Error en recorrido: ${err.message}`)
    }
  }

  const handleExport = async () => {
    try {
      await exportTree()
      alert('✅ Árbol exportado exitosamente como skybalance_avl.json')
    } catch (err) {
      console.error('Error exportando árbol:', err)
      alert(`❌ Error exportando árbol: ${err.message}`)
    }
  }

  const handleShowComparison = (show) => {
    if (show === true && !comparisonData) {
      alert('⚠️ Primero carga un archivo en Modo Inserción para ver la comparación')
      return
    }
    
    if (show === false) {
      setShowComparison(false)
    } else if (show === true && comparisonData) {
      setShowComparison(true)
    }
  }

  const handleDepthLimitChange = async (limit) => {
    try {
      const result = await updateDepthLimit(limit)
      setTree(result.tree)
      if (typeof result.depth_limit === 'number') {
        setDepthLimit(result.depth_limit)
      }
      await refreshMetrics()
    } catch (err) {
      console.error('Error actualizando límite de profundidad:', err)
      alert(`❌ Error actualizando límite de profundidad: ${err.message}`)
    }
  }

  const handleEliminateLeastProfitable = async () => {
    try {
      const result = await eliminateLeastProfitable()
      console.log('Vuelo eliminado:', result)
      // Mostrar alerta al usuario
      if (result.eliminated_code) {
        alert(`✅ Vuelo ${result.eliminated_code} eliminado!\n\nRentabilidad: $${result.eliminated_rentability}\nNodos eliminados: ${result.subtree_size_removed}`)
      }
  await refreshTree()
    } catch (err) {
      console.error('Error eliminando vuelo:', err)
      alert(`❌ Error: ${err.message}`)
    }
  }

  const handleEnableStress = async () => {
    try {
      await enableStressMode()
      setStressMode(true)
      setAuditReport(null)
      alert('✅ Modo estrés habilitado')
    } catch (err) {
      console.error('Error habilitando modo estrés:', err)
      alert(`❌ Error: ${err.message}`)
    }
  }

  const handleDisableStress = async () => {
    try {
      await disableStressMode()
      setStressMode(false)
      setAuditReport(null)
      alert('✅ Modo estrés deshabilitado')
    } catch (err) {
      console.error('Error deshabilitando modo estrés:', err)
      alert(`❌ Error: ${err.message}`)
    }
  }

  const handleRebalance = async () => {
    if (stressMode) {
      alert('⚠️ No puedes rebalancear en modo estrés. Deshabilita el modo primero.')
      return
    }
    try {
      const result = await rebalanceTree()
      if (result?.tree?.root) {
        setTree(result.tree.root)
      } else if (result?.tree) {
        setTree(result.tree)
      } else {
        await loadTree()
      }
      const rotations = result.total_rotations ?? result.rotations_applied ?? 0
      alert(`✅ Árbol rebalanceado\n\nRotaciones aplicadas: ${rotations}`)
      await refreshMetrics()
    } catch (err) {
      console.error('Error rebalanceando:', err)
      alert(`❌ Error: ${err.message}`)
    }
  }

  const handleAudit = async () => {
    if (!stressMode) {
      alert('⚠️ La auditoría solo está disponible en modo estrés')
      return
    }
    try {
      const result = await auditTree()
      setAuditReport(result)
    } catch (err) {
      console.error('Error en auditoría:', err)
      alert(`❌ Error: ${err.message}`)
    }
  }

  const clearAuditReport = () => setAuditReport(null)

  return {
    tree,
    bstTree,
    value,
    setValue,
    searchResult,
    treeHeight: calculateHeight(tree),
    balanceFactor,
    traversalMode,
    traversalResult,
    comparisonData,
    showComparison,
    metrics,
    stressMode,
    auditReport,
    bstNote,
    handleFileLoad,
    handleInsert,
    handleDelete,
    handleCancelFlight,
    handleSearch,
    handleUndo,
    handleRedo,
    handleReset,
    handleTraversal,
    handleExport,
    handleShowComparison,
    handleDepthLimitChange,
    depthLimit,
    handleEliminateLeastProfitable,
    handleEnableStress,
    handleDisableStress,
    handleRebalance,
    handleAudit,
    clearAuditReport,
    loadTree,
    refreshMetrics
  }
}

export default useAvlTree
