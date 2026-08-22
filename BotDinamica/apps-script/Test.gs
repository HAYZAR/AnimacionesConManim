/**
 * Generación del test: crea un Google Form nuevo con las preguntas
 * seleccionadas por el LLM, y vuelca automáticamente sus respuestas a la
 * hoja "Resultados" mediante un trigger onFormSubmit instalado por-Form.
 *
 * Ver docs/ARQUITECTURA.md (hoja "Formularios") y docs/BANCO_PROBLEMAS.md
 * (columnas Tipo_Pregunta, Opciones, Imagen_URL).
 */

/**
 * Crea un Form con las preguntas indicadas, para un estudiante dado.
 * Registra el mapeo item->pregunta en la hoja Formularios e instala el
 * trigger de calificación automática.
 *
 * @param {string} estudianteId
 * @param {Array<string>} idsSeleccionados IDs del Banco, en el orden en que
 *     deben presentarse.
 * @return {string} URL pública del Form para responder.
 */
function crearFormularioTest(estudianteId, idsSeleccionados) {
  const form = FormApp.create('Test Dinámica — ' + estudianteId + ' — ' +
    Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'America/Bogota', 'yyyy-MM-dd HH:mm'));
  form.setDescription('Generado automáticamente por NewtonBot para ' + estudianteId + '.');
  form.setCollectEmail(false);

  const mapaItems = [];

  idsSeleccionados.forEach(function (id) {
    const problema = buscarProblemaPorId(id);
    if (!problema) return; // ID inválido o inactivo; se ignora en silencio.

    agregarImagenSiExiste_(form, problema);

    const tipoPregunta = String(problema['Tipo_Pregunta'] || '').toUpperCase();

    if (tipoPregunta.indexOf('OM') !== -1) {
      const itemOM = form.addMultipleChoiceItem();
      itemOM.setTitle(String(problema['Enunciado'] || problema['ID']));
      itemOM.setChoiceValues(parsearOpciones_(problema['Opciones']).map(function (o) {
        return o.letra + ') ' + o.texto;
      }));
      itemOM.setRequired(true);

      mapaItems.push({
        item_id: itemOM.getId(),
        banco_id: problema['ID'],
        concepto_principal: problema['Concepto_Principal'],
        tipo_item: 'multiple',
        respuesta_correcta: String(problema['Respuesta_Correcta'] || '').trim().toUpperCase()
      });

      if (tipoPregunta.indexOf('JUSTIFICACI') !== -1) {
        const itemJust = form.addParagraphTextItem();
        itemJust.setTitle('Justifica tu respuesta a la pregunta anterior (' + problema['ID'] + ').');
        itemJust.setRequired(true);

        mapaItems.push({
          item_id: itemJust.getId(),
          banco_id: problema['ID'],
          concepto_principal: problema['Concepto_Principal'],
          tipo_item: 'parrafo_justificacion',
          respuesta_correcta: ''
        });
      }
    } else {
      const itemAbierto = form.addParagraphTextItem();
      itemAbierto.setTitle(String(problema['Enunciado'] || problema['ID']));
      itemAbierto.setRequired(true);

      mapaItems.push({
        item_id: itemAbierto.getId(),
        banco_id: problema['ID'],
        concepto_principal: problema['Concepto_Principal'],
        tipo_item: 'abierta',
        respuesta_correcta: ''
      });
    }

    incrementarVecesUsada_(problema['ID']);
  });

  registrarMapeoFormulario_(form.getId(), estudianteId, mapaItems);

  ScriptApp.newTrigger('onNuevoFormSubmit')
    .forForm(form)
    .onFormSubmit()
    .create();

  return form.getPublishedUrl();
}

/**
 * Si el problema trae Imagen_URL, la descarga y la agrega como ImageItem
 * justo antes de la pregunta. Cualquier error de descarga se ignora (el
 * test se genera igual, solo sin esa imagen) para no bloquear todo el test
 * por una URL caída.
 */
function agregarImagenSiExiste_(form, problema) {
  const url = problema['Imagen_URL'];
  if (!url) return;

  try {
    const blob = UrlFetchApp.fetch(url, { muteHttpExceptions: true }).getBlob();
    form.addImageItem()
      .setImage(blob)
      .setTitle('Diagrama — ' + problema['ID']);
  } catch (error) {
    Logger.log('No se pudo cargar Imagen_URL de ' + problema['ID'] + ': ' + error);
  }
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
 * Guarda en la hoja Formularios el mapeo item->pregunta de un Form recién
 * creado, para que el trigger de calificación lo pueda leer después.
 */
function registrarMapeoFormulario_(formId, estudianteId, mapaItems) {
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_FORMULARIOS);
  if (!hoja) throw new Error('No existe la hoja "' + HOJA_FORMULARIOS + '"');

  hoja.appendRow([formId, estudianteId, new Date(), JSON.stringify(mapaItems)]);
}

/**
 * Busca el mapeo guardado para un Form por su ID.
 * @return {{estudianteId: string, mapaItems: Array<Object>}|null}
 */
function obtenerMapeoFormulario_(formId) {
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_FORMULARIOS);
  if (!hoja) throw new Error('No existe la hoja "' + HOJA_FORMULARIOS + '"');

  const datos = hoja.getDataRange().getValues();
  for (let i = 1; i < datos.length; i++) {
    if (String(datos[i][0]) === String(formId)) {
      return { estudianteId: datos[i][1], mapaItems: JSON.parse(datos[i][3]) };
    }
  }
  return null;
}

/**
 * Trigger instalable (onFormSubmit) de cada Form generado por
 * crearFormularioTest(). Califica automáticamente los ítems de opción
 * múltiple y vuelca una fila por ítem respondido en la hoja Resultados.
 * Los ítems abiertos/de justificación quedan con Correcta vacío
 * (pendientes de revisión manual).
 *
 * @param {Object} e Evento de onFormSubmit.
 */
function onNuevoFormSubmit(e) {
  const formId = e.source.getId();
  const mapeo = obtenerMapeoFormulario_(formId);
  if (!mapeo) {
    Logger.log('Form ' + formId + ' no tiene mapeo registrado; se ignora la respuesta.');
    return;
  }

  const hojaResultados = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(HOJA_RESULTADOS);
  if (!hojaResultados) throw new Error('No existe la hoja "' + HOJA_RESULTADOS + '"');

  const itemResponses = e.response.getItemResponses();
  itemResponses.forEach(function (itemResponse) {
    const itemId = itemResponse.getItem().getId();
    const entrada = mapeo.mapaItems.filter(function (m) { return String(m.item_id) === String(itemId); })[0];
    if (!entrada) return;

    let correcta = '';
    let tipoErrorDetectado = '';

    if (entrada.tipo_item === 'multiple') {
      const letraElegida = String(itemResponse.getResponse() || '').trim().charAt(0).toUpperCase();
      correcta = letraElegida === entrada.respuesta_correcta;
      if (!correcta) {
        const problema = buscarProblemaPorId(entrada.banco_id);
        tipoErrorDetectado = problema ? problema['Tipo_Error_Diagnostica'] : '';
      }
    }

    hojaResultados.appendRow([
      new Date(),
      mapeo.estudianteId,
      entrada.banco_id,
      entrada.concepto_principal,
      correcta,
      1,
      tipoErrorDetectado
    ]);
  });
}
