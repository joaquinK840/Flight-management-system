const TreeInfo = ({ tree, treeHeight, balanceFactor }) => {
  const calculateHeight = (node) => {
    if (!node) return 0
    return 1 + Math.max(calculateHeight(node.left), calculateHeight(node.right))
  }

  const calculateLeaves = (node) => {
    if (!node) return 0
    if (!node.left && !node.right) return 1
    return calculateLeaves(node.left) + calculateLeaves(node.right)
  }

  const height = calculateHeight(tree)
  const leaves = calculateLeaves(tree)

  return (
    <div style={{
      marginBottom: '24px',
      padding: '18px',
      backgroundColor: '#E8F5E9',
      borderLeft: '4px solid #4CAF50',
      borderRadius: '8px'
    }}>
      <h3 style={{ marginTop: 0, color: '#2E7D32' }}>📊 Información del Árbol</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '15px' }}>
        <div>
          <strong>Altura:</strong>
          <p style={{ fontSize: '18px', margin: '5px 0 0 0', color: '#2E7D32' }}>{height}</p>
        </div>
        <div>
          <strong>Nodos Totales:</strong>
          <p style={{ fontSize: '18px', margin: '5px 0 0 0', color: '#2E7D32' }}>
            {tree ? countNodes(tree) : 0}
          </p>
        </div>
        <div>
          <strong>Hojas:</strong>
          <p style={{ fontSize: '18px', margin: '5px 0 0 0', color: '#2E7D32' }}>{leaves}</p>
        </div>
      </div>
    </div>
  )
}

const countNodes = (node) => {
  if (!node) return 0
  return 1 + countNodes(node.left) + countNodes(node.right)
}

export default TreeInfo
