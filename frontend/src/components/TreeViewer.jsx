import React from 'react'

const TreeViewer = ({ tree }) => {
  const formatValue = (value) => {
    if (value && typeof value === 'object') {
      if ('codigo' in value) return value.codigo
      return JSON.stringify(value)
    }
    return value
  }

  const renderNode = (node) => {
    if (!node) return null

    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <div
          style={{
            padding: '8px 12px',
            backgroundColor: '#4CAF50',
            color: 'white',
            borderRadius: '4px',
            display: 'inline-block',
            fontWeight: 'bold',
            minWidth: '32px',
            textAlign: 'center'
          }}
        >
          {formatValue(node.value)}
        </div>
        {(node.left || node.right) && (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '16px' }}>
            <div style={{ width: '2px', height: '16px', backgroundColor: '#999' }} />
            <div style={{ width: '100%', borderTop: '2px solid #999', margin: '6px 0 10px' }} />
            <div style={{ display: 'flex', gap: '40px' }}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <div style={{ width: '2px', height: '16px', backgroundColor: '#999' }} />
                {node.left ? renderNode(node.left) : <div style={{ width: '32px', height: '32px' }} />}
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <div style={{ width: '2px', height: '16px', backgroundColor: '#999' }} />
                {node.right ? renderNode(node.right) : <div style={{ width: '32px', height: '32px' }} />}
              </div>
            </div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div style={{ padding: '20px', backgroundColor: '#f5f5f5', borderRadius: '8px', marginTop: '20px' }}>
      <h2>Estructura del Árbol AVL</h2>
      {tree ? (
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          {renderNode(tree)}
        </div>
      ) : (
        <p style={{ color: '#666' }}>Árbol vacío - Inserta valores para comenzar</p>
      )}
    </div>
  )
}

export default TreeViewer
