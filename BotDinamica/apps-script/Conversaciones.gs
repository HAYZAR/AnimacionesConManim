/**
 * Historial de conversación (hoja "Conversaciones"): un turno por fila.
 */

/**
 * Guarda un turno de conversación.
 * @param {string} estudianteId
 * @param {string} rol 'user' o 'model'
 * @param {string} mensaje
 */
function guardarMensaje(estudianteId, rol, mensaje) {
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_CONVERSACIONES);
  if (!hoja) throw new Error('No existe la hoja "' + HOJA_CONVERSACIONES + '"');

  hoja.appendRow([new Date(), estudianteId, rol, mensaje]);
}

/**
 * Devuelve los últimos N turnos de un estudiante, en orden cronológico
 * ascendente, listos para mandarse a Gemini como `contents`:
 * [{ role: 'user'|'model', parts: [{ text }] }, ...]
 *
 * @param {string} estudianteId
 * @param {number=} n Cantidad de turnos a recuperar (por defecto
 *     TURNOS_HISTORIAL_POR_DEFECTO).
 * @return {Array<Object>}
 */
function obtenerHistorialReciente(estudianteId, n) {
  const limite = n || TURNOS_HISTORIAL_POR_DEFECTO;
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_CONVERSACIONES);
  if (!hoja) throw new Error('No existe la hoja "' + HOJA_CONVERSACIONES + '"');

  const datos = hoja.getDataRange().getValues();
  if (datos.length < 2) return [];

  const encabezados = datos[0].map(function (h) { return String(h).trim(); });
  const idxEstudiante = encabezados.indexOf('Estudiante_ID');
  const idxRol = encabezados.indexOf('Rol');
  const idxMensaje = encabezados.indexOf('Mensaje');

  const turnos = [];
  for (let i = 1; i < datos.length; i++) {
    const fila = datos[i];
    if (String(fila[idxEstudiante]) !== String(estudianteId)) continue;
    turnos.push({
      role: fila[idxRol] === 'model' ? 'model' : 'user',
      parts: [{ text: String(fila[idxMensaje]) }]
    });
  }

  return turnos.slice(-limite);
}
