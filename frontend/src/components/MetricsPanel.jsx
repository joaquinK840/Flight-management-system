import React from 'react';
import { getMetrics } from '../services/avlService';
import './MetricsPanel.css';

const MetricsPanel = ({ metrics, refreshMetrics }) => {
    const formatTraversal = (traversal) => {
        if (!traversal || traversal.length === 0) return 'Vacío';
        return traversal.join(' → ');
    };

    const getModeColor = (mode) => {
        return mode ? '#ff6b6b' : '#4ecdc4';
    };

    const getModeLabel = (mode) => {
        return mode ? 'ESTRÉS' : 'NORMAL';
    };

    if (!metrics) {
        return (
            <div className="metrics-panel empty-state">
                <p>Cargue un árbol para ver las métricas</p>
            </div>
        );
    }

    return (
        <div className="metrics-panel">
            <h2>Métricas del Árbol AVL</h2>
            
            <div className="metrics-grid">
                <div className="metric-item">
                    <label>Altura</label>
                    <span className="metric-value">{metrics.height}</span>
                </div>
                
                <div className="metric-item">
                    <label>Total de Nodos</label>
                    <span className="metric-value">{metrics.total_nodes}</span>
                </div>
                
                <div className="metric-item">
                    <label>Hojas</label>
                    <span className="metric-value">{metrics.leaves}</span>
                </div>

                <div className="metric-item">
                    <label>Modo</label>
                    <span 
                        className="metric-badge" 
                        style={{ backgroundColor: getModeColor(metrics.stress_mode) }}
                    >
                        {getModeLabel(metrics.stress_mode)}
                    </span>
                </div>
            </div>

            <div className="rotations-section">
                <h3>Rotaciones</h3>
                <div className="rotations-grid">
                    <div className="rotation-item">
                        <span className="rotation-type">LL</span>
                        <span className="rotation-count">{metrics.rotation_counts.LL}</span>
                    </div>
                    <div className="rotation-item">
                        <span className="rotation-type">RR</span>
                        <span className="rotation-count">{metrics.rotation_counts.RR}</span>
                    </div>
                    <div className="rotation-item">
                        <span className="rotation-type">LR</span>
                        <span className="rotation-count">{metrics.rotation_counts.LR}</span>
                    </div>
                    <div className="rotation-item">
                        <span className="rotation-type">RL</span>
                        <span className="rotation-count">{metrics.rotation_counts.RL}</span>
                    </div>
                    <div className="rotation-item total">
                        <span className="rotation-type">Total</span>
                        <span className="rotation-count">{metrics.total_rotations}</span>
                    </div>
                </div>
            </div>

            <div className="cancellations-section">
                <h3>Cancelaciones Masivas</h3>
                <span className="metric-value">{metrics.mass_cancellations}</span>
            </div>

            <div className="traversals-section">
                <div className="traversal-item">
                    <h4>Recorrido Inorden</h4>
                    <div className="traversal-value">
                        {formatTraversal(metrics.traversals.inorder)}
                    </div>
                </div>
                
                <div className="traversal-item">
                    <h4>Recorrido BFS (Anchura)</h4>
                    <div className="traversal-value">
                        {formatTraversal(metrics.traversals.bfs)}
                    </div>
                </div>
            </div>

            <div className="metadata">
                <p>Profundidad Límite: {metrics.depth_limit}</p>
            </div>
        </div>
    );
};

export default MetricsPanel;
