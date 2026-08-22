# NewtonBot — Tutor Socrático Adaptativo de Dinámica

Bot de tutoría adaptativa y socrática para el tema de Dinámica (Leyes de Newton),
pensado para estudiantes de grado 10°. Diagnostica el nivel del estudiante a
partir de sus resultados en tests, conversa con él siguiendo un método
socrático (nunca da la respuesta directa) y le asigna un nuevo test adaptado
a sus debilidades.

> Este proyecto vive dentro de `AnimacionesConManim/BotDinamica/` pero está
> pensado como una carpeta autocontenida: se puede mover tal cual a su propio
> repositorio de GitHub sin más cambios que actualizar las URLs del Web App
> en `frontend/script.js`.

## Arquitectura (Opción A del plan: rápida y de bajo costo)

```
Estudiante (celular/PC)
   │  abre
   ▼
frontend/  (GitHub Pages: chat HTML/CSS/JS)
   │  fetch POST (JSON)
   ▼
apps-script/  (Google Apps Script, Web App doPost/doGet)
   │  lee/escribe
   ▼
Google Sheet  ("Banco", "Resultados", "Conversaciones", "Formularios")
   │  perfil + banco + historial
   ▼
Gemini API (gemini-2.5-flash)  ← "cerebro" socrático
```

Ver el detalle completo en [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md).

## Contenido de esta carpeta

- `docs/ARQUITECTURA.md` — flujo completo, hojas de cálculo y responsabilidades de cada pieza.
- `docs/PROMPT_SOCRATICO.md` — system prompt exacto usado como "cerebro" del bot.
- `docs/BANCO_PROBLEMAS.md` — esquema de columnas del banco de problemas.
- `docs/DEPLOY.md` — pasos para desplegar (Apps Script + GitHub Pages).
- `docs/IMAGENES.md` — cómo crear diagramas (TikZ), compilarlos a PNG y
  alojarlos para usarlos como `Imagen_URL` en el Banco.
- `apps-script/` — código `.gs` para pegar en el editor de Apps Script.
- `frontend/` — chat estático para publicar en GitHub Pages.
- `imagenes/tikz/` — fuentes TikZ de los diagramas; `imagenes/render/` — PNG
  compilados automáticamente por `.github/workflows/build-imagenes-dinamica.yml`.

## Puesta en marcha rápida

1. Crea una Google Sheet nueva con las hojas `Banco`, `Resultados`,
   `Conversaciones` y `Formularios` (columnas en `docs/BANCO_PROBLEMAS.md`
   y `docs/ARQUITECTURA.md`).
2. Abre **Extensiones → Apps Script** desde esa hoja y copia el contenido de
   cada archivo de `apps-script/` (mismo nombre de archivo).
3. En **Configuración del proyecto → Propiedades del script**, agrega
   `GEMINI_API_KEY` con tu clave de la [Gemini API](https://ai.google.dev/).
4. Implementa el proyecto como **Aplicación web** (Web App), acceso
   "Cualquier usuario", y copia la URL que te entrega.
5. Pega esa URL en `frontend/script.js` (`WEB_APP_URL`) y publica `frontend/`
   en GitHub Pages.

Pasos detallados, permisos y solución de problemas en
[`docs/DEPLOY.md`](docs/DEPLOY.md).

## Estado del MVP

Implementado:
- Lectura del banco de problemas desde Sheets.
- Construcción del perfil del estudiante a partir de `Resultados`.
- Llamada a Gemini con el prompt socrático + perfil + banco + historial.
- Historial de conversación persistido en Sheets.
- Generación dinámica de un Google Form con las preguntas seleccionadas y
  volcado automático de sus respuestas a `Resultados`.
- Chat web mínimo para GitHub Pages, con soporte para mostrar diagramas
  (`Imagen_URL`) embebidos en la conversación.
- Diagramas de problemas en TikZ, con build automático a PNG vía GitHub
  Actions (ver `docs/IMAGENES.md`).

Pendiente / a mano de quien despliegue:
- Calificación automática de preguntas abiertas (el MVP solo autocalifica
  opción múltiple / respuesta corta exacta; lo demás queda "pendiente de
  revisión").
- Autenticación real de estudiantes (el MVP identifica por un
  `estudiante_id` de texto libre, sin login).
- Ajuste fino del prompt y de los pesos del algoritmo de perfil tras probar
  con estudiantes reales (paso 6 del plan original).
