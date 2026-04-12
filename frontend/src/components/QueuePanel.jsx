import React, { useEffect, useMemo, useState } from 'react'
import { enqueueFlight, listQueue, processNextQueue, clearQueueAvl } from '../services/avlService'

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const QueuePanel = ({ onTreeUpdate }) => {
  const [queueItems, setQueueItems] = useState([])
  const [processing, setProcessing] = useState(false)
  const [formData, setFormData] = useState({
    codigo: '',
    origen: '',
    destino: '',
    precioBase: '',
    pasajeros: '',
    prioridad: 1
  })

  const queueSize = useMemo(() => queueItems.length, [queueItems])

  const fetchQueue = async () => {
    const data = await listQueue()
    const items = data.queue || []
    setQueueItems(items)
    return items
  }

  useEffect(() => {
    fetchQueue().catch(() => {})
  }, [])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'pasajeros' || name === 'precioBase' || name === 'prioridad'
        ? value
        : value
    }))
  }

  const buildPayload = () => {
    const codigo = String(formData.codigo || '').trim()
    return {
      codigo: codigo,
      origen: String(formData.origen || '').trim(),
      destino: String(formData.destino || '').trim(),
      precioBase: parseFloat(formData.precioBase || 0),
      pasajeros: parseInt(formData.pasajeros || 0, 10),
      prioridad: parseInt(formData.prioridad || 1, 10)
    }
  }

  const validatePayload = (payload) => {
    if (!payload.codigo || !payload.origen || !payload.destino) {
      return 'Completa codigo, origen y destino'
    }
    if (!Number.isFinite(payload.precioBase) || payload.precioBase <= 0) {
      return 'Precio base invalido'
    }
    if (!Number.isFinite(payload.pasajeros) || payload.pasajeros <= 0) {
      return 'Pasajeros invalido'
    }
    return ''
  }

  const handleAdd = async () => {
    const payload = buildPayload()
    const error = validatePayload(payload)
    if (error) {
      alert(`❌ ${error}`)
      return
    }

    try {
      await enqueueFlight(payload)
      setFormData({
        codigo: '',
        origen: '',
        destino: '',
        precioBase: '',
        pasajeros: '',
        prioridad: 1
      })
      await fetchQueue()
    } catch (err) {
      alert(`❌ ${err.message}`)
    }
  }

  const handleProcessAll = async () => {
    if (processing) return
    setProcessing(true)
    try {
      const items = await fetchQueue()
      let next = items.length
      while (next > 0) {
        const result = await processNextQueue()
        if (result.tree && onTreeUpdate) {
          await onTreeUpdate(result.tree)
        }
        if (result.balance_conflict) {
          alert('⚠ Conflicto de balance critico detectado')
        }
        if (!result.processed) {
          break
        }
        await fetchQueue()
        next = result.remaining || 0
        if (next > 0) {
          await sleep(800)
        }
      }
    } catch (err) {
      alert(`❌ ${err.message}`)
    } finally {
      setProcessing(false)
    }
  }

  const handleClear = async () => {
    try {
      await clearQueueAvl()
      setQueueItems([])
    } catch (err) {
      alert(`❌ ${err.message}`)
    }
  }

  return (
    <div style={{ display: 'grid', gap: '16px' }}>
      <div style={{ display: 'grid', gap: '12px' }}>
        <div style={{ fontWeight: '700' }}>Cola de concurrencia</div>
        <div style={{ display: 'grid', gap: '8px', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))' }}>
          <input
            type="text"
            name="codigo"
            value={formData.codigo}
            onChange={handleInputChange}
            placeholder="Codigo (ej: SB999)"
          />
          <input
            type="text"
            name="origen"
            value={formData.origen}
            onChange={handleInputChange}
            placeholder="Origen"
          />
          <input
            type="text"
            name="destino"
            value={formData.destino}
            onChange={handleInputChange}
            placeholder="Destino"
          />
          <input
            type="number"
            name="precioBase"
            value={formData.precioBase}
            onChange={handleInputChange}
            placeholder="Precio base"
          />
          <input
            type="number"
            name="pasajeros"
            value={formData.pasajeros}
            onChange={handleInputChange}
            placeholder="Pasajeros"
          />
          <select name="prioridad" value={formData.prioridad} onChange={handleInputChange}>
            <option value={1}>Alta</option>
            <option value={2}>Media</option>
            <option value={3}>Baja</option>
          </select>
        </div>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          <button type="button" onClick={handleAdd}>➕ Agregar a cola</button>
          <button type="button" onClick={handleProcessAll} disabled={processing || queueSize === 0}>
            ▶ Procesar Cola Completa
          </button>
          <button type="button" onClick={handleClear} disabled={processing || queueSize === 0}>
            🗑 Limpiar Cola
          </button>
        </div>
      </div>

      <div>
        <div style={{ fontWeight: '700', marginBottom: '8px' }}>
          En cola ({queueSize})
        </div>
        {queueSize === 0 ? (
          <div>Cola vacia</div>
        ) : (
          <div style={{ display: 'grid', gap: '8px' }}>
            {queueItems.map((item, index) => (
              <div key={`${item.codigo}-${index}`} style={{ padding: '8px', border: '1px solid #ddd', borderRadius: '6px' }}>
                <div><strong>{item.codigo}</strong> {item.origen} → {item.destino}</div>
                <div>Precio: ${item.precioBase}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default QueuePanel
