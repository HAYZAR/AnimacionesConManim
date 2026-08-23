# Esquema del Banco de problemas

Hoja `Banco` en la Google Sheet. Una fila = un problema/pregunta. La primera
fila debe contener **exactamente estos encabezados, en este orden**
(`Banco.gs` los lee por nombre de columna, así que el nombre importa más que
el orden, pero se respeta el orden acordado):

| # | Columna | Tipo de dato | Descripción / Ejemplo |
|---|---|---|---|
| 1 | `ID` | Texto | `DIN-001`, `DIN-002`… identificador estable, único. |
| 2 | `Concepto_Principal` | Texto | `Diagrama de cuerpo libre`. Debe coincidir con los valores que se usan como `debilidades` en el perfil del estudiante. |
| 3 | `Conceptos_Secundarios` | Texto | `Fricción, Normal` (separados por coma). |
| 4 | `Dificultad` | Número 1-3 | 1 = Básico, 2 = Intermedio, 3 = Avanzado. |
| 5 | `Tipo_Error_Diagnostica` | Texto | `Olvidar la normal`. Error conceptual típico que detecta esta pregunta. |
| 6 | `Demanda_Cognitiva` | Texto | `Modelar + Justificar`. |
| 7 | `Tipo_Pregunta` | Texto | `OM+Justificación`, `OM`, `Abierta`. Ver "Cómo se interpreta `Tipo_Pregunta`" abajo. |
| 8 | `Andamiaje_Recomendado` | Texto | `Bajo` / `Medio` / `Alto`. Nivel de ayuda sugerido para el LLM al guiar esta pregunta. |
| 9 | `Contexto` | Texto largo (opcional) | Escenario/situación que enmarca el problema (ej. "Dos estudiantes compiten en un juego de tira y afloja en el descanso"), separado del enunciado técnico. Ver "Por qué separar `Contexto` de `Enunciado`" abajo. |
| 10 | `Enunciado` | Texto largo | La pregunta técnica en sí, tal como se le muestra al estudiante (sin repetir el contexto). |
| 11 | `Opciones` | Texto | `A) ... B) ... C) ... D) ...` — ver formato abajo. Vacío si `Tipo_Pregunta` no incluye `OM`. |
| 12 | `Respuesta_Correcta` | Texto | Letra de la opción correcta, ej. `B`. Vacío para preguntas abiertas (se revisan a mano). |
| 13 | `Explicacion_Completa` | Texto largo | Explicación detallada. **Uso interno/docente**: el bot nunca la envía al estudiante durante la sesión socrática (ver nota abajo). |
| 14 | `Pistas_Socraticas` | Texto | Pistas separadas por `\|`, ej. `1. ¿Qué fuerzas actúan...? \| 2. ¿Cuál es la fuerza neta...?`. Referencia que el LLM puede usar para calibrar sus propias preguntas de andamiaje. |
| 15 | `Activo` | `TRUE`/`FALSE` | Filas con `FALSE` se ignoran al leer el banco. |
| 16 | `Veces_Usada` | Número | Contador; `Test.gs` lo incrementa automáticamente cada vez que la pregunta se incluye en un test generado (para poder priorizar preguntas menos usadas más adelante). |
| 17 | `Observaciones` | Texto | Notas de validación del docente; no se envía al LLM. |
| 18 | `Imagen_URL` | Texto (URL, opcional) | URL pública de un diagrama (ej. diagrama de cuerpo libre) para este problema, ej. `https://raw.githubusercontent.com/hayzar/AnimacionesConManim/master/BotDinamica/imagenes/render/DIAG-02.png`. Vacío si el problema no necesita imagen. Ver `docs/IMAGENES.md`. |

## Por qué separar `Contexto` de `Enunciado`

Para que la Dinámica "enganche" a un estudiante de secundaria, ayuda enmarcar
el problema en una situación reconocible (un partido de fútbol, un bus, un
ciclista) antes de la pregunta técnica — el mismo patrón "context + stem" que
usa `Evaluaciones-Saber-11`. Mantenerlos en columnas separadas permite:
- reutilizar el mismo `Contexto` en varias preguntas relacionadas sin
  duplicar texto,
- que el LLM decida *cómo* presentar el contexto (puede parafrasearlo de
  forma más conversacional) sin alterar el enunciado técnico exacto,
- y que `Contexto` sea opcional: si está vacío, el bot simplemente presenta
  el `Enunciado` directo (ver `INSTRUCCION_CONTEXTO` en `Constantes.gs`).

## Formato de `Opciones`

Texto plano con las 4 (o más) opciones en línea, marcadas con letra y
paréntesis: `A) Solo el peso  B) Peso y normal  C) Peso, normal y fricción  D) Ninguna`.
`Test.gs::parsearOpciones_()` lo separa con la expresión regular
`/([A-E])\)\s*/g` en pares `{letra, texto}`.

## Formato de `Pistas_Socraticas`

Pistas separadas por `|`, numeradas o no: `1. ¿Qué fuerzas actúan sobre el bloque? | 2. ¿Cuál es la fuerza neta en el eje x?`.
`Test.gs`/`LLM.gs` las tratan como texto de referencia (se envían tal cual
dentro del banco completo a Gemini); el LLM decide cómo y cuándo usarlas
como parte del andamiaje socrático — no se muestran automáticamente al
estudiante.

## Cómo se interpreta `Tipo_Pregunta`

Al servir el test al frontend y calificarlo (`Test.gs::obtenerProblemasTest` /
`calificarTest`):

- Si el valor **contiene** `"OM"` (opción múltiple): el frontend muestra las
  opciones parseadas de `Opciones` como tarjetas A/B/C/D, y se autocalifica
  en el servidor comparando la letra elegida contra `Respuesta_Correcta`
  (que nunca se envía al navegador).
- Si además **contiene** `"Justificaci"` (para cubrir "Justificación" /
  "Justificacion"): el frontend muestra un cuadro de texto adicional pidiendo
  que justifique su respuesta. Esa justificación **no se autocalifica**
  (queda como texto libre en `Respuesta_Texto`, pendiente de revisión
  manual del docente).
- Cualquier otro valor (ej. `Abierta`): el frontend muestra un único cuadro
  de texto libre, sin autocalificación.

## Notas de diseño

- `Banco.gs::leerBanco()` devuelve un array de objetos JS con estas mismas
  claves (respetando los nombres de columna), filtrando `Activo = FALSE`.
- El **banco completo** (todas las columnas, no solo un resumen) se envía a
  Gemini en cada `iniciarSesion` — el LLM necesita `Enunciado`, `Opciones`,
  `Andamiaje_Recomendado` y `Pistas_Socraticas` para poder seleccionar
  preguntas *y* presentar la primera directamente en su respuesta (paso 2 y 3
  del prompt socrático). Si el banco crece mucho (cientos de filas), esto
  empieza a pesar en tokens; una mejora natural sería pre-filtrar en
  `Perfil.gs` antes de llamar al LLM (ej. solo enviar los conceptos
  relacionados con las debilidades + una muestra de los demás) — no
  implementado en este MVP.
- `ID` se usa como llave para: la selección que hace el LLM y la
  calificación de cada respuesta al recibir el test (`Test.gs::calificarTest`).
- `Imagen_URL` se usa en dos lugares: `LLM.gs` la reenvía al LLM (dentro del
  banco completo) para que la incluya como Markdown en su mensaje al
  presentar el problema, y `Test.gs::obtenerProblemasTest` la incluye tal
  cual para que el frontend la muestre como `<img>` en la tarjeta del test.
  Ver `docs/IMAGENES.md` para cómo crear y alojar estos diagramas.
- `Explicacion_Completa` es deliberadamente **texto de uso docente**: las
  reglas estrictas del prompt socrático prohíben que el bot revele la
  solución completa durante la conversación. Este MVP no implementa un
  "revelar explicación tras N intentos" automático (mencionado en el diseño
  original) — queda como mejora futura, ya sea en el frontend (botón que
  aparece tras varios intentos) o como un paso manual del docente.
