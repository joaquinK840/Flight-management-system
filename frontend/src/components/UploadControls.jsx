import { useState } from 'react'
import { loadJson, setDepthLimit } from '../services/avlService'

const UploadControls = ({ onTreeUpdate }) => {
    const [depthLimit, setDepthLimitValue] = useState(3)
    const [fileError, setFileError] = useState('')
    const [statusMessage, setStatusMessage] = useState('')

    const handleApplyDepth = async () => {
        try {
            const result = await setDepthLimit(depthLimit)
            const treeRoot = result?.tree?.root ?? null
            const rotations = result?.tree?.rotations ?? null
            onTreeUpdate(treeRoot, rotations)
            setStatusMessage('Profundidad aplicada.')
        } catch (error) {
            console.error('Error aplicando profundidad límite:', error)
            setStatusMessage('No se pudo aplicar la profundidad.')
        }
    }

    const handleFileChange = async (event) => {
        const file = event.target.files?.[0]
        if (!file) return

        try {
            await setDepthLimit(depthLimit)
            const text = await file.text()
            const payload = JSON.parse(text)
            const result = await loadJson(payload)
            const treeRoot = result?.trees?.avl?.root ?? null
            const rotations = result?.trees?.avl?.rotations ?? null
            onTreeUpdate(treeRoot, rotations)
            setFileError('')
            setStatusMessage('JSON cargado correctamente.')
        } catch (error) {
            console.error('Error cargando archivo JSON:', error)
            setFileError('No se pudo leer el JSON. Verifica el archivo.')
            setStatusMessage('')
        }
    }

    return (
        <div style={{
            padding: '16px',
            backgroundColor: '#f0f4ff',
            borderRadius: '8px',
            marginBottom: '20px',
            maxWidth: '500px',
            margin: '0 auto 20px'
        }}>
            <h3>Configuración y carga</h3>
            <div style={{ display: 'flex', gap: '10px', alignItems: 'center', marginBottom: '12px' }}>
                <label htmlFor="depthLimit" style={{ fontWeight: 'bold' }}>Profundidad límite crítica</label>
                <input
                    id="depthLimit"
                    type="number"
                    min="1"
                    value={depthLimit}
                    onChange={(e) => setDepthLimitValue(parseInt(e.target.value || '0', 10))}
                    style={{ width: '80px', padding: '6px' }}
                />
                <button
                    onClick={handleApplyDepth}
                    style={{
                        padding: '6px 12px',
                        backgroundColor: '#4c6ef5',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontWeight: 'bold'
                    }}
                >
                    Aplicar
                </button>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                <label htmlFor="jsonFile" style={{ fontWeight: 'bold' }}>Cargar JSON</label>
                <input
                    id="jsonFile"
                    type="file"
                    accept="application/json"
                    onChange={handleFileChange}
                />
                {fileError && <span style={{ color: '#d32f2f' }}>{fileError}</span>}
                {statusMessage && <span style={{ color: '#2e7d32' }}>{statusMessage}</span>}
            </div>
        </div>
    )
}

export default UploadControls
