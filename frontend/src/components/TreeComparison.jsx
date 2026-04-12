const TreeComparison = ({ data, onClose }) => {
  return (
    <div style={{
      position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      backgroundColor: 'white',
      padding: '30px',
      borderRadius: '12px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      zIndex: 1000,
      maxWidth: '500px',
      width: '90%',
      maxHeight: '80vh',
      overflowY: 'auto'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2 style={{ margin: 0 }}>📊 Comparación AVL vs BST</h2>
        <button
          onClick={onClose}
          style={{
            backgroundColor: '#f44336',
            color: 'white',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '4px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          ✕ Cerrar
        </button>
      </div>

      {data && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div>
            <h3 style={{ textAlign: 'center', color: '#4CAF50' }}>Árbol AVL</h3>
            <div style={{ padding: '15px', backgroundColor: '#F1F8E9', borderRadius: '8px' }}>
              <p><strong>Altura:</strong> {data.avl?.height || 'N/A'}</p>
              <p><strong>Nodos:</strong> {data.avl?.nodes || 'N/A'}</p>
              <p><strong>Rotaciones:</strong> {data.avl?.rotations || 0}</p>
            </div>
          </div>
          <div>
            <h3 style={{ textAlign: 'center', color: '#2196F3' }}>Árbol BST</h3>
            <div style={{ padding: '15px', backgroundColor: '#E3F2FD', borderRadius: '8px' }}>
              <p><strong>Altura:</strong> {data.bst?.height || 'N/A'}</p>
              <p><strong>Nodos:</strong> {data.bst?.nodes || 'N/A'}</p>
              <p><strong>Balance:</strong> {data.bst?.balanced ? 'Sí' : 'No'}</p>
            </div>
          </div>
        </div>
      )}

      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#FFF3E0', borderRadius: '8px' }}>
        <p><strong>✓ El Árbol AVL es más eficiente para búsquedas debido a su balanceo automático.</strong></p>
      </div>
    </div>
  )
}

export default TreeComparison
