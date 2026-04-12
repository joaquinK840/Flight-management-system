const TreeOperations = ({
  value,
  onValueChange,
  onInsert,
  onDelete,
  onCancelFlight,
  onSearch,
  onShowComparison,
  onUndo,
  onRedo,
  onReset,
  onEliminateLeastProfitable,
  onExport
}) => {
  return (
    <div style={{
      marginBottom: '24px',
      padding: '20px',
      backgroundColor: '#f9f9f9',
      borderRadius: '16px',
      boxShadow: '0 10px 22px rgba(24, 110, 255, 0.08)'
    }}>
      <h3>Operaciones del Árbol</h3>
      <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
        <input
          type="number"
          value={value}
          onChange={(e) => onValueChange(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && onInsert()}
          placeholder="Ingresa un valor"
          style={{
            flex: 1,
            padding: '10px',
            border: '1px solid #ccc',
            borderRadius: '8px',
            fontSize: '14px'
          }}
        />
      </div>
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <button onClick={onInsert} style={{ padding: '10px 20px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          ➕ Insertar
        </button>
        <button onClick={onSearch} style={{ padding: '10px 20px', backgroundColor: '#2196F3', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          🔍 Buscar
        </button>
        <button onClick={onDelete} style={{ padding: '10px 20px', backgroundColor: '#FF9800', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          🗑️ Eliminar
        </button>
        <button onClick={onCancelFlight} style={{ padding: '10px 20px', backgroundColor: '#9C27B0', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          ✈️ Cancelar Vuelo
        </button>
        <button onClick={onEliminateLeastProfitable} style={{ padding: '10px 20px', backgroundColor: '#E91E63', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          💰 Eliminar Menor Rentabilidad
        </button>
        <button onClick={onShowComparison} style={{ padding: '10px 20px', backgroundColor: '#00BCD4', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          📊 Comparar
        </button>
        <button onClick={onReset} style={{ padding: '10px 20px', backgroundColor: '#f44336', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          🔄 Reiniciar
        </button>
        <button onClick={onExport} style={{ padding: '10px 20px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>
          💾 Exportar
        </button>
      </div>
    </div>
  )
}

export default TreeOperations
