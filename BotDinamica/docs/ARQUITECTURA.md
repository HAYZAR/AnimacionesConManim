# Arquitectura detallada

Implementa la **Opción A** del plan original: Google Sheets + Apps Script +
Gemini API + un chat estático en GitHub Pages. Todo el estado vive en una
sola Google Sheet, dividida en 4 hojas.

## Hojas de la Google Sheet

### `Banco`
Ver [`BANCO_PROBLEMAS.md`](BANCO_PROBLEMAS.md). El banco de problemas, editado
a mano por el docente.

### `Resultados`
Una fila por (intento de) pregunta respondida. La llena automáticamente el
trigger `onNuevoFormSubmit` (`Test.gs`) cuando un estudiante envía un Form.

| Columna | Descripción |
|---|---|
| `Timestamp` | Fecha/hora de la respuesta. |
| `Estudiante_ID` | Identificador del estudiante (texto libre, ej. `EST-045`). |
| `ID_Pregunta` | `ID` del `Banco`. |
| `Concepto_Principal` | Copiado del `Banco` al momento de calificar (para no tener que hacer join después). |
| `Correcta` | `TRUE` / `FALSE` / vacío (`abierta` sin autocalificar). |
| `Intentos` | Siempre `1` en el MVP (no hay reintentos dentro del mismo Form). |
| `Tipo_Error_Detectado` | Si `Correcta = FALSE`, se copia `Tipo_Error_Diagnostica` del `Banco` como hipótesis de error; el docente puede corregirlo a mano. |

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

### `Formularios`
Mapeo entre un Google Form generado dinámicamente y el estudiante/preguntas
que contiene, para poder calificar automáticamente al recibir respuestas.

| Columna | Descripción |
|---|---|
| `Form_ID` | ID del Form creado (`FormApp.create(...).getId()`). |
| `Estudiante_ID` | Para quién se creó. |
| `Timestamp_Creacion` | Cuándo se generó. |
| `Mapa_Items_JSON` | JSON con `[{item_id, banco_id, concepto_principal, tipo_item, respuesta_correcta}, ...]` — `tipo_item` es `'multiple'` (autocalificable), `'parrafo_justificacion'` o `'abierta'` (ambas pendientes de revisión manual). |

`Test.gs::crearFormularioTest()` escribe esta fila; el trigger
`onNuevoFormSubmit` la lee para saber cómo calificar cada respuesta.

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
      `ids_seleccionados` quedan disponibles para cuando el docente/bot pida
      generar el siguiente test (`accion: "generar_test"`).

2. **Turno de conversación** (`accion: "mensaje"`):
   1. `Conversaciones.gs::guardarMensaje(estudiante_id, "user", mensaje)`.
   2. `Conversaciones.gs::obtenerHistorialReciente(estudiante_id, 10)`.
   3. `LLM.gs::continuarConversacion()` llama a Gemini con
      `system_instruction` + el historial como `contents` (roles
      alternados `user`/`model`).
   4. Se guarda la respuesta como turno `model` y se devuelve al frontend.

3. **Generar/asignar nuevo test** (`accion: "generar_test"`, con los
   `ids_seleccionados` de la sesión):
   1. `Test.gs::crearFormularioTest(estudiante_id, ids)` crea un Form nuevo,
      agrega un item por cada `ID` (tipo según `Tipo_Pregunta`), guarda el
      mapeo en `Formularios`, e instala el trigger `onFormSubmit` para ese
      Form específico.
   2. Devuelve la URL pública del Form al frontend, que la muestra como
      enlace al estudiante.
   3. Cuando el estudiante responde el Form, `onNuevoFormSubmit` (instalado
      por Form) se dispara, califica automáticamente lo autocalificable y
      escribe filas nuevas en `Resultados`. Así el próximo `iniciar` ya ve
      un perfil actualizado.

## Por qué esta arquitectura y no otra

- **Todo en Apps Script** evita tener que operar un backend separado
  (servidor, hosting, autenticación de servicio) — encaja con el "tier
  gratuito" del plan y con que el docente ya usa Sheets/Forms.
- **Gemini 1.5 Flash** por costo/latencia; el código en `LLM.gs` es
  intercambiable por Claude/OpenAI cambiando solo el cuerpo de la función
  que arma el `payload` y el endpoint.
- **Un Form nuevo por sesión de test** (en vez de reusar un único Form
  gigante) permite que cada estudiante reciba exactamente el subconjunto de
  preguntas que el LLM seleccionó, sin exponerle el resto del banco.
