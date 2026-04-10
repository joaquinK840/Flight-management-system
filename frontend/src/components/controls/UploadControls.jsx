import { useRef } from 'react'
import { LOAD_MODE_INSERTION, LOAD_MODE_TOPOLOGY } from '../../models/treeModes'

const UploadControls = ({ onFileLoad, onExport }) => {
  const topologyInputRef = useRef(null)
  const insertionInputRef = useRef(null)

  const handleFileChange = async (event, loadType) => {
    const file = event.target.files?.[0]
    if (file) {
      await onFileLoad(file, loadType)
    }
    event.target.value = ''
  }

  return (
    <section style={{ marginBottom: '24px', padding: '20px', backgroundColor: '#e8f5e9', borderRadius: '16px', boxShadow: '0 10px 22px rgba(44, 160, 50, 0.12)' }}>
      <h2 style={{ marginTop: 0 }}>📁 Cargar desde JSON</h2>
      <p style={{ marginBottom: '16px', color: '#435158' }}>
        Archivos disponibles: <code>ModoTopología.json</code> y <code>ModoInserción.json</code> en la carpeta data/
      </p>

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
