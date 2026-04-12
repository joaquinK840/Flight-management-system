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
    return (
      <div style={styles.container}>
        <h3 style={styles.title}>{title}</h3>
        <p style={styles.empty}>Árbol vacío - Inserta valores para comenzar</p>
      </div>
    )
  }

  const { totalNodes, levels, maxDepth } = treeData
  const isTruncated = totalNodes > 15

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

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>{title}</h3>
      {isTruncated && (
        <div style={styles.truncatedWarning}>
          📊 Árbol con {totalNodes} nodos (mostrando hasta {maxDepth} niveles)
        </div>
      )}
      <div style={styles.treeContainer}>
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
  empty: {
    color: '#999',
    textAlign: 'center',
    padding: '40px'
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
