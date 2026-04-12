import { useEffect, useRef, useState } from 'react'
import { LOAD_MODE_INSERTION, LOAD_MODE_TOPOLOGY } from '../../models/treeModes'

const UploadControls = ({ onFileLoad, onExport, onDepthLimitChange, depthLimit: depthLimitProp }) => {
  const topologyInputRef = useRef(null)
  const insertionInputRef = useRef(null)
  const [depthLimit, setDepthLimit] = useState(3)
  const [isApplying, setIsApplying] = useState(false)

  useEffect(() => {
    if (typeof depthLimitProp === 'number') {
      setDepthLimit(depthLimitProp)
    }
  }, [depthLimitProp])

  const handleFileChange = async (event, loadType) => {
    const file = event.target.files?.[0]
    if (file) {
      await onFileLoad(file, loadType)
    }
    event.target.value = ''
  }

  const handleApplyDepthLimit = async () => {
    if (!Number.isFinite(depthLimit)) {
      alert('⚠️ Ingresa un valor de profundidad válido')
      return
    }
    setIsApplying(true)
    try {
      await onDepthLimitChange(depthLimit)
    } finally {
      setIsApplying(false)
    }
  }

  return (
    <section style={{ marginBottom: '24px', padding: '20px', backgroundColor: '#e8f5e9', borderRadius: '16px', boxShadow: '0 10px 22px rgba(44, 160, 50, 0.12)' }}>
      <h2 style={{ marginTop: 0 }}>📁 Cargar desde JSON</h2>
      <p style={{ marginBottom: '16px', color: '#435158' }}>
        Archivos disponibles: <code>ModoTopología.json</code> y <code>ModoInserción.json</code> en la carpeta data/
      </p>

      {/* PROMPT 2: Profundidad Límite Crítica */}
      <div style={{
        marginBottom: '20px',
        padding: '16px',
        backgroundColor: '#fff9c4',
        borderRadius: '8px',
        border: '2px solid #FDD835'
      }}>
        <label style={{ display: 'block', fontWeight: '700', marginBottom: '8px', color: '#f57f17' }}>
          ⚠️ Profundidad límite crítica
        </label>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <input
            type="number"
            min="0"
            max="20"
            value={Number.isFinite(depthLimit) ? depthLimit : ''}
            onChange={(e) => {
              const raw = e.target.value
              if (raw === '') {
                setDepthLimit(NaN)
                return
              }
              const parsed = parseInt(raw, 10)
              setDepthLimit(Number.isNaN(parsed) ? NaN : parsed)
            }}
            style={{
              padding: '10px 12px',
              borderRadius: '6px',
              border: '2px solid #FDD835',
              fontSize: '16px',
              width: '80px',
              fontWeight: '600'
            }}
          />
          <button
            type="button"
            onClick={handleApplyDepthLimit}
            disabled={isApplying}
            style={{
              ...buttonStyle('#FDD835'),
              color: '#333',
              cursor: isApplying ? 'not-allowed' : 'pointer',
              opacity: isApplying ? 0.6 : 1
            }}
          >
            {isApplying ? '⏳ Aplicando...' : '✓ Aplicar'}
          </button>
          <span style={{ fontSize: '12px', color: '#666' }}>
            (Los nodos más profundos de este límite tendrán penalización de precio)
          </span>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
        <input
          ref={topologyInputRef}
          type="file"
          accept=".json"
          style={{ display: 'none' }}
          onChange={(event) => handleFileChange(event, LOAD_MODE_TOPOLOGY)}
        />
        <button
          type="button"
          onClick={() => topologyInputRef.current?.click()}
          style={buttonStyle('#4CAF50')}
        >
          Cargar Topología
        </button>

        <input
          ref={insertionInputRef}
          type="file"
          accept=".json"
          style={{ display: 'none' }}
          onChange={(event) => handleFileChange(event, LOAD_MODE_INSERTION)}
        />
        <button
          type="button"
          onClick={() => insertionInputRef.current?.click()}
          style={buttonStyle('#2196F3')}
        >
          Cargar por Inserción
        </button>

        <button
          type="button"
          onClick={onExport}
          style={buttonStyle('#FF9800')}
        >
          Exportar JSON
        </button>
      </div>

      <p style={{ marginTop: '16px', fontSize: '14px', color: '#5f6a72' }}>
        <strong>Modo Topología:</strong> carga la estructura completa del árbol desde <code>ModoTopología.json</code>.<br />
        <strong>Modo Inserción:</strong> extrae códigos que comienzan con <code>SB</code>, convierte los números y los inserta uno por uno.
      </p>
    </section>
  )
}

const buttonStyle = (backgroundColor) => ({
  padding: '12px 20px',
  backgroundColor,
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  cursor: 'pointer',
  fontWeight: '700'
})

export default UploadControls
