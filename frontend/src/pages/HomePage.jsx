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
    refreshMetrics
  } = useAvlTree()

  return (
    <div className="App" style={{ padding: '20px 24px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '24px' }}>🌲 Árbol AVL - Sistema de Gestión de Vuelos</h1>

      <UploadControls
        onFileLoad={handleFileLoad}
        onExport={handleExport}
        onDepthLimitChange={handleDepthLimitChange}
        depthLimit={depthLimit}
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

      <div style={{ marginBottom: '24px', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '16px', boxShadow: '0 10px 22px rgba(24, 110, 255, 0.08)' }}>
        <TraversalControls onTraversal={handleTraversal} />
      </div>

      {stressMode && (
        <div style={{ marginBottom: '24px', padding: '18px', backgroundColor: '#d32f2f', color: 'white', borderRadius: '14px', fontWeight: 'bold', fontSize: '16px' }}>
          ⚠️ MODO ESTRÉS ACTIVO - Sin balanceo automático
        </div>
      )}

      <div style={{ marginBottom: '24px', padding: '20px', backgroundColor: stressMode ? '#fff3e0' : '#e3f2fd', borderRadius: '16px', boxShadow: '0 10px 22px rgba(24, 110, 255, 0.08)' }}>
        <h3 style={{ marginTop: 0 }}>{stressMode ? '🔥' : '✅'} Modo Estrés</h3>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          {!stressMode ? (
            <button
              onClick={handleEnableStress}
              style={{
                padding: '10px 16px',
                backgroundColor: '#d32f2f',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 'bold',
                fontSize: '14px'
              }}
            >
              🔥 Activar Modo Estrés
            </button>
          ) : (
            <button
              onClick={handleDisableStress}
              style={{
                padding: '10px 16px',
                backgroundColor: '#4caf50',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 'bold',
                fontSize: '14px'
              }}
            >
              ✅ Modo Normal
            </button>
          )}
          <button
            onClick={handleRebalance}
            disabled={stressMode}
            style={{
              padding: '10px 16px',
              backgroundColor: stressMode ? '#ccc' : '#2196f3',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: stressMode ? 'not-allowed' : 'pointer',
              fontWeight: 'bold',
              fontSize: '14px',
              opacity: stressMode ? 0.6 : 1
            }}
          >
            ⚖️ Rebalancear
          </button>
          {stressMode && (
            <button
              onClick={handleAudit}
              style={{
                padding: '10px 16px',
                backgroundColor: '#ff9800',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: 'bold',
                fontSize: '14px'
              }}
            >
              🔍 Auditar AVL
            </button>
          )}
        </div>
      </div>

      {auditReport && (
        <div style={{ marginBottom: '24px', padding: '18px', backgroundColor: '#f5f5f5', borderRadius: '14px', border: '2px solid #ff9800' }}>
          <h3 style={{ marginTop: 0 }}>Reporte de Auditoría</h3>
          <pre style={{ backgroundColor: '#fff', padding: '12px', borderRadius: '8px', overflow: 'auto', fontSize: '12px' }}>
            {JSON.stringify(auditReport, null, 2)}
          </pre>
        </div>
      )}

      {tree && <TreeInfo tree={tree} treeHeight={treeHeight} balanceFactor={balanceFactor} />}

      {searchResult && (
        <div style={{ marginBottom: '24px', padding: '18px', backgroundColor: '#1f2833', color: 'white', borderRadius: '14px' }}>
          <h3 style={{ marginTop: 0 }}>Resultado de búsqueda</h3>
          <p><strong>Valor:</strong> {searchResult.value}</p>
          <p><strong>Encontrado:</strong> {searchResult.found ? '✓ Sí' : '✗ No'}</p>
        </div>
      )}

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

      <MetricsPanel metrics={metrics} refreshMetrics={refreshMetrics} />

      <VersionPanel onVersionRestored={loadTree} />

      <div style={{ marginBottom: '24px', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '16px', boxShadow: '0 10px 22px rgba(24, 110, 255, 0.08)' }}>
        <h3 style={{ marginTop: 0, marginBottom: '16px' }}>📋 Cola de Inserción</h3>
        <QueueControlComponent />
      </div>

      <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap', justifyContent: 'center' }}>
        <TreeViewer tree={tree} title="Árbol AVL" />
        {showComparison && bstTree && <TreeViewer tree={bstTree} title="Árbol BST (Comparación)" />}
      </div>
    </div>
  )
}

export default HomePage
