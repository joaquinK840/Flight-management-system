const TreeOperations = ({ value, onValueChange, onInsert, onDelete, onCancelFlight, onSearch, onUndo, onRedo, onReset, onShowComparison }) => {
  return (
    <section style={{ marginBottom: '24px', padding: '20px', backgroundColor: '#ffffff', borderRadius: '16px', boxShadow: '0 10px 22px rgba(60, 72, 88, 0.08)' }}>
      <h2 style={{ marginTop: 0 }}>Operaciones del Árbol</h2>

      <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', marginBottom: '18px' }}>
        <input
          type="number"
          value={value}
          onChange={(event) => onValueChange(event.target.value)}
          placeholder="Ingresa un valor"
          style={{ flex: 1, minWidth: '220px', padding: '12px 14px', border: '1px solid #d1d9e6', borderRadius: '10px', fontSize: '15px' }}
        />

        <button type="button" onClick={onInsert} style={buttonStyle('#4CAF50')}>
          Insertar
        </button>
        <button type="button" onClick={onDelete} style={buttonStyle('#FF5722')}>
          Eliminar
        </button>
        <button type="button" onClick={onCancelFlight} style={buttonStyle('#9C27B0')}>
          Cancelar Vuelo
        </button>
      </div>

      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
        <button type="button" onClick={onSearch} style={buttonStyle('#2196F3')}>
          Buscar
        </button>
        <button type="button" onClick={onShowComparison} style={buttonStyle('#009688')}>
          Mostrar Comparación
        </button>
        <button type="button" onClick={onUndo} style={buttonStyle('#607D8B')}>
          ↶ Undo
        </button>
        <button type="button" onClick={onRedo} style={buttonStyle('#607D8B')}>
          ↷ Redo
        </button>
        <button type="button" onClick={onReset} style={buttonStyle('#f44336')}>
          Reiniciar
        </button>
      </div>
    </section>
  )
}

const buttonStyle = (backgroundColor) => ({
  padding: '12px 18px',
  backgroundColor,
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  cursor: 'pointer',
  fontWeight: '700'
})

export default TreeOperations
