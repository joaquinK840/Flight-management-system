const TraversalControls = ({ onTraversal }) => {
  return (
    <div>
      <h3 style={{ marginTop: 0 }}>Recorridos del Árbol</h3>
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <button type="button" onClick={() => onTraversal('pre')} style={buttonStyle('#FF9800')}>
          Preorden
        </button>
        <button type="button" onClick={() => onTraversal('in')} style={buttonStyle('#9C27B0')}>
          Inorden
        </button>
        <button type="button" onClick={() => onTraversal('post')} style={buttonStyle('#E91E63')}>
          Postorden
        </button>
        <button type="button" onClick={() => onTraversal('bfs')} style={buttonStyle('#673AB7')}>
          Por Niveles
        </button>
      </div>
    </div>
  )
}

const buttonStyle = (backgroundColor) => ({
  padding: '10px 16px',
  backgroundColor,
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  cursor: 'pointer',
  fontSize: '14px',
  fontWeight: '700'
})

export default TraversalControls
