/**
 * Tree Helpers Utility Module.
 * Functions for parsing and normalizing flight data for tree insertion.
 */

/**
 * Parse insertion-mode flights from JSON data.
 * 
 * Extracts flights with codes starting with "SB" prefix,
 * parses the numeric portion, and sorts by flight number.
 * Filters out malformed entries.
 * 
 * @param {Object} data - JSON data object with vuelos array
 *   Expected format: { vuelos: Array<{ codigo, ... }> }
 * @returns {Array<Object>} Sorted array of parsed flights:
 *   Each item: { number: number, data: flightObject }
 */
export const parseInsertionFlights = (data) => {
  if (!data || !Array.isArray(data.vuelos)) {
    return []
  }

  return data.vuelos
    .map((flightData) => {
      const codigoStr = flightData.codigo || ''
      // Filter flights with SB prefix (SkyBalance)
      if (!codigoStr.startsWith('SB')) {
        return null
      }

      // Parse flight number from codigo (e.g., "SB123" -> 123)
      const flightNumber = parseInt(codigoStr.substring(2), 10)
      if (Number.isNaN(flightNumber)) {
        return null
      }

      return {
        number: flightNumber,
        data: flightData
      }
    })
    .filter((item) => item !== null)
    .sort((a, b) => a.number - b.number)
}
