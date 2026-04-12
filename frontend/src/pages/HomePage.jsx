import { useEffect, useState } from 'react'
import TraversalControls from '../components/controls/TraversalControls'
import TreeOperations from '../components/controls/TreeOperations'
import UploadControls from '../components/controls/UploadControls'
import TreeComparison from '../components/TreeComparison'
import TreeInfo from '../components/TreeInfo'
import TreeViewer from '../components/TreeViewer'
import MetricsPanel from '../components/MetricsPanel'
import VersionPanel from '../components/VersionPanel'
import QueueControlComponent from '../components/QueueControlComponent'
import useAvlTree from '../hooks/useAvlTree'

const HomePage = () => {
  const {
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
  } = useAvlTree()

  const [depthDraft, setDepthDraft] = useState(depthLimit)
  const depthLimitValid = Number.isFinite(depthDraft)

  useEffect(() => {
    setDepthDraft(depthLimit)
  }, [depthLimit])

  return (
    <div className="App" style={{ padding: '20px 24px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{
        position: 'sticky',
        top: 0,
        zIndex: 20,
        backgroundColor: '#0b1c2c',
        color: 'white',
        padding: '12px 16px',
        borderRadius: '12px',
        marginBottom: '16px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '12px'
      }}>
        <span>{stressMode ? '⚡ Modo Estrés' : '🟢 Modo Normal'}</span>
        <span>Profundidad crítica: {depthLimit}</span>
      </div>

      <header style={{ marginBottom: '20px' }}>
        <h1 style={{ textAlign: 'center', marginBottom: '6px' }}>SkyBalance AVL</h1>
        <p style={{ textAlign: 'center', color: '#5f6a72', margin: 0 }}>Sistema de Gestión de Vuelos</p>
      </header>

      <section style={{
        marginBottom: '24px',
        padding: '16px',
        backgroundColor: '#f6f8fb',
        borderRadius: '14px',
        border: '1px solid #e1e6ef'
      }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <label style={{ fontWeight: 600 }}>Profundidad límite</label>
            <input
              type="number"
              min="0"
              max="20"
              value={Number.isFinite(depthDraft) ? depthDraft : ''}
              onChange={(e) => {
                const raw = e.target.value
                if (raw === '') {
                  setDepthDraft(NaN)
                  return
                }
                const parsed = parseInt(raw, 10)
                setDepthDraft(Number.isNaN(parsed) ? NaN : parsed)
              }}
              style={{ padding: '8px 10px', borderRadius: '8px', border: '1px solid #c9d4e5', width: '90px' }}
            />
            <button
              type="button"
              onClick={() => depthLimitValid && handleDepthLimitChange(depthDraft)}
              disabled={!depthLimitValid}
              style={{
                padding: '8px 12px',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: depthLimitValid ? '#fdd835' : '#ddd',
                fontWeight: 700,
                cursor: depthLimitValid ? 'pointer' : 'not-allowed'
              }}
            >
              Aplicar
            </button>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', alignItems: 'center' }}>
            {!stressMode ? (
              <button
                onClick={handleEnableStress}
                style={{
                  padding: '8px 12px',
                  backgroundColor: '#d32f2f',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold'
                }}
              >
                🔥 Activar Modo Estrés
              </button>
            ) : (
              <button
                onClick={handleDisableStress}
                style={{
                  padding: '8px 12px',
                  backgroundColor: '#4caf50',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold'
                }}
              >
                ✅ Modo Normal
              </button>
            )}
            <button
              onClick={handleRebalance}
              disabled={stressMode}
              style={{
                padding: '8px 12px',
                backgroundColor: stressMode ? '#ccc' : '#2196f3',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: stressMode ? 'not-allowed' : 'pointer',
                fontWeight: 'bold',
                opacity: stressMode ? 0.6 : 1
              }}
            >
              ⚖️ Rebalancear
            </button>
            {stressMode && (
              <button
                onClick={handleAudit}
                style={{
                  padding: '8px 12px',
                  backgroundColor: '#ff9800',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold'
                }}
              >
                🔍 Auditar AVL
              </button>
            )}
          </div>
        </div>
      </section>

      <UploadControls
        onFileLoad={handleFileLoad}
        onExport={handleExport}
        onDepthLimitChange={handleDepthLimitChange}
        depthLimit={depthLimit}
        showDepthLimit={false}
      />

      <TreeOperations
        value={value}
        onValueChange={setValue}
        onInsert={handleInsert}
        onDelete={handleDelete}
        onCancelFlight={handleCancelFlight}
        onSearch={handleSearch}
        onShowComparison={() => handleShowComparison()}
        onUndo={handleUndo}
        onRedo={handleRedo}
        onReset={handleReset}
        onEliminateLeastProfitable={handleEliminateLeastProfitable}
        onExport={handleExport}
      />

      {auditReport && (
        <div style={{ marginBottom: '24px', padding: '18px', backgroundColor: '#f5f5f5', borderRadius: '14px', border: '2px solid #ff9800' }}>
          <h3 style={{ marginTop: 0 }}>Reporte de Auditoría</h3>
          <pre style={{ backgroundColor: '#fff', padding: '12px', borderRadius: '8px', overflow: 'auto', fontSize: '12px' }}>
            {JSON.stringify(auditReport, null, 2)}
          </pre>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px', alignItems: 'start', marginBottom: '24px' }}>
        <MetricsPanel metrics={metrics} refreshMetrics={refreshMetrics} />
        <TreeViewer tree={tree} title="Árbol AVL" />
      </div>

      {showComparison && bstTree && (
        <div style={{ marginBottom: '24px' }}>
          <TreeViewer tree={bstTree} title="BST (sin balanceo)" />
        </div>
      )}

      <details style={{ marginBottom: '24px' }}>
        <summary style={{ cursor: 'pointer', fontWeight: 700, marginBottom: '12px' }}>Versiones (colapsable)</summary>
        <VersionPanel onVersionRestored={refreshTree} />
      </details>

      <details style={{ marginBottom: '24px' }}>
        <summary style={{ cursor: 'pointer', fontWeight: 700, marginBottom: '12px' }}>Cola de inserción (colapsable)</summary>
        <QueueControlComponent onQueueUpdated={refreshTree} />
      </details>

      {tree && <TreeInfo tree={tree} treeHeight={treeHeight} balanceFactor={balanceFactor} />}

      {searchResult && (
        <div style={{ marginBottom: '24px', padding: '18px', backgroundColor: '#1f2833', color: 'white', borderRadius: '14px' }}>
          <h3 style={{ marginTop: 0 }}>Resultado de búsqueda</h3>
          <p><strong>Valor:</strong> {searchResult.value}</p>
          <p><strong>Encontrado:</strong> {searchResult.found ? '✓ Sí' : '✗ No'}</p>
        </div>
      )}

      <div style={{ marginBottom: '24px', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '16px', boxShadow: '0 10px 22px rgba(24, 110, 255, 0.08)' }}>
        <TraversalControls onTraversal={handleTraversal} />
      </div>

      {traversalResult && (
        <div style={{ marginBottom: '24px', padding: '18px', backgroundColor: '#FFF3E0', borderRadius: '14px' }}>
          <h3 style={{ marginTop: 0 }}>
            Recorrido {
              traversalMode === 'pre' ? 'Preorden' :
              traversalMode === 'in' ? 'Inorden' :
              traversalMode === 'post' ? 'Postorden' :
              'Por Niveles'
            }
          </h3>
          <p style={{ wordBreak: 'break-all', fontFamily: 'monospace' }}>
            {Array.isArray(traversalResult) ? traversalResult.join(' → ') : traversalResult}
          </p>
        </div>
      )}

      {showComparison && comparisonData && (
        <TreeComparison data={comparisonData} onClose={() => handleShowComparison(false)} />
      )}
    </div>
  )
}

export default HomePage
