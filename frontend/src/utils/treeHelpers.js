export const parseInsertionFlights = (data) => {
  if (!data || !Array.isArray(data.vuelos)) {
    return []
  }

  return data.vuelos
    .map((flightData) => {
      const codigoStr = flightData.codigo || ''
      if (!codigoStr.startsWith('SB')) {
        return null
      }

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
