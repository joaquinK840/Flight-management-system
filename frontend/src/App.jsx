import { useEffect, useRef, useState } from 'react'
import './App.css'
import TreeViewer from './components/TreeViewer'
import { cancelFlight, deleteValue, exportToJSON, getBalanceFactor, getBreadthFirst, getInOrder, getPostOrder, getPreOrder, getTree, getTreeComparison, getTreeHeight, insertValue, loadFromJSON, redoOperation, resetTree, searchValue, undoOperation } from './services/avlService'

function App() {
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
  const fileInputRef = useRef(null)

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
      await insertValue(parseInt(value))
      setValue('')
      loadTree()
    } catch (error) {
      console.error('Error insertando:', error)
    }
  }

  const handleDelete = async () => {
    if (!value) return
    try {
      await deleteValue(parseInt(value))
      setValue('')
      loadTree()
    } catch (error) {
      console.error('Error eliminando:', error)
    }
  }

  const handleCancelFlight = async () => {
    if (!value) return
    try {
      await cancelFlight(parseInt(value))
      setValue('')
      loadTree()
    } catch (error) {
      console.error('Error cancelando vuelo:', error)
    }
  }

  const handleSearch = async () => {
    if (!value) return
    try {
      const result = await searchValue(parseInt(value))
      setSearchResult(result)
    } catch (error) {
      console.error('Error buscando:', error)
    }
  }

  const handleUndo = async () => {
    try {
      await undoOperation()
      loadTree()
    } catch (error) {
      console.error('Error en undo:', error)
    }
  }

  const handleRedo = async () => {
    try {
      await redoOperation()
      loadTree()
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
      let result
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

  const handleFileLoad = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    const loadType = event.target.dataset.loadType || 'topology'

    try {
      if (loadType === 'topology') {
        // Modo topología: carga directa
        const result = await loadFromJSON(file, loadType)
        setTree(result.trees.avl)
        setBstTree(result.trees.bst)
        setComparisonData(result.comparison)
        setShowComparison(true)

        // Actualizar propiedades del AVL
        const heightData = await getTreeHeight()
        setTreeHeight(heightData.height)
        const bfData = await getBalanceFactor()
        setBalanceFactor(bfData.balance_factor)

      } else if (loadType === 'insertion') {
        // Modo inserción: carga progresiva simulada en frontend
        const text = await file.text()
        const data = JSON.parse(text)

        if (data.vuelos && Array.isArray(data.vuelos)) {
          // Reiniciar árboles
          await resetTree()
          setTree(null)
          setBstTree(null)
          setComparisonData(null)
          setShowComparison(false)

          // Extraer códigos numéricos y ordenarlos
          const flights = data.vuelos
            .map(flight => {
              const codigoStr = flight.codigo || ''
              if (codigoStr.startsWith('SB')) {
                try {
                  const flightNumber = parseInt(codigoStr.substring(2))
                  return { number: flightNumber, data: flight }
                } catch (e) {
                  return null
                }
              }
              return null
            })
            .filter(flight => flight !== null)
            .sort((a, b) => a.number - b.number)

          // Insertar uno por uno con delay visual
          for (let i = 0; i < flights.length; i++) {
            const { number, data: flightData } = flights[i]

            // Insertar en AVL
            await insertValue(number)

            // Actualizar estado del árbol cada inserción
            const treeData = await getTree()
            setTree(treeData.tree)

            // Actualizar propiedades
            const heightData = await getTreeHeight()
            setTreeHeight(heightData.height)
            const bfData = await getBalanceFactor()
            setBalanceFactor(bfData.balance_factor)

            // Delay de 1 segundo para visualización
            await new Promise(resolve => setTimeout(resolve, 1000))
          }

          // Después de todas las inserciones, crear BST para comparación
          const comparisonResult = await getTreeComparison()
          setComparisonData(comparisonResult.comparison)
          setBstTree(comparisonResult.trees.bst)
          setShowComparison(true)
        }
      }

    } catch (error) {
      console.error('Error cargando archivo:', error)
      alert('Error al cargar el archivo JSON')
    }

    // Limpiar input
    event.target.value = ''
  }

  const handleExport = async () => {
    try {
      const blob = await exportToJSON()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'avl_tree.json'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Error exportando:', error)
      alert('Error al exportar el árbol')
    }
  }

  const handleShowComparison = async () => {
    try {
      const result = await getTreeComparison()
      setComparisonData(result.comparison)
      setTree(result.trees.avl)
      setBstTree(result.trees.bst)
      setShowComparison(true)
    } catch (error) {
      console.error('Error obteniendo comparación:', error)
    }
  }

  return (
    <div className="App">
      <h1>🌲 Árbol AVL - Sistema de Gestión de Vuelos</h1>

      {/* Carga desde JSON */}
      <div style={{
        padding: '20px',
        backgroundColor: '#e8f5e9',
        borderRadius: '8px',
        marginBottom: '20px',
        maxWidth: '800px',
        margin: '0 auto 20px'
      }}>
        <h3>📁 Cargar desde JSON</h3>
        <p style={{ fontSize: '14px', color: '#666', marginBottom: '15px' }}>
          Archivos disponibles: <code>ModoTopología.json</code> y <code>ModoInserción.json</code> en la carpeta data/
        </p>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '15px' }}>
          <input
            type="file"
            accept=".json"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileLoad}
            data-load-type="topology"
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            style={{
              padding: '10px 20px',
              backgroundColor: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Cargar Topología
          </button>

          <input
            type="file"
            accept=".json"
            style={{ display: 'none' }}
            onChange={(e) => {
              e.target.dataset.loadType = 'insertion'
              handleFileLoad(e)
            }}
          />
          <button
            onClick={() => {
              const input = document.createElement('input')
              input.type = 'file'
              input.accept = '.json'
              input.dataset.loadType = 'insertion'
              input.onchange = handleFileLoad
              input.click()
            }}
            style={{
              padding: '10px 20px',
              backgroundColor: '#2196F3',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Cargar por Inserción (SB + número)
          </button>

          <button
            onClick={handleExport}
            style={{
              padding: '10px 20px',
              backgroundColor: '#FF9800',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Exportar JSON
          </button>
        </div>
        <div style={{ fontSize: '12px', color: '#666' }}>
          <strong>Modo Topología:</strong> Carga la estructura completa del árbol desde ModoTopología.json<br/>
          <strong>Modo Inserción:</strong> Extrae números de códigos (ignora "SB"), inserta uno por uno con balanceo automático cada segundo
        </div>
      </div>

      <div style={{
        padding: '20px',
        backgroundColor: '#f9f9f9',
        borderRadius: '8px',
        marginBottom: '20px',
        maxWidth: '800px',
        margin: '0 auto 20px'
      }}>
        <h3>Operaciones del Árbol</h3>
        <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
          <input
            type="number"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleInsert()}
            placeholder="Ingresa un valor"
            style={{
              flex: 1,
              padding: '10px',
              border: '1px solid #ccc',
              borderRadius: '4px',
              fontSize: '14px'
            }}
          />
        </div>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '15px' }}>
          <button
            onClick={handleInsert}
            style={{
              padding: '10px 20px',
              backgroundColor: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Insertar
          </button>
          <button
            onClick={handleDelete}
            style={{
              padding: '10px 20px',
              backgroundColor: '#FF5722',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Eliminar
          </button>
          <button
            onClick={handleCancelFlight}
            style={{
              padding: '10px 20px',
              backgroundColor: '#9C27B0',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Cancelar Vuelo
          </button>
          <button
            onClick={handleSearch}
            style={{
              padding: '10px 20px',
              backgroundColor: '#2196F3',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Buscar
          </button>
          <button
            onClick={handleUndo}
            style={{
              padding: '10px 20px',
              backgroundColor: '#607D8B',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            ↶ Undo
          </button>
          <button
            onClick={handleRedo}
            style={{
              padding: '10px 20px',
              backgroundColor: '#607D8B',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            ↷ Redo
          </button>
          <button
            onClick={handleReset}
            style={{
              padding: '10px 20px',
              backgroundColor: '#f44336',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            Reiniciar
          </button>
        </div>

        {/* Recorridos */}
        <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #ddd' }}>
          <h4 style={{ margin: '0 0 10px' }}>Recorridos del Árbol</h4>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            <button
              onClick={() => handleTraversal('pre')}
              style={{
                padding: '8px 16px',
                backgroundColor: '#FF9800',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '12px',
                fontWeight: 'bold'
              }}
            >
              Preorden
            </button>
            <button
              onClick={() => handleTraversal('in')}
              style={{
                padding: '8px 16px',
                backgroundColor: '#9C27B0',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '12px',
                fontWeight: 'bold'
              }}
            >
              Inorden
            </button>
            <button
              onClick={() => handleTraversal('post')}
              style={{
                padding: '8px 16px',
                backgroundColor: '#E91E63',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '12px',
                fontWeight: 'bold'
              }}
            >
              Postorden
            </button>
            <button
              onClick={() => handleTraversal('bfs')}
              style={{
                padding: '8px 16px',
                backgroundColor: '#673AB7',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '12px',
                fontWeight: 'bold'
              }}
            >
              Por Niveles (BFS)
            </button>
          </div>
        </div>
      </div>

      {/* Información del árbol */}
      {tree && (
        <div style={{
          padding: '15px',
          backgroundColor: '#E8F5E9',
          borderLeft: '4px solid #4CAF50',
          borderRadius: '4px',
          marginBottom: '20px',
          maxWidth: '800px',
          margin: '0 auto 20px'
        }}>
          <h3 style={{ margin: '0 0 10px' }}>Información del Árbol AVL</h3>
          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
            <div>
              <strong>Raíz:</strong> {treeHeight !== null ? treeHeight : 'N/A'}
            </div>
            <div>
              <strong>Profundidad:</strong> {treeHeight}
            </div>
            <div>
              <strong>Hojas:</strong> {tree ? 'Calculando...' : 'N/A'}
            </div>
            <div>
              <strong>Factor de Balance (Raíz):</strong> {balanceFactor}
            </div>
          </div>
        </div>
      )}

      {/* Resultado de búsqueda */}
      {searchResult && (
        <div style={{
          padding: '15px',
          backgroundColor: '#3e4245',
          borderLeft: '4px solid #2196F3',
          borderRadius: '4px',
          marginBottom: '20px',
          maxWidth: '800px',
          margin: '0 auto 20px'
        }}>
          <h3>Resultado de búsqueda:</h3>
          <p>
            <strong>Valor:</strong> {searchResult.value}
          </p>
          <p>
            <strong>Encontrado:</strong> {searchResult.found ? '✓ Sí' : '✗ No'}
          </p>
        </div>
      )}

      {/* Resultado de recorrido */}
      {traversalResult && (
        <div style={{
          padding: '15px',
          backgroundColor: '#FFF3E0',
          borderLeft: '4px solid #FF9800',
          borderRadius: '4px',
          marginBottom: '20px',
          maxWidth: '800px',
          margin: '0 auto 20px'
        }}>
          <h3>
            Recorrido {
              traversalMode === 'pre' ? 'Preorden' :
              traversalMode === 'in' ? 'Inorden' :
              traversalMode === 'post' ? 'Postorden' :
              'Por Niveles'
            }:
          </h3>
          <p style={{ wordBreak: 'break-all', fontFamily: 'monospace' }}>
            {traversalResult.join(' → ')}
          </p>
        </div>
      )}

      {/* Comparación de árboles */}
      {showComparison && comparisonData && (
        <div style={{
          padding: '20px',
          backgroundColor: '#FCE4EC',
          borderRadius: '8px',
          marginBottom: '20px',
          maxWidth: '800px',
          margin: '0 auto 20px'
        }}>
          <h3>📊 Comparación AVL vs BST</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div style={{ padding: '15px', backgroundColor: '#E8F5E9', borderRadius: '8px' }}>
              <h4>🌲 Árbol AVL</h4>
              <p><strong>Raíz:</strong> {comparisonData.avl.root}</p>
              <p><strong>Altura:</strong> {comparisonData.avl.height}</p>
              <p><strong>Hojas:</strong> {comparisonData.avl.leaves}</p>
              <p><strong>Balanceado:</strong> ✓ Sí</p>
            </div>
            <div style={{ padding: '15px', backgroundColor: '#FFF3E0', borderRadius: '8px' }}>
              <h4>🌳 Árbol BST</h4>
              <p><strong>Raíz:</strong> {comparisonData.bst.root}</p>
              <p><strong>Altura:</strong> {comparisonData.bst.height}</p>
              <p><strong>Hojas:</strong> {comparisonData.bst.leaves}</p>
              <p><strong>Balanceado:</strong> ✗ No</p>
            </div>
          </div>
          <button
            onClick={() => setShowComparison(false)}
            style={{
              marginTop: '10px',
              padding: '8px 16px',
              backgroundColor: '#f44336',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Cerrar Comparación
          </button>
        </div>
      )}

      {/* Visualización de árboles */}
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', justifyContent: 'center' }}>
        <TreeViewer tree={tree} title="Árbol AVL" />
        {showComparison && bstTree && (
          <TreeViewer tree={bstTree} title="Árbol BST (Comparación)" />
        )}
      </div>
    </div>
  )
}

export default App
