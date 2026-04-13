/**
 * AVL Tree Service.
 * API client gateway for all AVL tree operations, flight management,
 * versioning, and stress mode controls. All functions are async and return 
 * JSON responses from the backend API.
 */

const API_BASE_URL = 'http://localhost:8000'; // Adjust if backend runs on a different port

// ============================================================================
// TREE OPERATIONS
// ============================================================================

/**
 * Insert a new value into the AVL tree.
 * @param {number} value - Value to insert
 * @returns {Promise<object>} Tree state after insertion
 */
export const insertValue = async (value) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/insert/${value}`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error inserting value');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in insertValue:', error);
        throw error;
    }
};

/**
 * Retrieve the current AVL tree structure.
 * @returns {Promise<object>} Complete tree with depth_limit, rotations, and metrics
 */
export const getTree = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/tree`);
        if (!response.ok) {
            throw new Error('Error getting tree');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in getTree:', error);
        throw error;
    }
};

/**
 * Search for a value in the AVL tree.
 * @param {number} value - Value to search for
 * @returns {Promise<object>} Search result (found/not found)
 */
export const searchValue = async (value) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/search/${value}`);
        if (!response.ok) {
            throw new Error('Error searching value');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in searchValue:', error);
        throw error;
    }
};

/**
 * Reset the AVL tree to empty state.
 * @returns {Promise<object>} Confirmation of reset
 */
export const resetTree = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/reset`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Error resetting tree');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in resetTree:', error);
        throw error;
    }
};

/**
 * Get current tree metrics (height, nodes, leaves, rotations, etc).
 * @returns {Promise<object>} Tree metrics
 */
export const getMetrics = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/metrics`);
        if (!response.ok) {
            throw new Error('Error getting metrics');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in getMetrics:', error);
        throw error;
    }
};

/**
 * Eliminate the flight with least profitability from the tree.
 * @returns {Promise<object>} Confirmation and updated tree
 */
export const eliminateLeastProfitable = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/eliminate-least-profitable`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error eliminating least profitable flight (code ${response.status})`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error in eliminateLeastProfitable:', error);
        throw error;
    }
};

/**
 * Export the AVL tree to a JSON file on the client.
 * Downloads the tree topology as a JSON file.
 * @returns {Promise<boolean>} True if export successful
 */
export const exportTree = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/export-json`);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP Error ${response.status}`);
        }
        
        // Get the blob (file)
        const blob = await response.blob();
        
        // Create temporary URL
        const url = window.URL.createObjectURL(blob);
        
        // Create temporary link
        const link = document.createElement('a');
        link.href = url;
        link.download = 'skybalance_avl.json';
        
        // Simulate click to download
        document.body.appendChild(link);
        link.click();
        
        // Clean up
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        
        return true;
    } catch (error) {
        console.error('Error in exportTree:', error);
        throw error;
    }
};

/**
 * Load a tree from a JSON file.
 * Supports both topology and insertion modes.
 * @param {File} file - JSON file to load
 * @param {string} loadType - "topology" or "insertion"
 * @returns {Promise<object>} Loaded tree data with AVL and BST
 */
export const loadFile = async (file, loadType) => {
    const formData = new FormData();
    formData.append('file', file);
    if (loadType) {
        formData.append('load_type', loadType);
    }
    const response = await fetch(`${API_BASE_URL}/avl/load-file`, {
        method: 'POST',
        body: formData  // Do NOT set Content-Type header, fetch sets it automatically
    });
    if (!response.ok) throw new Error(await response.text());
    return response.json();
};

// ============================================================================
// FLIGHT OPERATIONS
// ============================================================================

/**
 * Insert a new flight into the tree.
 * @param {object} flightData - Flight object with codigo, origen, destino, etc.
 * @returns {Promise<object>} Updated tree and flight info
 */
export const insertFlight = async (flightData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/insert`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(flightData),
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP Error ${response.status}`)
        }
        return await response.json();
    } catch (error) {
        console.error('Error in insertFlight:', error);
        throw error;
    }
};

/**
 * Delete a flight by its codigo (flight code).
 * Uses inorder successor replacement if node has two children.
 * @param {number} codigo - Flight code to delete
 * @returns {Promise<object>} Updated tree
 */
export const deleteFlight = async (codigo) => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/delete/${codigo}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error deleting flight (code ${response.status})`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error in deleteFlight:', error);
        throw error;
    }
};

/**
 * Delete a value (simple deletion, not flight-specific).
 * @param {number} codigo - Code/value to delete
 * @returns {Promise<object>} Updated tree
 */
export const deleteValue = async (codigo) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/delete/${codigo}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error deleting value (code ${response.status})`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error in deleteValue:', error);
        throw error;
    }
};

/**
 * Cancel a flight and ALL its descendants (subtree cancellation).
 * Increments mass cancellation counter.
 * @param {number} codigo - Root flight code of subtree to cancel
 * @returns {Promise<object>} Updated tree with mass cancellation count
 */
export const cancelFlight = async (codigo) => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/cancel/${codigo}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP Error ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error in cancelFlight:', error);
        throw error;
    }
};

/**
 * Cancel a value and its entire subtree.
 * @param {number} codigo - Value/code to cancel with descendants
 * @returns {Promise<object>} Updated tree
 */
export const cancelValue = async (codigo) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/cancel/${codigo}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error canceling value (code ${response.status})`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error in cancelValue:', error);
        throw error;
    }
};

// ============================================================================
// UNDO/REDO OPERATIONS
// ============================================================================

/**
 * Undo the last tree operation.
 * @returns {Promise<object>} Tree state before last operation
 */
export const undoOperation = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/undo`, {
            method: 'POST',
        });
        if (!response.ok) {
            const error = new Error('Error undoing operation');
            error.status = response.status;
            throw error;
        }
        return await response.json();
    } catch (error) {
        console.error('Error in undoOperation:', error);
        throw error;
    }
};

/**
 * Redo the last undone operation.
 * @returns {Promise<object>} Tree state after redo
 */
export const redoOperation = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/redo`, {
            method: 'POST',
        });
        if (!response.ok) {
            const error = new Error('Error redoing operation');
            error.status = response.status;
            throw error;
        }
        return await response.json();
    } catch (error) {
        console.error('Error in redoOperation:', error);
        throw error;
    }
};

// ============================================================================
// TRAVERSAL OPERATIONS
// ============================================================================

/**
 * Get tree traversal in specified mode.
 * @param {string} mode - Traversal mode ("inorder", "preorder", "postorder", "bfs")
 * @returns {Promise<object>} Traversal result with all node values in order
 */
export const getTraversal = async (mode) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/traversal/${mode}`, {
            method: 'GET',
        });
        if (!response.ok) {
            throw new Error('Error getting traversal');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in getTraversal:', error);
        throw error;
    }
};

// ============================================================================
// CONFIGURATION OPERATIONS
// ============================================================================

/**
 * Update the critical depth limit for price penalties.
 * Nodes beyond this depth get a 25% price penalty.
 * @param {number} limit - New depth limit
 * @returns {Promise<object>} Updated tree with recalculated prices
 */
export const updateDepthLimit = async (limit) => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/config/depth-limit`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ limit }),
        });
        if (!response.ok) {
            throw new Error(await response.text());
        }
        return await response.json();
    } catch (error) {
        console.error('Error in updateDepthLimit:', error);
        throw error;
    }
};

// ============================================================================
// STRESS MODE OPERATIONS
// ============================================================================

/**
 * Enable stress mode.
 * In stress mode, AVL tree skips rotations (acts like BST).
 * @returns {Promise<object>} Confirmation with new stress mode status
 */
export const enableStressMode = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/stress-mode/enable`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error enabling stress mode');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in enableStressMode:', error);
        throw error;
    }
};

/**
 * Disable stress mode.
 * Returns AVL tree to normal balanced behavior.
 * @returns {Promise<object>} Confirmation with stress mode disabled
 */
export const disableStressMode = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/stress-mode/disable`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error disabling stress mode');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in disableStressMode:', error);
        throw error;
    }
};

/**
 * Rebalance the AVL tree.
 * Performs rotations to restore balance after stress mode is disabled.
 * @returns {Promise<object>} Rebalanced tree structure
 */
export const rebalanceTree = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/rebalance`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error rebalancing tree');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in rebalanceTree:', error);
        throw error;
    }
};

/**
 * Audit the AVL tree for structural integrity.
 * Validates AVL properties and returns audit report.
 * @returns {Promise<object>} Audit report with balance factor checks
 */
export const auditTree = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/avl/audit`);
        if (!response.ok) {
            throw new Error('Error auditing tree');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in auditTree:', error);
        throw error;
    }
};

// ============================================================================
// VERSION MANAGEMENT OPERATIONS
// ============================================================================

/**
 * List all saved tree versions.
 * @returns {Promise<object>} Array of version metadata (name, timestamp, tree state, etc)
 */
export const listVersions = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/versions/list`);
        if (!response.ok) {
            throw new Error('Error listing versions');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in listVersions:', error);
        throw error;
    }
};

/**
 * Save the current tree state as a named version.
 * @param {string} name - Version name/identifier
 * @returns {Promise<object>} Confirmation with version metadata
 */
export const saveVersion = async (name) => {
    try {
        const response = await fetch(`${API_BASE_URL}/versions/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name }),
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error saving version');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in saveVersion:', error);
        throw error;
    }
};

/**
 * Restore the tree to a previously saved version.
 * Replaces current tree state with the specified version.
 * @param {string} name - Version name to restore
 * @returns {Promise<object>} Tree state from the restored version
 */
export const restoreVersion = async (name) => {
    try {
        // Encode the name for URL (spaces, special characters, etc)
        const encodedName = encodeURIComponent(name);
        const response = await fetch(`${API_BASE_URL}/versions/restore/${encodedName}`, {
            method: 'POST',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error restoring version');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in restoreVersion:', error);
        throw error;
    }
};

/**
 * Delete a previously saved version.
 * Permanently removes the specified version from storage.
 * @param {string} name - Version name to delete
 * @returns {Promise<object>} Confirmation of deletion
 */
export const deleteVersion = async (name) => {
    try {
        // Encode the name for URL
        const encodedName = encodeURIComponent(name);
        const response = await fetch(`${API_BASE_URL}/versions/${encodedName}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Error deleting version');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in deleteVersion:', error);
        throw error;
    }
};

// ============================================================================
// QUEUE OPERATIONS
// ============================================================================

/**
 * Add a flight to the pending queue.
 * Queued flights are waiting to be inserted into the tree.
 * @param {object} flightData - Flight object to queue
 * @returns {Promise<object>} Queue confirmation with updated queue state
 */
export const addToQueue = async (flightData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/queue/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(flightData),
        });
        if (!response.ok) {
            throw new Error('Error adding flight to queue');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in addToQueue:', error);
        throw error;
    }
};

/**
 * Get list of all flights currently in the pending queue.
 * @returns {Promise<object>} Queue data with list of pending flight insertions
 */
export const getPendingQueue = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/queue/pending`);
        if (!response.ok) {
            throw new Error('Error getting pending queue');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in getPendingQueue:', error);
        throw error;
    }
};

/**
 * Process one flight from the queue.
 * Removes the next flight from queue and inserts it into the tree.
 * @returns {Promise<object>} Updated tree and queue state
 */
export const processOneFromQueue = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/queue/process-one`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error processing flight from queue');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in processOneFromQueue:', error);
        throw error;
    }
};

/**
 * Process all flights from the queue.
 * Removes all queued flights and inserts them all into the tree.
 * @returns {Promise<object>} Updated tree and empty queue state
 */
export const processAllFromQueue = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/queue/process-all`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Error processing complete queue');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in processAllFromQueue:', error);
        throw error;
    }
};

/**
 * Clear all flights from the pending queue.
 * Discards all queued flights without inserting them.
 * @returns {Promise<object>} Confirmation with empty queue
 */
export const clearQueue = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/queue/clear`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Error clearing queue');
        }
        return await response.json();
    } catch (error) {
        console.error('Error in clearQueue:', error);
        throw error;
    }
};

// ============================================================================
// QUEUE OPERATION ALIASES
// Convenience aliases used by QueueControlComponent and other UI components
// ============================================================================

/**
 * Alias for addToQueue function.
 * Adds a flight to the pending queue.
 * @see addToQueue
 */
export const enqueueFlight = addToQueue;

/**
 * Alias for getPendingQueue function.
 * Retrieves the list of pending queue operations.
 * @see getPendingQueue
 */
export const listQueue = getPendingQueue;

/**
 * Alias for processOneFromQueue function.
 * Processes the next flight in the queue.
 * @see processOneFromQueue
 */
export const processNextQueue = processOneFromQueue;

/**
 * Alias for clearQueue function.
 * Clears all flights from the AVL queue.
 * @see clearQueue
 */
export const clearQueueAvl = clearQueue;