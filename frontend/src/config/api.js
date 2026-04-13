/**
 * API configuration for the frontend.
 * Retrieves the base API URL from environment variables or defaults to localhost:8000
 */

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
