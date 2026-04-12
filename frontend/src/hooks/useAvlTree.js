import { useEffect, useState } from 'react'
import { LOAD_MODE_INSERTION, LOAD_MODE_TOPOLOGY } from '../models/treeModes'
import {
    cancelFlight,
    deleteValue,
    exportToJSON,
    getBalanceFactor,
    getBreadthFirst,
    getInOrder,
    getPostOrder,
    getPreOrder,
    getTree,
    getTreeComparison,
    getTreeHeight,
    insertValue,
    loadFromJSON,
    redoOperation,
    resetTree,
    searchValue,
    undoOperation,
    setDepthLimit
} from '../services/avlService'
import { parseInsertionFlights } from '../utils/treeHelpers'

const useAvlTree = () => {
  const [tree, setTree] = useState(null)
  const [bstTree, setBstTree] = useState(null)
  const [value, setValue] = useState('')
  const [searchResult, setSearchResult] = useState(null)
  const [treeHeight, setTreeHeight] = useState(null)
  const [balanceFactor, setBalanceFactor] = useState(null)
  const [traversalMode, setTraversalMode] = useState(null)
  const [traversalResult, setTraversalResult] = useState(null)
  const [comparisonData, setComparisonData] = useState(null)
  const [showComparison, setShowComparison] = useState(false)

  useEffect(() => {
    loadTree()
  }, [])

  const loadTree = async () => {
    try {
      const data = await getTree()
      setTree(data.tree)
      const heightData = await getTreeHeight()
      setTreeHeight(heightData.height)
      const bfData = await getBalanceFactor()
      setBalanceFactor(bfData.balance_factor)
    } catch (error) {
      console.error('Error cargando el árbol:', error)
    }
  }

  const handleInsert = async () => {
    if (!value) return

    try {
      await insertValue(parseInt(value, 10))
      setValue('')
      await loadTree()
    } catch (error) {
      console.error('Error insertando:', error)
    }
  }

  const handleDelete = async () => {
    if (!value) return

    try {
      await deleteValue(parseInt(value, 10))
      setValue('')
      await loadTree()
    } catch (error) {
      console.error('Error eliminando:', error)
    }
  }

  const handleCancelFlight = async () => {
    if (!value) return

    try {
      await cancelFlight(parseInt(value, 10))
      setValue('')
      await loadTree()
    } catch (error) {
      console.error('Error cancelando vuelo:', error)
    }
  }

  const handleSearch = async () => {
    if (!value) return

    try {
      const result = await searchValue(parseInt(value, 10))
      setSearchResult(result)
    } catch (error) {
      console.error('Error buscando:', error)
    }
  }

  const handleUndo = async () => {
    try {
      await undoOperation()
      await loadTree()
    } catch (error) {
      console.error('Error en undo:', error)
    }
  }

  const handleRedo = async () => {
    try {
      await redoOperation()
      await loadTree()
    } catch (error) {
      console.error('Error en redo:', error)
    }
  }

  const handleReset = async () => {
    try {
      await resetTree()
      setTree(null)
      setBstTree(null)
      setSearchResult(null)
      setTreeHeight(null)
      setBalanceFactor(null)
      setTraversalResult(null)
      setComparisonData(null)
      setShowComparison(false)
    } catch (error) {
      console.error('Error reiniciando:', error)
    }
  }

  const handleTraversal = async (mode) => {
    try {
      let result = null

      switch (mode) {
        case 'pre':
          result = await getPreOrder()
          break
        case 'in':
          result = await getInOrder()
          break
        case 'post':
          result = await getPostOrder()
          break
        case 'bfs':
          result = await getBreadthFirst()
          break
        default:
          return
      }

      setTraversalMode(mode)
      setTraversalResult(result.traversal)
    } catch (error) {
      console.error('Error en recorrido:', error)
    }
  }

  const handleFileLoad = async (file, loadType) => {
    if (!file) return

    try {
      if (loadType === LOAD_MODE_TOPOLOGY) {
        const result = await loadFromJSON(file, loadType)
        setTree(result.trees.avl)
        setBstTree(result.trees.bst)
        setComparisonData(result.comparison)
        setShowComparison(true)

        const heightData = await getTreeHeight()
        setTreeHeight(heightData.height)
        const bfData = await getBalanceFactor()
        setBalanceFactor(bfData.balance_factor)
      } else if (loadType === LOAD_MODE_INSERTION) {
        const text = await file.text()
        const data = JSON.parse(text)
        const flights = parseInsertionFlights(data)

        if (!flights.length) {
          alert('El archivo no contiene vuelos válidos para inserción.')
          return
        }

        await resetTree()
        setTree(null)
        setBstTree(null)
        setComparisonData(null)
        setShowComparison(false)

        for (let i = 0; i < flights.length; i += 1) {
          const { number } = flights[i]
          await insertValue(number)
          const treeData = await getTree()
          setTree(treeData.tree)
          const heightData = await getTreeHeight()
          setTreeHeight(heightData.height)
          const bfData = await getBalanceFactor()
          setBalanceFactor(bfData.balance_factor)
          await new Promise((resolve) => setTimeout(resolve, 1000))
        }

        const comparisonResult = await getTreeComparison()
        setComparisonData(comparisonResult.comparison)
        setBstTree(comparisonResult.trees.bst)
        setShowComparison(true)
      }
    } catch (error) {
      console.error('Error cargando archivo:', error)
      alert('Error al cargar el archivo JSON')
    }
  }

  const handleExport = async () => {
    try {
      const blob = await exportToJSON()
      const url = window.URL.createObjectURL(blob)
      const anchor = document.createElement('a')
      anchor.href = url
      anchor.download = 'avl_tree.json'
      document.body.appendChild(anchor)
      anchor.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(anchor)
    } catch (error) {
      console.error('Error exportando:', error)
      alert('Error al exportar el árbol')
    }
  }

  const handleShowComparison = (visible) => {
    if (visible === false) {
      setShowComparison(false)
      return
    }

    return getTreeComparison()
      .then((result) => {
        setComparisonData(result.comparison)
        setTree(result.trees.avl)
        setBstTree(result.trees.bst)
        setShowComparison(true)
      })
      .catch((error) => {
        console.error('Error obteniendo comparación:', error)
      })
  }

  const handleDepthLimitChange = async (depthLimit) => {
    try {
      const result = await setDepthLimit(depthLimit)
      // Actualizar el árbol con los nuevos valores de precios
      setTree(result.tree)
      setComparisonData(result.comparison)
    } catch (error) {
      console.error('Error cambiando profundidad límite:', error)
      alert('Error al aplicar la profundidad límite')
    }
  }

  return {
    tree,
    bstTree,
    value,
    setValue,
    searchResult,
    treeHeight,
    balanceFactor,
    traversalMode,
    traversalResult,
    comparisonData,
    showComparison,
    loadTree,
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
    handleDepthLimitChange
  }
}

export default useAvlTree
