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
  } = useAvlTree()

  const findDepthByCode = (node, code, depth = 0) => {
    if (!node) return null
    const nodeCode = node.codigo ?? node.value
    if (nodeCode === code) return depth
    const leftDepth = findDepthByCode(node.left, code, depth + 1)
    if (leftDepth !== null) return leftDepth
    return findDepthByCode(node.right, code, depth + 1)
  }

  const buildAuditError = (item) => {
    const heightMismatch = item.expected_height !== item.actual_height
    const balanceMismatch = item.expected_balance === false
    if (heightMismatch && balanceMismatch) return 'Altura y balance'
    if (heightMismatch) return 'Altura incorrecta'
    if (balanceMismatch) return 'Desbalanceado'
    return 'Inconsistencia'
  }

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
        <div
          style={{
            marginBottom: '24px',
            padding: '18px',
            borderRadius: '14px',
            border: `2px solid ${auditReport.valid ? '#4caf50' : '#f44336'}`,
            backgroundColor: auditReport.valid ? '#e8f5e9' : '#ffebee'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px' }}>
            <div style={{ fontWeight: '700' }}>
              {auditReport.valid
                ? `✅ Árbol válido — ${auditReport.nodes_checked} nodos verificados sin inconsistencias`
                : `⚠ Se encontraron ${auditReport.inconsistent_nodes?.length || 0} nodos inconsistentes`}
            </div>
            <button
              onClick={clearAuditReport}
              style={{
                backgroundColor: 'transparent',
                border: 'none',
                fontSize: '16px',
                cursor: 'pointer'
              }}
              aria-label="Cerrar reporte"
            >
              ✕
            </button>
          </div>

          {!auditReport.valid && (
            <div style={{ marginTop: '16px', overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
                <thead>
                  <tr style={{ backgroundColor: '#ffcdd2' }}>
                    <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ef9a9a' }}>Codigo</th>
                    <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ef9a9a' }}>Profundidad</th>
                    <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ef9a9a' }}>Factor Balance</th>
                    <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ef9a9a' }}>Altura Real</th>
                    <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ef9a9a' }}>Altura Esperada</th>
                    <th style={{ textAlign: 'left', padding: '8px', borderBottom: '1px solid #ef9a9a' }}>Error</th>
                  </tr>
                </thead>
                <tbody>
                  {auditReport.inconsistent_nodes?.map((item) => {
                    const depth = findDepthByCode(tree, item.codigo)
                    return (
                      <tr key={`audit-${item.codigo}`}>
                        <td style={{ padding: '8px', borderBottom: '1px solid #ef9a9a' }}>{item.codigo}</td>
                        <td style={{ padding: '8px', borderBottom: '1px solid #ef9a9a' }}>{depth ?? '-'}</td>
                        <td style={{ padding: '8px', borderBottom: '1px solid #ef9a9a' }}>{item.balance_factor}</td>
                        <td style={{ padding: '8px', borderBottom: '1px solid #ef9a9a' }}>{item.actual_height}</td>
                        <td style={{ padding: '8px', borderBottom: '1px solid #ef9a9a' }}>{item.expected_height}</td>
                        <td style={{ padding: '8px', borderBottom: '1px solid #ef9a9a' }}>{buildAuditError(item)}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          )}
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
        <h3 style={{ marginTop: 0, marginBottom: '16px' }}>📋 Cola de Concurrencia</h3>
        <QueueControlComponent
          onQueueUpdated={async () => {
            await loadTree()
            await refreshMetrics()
          }}
        />
      </div>

      <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap', justifyContent: 'center' }}>
        <TreeViewer tree={tree} title="Árbol AVL" />
        {showComparison && bstTree && (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <TreeViewer tree={bstTree} title="Árbol BST (Comparación)" />
            {bstNote && (
              <div style={{ marginTop: '8px', maxWidth: '420px', textAlign: 'center', color: '#b45309', fontSize: '12px' }}>
                {bstNote}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default HomePage
