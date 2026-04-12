const TraversalControls = ({ onTraversal }) => {
  return (
    <div style={{ marginBottom: '24px', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '16px' }}>
      <h3>Recorridos del Árbol</h3>
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <button
          onClick={() => onTraversal('pre')}
          style={{ padding: '10px 20px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}
        >
          ⬇️ Preorden
        </button>
        <button
          onClick={() => onTraversal('in')}
          style={{ padding: '10px 20px', backgroundColor: '#2196F3', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}
        >
          ➡️ Inorden
        </button>
        <button
          onClick={() => onTraversal('post')}
          style={{ padding: '10px 20px', backgroundColor: '#FF9800', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}
        >
          ⬆️ Postorden
        </button>
        <button
          onClick={() => onTraversal('level')}
          style={{ padding: '10px 20px', backgroundColor: '#9C27B0', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}
        >
          📊 Por Niveles
        </button>
      </div>
    </div>
  )
}

export default TraversalControls
