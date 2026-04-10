const TreeComparison = ({ data, onClose }) => {
  return (
    <section style={{ marginBottom: '24px', padding: '20px', backgroundColor: '#FCE4EC', borderRadius: '16px', boxShadow: '0 10px 22px rgba(209, 126, 172, 0.16)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '16px', flexWrap: 'wrap' }}>
        <h2 style={{ marginTop: 0 }}>📊 Comparación AVL vs BST</h2>
        <button type="button" onClick={onClose} style={{ ...buttonStyle('#f44336'), padding: '10px 16px' }}>
          Cerrar Comparación
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '18px', marginTop: '18px' }}>
        <div style={{ padding: '18px', backgroundColor: '#FFFFFF', borderRadius: '14px' }}>
          <h3 style={{ marginTop: 0 }}>🌲 Árbol AVL</h3>
          <p><strong>Raíz:</strong> {data.avl.root}</p>
          <p><strong>Altura:</strong> {data.avl.height}</p>
          <p><strong>Hojas:</strong> {data.avl.leaves}</p>
          <p><strong>Balanceado:</strong> ✓ Sí</p>
        </div>
        <div style={{ padding: '18px', backgroundColor: '#FFFFFF', borderRadius: '14px' }}>
          <h3 style={{ marginTop: 0 }}>🌳 Árbol BST</h3>
          <p><strong>Raíz:</strong> {data.bst.root}</p>
          <p><strong>Altura:</strong> {data.bst.height}</p>
          <p><strong>Hojas:</strong> {data.bst.leaves}</p>
          <p><strong>Balanceado:</strong> ✗ No</p>
        </div>
      </div>
    </section>
  )
}

const buttonStyle = (backgroundColor) => ({
  backgroundColor,
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  cursor: 'pointer',
  fontWeight: '700'
})

export default TreeComparison
