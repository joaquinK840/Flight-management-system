import React from 'react'

const TreeViewer = ({ tree }) => {
  const renderNode = (node, depth = 0) => {
    if (!node) {
      return null
    }

    const paddingLeft = depth * 30

    return (
      <div key={`${node.value}-${depth}`} style={{ marginLeft: `${paddingLeft}px` }}>
        <div
          style={{
            padding: '8px 12px',
            margin: '5px 0',
            backgroundColor: '#4CAF50',
            color: 'white',
            borderRadius: '4px',
            display: 'inline-block',
            fontWeight: 'bold'
          }}
        >
          {node.value}
        </div>
        {(node.left || node.right) && (
          <div style={{ marginLeft: '20px', borderLeft: '2px solid #999', paddingLeft: '10px' }}>
            {node.left && (
              <div>
                <span style={{ color: '#666', fontSize: '12px' }}>L:</span>
                {renderNode(node.left, depth + 1)}
              </div>
            )}
            {node.right && (
              <div>
                <span style={{ color: '#666', fontSize: '12px' }}>R:</span>
                {renderNode(node.right, depth + 1)}
              </div>
            )}
          </div>
        )}
      </div>
    )
  }

  return (
    <div style={{ padding: '20px', backgroundColor: '#f5f5f5', borderRadius: '8px', marginTop: '20px' }}>
      <h2>Estructura del Árbol AVL</h2>
      {tree ? (
        <div style={{ fontFamily: 'monospace' }}>
          {renderNode(tree)}
        </div>
      ) : (
        <p style={{ color: '#666' }}>Árbol vacío - Inserta valores para comenzar</p>
      )}
    </div>
  )
}

export default TreeViewer
