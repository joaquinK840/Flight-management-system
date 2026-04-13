/**
 * API Client for communicating with the backend.
 * Provides HTTP methods (GET, POST, PUT, DELETE, UPLOAD)
 * for REST API calls with centralized configuration.
 */

const API_BASE = "http://localhost:8000";

/**
 * Perform a GET request to the API.
 * @param {string} path - API endpoint path
 * @returns {Promise<object>} JSON response from the server
 */
export const apiGet = async (path) => {
  const res = await fetch(`${API_BASE}${path}`);
  return res.json();
};

/**
 * Perform a POST request to the API.
 * @param {string} path - API endpoint path
 * @param {object} body - Request body data (default: {})
 * @returns {Promise<object>} JSON response from the server
 */
export const apiPost = async (path, body = {}) => {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return res.json();
};

/**
 * Perform a DELETE request to the API.
 * @param {string} path - API endpoint path
 * @returns {Promise<object>} JSON response from the server
 */
export const apiDelete = async (path) => {
  const res = await fetch(`${API_BASE}${path}`, { method: "DELETE" });
  return res.json();
};

/**
 * Perform a PUT request to the API.
 * @param {string} path - API endpoint path
 * @param {object} body - Request body data (default: {})
 * @returns {Promise<object>} JSON response from the server
 */
export const apiPut = async (path, body = {}) => {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return res.json();
};

/**
 * Upload a file or form data to the API.
 * @param {string} path - API endpoint path
 * @param {FormData} formData - Form data to upload
 * @returns {Promise<object>} JSON response from the server
 */
export const apiUpload = async (path, formData) => {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    body: formData
  });
  return res.json();
};

/** Base URL for all API requests */
export const API_BASE_URL = API_BASE;
