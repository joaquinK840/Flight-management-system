import React, { useMemo } from 'react'

const TreeViewer = ({ tree, title = 'Estructura del Árbol AVL' }) => {
  const countNodes = (node) => {
    if (!node) return 0
    return 1 + countNodes(node.left) + countNodes(node.right)
  }

  const getLevels = (node, maxDepth = Infinity) => {
    if (!node) return []
    
    const levels = []
    const queue = [{ node, level: 0 }]
    
    while (queue.length > 0) {
      const { node: currentNode, level } = queue.shift()
      
      if (level > maxDepth) continue
      
      if (!levels[level]) {
        levels[level] = []
      }
      
      levels[level].push(currentNode)
      
      if (currentNode.left) {
        queue.push({ node: currentNode.left, level: level + 1 })
      }
      if (currentNode.right) {
        queue.push({ node: currentNode.right, level: level + 1 })
      }
    }
    
    return levels
  }

  const treeData = useMemo(() => {
    if (!tree) return null
    const totalNodes = countNodes(tree)
    const maxDepth = totalNodes > 15 ? 4 : Infinity
    const levels = getLevels(tree, maxDepth)
    return { totalNodes, levels, maxDepth }
  }, [tree])

  if (!tree || !treeData) {
    const isBst = title.includes('BST')
    return (
      <div style={styles.container}>
        <h3 style={styles.title}>{title}</h3>
        {isBst && <div style={styles.bstBadge}>Sin balanceo</div>}
        <div style={styles.emptyPanel}>
          <div style={styles.emptyTitle}>Árbol vacío</div>
          <div style={styles.emptyText}>
            Para comenzar, carga uno de los archivos JSON del profesor usando el panel superior, o inserta vuelos manualmente con el formulario de inserción.
          </div>
          <div style={styles.emptyActions}>
            <button type="button" style={{ ...styles.emptyButton, ...styles.emptyButtonTopology }}>
              📂 Modo Topología
            </button>
            <button type="button" style={{ ...styles.emptyButton, ...styles.emptyButtonInsertion }}>
              📋 Modo Inserción
            </button>
          </div>
        </div>
      </div>
    )
  }

  const { totalNodes, levels, maxDepth } = treeData
  const isTruncated = totalNodes > 15
  const isWideTree = totalNodes > 10

  const renderNode = (node) => {
    if (!node) return null

    const isNodoCritico = node.nodoCritico === true
    const isRoot = node.value === tree?.value
    const backgroundColor = isNodoCritico
      ? '#FF6B35'
      : isRoot
        ? '#0B3D91'
        : '#4A90E2'
    const borderStyle = isNodoCritico
      ? '2px dashed #C62828'
      : isRoot
        ? '2px solid #062A6B'
        : '2px solid #1E5AA8'
    const origen = node.origen || node.datos?.origen || ''
    const destino = node.destino || node.datos?.destino || ''
    const balance = node.balance_factor ?? node.balance
    const displayValue = node.codigo || node.value || '?'
    const routeLabel = origen && destino ? `${origen} → ${destino}` : ''
    const precioFinal = typeof node.precioFinal === 'number' ? node.precioFinal : null
    const alertaValue = node.alerta ?? node.datos?.alerta
    const alertaActiva = Boolean(alertaValue)
    const tooltip = [
      `Codigo: ${displayValue}`,
      `Origen: ${origen || '-'}`,
      `Destino: ${destino || '-'}`,
      `Hora: ${node.horaSalida || '-'}`,
      `Precio Base: ${node.precioBase ?? 0}`,
      `Precio Final: ${precioFinal ?? 0}`,
      `Pasajeros: ${node.pasajeros ?? 0}`,
      `Prioridad: ${node.prioridad ?? 0}`,
      `Promocion: ${node.promocion ? 'si' : 'no'}`,
      `Alerta: ${alertaActiva ? 'si' : 'no'}`,
      `Profundidad: ${node.profundidad ?? 0}`,
      `Factor Balance: ${balance ?? 0}`
    ].join('\n')

    return (
      <div key={`${displayValue}-${JSON.stringify(node)}`} style={styles.nodeWrapper}>
        <div
          title={tooltip}
          style={{
            ...styles.node,
            backgroundColor: backgroundColor,
            border: borderStyle,
            boxShadow: isNodoCritico
              ? '0 4px 8px rgba(255, 107, 53, 0.4)'
              : isRoot
                ? '0 4px 8px rgba(11, 61, 145, 0.4)'
                : '0 4px 8px rgba(74, 144, 226, 0.4)'
          }}
        >
          <div style={styles.nodeValue}>
            <span style={styles.flightCode}>{displayValue}</span>
          </div>
          {routeLabel && (
            <div style={styles.route}>{routeLabel}</div>
          )}
          {isNodoCritico && precioFinal !== null && (
            <div style={styles.criticalPrice}>⚠ ${precioFinal}</div>
          )}
          {balance !== undefined && balance !== null && (
            <div style={styles.balance}>bal: {balance}</div>
          )}
        </div>
      </div>
    )
  }

  const isBst = title.includes('BST')

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>{title}</h3>
      {isBst && <div style={styles.bstBadge}>Sin balanceo</div>}
      {isTruncated && (
        <div style={styles.truncatedWarning}>
          📊 Árbol con {totalNodes} nodos (mostrando hasta {maxDepth} niveles)
        </div>
      )}
      <div style={{ ...styles.treeScroll, ...(isWideTree ? styles.treeScrollWide : {}) }}>
        <div style={{ ...styles.treeContainer, ...(isWideTree ? styles.treeContainerWide : {}) }}>
          {levels.map((levelNodes, levelIndex) => (
            <div key={`level-${levelIndex}`} style={styles.level}>
              <div style={styles.levelLabel}>Nivel {levelIndex}</div>
              <div style={styles.levelNodes}>
                {levelNodes.map((node, idx) => (
                  <div key={`${node.value}-${idx}`}>{renderNode(node)}</div>
                ))}
              </div>
              {levelIndex < levels.length - 1 && (
                <div style={styles.connector}>↓</div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    padding: '24px',
    backgroundColor: '#fafafa',
    borderRadius: '12px',
    marginTop: '20px',
    border: '1px solid #e0e0e0',
    maxHeight: '700px',
    overflowY: 'auto'
  },
  title: {
    margin: '0 0 16px 0',
    fontSize: '18px',
    fontWeight: '600',
    color: '#212121'
  },
  bstBadge: {
    display: 'inline-block',
    padding: '4px 10px',
    backgroundColor: '#f59e0b',
    color: '#fff7ed',
    borderRadius: '999px',
    fontSize: '11px',
    fontWeight: '700',
    marginBottom: '12px'
  },
  empty: {
    color: '#999',
    textAlign: 'center',
    padding: '40px'
  },
  emptyPanel: {
    padding: '20px',
    backgroundColor: '#fff',
    borderRadius: '12px',
    border: '1px dashed #cbd5f5',
    textAlign: 'center'
  },
  emptyTitle: {
    fontSize: '18px',
    fontWeight: '700',
    color: '#1f2937',
    marginBottom: '8px'
  },
  emptyText: {
    fontSize: '13px',
    color: '#4b5563',
    marginBottom: '16px'
  },
  emptyActions: {
    display: 'flex',
    justifyContent: 'center',
    gap: '12px',
    flexWrap: 'wrap'
  },
  emptyButton: {
    border: 'none',
    padding: '8px 14px',
    borderRadius: '999px',
    fontWeight: '700',
    cursor: 'default'
  },
  emptyButtonTopology: {
    backgroundColor: '#1d4ed8',
    color: '#eff6ff'
  },
  emptyButtonInsertion: {
    backgroundColor: '#10b981',
    color: '#ecfdf5'
  },
  truncatedWarning: {
    padding: '12px',
    marginBottom: '16px',
    backgroundColor: '#fff3cd',
    borderLeft: '4px solid #ffc107',
    borderRadius: '4px',
    color: '#856404',
    fontSize: '13px'
  },
  treeContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '24px'
  },
  treeContainerWide: {
    minWidth: '1100px'
  },
  treeScroll: {
    width: '100%'
  },
  treeScrollWide: {
    overflowX: 'auto',
    paddingBottom: '8px'
  },
  level: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '100%'
  },
  levelLabel: {
    fontSize: '12px',
    color: '#999',
    marginBottom: '8px',
    fontWeight: '500'
  },
  levelNodes: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: '16px',
    width: '100%'
  },
  nodeWrapper: {
    display: 'flex',
    justifyContent: 'center'
  },
  node: {
    padding: '12px 16px',
    borderRadius: '8px',
    minWidth: '120px',
    textAlign: 'center',
    border: '2px solid',
    color: 'white',
    position: 'relative',
    transition: 'all 0.2s ease'
  },
  nodeValue: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '6px',
    fontSize: '14px',
    fontWeight: '700'
  },
  warningIcon: {
    fontSize: '16px'
  },
  flightCode: {
    letterSpacing: '0.5px'
  },
  route: {
    fontSize: '11px',
    marginTop: '4px',
    opacity: '0.9',
    fontStyle: 'italic'
  },
  criticalPrice: {
    fontSize: '11px',
    marginTop: '4px',
    fontWeight: '700'
  },
  balance: {
    fontSize: '10px',
    marginTop: '4px',
    opacity: '0.85',
    fontFamily: 'monospace'
  },
  connector: {
    fontSize: '20px',
    color: '#bdbdbd',
    marginTop: '8px'
  }
}

export default TreeViewer
