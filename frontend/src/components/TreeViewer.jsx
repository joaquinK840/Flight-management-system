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
    const backgroundColor = isNodoCritico ? '#ef5350' : '#66bb6a'
    const origen = node.datos?.origen ? node.datos.origen.substring(0, 3) : ''
    const destino = node.datos?.destino ? node.datos.destino.substring(0, 3) : ''
    const balance = node.datos?.balance ?? node.balance
    const displayValue = node.value || node.codigo || '?'

    return (
      <div key={`${displayValue}-${JSON.stringify(node)}`} style={styles.nodeWrapper}>
        <div
          style={{
            ...styles.node,
            backgroundColor: backgroundColor,
            borderColor: isNodoCritico ? '#c62828' : '#2e7d32',
            boxShadow: isNodoCritico
              ? '0 4px 8px rgba(239, 83, 80, 0.4)'
              : '0 4px 8px rgba(102, 187, 106, 0.4)'
          }}
        >
          <div style={styles.nodeValue}>
            {isNodoCritico && <span style={styles.warningIcon}>⚠️</span>}
            <span style={styles.flightCode}>{displayValue}</span>
          </div>
          {origen && destino && (
            <div style={styles.route}>{origen} → {destino}</div>
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
