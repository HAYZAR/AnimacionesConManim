/**
 * Integración con Gemini API: el "cerebro" socrático del bot.
 * Ver docs/PROMPT_SOCRATICO.md para el contrato de entrada/salida esperado.
 */

/**
 * Llamada de bajo nivel a Gemini. Lanza un Error si la API responde con
 * error o con una respuesta sin candidatos (ej. bloqueada por seguridad).
 *
 * @param {Array<Object>} contents Turnos [{role, parts:[{text}]}, ...]
 * @return {string} El texto de la primera respuesta candidata.
 */
function llamarGemini_(contents) {
  const apiKey = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
  if (!apiKey) {
    throw new Error('Falta la propiedad de script GEMINI_API_KEY. Ver docs/DEPLOY.md.');
  }

  const url = 'https://generativelanguage.googleapis.com/v1beta/models/' +
    GEMINI_MODELO + ':generateContent?key=' + apiKey;

  const payload = {
    system_instruction: { parts: [{ text: PROMPT_SOCRATICO_COMPLETO + INSTRUCCION_IMAGENES + INSTRUCCION_CONTEXTO }] },
    contents: contents,
    generationConfig: {
      temperature: GEMINI_TEMPERATURA,
      maxOutputTokens: GEMINI_MAX_TOKENS_SALIDA
    }
  };

  const respuesta = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });

  const codigo = respuesta.getResponseCode();
  const cuerpo = JSON.parse(respuesta.getContentText());

  if (codigo !== 200) {
    throw new Error('Gemini API error ' + codigo + ': ' + respuesta.getContentText());
  }
  if (!cuerpo.candidates || cuerpo.candidates.length === 0) {
    throw new Error('Gemini no devolvió candidatos (posible bloqueo de seguridad): ' +
      JSON.stringify(cuerpo.promptFeedback || cuerpo));
  }

  return cuerpo.candidates[0].content.parts.map(function (p) { return p.text; }).join('');
}

/**
 * Inicia una nueva sesión de tutoría para un estudiante: arma su perfil,
 * llama a Gemini con perfil + banco, separa la selección de IDs del mensaje
 * y persiste el turno inicial en el historial.
 *
 * @param {string} estudianteId
 * @return {{mensaje: string, ids_seleccionados: Array<string>}}
 */
function iniciarSesion(estudianteId) {
  const perfil = construirPerfilEstudiante(estudianteId);
  const banco = leerBanco();

  const mensajeEntrada = 'Perfil del estudiante:\n' + JSON.stringify(perfil) +
    '\n\nBanco de problemas:\n' + JSON.stringify(banco);

  const textoRespuesta = llamarGemini_([
    { role: 'user', parts: [{ text: mensajeEntrada }] }
  ]);

  const partes = parsearRespuestaInicial_(textoRespuesta);

  guardarMensaje(estudianteId, 'model', partes.mensaje);
  guardarSeleccionIds_(estudianteId, partes.idsSeleccionados);

  return { mensaje: partes.mensaje, ids_seleccionados: partes.idsSeleccionados };
}

/**
 * Continúa una conversación ya iniciada: guarda el mensaje del estudiante,
 * recupera el historial reciente y pide la siguiente respuesta a Gemini.
 *
 * @param {string} estudianteId
 * @param {string} mensajeEstudiante
 * @return {string} El mensaje de respuesta del bot.
 */
function continuarConversacion(estudianteId, mensajeEstudiante) {
  guardarMensaje(estudianteId, 'user', mensajeEstudiante);

  const historial = obtenerHistorialReciente(estudianteId);
  const respuesta = llamarGemini_(historial);

  guardarMensaje(estudianteId, 'model', respuesta);
  return respuesta;
}

/**
 * Parsea el formato de la primera respuesta del prompt socrático:
 *
 *   **Selección de preguntas:**
 *   - ID-01
 *   - ID-02
 *
 *   **Inicio de la conversación:**
 *   (mensaje...)
 *
 * Si el LLM no siguió el formato exactamente, hace un mejor esfuerzo: busca
 * líneas tipo "- ID-xxx" en todo el texto para los IDs, y si no encuentra el
 * separador "Inicio de la conversación", usa el texto completo como mensaje.
 *
 * @param {string} texto
 * @return {{idsSeleccionados: Array<string>, mensaje: string}}
 */
function parsearRespuestaInicial_(texto) {
  const marcaInicio = texto.search(/\*\*Inicio de la conversaci[oó]n:?\*\*/i);

  let bloqueIds = texto;
  let mensaje = texto;

  if (marcaInicio !== -1) {
    bloqueIds = texto.substring(0, marcaInicio);
    mensaje = texto.substring(marcaInicio)
      .replace(/\*\*Inicio de la conversaci[oó]n:?\*\*/i, '')
      .trim();
  }

  const idsSeleccionados = [];
  const regexId = /^[\s*-]*([A-Za-z]+-[A-Za-z0-9]+)\s*$/gm;
  let coincidencia;
  while ((coincidencia = regexId.exec(bloqueIds)) !== null) {
    idsSeleccionados.push(coincidencia[1]);
  }

  return { idsSeleccionados: idsSeleccionados, mensaje: mensaje };
}

/**
 * Persiste la última selección de IDs de un estudiante (para usarla luego al
 * generar el Google Form del test). Se guarda en Propiedades del script en
 * vez de una hoja porque es un dato efímero de "sesión", no un registro que
 * interese conservar/analizar.
 */
function guardarSeleccionIds_(estudianteId, ids) {
  PropertiesService.getScriptProperties().setProperty(
    'seleccion_' + estudianteId, JSON.stringify(ids)
  );
}

/**
 * Recupera la última selección de IDs guardada para un estudiante.
 * @return {Array<string>}
 */
function obtenerSeleccionIds(estudianteId) {
  const json = PropertiesService.getScriptProperties().getProperty('seleccion_' + estudianteId);
  return json ? JSON.parse(json) : [];
}
