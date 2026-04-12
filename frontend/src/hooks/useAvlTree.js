import { useState, useEffect } from 'react'
import { getTree, insertValue, searchValue, resetTree, getMetrics, eliminateLeastProfitable, exportTree } from '../services/avlService'

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

  useEffect(() => {
    loadTree()
  }, [])

  const loadTree = async () => {
    try {
      const data = await getTree()
      setTree(data.tree)
      await refreshMetrics()
    } catch (err) {
      console.error('Error cargando árbol:', err)
    }
  }

  const refreshMetrics = async () => {
    try {
      const metricsData = await getMetrics()
      setMetrics(metricsData)
    } catch (err) {
      console.error('Error cargando métricas:', err)
    }
  }

  const calculateHeight = (node) => {
    if (!node) return 0
    return 1 + Math.max(calculateHeight(node.left), calculateHeight(node.right))
  }

  const countNodes = (node) => {
    if (!node) return 0
    return 1 + countNodes(node.left) + countNodes(node.right)
  }

  const handleFileLoad = async (file) => {
    console.log('Cargar archivo:', file)
  }

  const handleInsert = async () => {
    if (!value) return
    try {
      await insertValue(parseInt(value))
      setValue('')
      await loadTree()
    } catch (err) {
      console.error('Error insertando:', err)
    }
  }

  const handleDelete = async () => {
    if (!value) return
    console.log('Eliminar:', value)
    setValue('')
    await loadTree()
  }

  const handleCancelFlight = async () => {
    console.log('Cancelar vuelo')
    await loadTree()
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

  const handleUndo = () => {
    console.log('Deshacer')
  }

  const handleRedo = () => {
    console.log('Rehacer')
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
    console.log('Recorrido:', mode)
    setTraversalMode(mode)
    setTraversalResult([1, 2, 3, 4, 5])
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
    setShowComparison(show !== false)
    if (show) {
      setComparisonData({
        avl: { height: calculateHeight(tree), nodes: countNodes(tree), rotations: metrics?.rotation_counts?.total || 0 },
        bst: { height: calculateHeight(tree), nodes: countNodes(tree), balanced: false }
      })
    }
  }

  const handleDepthLimitChange = (limit) => {
    console.log('Límite de profundidad:', limit)
  }

  const handleEliminateLeastProfitable = async () => {
    try {
      const result = await eliminateLeastProfitable()
      console.log('Vuelo eliminado:', result)
      // Mostrar alerta al usuario
      if (result.eliminated_code) {
        alert(`✅ Vuelo ${result.eliminated_code} eliminado!\n\nRentabilidad: $${result.eliminated_rentability}\nNodos eliminados: ${result.subtree_size_removed}`)
      }
      await loadTree()
      await refreshMetrics()
    } catch (err) {
      console.error('Error eliminando vuelo:', err)
      alert(`❌ Error: ${err.message}`)
    }
  }

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
    handleEliminateLeastProfitable,
    refreshMetrics
  }
}

export default useAvlTree
