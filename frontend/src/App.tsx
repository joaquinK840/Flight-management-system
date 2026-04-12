import { useEffect, useState } from 'react'
import './App.css'
import TreeViewer from './components/TreeViewer'
import { getTree, insertValue, resetTree, searchValue } from './services/avlService'

function App() {
  const [tree, setTree] = useState(null)
  const [rotations, setRotations] = useState(null)
  const [showRotations, setShowRotations] = useState(false)
  const [value, setValue] = useState('')
  const [searchResult, setSearchResult] = useState(null)

  useEffect(() => {
    loadTree()
  }, [])

  const loadTree = async () => {
    try {
      const data = await getTree()
      const treeRoot = data?.tree?.root ?? data?.tree ?? null
      const rotationData = data?.tree?.rotations ?? null
      setTree(treeRoot)
      setRotations(rotationData)
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

  const handleSearch = async () => {
    if (!value) return
    try {
      const result = await searchValue(parseInt(value))
      setSearchResult(result)
    } catch (error) {
      console.error('Error buscando:', error)
    }
  }

  const handleReset = async () => {
    try {
      await resetTree()
      setTree(null)
      setRotations(null)
      setShowRotations(false)
      setSearchResult(null)
    } catch (error) {
      console.error('Error reiniciando:', error)
    }
  }

  return (
    <div className="App">
      <h1>🌲 Árbol AVL</h1>
      
      <div style={{ 
        padding: '20px', 
        backgroundColor: '#f9f9f9', 
        borderRadius: '8px', 
        marginBottom: '20px',
        maxWidth: '500px',
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
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
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
      </div>

      {searchResult && (
        <div style={{
          padding: '15px',
          backgroundColor: '#e3f2fd',
          borderLeft: '4px solid #2196F3',
          borderRadius: '4px',
          marginBottom: '20px',
          maxWidth: '500px',
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

      <TreeViewer tree={tree} />

      {rotations && (
        <div style={{
          padding: '12px',
          backgroundColor: '#fff7e6',
          borderLeft: '4px solid #ffb300',
          borderRadius: '4px',
          marginTop: '20px',
          maxWidth: '500px',
          margin: '20px auto 0'
        }}>
          <button
            onClick={() => setShowRotations((prev) => !prev)}
            style={{
              padding: '6px 12px',
              backgroundColor: '#ffb300',
              color: '#1f1f1f',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold'
            }}
          >
            {showRotations ? 'Ocultar detalles' : 'Ver detalles'}
          </button>
          {showRotations && (
            <p style={{ marginTop: '10px' }}>
              Rotaciones: LL {rotations.LL ?? 0} | RR {rotations.RR ?? 0} | LR {rotations.LR ?? 0} | RL {rotations.RL ?? 0}
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export default App
