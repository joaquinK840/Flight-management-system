const TreeInfo = ({ tree, treeHeight, balanceFactor }) => {
  return (
    <section style={{ marginBottom: '24px', padding: '20px', backgroundColor: '#E8F5E9', borderLeft: '4px solid #4CAF50', borderRadius: '12px' }}>
      <h2 style={{ marginTop: 0 }}>Información del Árbol AVL</h2>
      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
        <div>
          <strong>Raíz:</strong> {tree?.value ?? 'N/A'}
        </div>
        <div>
          <strong>Profundidad:</strong> {treeHeight ?? 'N/A'}
        </div>
        <div>
          <strong>Factor de Balance (Raíz):</strong> {balanceFactor ?? 'N/A'}
        </div>
      </div>
    </section>
  )
}

export default TreeInfo
