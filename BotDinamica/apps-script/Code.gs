/**
 * Punto de entrada del Web App. El frontend (frontend/script.js) hace POST
 * de un JSON como body con forma { accion, estudiante_id, mensaje? }.
 *
 * Ver docs/DEPLOY.md sobre por qué el fetch del frontend usa
 * Content-Type: text/plain (para evitar el preflight CORS) aunque el body
 * sea JSON — por eso aquí se parsea manualmente desde e.postData.contents.
 */

function doGet() {
  return ContentService.createTextOutput(JSON.stringify({
    ok: true,
    info: 'NewtonBot Web App activo. Usa POST con { accion, estudiante_id, mensaje }.'
  })).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  let respuesta;
  try {
    const body = JSON.parse(e.postData.contents);
    respuesta = enrutarAccion_(body);
  } catch (error) {
    respuesta = { ok: false, error: String(error && error.message || error) };
  }

  return ContentService.createTextOutput(JSON.stringify(respuesta))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Despacha la acción pedida por el frontend.
 * Acciones soportadas:
 *  - "iniciar": { accion, estudiante_id } -> inicia/reinicia una sesión.
 *  - "mensaje": { accion, estudiante_id, mensaje } -> turno de conversación.
 *  - "generar_test": { accion, estudiante_id } -> devuelve las preguntas de
 *      la última selección para resolverlas dentro del chat (sin
 *      Respuesta_Correcta ni Explicacion_Completa).
 *  - "enviar_test": { accion, estudiante_id, respuestas } -> califica las
 *      respuestas y las guarda en Resultados.
 *
 * @param {Object} body
 * @return {Object} Respuesta serializable a JSON.
 */
function enrutarAccion_(body) {
  const accion = body.accion;
  const estudianteId = body.estudiante_id;

  if (!estudianteId) {
    return { ok: false, error: 'Falta estudiante_id.' };
  }

  if (accion === 'iniciar') {
    const resultado = iniciarSesion(estudianteId);
    return { ok: true, mensaje: resultado.mensaje };
  }

  if (accion === 'mensaje') {
    if (!body.mensaje) return { ok: false, error: 'Falta mensaje.' };
    const respuestaTexto = continuarConversacion(estudianteId, body.mensaje);
    return { ok: true, mensaje: respuestaTexto };
  }

  if (accion === 'generar_test') {
    const ids = obtenerSeleccionIds(estudianteId);
    if (!ids || ids.length === 0) {
      return { ok: false, error: 'No hay una selección de preguntas activa. Inicia una sesión primero.' };
    }
    const problemas = obtenerProblemasTest(ids);
    return { ok: true, problemas: problemas };
  }

  if (accion === 'enviar_test') {
    if (!Array.isArray(body.respuestas) || body.respuestas.length === 0) {
      return { ok: false, error: 'Falta respuestas.' };
    }
    const resultado = calificarTest(estudianteId, body.respuestas);
    return { ok: true, resultado: resultado };
  }

  return { ok: false, error: 'Acción desconocida: ' + accion };
}
