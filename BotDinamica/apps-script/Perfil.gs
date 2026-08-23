/**
 * Construcción del perfil del estudiante a partir de la hoja "Resultados".
 * Ver docs/ARQUITECTURA.md para el esquema de esa hoja.
 */

/**
 * Lee todas las filas de Resultados para un estudiante dado.
 * @param {string} estudianteId
 * @return {Array<Object>}
 */
function leerResultadosDeEstudiante_(estudianteId) {
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_RESULTADOS);
  if (!hoja) throw new Error('No existe la hoja "' + HOJA_RESULTADOS + '"');

  const datos = hoja.getDataRange().getValues();
  if (datos.length < 2) return [];

  const encabezados = datos[0].map(function (h) { return String(h).trim(); });
  const idxEstudiante = encabezados.indexOf('Estudiante_ID');

  const resultados = [];
  for (let i = 1; i < datos.length; i++) {
    const fila = datos[i];
    if (String(fila[idxEstudiante]) !== String(estudianteId)) continue;

    const registro = {};
    for (let j = 0; j < encabezados.length; j++) {
      registro[encabezados[j]] = fila[j];
    }
    resultados.push(registro);
  }
  return resultados;
}

/**
 * Construye el objeto de perfil del estudiante que se envía al LLM:
 * { estudiante_id, nivel_global, debilidades, errores_recientes,
 *   ultimo_desempeno, intentos_promedio }
 *
 * Si el estudiante no tiene resultados previos (primera vez), devuelve un
 * perfil "neutro" de nivel bajo-medio para que el bot empiece por lo básico.
 *
 * @param {string} estudianteId
 * @return {Object}
 */
function construirPerfilEstudiante(estudianteId) {
  const resultados = leerResultadosDeEstudiante_(estudianteId);

  if (resultados.length === 0) {
    return {
      estudiante_id: estudianteId,
      nivel_global: 1,
      debilidades: [],
      errores_recientes: [],
      ultimo_desempeno: null,
      intentos_promedio: 1,
      nota: 'Estudiante sin historial previo; es su primera sesión.'
    };
  }

  // Solo se usan filas autocalificadas (Correcta = TRUE/FALSE) para las
  // métricas de desempeño; los ítems abiertos/de justificación quedan con
  // Correcta vacío (pendientes de revisión manual) y no deben contar como
  // errores ni aciertos.
  const calificados = resultados.filter(function (r) { return esCalificado_(r['Correcta']); });

  // nivel_global: dificultad promedio de las preguntas respondidas
  // correctamente (si no ha acertado ninguna, usa 1 como piso).
  const correctas = calificados.filter(function (r) { return esVerdadero_(r['Correcta']); });
  const dificultadesAcertadas = correctas
    .map(function (r) { return Number(r['Dificultad']) || 0; })
    .filter(function (d) { return d > 0; });
  const nivelGlobal = dificultadesAcertadas.length > 0
    ? promedio_(dificultadesAcertadas)
    : 1;

  // debilidades: conceptos con mayor tasa de error, ordenados de peor a mejor.
  const porConcepto = {}; // concepto -> { total, incorrectas }
  calificados.forEach(function (r) {
    const concepto = r['Concepto_Principal'];
    if (!concepto) return;
    if (!porConcepto[concepto]) porConcepto[concepto] = { total: 0, incorrectas: 0 };
    porConcepto[concepto].total++;
    if (!esVerdadero_(r['Correcta'])) porConcepto[concepto].incorrectas++;
  });

  const debilidades = Object.keys(porConcepto)
    .map(function (concepto) {
      const c = porConcepto[concepto];
      return { concepto: concepto, tasaError: c.incorrectas / c.total };
    })
    .filter(function (c) { return c.tasaError > 0; })
    .sort(function (a, b) { return b.tasaError - a.tasaError; })
    .slice(0, 5)
    .map(function (c) { return c.concepto; });

  // errores_recientes: últimos Tipo_Error_Detectado no vacíos, sin duplicar,
  // más recientes primero (asumiendo que Resultados está en orden cronológico
  // de inserción, como lo deja el trigger de Forms).
  const erroresRecientes = [];
  for (let i = resultados.length - 1; i >= 0 && erroresRecientes.length < 5; i--) {
    const tipoError = resultados[i]['Tipo_Error_Detectado'];
    if (tipoError && erroresRecientes.indexOf(tipoError) === -1) {
      erroresRecientes.push(tipoError);
    }
  }

  // ultimo_desempeno: % de correctas en la sesión de test más reciente
  // (agrupando por el mismo día/timestamp más cercano entre sí no es trivial
  // con Apps Script puro; como aproximación simple tomamos las últimas N
  // filas, donde N = tamaño típico de un test, tope 8).
  const ultimasN = calificados.slice(-8);
  const ultimoDesempeno = ultimasN.length > 0
    ? Math.round((ultimasN.filter(function (r) { return esVerdadero_(r['Correcta']); }).length / ultimasN.length) * 100)
    : null;

  const intentos = resultados
    .map(function (r) { return Number(r['Intentos']) || 1; });
  const intentosPromedio = Math.round(promedio_(intentos) * 10) / 10;

  return {
    estudiante_id: estudianteId,
    nivel_global: Math.round(nivelGlobal * 10) / 10,
    debilidades: debilidades,
    errores_recientes: erroresRecientes,
    ultimo_desempeno: ultimoDesempeno,
    intentos_promedio: intentosPromedio
  };
}

function esVerdadero_(valor) {
  return String(valor).toUpperCase() === 'TRUE';
}

// Distingue "autocalificado" (TRUE/FALSE) de "vacío" (pendiente de revisión
// manual: ítems abiertos o de justificación). Ver Test.gs::calificarTest.
function esCalificado_(valor) {
  return valor === true || valor === false || String(valor).toUpperCase() === 'TRUE' || String(valor).toUpperCase() === 'FALSE';
}

function promedio_(numeros) {
  if (numeros.length === 0) return 0;
  const suma = numeros.reduce(function (a, b) { return a + b; }, 0);
  return suma / numeros.length;
}
