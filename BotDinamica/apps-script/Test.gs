/**
 * Generación y calificación del test adaptativo, resuelto dentro del propio
 * chat (ya no genera un Google Form aparte). El frontend pide las preguntas
 * con la acción "generar_test", las muestra como tarjetas, y envía las
 * respuestas con "enviar_test" para que se califiquen aquí mismo.
 *
 * Ver docs/ARQUITECTURA.md y docs/BANCO_PROBLEMAS.md (columnas
 * Tipo_Pregunta, Opciones, Imagen_URL, Contexto).
 */

/**
 * Arma la versión "para el estudiante" de cada problema seleccionado: sin
 * Respuesta_Correcta ni Explicacion_Completa, que nunca deben llegar al
 * navegador (es código público, cualquiera podría leerlas en las
 * herramientas de desarrollador).
 *
 * @param {Array<string>} idsSeleccionados IDs del Banco, en el orden en que
 *     deben presentarse.
 * @return {Array<Object>} Uno por problema válido:
 *     { id, concepto_principal, contexto, enunciado, tipo_pregunta,
 *       opciones: [{letra, texto}], requiere_justificacion, imagen_url }
 */
function obtenerProblemasTest(idsSeleccionados) {
  return idsSeleccionados
    .map(function (id) { return buscarProblemaPorId(id); })
    .filter(function (problema) { return problema !== null; })
    .map(function (problema) {
      const tipoPregunta = String(problema['Tipo_Pregunta'] || '').toUpperCase();
      const esOM = tipoPregunta.indexOf('OM') !== -1;

      return {
        id: problema['ID'],
        concepto_principal: problema['Concepto_Principal'],
        contexto: problema['Contexto'] || '',
        enunciado: problema['Enunciado'],
        tipo_pregunta: tipoPregunta,
        opciones: esOM ? parsearOpciones_(problema['Opciones']) : [],
        requiere_justificacion: tipoPregunta.indexOf('JUSTIFICACI') !== -1,
        imagen_url: problema['Imagen_URL'] || ''
      };
    });
}

/**
 * Parsea un texto de opciones tipo "A) ... B) ... C) ... D) ..." en pares
 * {letra, texto}.
 * @param {string} opcionesTexto
 * @return {Array<{letra: string, texto: string}>}
 */
function parsearOpciones_(opcionesTexto) {
  const texto = String(opcionesTexto || '');
  const regex = /([A-E])\)\s*/g;
  const marcas = [];
  let coincidencia;
  while ((coincidencia = regex.exec(texto)) !== null) {
    marcas.push({ letra: coincidencia[1], inicioMarca: coincidencia.index, finEncabezado: regex.lastIndex });
  }

  const opciones = [];
  for (let i = 0; i < marcas.length; i++) {
    const inicio = marcas[i].finEncabezado;
    const fin = i + 1 < marcas.length ? marcas[i + 1].inicioMarca : texto.length;
    opciones.push({ letra: marcas[i].letra, texto: texto.substring(inicio, fin).trim() });
  }
  return opciones;
}

/**
 * Califica las respuestas que el estudiante envió desde el chat: escribe
 * una fila por problema en Resultados (autocalificando las de opción
 * múltiple contra Respuesta_Correcta, que nunca sale del servidor) y
 * devuelve un resumen para mostrar en el frontend.
 *
 * @param {string} estudianteId
 * @param {Array<{id: string, respuesta: string, justificacion: string}>} respuestas
 * @return {{puntaje: number, total: number, detalle: Array<Object>}}
 */
function calificarTest(estudianteId, respuestas) {
  const hojaResultados = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_RESULTADOS);
  if (!hojaResultados) throw new Error('No existe la hoja "' + HOJA_RESULTADOS + '"');

  const detalle = [];

  respuestas.forEach(function (r) {
    const problema = buscarProblemaPorId(r.id);
    if (!problema) return;

    const tipoPregunta = String(problema['Tipo_Pregunta'] || '').toUpperCase();
    const esOM = tipoPregunta.indexOf('OM') !== -1;

    let correcta = '';
    let tipoErrorDetectado = '';

    if (esOM) {
      const letraElegida = String(r.respuesta || '').trim().charAt(0).toUpperCase();
      const respuestaCorrecta = String(problema['Respuesta_Correcta'] || '').trim().toUpperCase();
      correcta = letraElegida === respuestaCorrecta;
      if (!correcta) tipoErrorDetectado = problema['Tipo_Error_Diagnostica'];
    }

    const respuestaTexto = [r.respuesta, r.justificacion].filter(Boolean).join(' — ');

    hojaResultados.appendRow([
      new Date(),
      estudianteId,
      problema['ID'],
      problema['Concepto_Principal'],
      correcta,
      1,
      tipoErrorDetectado,
      respuestaTexto
    ]);

    incrementarVecesUsada_(problema['ID']);

    detalle.push({
      id: problema['ID'],
      concepto_principal: problema['Concepto_Principal'],
      correcta: esOM ? correcta : null
    });
  });

  const calificables = detalle.filter(function (d) { return d.correcta !== null; });
  const puntaje = calificables.filter(function (d) { return d.correcta === true; }).length;

  return { puntaje: puntaje, total: calificables.length, detalle: detalle };
}
