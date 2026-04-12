import { useState, useEffect } from 'react'
import { getTree, insertValue, searchValue, resetTree, getMetrics, eliminateLeastProfitable, exportTree, loadFile, insertFlight, deleteFlight, cancelFlight, undoOperation, redoOperation, getTraversal, updateDepthLimit, enableStressMode, disableStressMode, rebalanceTree, auditTree } from '../services/avlService'

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

  useEffect(() => {
    loadTree()
  }, [])

  const loadTree = async () => {
    try {
      const data = await getTree()
      // El backend retorna { root, depth_limit, rotations, metrics }
      setTree(data.root)
      setBalanceFactor(data.root?.balance_factor ?? 0)
      if (typeof data.depth_limit === 'number') {
        setDepthLimit(data.depth_limit)
      }
      await refreshMetrics()
    } catch (err) {
      console.error('Error cargando árbol:', err)
    }
  }

  const refreshTree = async () => {
    await loadTree()
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

  const handleFileLoad = async (file, loadType) => {
    if (!file) return
    try {
      const data = await loadFile(file, loadType)
      
      // Actualizar árboles
      setTree(data.avl.tree)
      setBstTree(data.bst.tree.root)
      
      // Guardar datos de comparación con métricas reales del servidor
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
      
      await refreshTree()
    } catch (err) {
      console.error('Error cargando archivo:', err)
      alert(`❌ Error cargando archivo: ${err.message}`)
    }
  }

  const handleInsert = async () => {
    if (!value) return
    try {
      const codigo = parseInt(value)
      const flightData = {
        codigo,
        origen: 'N/A',
        destino: 'N/A',
        horaSalida: '00:00',
        precioBase: 0.0,
        pasajeros: 0,
        prioridad: 0,
        promocion: false,
        alerta: 'normal',
        precioFinal: 0.0
      }
      const result = await insertFlight(flightData)
      setTree(result.tree.root)
      setValue('')
      await refreshTree()
    } catch (err) {
      console.error('Error insertando vuelo:', err)
      alert(`❌ Error insertando vuelo: ${err.message}`)
    }
  }

  const handleDelete = async () => {
    if (!value) return
    try {
      const codigo = parseInt(value)
      const result = await deleteFlight(codigo)
      setTree(result.tree.root)
      setValue('')
      await refreshTree()
    } catch (err) {
      console.error('Error eliminando vuelo:', err)
      alert(`❌ Error eliminando vuelo: ${err.message}`)
    }
  }

  const handleCancelFlight = async () => {
    if (!value) return
    try {
      const codigo = parseInt(value)
      const result = await cancelFlight(codigo)
      setTree(result.tree.root)
      const nodesCanceled = result.nodes_canceled || 1
      alert(`✅ Vuelo ${codigo} cancelado!\n\nNodos cancelados: ${nodesCanceled}`)
      setValue('')
      await refreshTree()
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
      await refreshTree()
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
      await refreshTree()
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
      await refreshTree()
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
    if (show === undefined) {
      if (!comparisonData) {
        alert('⚠️ Primero carga un archivo en Modo Inserción para ver la comparación')
        return
      }
      setShowComparison((prev) => !prev)
      return
    }
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
      await refreshTree()
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
      await loadTree()
      await refreshTree()
    } catch (err) {
      console.error('Error eliminando vuelo:', err)
      alert(`❌ Error: ${err.message}`)
    }
  }

  const handleEnableStress = async () => {
    try {
      const result = await enableStressMode()
      setStressMode(Boolean(result?.stress_mode))
      setAuditReport(null)
      alert('✅ Modo estrés habilitado')
      await refreshTree()
    } catch (err) {
      console.error('Error habilitando modo estrés:', err)
      alert(`❌ Error: ${err.message}`)
    }
  }

  const handleDisableStress = async () => {
    try {
      const result = await disableStressMode()
      setStressMode(Boolean(result?.stress_mode))
      setAuditReport(null)
      alert('✅ Modo estrés deshabilitado')
      await refreshTree()
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
      setTree(result.tree.root)
      const rotations = result.rotations_applied || 0
      alert(`✅ Árbol rebalanceado\n\nRotaciones aplicadas: ${rotations}`)
      await refreshTree()
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
    loadTree,
    refreshTree,
    refreshMetrics
  }
}

export default useAvlTree
