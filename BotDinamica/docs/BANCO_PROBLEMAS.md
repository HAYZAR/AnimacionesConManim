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
| 9 | `Enunciado` | Texto largo | Texto completo del problema, tal como se le muestra al estudiante. |
| 10 | `Opciones` | Texto | `A) ... B) ... C) ... D) ...` — ver formato abajo. Vacío si `Tipo_Pregunta` no incluye `OM`. |
| 11 | `Respuesta_Correcta` | Texto | Letra de la opción correcta, ej. `B`. Vacío para preguntas abiertas (se revisan a mano). |
| 12 | `Explicacion_Completa` | Texto largo | Explicación detallada. **Uso interno/docente**: el bot nunca la envía al estudiante durante la sesión socrática (ver nota abajo). |
| 13 | `Pistas_Socraticas` | Texto | Pistas separadas por `\|`, ej. `1. ¿Qué fuerzas actúan...? \| 2. ¿Cuál es la fuerza neta...?`. Referencia que el LLM puede usar para calibrar sus propias preguntas de andamiaje. |
| 14 | `Activo` | `TRUE`/`FALSE` | Filas con `FALSE` se ignoran al leer el banco. |
| 15 | `Veces_Usada` | Número | Contador; `Test.gs` lo incrementa automáticamente cada vez que la pregunta se incluye en un test generado (para poder priorizar preguntas menos usadas más adelante). |
| 16 | `Observaciones` | Texto | Notas de validación del docente; no se envía al LLM. |
| 17 | `Imagen_URL` | Texto (URL, opcional) | URL pública de un diagrama (ej. diagrama de cuerpo libre) para este problema, ej. `https://raw.githubusercontent.com/hayzar/AnimacionesConManim/master/BotDinamica/imagenes/render/DIN-001.png`. Vacío si el problema no necesita imagen. Ver `docs/IMAGENES.md`. |

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

Al generar el Google Form (`Test.gs::crearFormularioTest`):

- Si el valor **contiene** `"OM"` (opción múltiple): se crea un ítem de
  opción múltiple con las opciones parseadas de `Opciones`, y se autocalifica
  comparando la letra elegida contra `Respuesta_Correcta`.
- Si además **contiene** `"Justificaci"` (para cubrir "Justificación" /
  "Justificacion"): se agrega un segundo ítem de párrafo pidiendo que
  justifique su respuesta. Ese ítem **no se autocalifica** (queda como
  `Correcta` vacío en `Resultados`, pendiente de revisión manual).
- Cualquier otro valor (ej. `Abierta`): se crea un único ítem de párrafo, sin
  autocalificación.

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
- `ID` se usa como llave para: la selección que hace el LLM, el mapeo
  `Formularios` (qué pregunta corresponde a qué ítem del Form), y la
  calificación automática al recibir una respuesta de Form.
- `Imagen_URL` se usa en dos lugares: `LLM.gs` la reenvía al LLM (dentro del
  banco completo) para que la incluya como Markdown en su mensaje al
  presentar el problema, y `Test.gs` la descarga y la agrega como
  `ImageItem` justo antes del ítem de la pregunta al generar el Google Form.
  Ver `docs/IMAGENES.md` para cómo crear y alojar estos diagramas.
- `Explicacion_Completa` es deliberadamente **texto de uso docente**: las
  reglas estrictas del prompt socrático prohíben que el bot revele la
  solución completa durante la conversación. Este MVP no implementa un
  "revelar explicación tras N intentos" automático (mencionado en el diseño
  original) — queda como mejora futura, ya sea en el frontend (botón que
  aparece tras varios intentos) o como un paso manual del docente.
