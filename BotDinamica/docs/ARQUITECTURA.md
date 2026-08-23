# Arquitectura detallada

Implementa la **Opción A** del plan original: Google Sheets + Apps Script +
Gemini API + un chat estático en GitHub Pages. Todo el estado vive en una
sola Google Sheet, dividida en 3 hojas.

La prueba adaptativa se resuelve **dentro del propio chat** (no genera un
Google Form aparte) — ver "Flujo end-to-end" abajo.

## Hojas de la Google Sheet

### `Banco`
Ver [`BANCO_PROBLEMAS.md`](BANCO_PROBLEMAS.md). El banco de problemas, editado
a mano por el docente.

### `Resultados`
Una fila por pregunta respondida en un test. La llena `Test.gs::calificarTest()`
cuando el estudiante envía sus respuestas desde el frontend.

| Columna | Descripción |
|---|---|
| `Timestamp` | Fecha/hora de la respuesta. |
| `Estudiante_ID` | Identificador del estudiante (texto libre, ej. `EST-045`). |
| `ID_Pregunta` | `ID` del `Banco`. |
| `Concepto_Principal` | Copiado del `Banco` al momento de calificar (para no tener que hacer join después). |
| `Correcta` | `TRUE` / `FALSE` (autocalificado si la pregunta es `OM`) o vacío (preguntas `Abierta`, pendientes de revisión manual). |
| `Intentos` | Siempre `1` en el MVP (no hay reintentos dentro del mismo test). |
| `Tipo_Error_Detectado` | Si `Correcta = FALSE`, se copia `Tipo_Error_Diagnostica` del `Banco` como hipótesis de error; el docente puede corregirlo a mano. |
| `Respuesta_Texto` | Texto libre que escribió el estudiante: la letra elegida y/o su justificación (ej. `"B — Porque está en equilibrio."`). Para que el docente pueda revisar el razonamiento, no solo si acertó. |

`Perfil.gs::construirPerfilEstudiante()` lee esta hoja completa filtrando por
`Estudiante_ID`.

### `Conversaciones`
Historial de chat, una fila por turno.

| Columna | Descripción |
|---|---|
| `Timestamp` | Fecha/hora del turno. |
| `Estudiante_ID` | A quién pertenece el turno. |
| `Rol` | `user` (estudiante) o `model` (NewtonBot). |
| `Mensaje` | Texto del turno. |

`Conversaciones.gs` expone `guardarMensaje()` y `obtenerHistorialReciente(n)`
(por defecto los últimos 10 turnos, ver `Constantes.gs`).

## Flujo end-to-end

1. **Primer contacto / nueva sesión** (`accion: "iniciar"` en el Web App):
   1. `Perfil.gs::construirPerfilEstudiante(estudiante_id)` arma el perfil
      desde `Resultados`.
   2. `Banco.gs::leerBanco()` trae el banco completo.
   3. `LLM.gs::iniciarSesion(estudiante_id)` llama a Gemini con
      `system_instruction = PROMPT_SOCRATICO_COMPLETO` y, como mensaje de
      usuario, el perfil + banco en JSON.
   4. Se parsea la respuesta en `ids_seleccionados` + `mensaje_inicial`
      (ver `PROMPT_SOCRATICO.md`).
   5. Se guarda el turno `model` en `Conversaciones`.
   6. Se devuelve al frontend `{ mensaje: mensaje_inicial }`. Los
      `ids_seleccionados` quedan disponibles (en Propiedades del script, ver
      `LLM.gs::guardarSeleccionIds_`) para cuando se pida el test
      (`accion: "generar_test"`).

2. **Turno de conversación** (`accion: "mensaje"`):
   1. `Conversaciones.gs::guardarMensaje(estudiante_id, "user", mensaje)`.
   2. `Conversaciones.gs::obtenerHistorialReciente(estudiante_id, 10)`.
   3. `LLM.gs::continuarConversacion()` llama a Gemini con
      `system_instruction` + el historial como `contents` (roles
      alternados `user`/`model`).
   4. Se guarda la respuesta como turno `model` y se devuelve al frontend.

3. **Generar el test adaptativo** (`accion: "generar_test"`):
   1. `Test.gs::obtenerProblemasTest(ids)` arma, para cada ID seleccionado,
      la versión "segura para el navegador" del problema:
      `{ id, concepto_principal, contexto, enunciado, tipo_pregunta,
      opciones, requiere_justificacion, imagen_url }` — **sin**
      `Respuesta_Correcta` ni `Explicacion_Completa` (el frontend es código
      público; nunca deben viajar al navegador).
   2. El frontend renderiza una tarjeta por problema (reutilizando el mismo
      componente de opciones A/B/C/D del chat) y recolecta las respuestas.

4. **Enviar el test** (`accion: "enviar_test"`, con `respuestas: [{id,
   respuesta, justificacion}, ...]`):
   1. `Test.gs::calificarTest(estudiante_id, respuestas)` compara cada
      respuesta contra `Respuesta_Correcta` del `Banco` (esto sí ocurre en
      el servidor) y escribe una fila por problema en `Resultados`.
   2. Devuelve `{ puntaje, total, detalle }` para que el frontend muestre
      una pantalla de resultados. Así el próximo `iniciar` ya ve un perfil
      actualizado.

## Por qué esta arquitectura y no otra

- **Todo en Apps Script** evita tener que operar un backend separado
  (servidor, hosting, autenticación de servicio) — encaja con el "tier
  gratuito" del plan y con que el docente ya usa Sheets.
- **Gemini 2.5 Flash** por costo/latencia; el código en `LLM.gs` es
  intercambiable por Claude/OpenAI cambiando solo el cuerpo de la función
  que arma el `payload` y el endpoint.
- **El test se resuelve dentro del chat** (no en un Google Form aparte):
  la primera versión sí generaba un Form nuevo por sesión, pero eso sacaba
  al estudiante de la experiencia socrática justo al momento de resolver
  los problemas — se cambió para mantener todo en una sola interfaz.
  `Respuesta_Correcta`/`Explicacion_Completa` nunca se envían al frontend;
  la calificación ocurre siempre en Apps Script.
