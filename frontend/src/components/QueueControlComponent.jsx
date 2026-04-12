import React, { useState, useEffect } from 'react';
import './QueueControlComponent.css';
import { addToQueue, getPendingQueue, processOneFromQueue, processAllFromQueue, clearQueue } from '../services/avlService';

/**
 * QueueControlComponent
 * Componente para manejar la simulación de concurrencia con cola FIFO
 */
const QueueControlComponent = ({ onQueueUpdated }) => {
  const [pendingFlights, setPendingFlights] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [processResults, setProcessResults] = useState([]);
  const [conflictCount, setConflictCount] = useState(0);
  const [showForm, setShowForm] = useState(false);

  // Form state
  const [formData, setFormData] = useState({
    codigo: '',
    origen: '',
    destino: '',
    horaSalida: '',
    precioBase: '',
    pasajeros: '',
    prioridad: 1,
  });

  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success', 'error', 'info'

  // =====================================================
  // Funciones auxiliares
  // =====================================================

  const showMsg = (text, type = 'info') => {
    setMessage(text);
    setMessageType(type);
    setTimeout(() => setMessage(''), 3000);
  };

  const fetchPendingFlights = async () => {
    try {
      const data = await getPendingQueue();
      if (data.status === 'success') {
        setPendingFlights(data.flights || []);
      }
    } catch (error) {
      console.error('Error fetching pending flights:', error);
      showMsg('Error al obtener vuelos pendientes', 'error');
    }
  };

  // =====================================================
  // Cargar vuelos pendientes al montar
  // =====================================================

  useEffect(() => {
    fetchPendingFlights();
    // Recargar cada 2 segundos
    const interval = setInterval(fetchPendingFlights, 2000);
    return () => clearInterval(interval);
  }, []);

  // =====================================================
  // Manejo de formulario
  // =====================================================

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'prioridad' || name === 'pasajeros' || name === 'precioBase'
        ? parseFloat(value)
        : value,
    }));
  };

  // =====================================================
  // Agregar vuelo a la cola
  // =====================================================

  const handleAddFlight = async (e) => {
    e.preventDefault();

    // Validar
    if (
      !formData.codigo ||
      !formData.origen ||
      !formData.destino ||
      !formData.horaSalida ||
      !formData.precioBase ||
      !formData.pasajeros
    ) {
      showMsg('Por favor completa todos los campos', 'error');
      return;
    }

    try {
      await addToQueue({
        ...formData,
        precioBase: parseFloat(formData.precioBase),
        pasajeros: parseInt(formData.pasajeros, 10),
        prioridad: parseInt(formData.prioridad, 10)
      });
      showMsg(`✅ Vuelo ${formData.codigo} agregado a la cola`, 'success');
      setFormData({
        codigo: '',
        origen: '',
        destino: '',
        horaSalida: '',
        precioBase: '',
        pasajeros: '',
        prioridad: 1,
      });
      setShowForm(false);
      await fetchPendingFlights();
      if (onQueueUpdated) {
        await onQueueUpdated();
      }
    } catch (error) {
      console.error('Error adding flight:', error);
      showMsg('Error al agregar vuelo', 'error');
    }
  };

  // =====================================================
  // Procesar un vuelo
  // =====================================================

  const handleProcessOne = async () => {
    if (pendingFlights.length === 0) {
      showMsg('No hay vuelos en la cola', 'info');
      return;
    }

    setProcessing(true);
    try {
      const data = await processOneFromQueue();

      if (data.status === 'success') {
        showMsg(
          `✅ Vuelo ${data.flight_inserted.codigo} procesado${
            data.conflict ? ' (⚠️ CON CONFLICTO)' : ''
          }`,
          data.conflict ? 'error' : 'success'
        );
        await fetchPendingFlights();
        if (onQueueUpdated) {
          await onQueueUpdated();
        }
        
        if (data.conflict) {
          setConflictCount((prev) => prev + 1);
        }
      } else {
        showMsg(data.message || 'Error al procesar vuelo', 'error');
      }
    } catch (error) {
      console.error('Error processing flight:', error);
      showMsg('Error al procesar vuelo', 'error');
    } finally {
      setProcessing(false);
    }
  };

  // =====================================================
  // Procesar todos los vuelos
  // =====================================================

  const handleProcessAll = async () => {
    if (pendingFlights.length === 0) {
      showMsg('No hay vuelos en la cola', 'info');
      return;
    }

    setProcessing(true);
    try {
      const data = await processAllFromQueue();

      if (data.status === 'success') {
        setProcessResults(data.results || []);
        setConflictCount(data.total_conflicts || 0);

        showMsg(
          `✅ ${data.total_processed} vuelos procesados${
            data.total_conflicts > 0 ? ` (${data.total_conflicts} conflictos)` : ''
          }`,
          data.total_conflicts > 0 ? 'error' : 'success'
        );

        await fetchPendingFlights();
        if (onQueueUpdated) {
          await onQueueUpdated();
        }
      } else {
        showMsg('Error al procesar cola', 'error');
      }
    } catch (error) {
      console.error('Error processing queue:', error);
      showMsg('Error al procesar cola', 'error');
    } finally {
      setProcessing(false);
    }
  };

  // =====================================================
  // Limpiar cola
  // =====================================================

  const handleClear = async () => {
    if (window.confirm('¿Estás seguro de que deseas limpiar la cola?')) {
      try {
        const data = await clearQueue();

        if (data.status === 'success') {
          showMsg(`🗑️ Cola vaciada (${data.cleared_count} vuelos eliminados)`, 'success');
          setPendingFlights([]);
          setProcessResults([]);
          setConflictCount(0);
          if (onQueueUpdated) {
            await onQueueUpdated();
          }
        } else {
          showMsg('Error al limpiar cola', 'error');
        }
      } catch (error) {
        console.error('Error clearing queue:', error);
        showMsg('Error al limpiar cola', 'error');
      }
    }
  };

  // =====================================================
  // Render
  // =====================================================

  return (
    <div className="queue-control-container">
      {/* Encabezado */}
      <div className="queue-header">
        <h2>🚀 Simulador de Concurrencia - Cola FIFO</h2>
        <p>Gestiona vuelos en la cola antes de insertarlos en el árbol AVL</p>
      </div>

      {/* Mensaje de estado */}
      {message && (
        <div className={`message message-${messageType}`}>
          {message}
        </div>
      )}

      <div className="queue-content">
        {/* Left panel: Agregar vuelos */}
        <div className="queue-panel queue-input-panel">
          <div className="panel-header">
            <h3>➕ Agregar Vuelo a la Cola</h3>
          </div>

          {!showForm ? (
            <button
              className="btn btn-primary btn-large"
              onClick={() => setShowForm(true)}
            >
              + Agregar Nuevo Vuelo
            </button>
          ) : (
            <form className="flight-form" onSubmit={handleAddFlight}>
              <div className="form-group">
                <label>Código</label>
                <input
                  type="number"
                  name="codigo"
                  value={formData.codigo}
                  onChange={handleInputChange}
                  placeholder="Ej: 100"
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Origen</label>
                  <input
                    type="text"
                    name="origen"
                    value={formData.origen}
                    onChange={handleInputChange}
                    placeholder="Ej: Madrid"
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Destino</label>
                  <input
                    type="text"
                    name="destino"
                    value={formData.destino}
                    onChange={handleInputChange}
                    placeholder="Ej: Barcelona"
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Hora Salida</label>
                  <input
                    type="time"
                    name="horaSalida"
                    value={formData.horaSalida}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Precio Base</label>
                  <input
                    type="number"
                    step="0.01"
                    name="precioBase"
                    value={formData.precioBase}
                    onChange={handleInputChange}
                    placeholder="Ej: 150.00"
                    required
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Pasajeros</label>
                  <input
                    type="number"
                    name="pasajeros"
                    value={formData.pasajeros}
                    onChange={handleInputChange}
                    placeholder="Ej: 180"
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Prioridad</label>
                  <select
                    name="prioridad"
                    value={formData.prioridad}
                    onChange={handleInputChange}
                  >
                    <option value={1}>Alta</option>
                    <option value={2}>Media</option>
                    <option value={3}>Baja</option>
                  </select>
                </div>
              </div>

              <div className="form-buttons">
                <button type="submit" className="btn btn-success">
                  ✅ Agregar a Cola
                </button>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowForm(false)}
                >
                  ❌ Cancelar
                </button>
              </div>
            </form>
          )}
        </div>

        {/* Middle panel: Cola pendiente */}
        <div className="queue-panel queue-pending-panel">
          <div className="panel-header">
            <h3>📋 Vuelos en la Cola ({pendingFlights.length})</h3>
          </div>

          {pendingFlights.length === 0 ? (
            <div className="empty-queue">
              <p>La cola está vacía</p>
            </div>
          ) : (
            <div className="flights-list">
              {pendingFlights.map((flight, index) => (
                <div key={index} className="flight-item">
                  <div className="flight-position">#{index + 1}</div>
                  <div className="flight-info">
                    <div className="flight-codigo">✈️ {flight.codigo}</div>
                    <div className="flight-route">
                      {flight.origen} → {flight.destino}
                    </div>
                    <div className="flight-meta">
                      <span>{flight.horaSalida}</span>
                      <span>${flight.precioBase}</span>
                      <span>{flight.pasajeros} pax</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right panel: Controles y resultados */}
        <div className="queue-panel queue-controls-panel">
          <div className="panel-header">
            <h3>⚙️ Procesar Cola</h3>
          </div>

          <div className="controls-buttons">
            <button
              className="btn btn-info btn-large"
              onClick={handleProcessOne}
              disabled={processing || pendingFlights.length === 0}
            >
              ⏭️ Procesar Uno
            </button>

            <button
              className="btn btn-success btn-large"
              onClick={handleProcessAll}
              disabled={processing || pendingFlights.length === 0}
            >
              🚀 Procesar Todo
            </button>

            <button
              className="btn btn-danger"
              onClick={handleClear}
              disabled={processing || pendingFlights.length === 0}
            >
              🗑️ Limpiar Cola
            </button>
          </div>

          {/* Estadísticas */}
          <div className="queue-stats">
            <div className="stat-card">
              <div className="stat-value">{pendingFlights.length}</div>
              <div className="stat-label">En la Cola</div>
            </div>
            <div className="stat-card conflict-card">
              <div className="stat-value">{conflictCount}</div>
              <div className="stat-label">Conflictos</div>
            </div>
          </div>

          {/* Resultados */}
          {processResults.length > 0 && (
            <div className="results-section">
              <h4>📊 Últimos Resultados</h4>
              <div className="results-summary">
                {processResults.map((result, index) => (
                  <div
                    key={index}
                    className={`result-item ${result.conflict ? 'conflict' : 'success'}`}
                  >
                    <span className="result-flight">
                      Vuelo {result.flight_inserted?.codigo}
                    </span>
                    {result.conflict && <span className="conflict-badge">⚠️ CONFLICTO</span>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Loading indicator */}
          {processing && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Procesando...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QueueControlComponent;
