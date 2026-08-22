/**
 * Lectura del banco de problemas (hoja "Banco").
 * Ver docs/BANCO_PROBLEMAS.md para el esquema de columnas.
 */

/**
 * Lee todas las filas activas de la hoja Banco y las devuelve como array de
 * objetos JS, usando los encabezados de la fila 1 como claves.
 * @return {Array<Object>}
 */
function leerBanco() {
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_BANCO);
  if (!hoja) {
    throw new Error('No existe la hoja "' + HOJA_BANCO + '"');
  }

  const datos = hoja.getDataRange().getValues();
  if (datos.length < 2) return [];

  const encabezados = datos[0].map(function (h) { return String(h).trim(); });
  const filas = datos.slice(1);

  const banco = [];
  for (let i = 0; i < filas.length; i++) {
    const fila = filas[i];
    if (fila.every(function (celda) { return celda === '' || celda === null; })) continue;

    const problema = {};
    for (let j = 0; j < encabezados.length; j++) {
      problema[encabezados[j]] = fila[j];
    }

    const activo = String(problema['Activo']).toUpperCase();
    if (activo === 'FALSE') continue;

    banco.push(problema);
  }

  return banco;
}

/**
 * Busca un problema del banco por su ID.
 * @param {string} id
 * @return {Object|null}
 */
function buscarProblemaPorId(id) {
  const banco = leerBanco();
  for (let i = 0; i < banco.length; i++) {
    if (String(banco[i]['ID']) === String(id)) return banco[i];
  }
  return null;
}

/**
 * Incrementa en 1 el contador Veces_Usada de un problema (se llama cada vez
 * que ese ID se incluye en un test generado). No falla si el ID no existe.
 * @param {string} id
 */
function incrementarVecesUsada_(id) {
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_BANCO);
  if (!hoja) throw new Error('No existe la hoja "' + HOJA_BANCO + '"');

  const datos = hoja.getDataRange().getValues();
  const encabezados = datos[0].map(function (h) { return String(h).trim(); });
  const idxId = encabezados.indexOf('ID');
  const idxVecesUsada = encabezados.indexOf('Veces_Usada');
  if (idxId === -1 || idxVecesUsada === -1) return;

  for (let i = 1; i < datos.length; i++) {
    if (String(datos[i][idxId]) === String(id)) {
      const actual = Number(datos[i][idxVecesUsada]) || 0;
      hoja.getRange(i + 1, idxVecesUsada + 1).setValue(actual + 1);
      return;
    }
  }
}
