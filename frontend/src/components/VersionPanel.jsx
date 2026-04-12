import React, { useState, useEffect } from 'react'
import { listVersions, saveVersion, restoreVersion, deleteVersion } from '../services/avlService'

const VersionPanel = ({ onVersionRestored }) => {
  const [versions, setVersions] = useState([])
  const [versionName, setVersionName] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadVersions()
  }, [])

  const loadVersions = async () => {
    try {
      const data = await listVersions()
      setVersions(data.versions || [])
    } catch (err) {
      console.error('Error cargando versiones:', err)
    }
  }

  const handleSaveVersion = async () => {
    if (!versionName.trim()) {
      alert('Por favor ingresa un nombre para la versión')
      return
    }

    setLoading(true)
    try {
      const response = await saveVersion(versionName)
      
      // Mostrar estadísticas del árbol y cola guardados
      const stats = response.tree_stats
      const queueInfo = stats && stats.queue_size > 0 
        ? ` + Cola: ${stats.queue_size} vuelos`
        : ''
      
      const message = stats
        ? `✅ Versión "${versionName}" guardada\n📊 Árbol: ${stats.total_nodes} nodos, altura ${stats.height}${queueInfo}`
        : `✅ Versión "${versionName}" guardada exitosamente`
      
      alert(message)
      setVersionName('')
      await loadVersions()
    } catch (err) {
      console.error('Error guardando versión:', err)
      alert(`❌ Error guardando versión: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleRestoreVersion = async (name) => {
    if (!window.confirm(`¿Deseas restaurar la versión "${name}"?`)) {
      return
    }

    setLoading(true)
    try {
      const response = await restoreVersion(name)
      
      // Esperar un poco para asegurar que el backend esté listo
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // Mostrar información detallada
      const metrics = response.metrics || {}
      const queueInfo = response.queue_restored 
        ? ` + Cola FIFO (${response.queue_size} vuelos)`
        : ''
      
      const message = `✅ Versión "${name}" restaurada\n📊 Árbol: ${metrics.total_nodes} nodos, altura ${metrics.height}${queueInfo}`
      
      // Luego cargar el árbol actualizado desde el servidor
      if (onVersionRestored) {
        await onVersionRestored()
      }
      
      alert(message)
    } catch (err) {
      console.error('Error restaurando versión:', err)
      alert(`❌ Error restaurando versión: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteVersion = async (name) => {
    if (!window.confirm(`¿Deseas eliminar la versión "${name}"? Esta acción no se puede deshacer.`)) {
      return
    }

    setLoading(true)
    try {
      await deleteVersion(name)
      alert(`✅ Versión "${name}" eliminada`)
      await loadVersions()
    } catch (err) {
      console.error('Error eliminando versión:', err)
      alert(`❌ Error eliminando versión: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ marginBottom: '24px', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '16px', boxShadow: '0 10px 22px rgba(24, 110, 255, 0.08)' }}>
      <h3 style={{ marginTop: 0, marginBottom: '16px' }}>💾 Gestor de Versiones</h3>

      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <input
          type="text"
          value={versionName}
          onChange={(e) => setVersionName(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSaveVersion()}
          placeholder="Nombre de la versión (ej: v1.0)"
          disabled={loading}
          style={{
            padding: '10px 12px',
            borderRadius: '8px',
            border: '2px solid #2196f3',
            fontSize: '14px',
            flex: 1,
            minWidth: '200px',
            fontFamily: 'inherit'
          }}
        />
        <button
          onClick={handleSaveVersion}
          disabled={loading || !versionName.trim()}
          style={{
            padding: '10px 16px',
            backgroundColor: loading || !versionName.trim() ? '#ccc' : '#4caf50',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: loading || !versionName.trim() ? 'not-allowed' : 'pointer',
            fontWeight: 'bold',
            fontSize: '14px',
            opacity: loading || !versionName.trim() ? 0.6 : 1
          }}
        >
          💾 Guardar versión actual
        </button>
      </div>

      <div style={{ borderTop: '2px solid #e0e0e0', paddingTop: '16px' }}>
        <h4 style={{ marginTop: 0, marginBottom: '12px' }}>Versiones disponibles ({versions.length})</h4>
        {versions.length === 0 ? (
          <p style={{ color: '#666', fontStyle: 'italic' }}>No hay versiones guardadas</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {versions.map((version) => (
              <div
                key={version.name}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '12px',
                  backgroundColor: '#fff',
                  borderRadius: '8px',
                  border: '1px solid #e0e0e0',
                  gap: '10px'
                }}
              >
                <div style={{ flex: 1, minWidth: 0 }}>
                  <strong style={{ fontSize: '14px', display: 'block', marginBottom: '4px' }}>
                    {version.name}
                  </strong>
                  <span style={{ fontSize: '12px', color: '#666' }}>
                    {version.created_at
                      ? new Date(version.created_at).toLocaleString('es-ES')
                      : 'Fecha desconocida'}
                  </span>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    onClick={() => handleRestoreVersion(version.name)}
                    disabled={loading}
                    style={{
                      padding: '8px 12px',
                      backgroundColor: loading ? '#ccc' : '#2196f3',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: loading ? 'not-allowed' : 'pointer',
                      fontSize: '12px',
                      fontWeight: 'bold',
                      whiteSpace: 'nowrap',
                      opacity: loading ? 0.6 : 1
                    }}
                  >
                    ↩️ Restaurar
                  </button>
                  <button
                    onClick={() => handleDeleteVersion(version.name)}
                    disabled={loading}
                    style={{
                      padding: '8px 12px',
                      backgroundColor: loading ? '#ccc' : '#f44336',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: loading ? 'not-allowed' : 'pointer',
                      fontSize: '12px',
                      fontWeight: 'bold',
                      whiteSpace: 'nowrap',
                      opacity: loading ? 0.6 : 1
                    }}
                  >
                    🗑️ Eliminar
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default VersionPanel
