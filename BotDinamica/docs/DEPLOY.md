# Despliegue

## 1. Google Sheet

1. Crea una Google Sheet nueva (ej. "NewtonBot - Datos").
2. Crea 4 hojas con estos nombres **exactos**: `Banco`, `Resultados`,
   `Conversaciones`, `Formularios`.
3. En cada una, agrega la fila de encabezados según
   [`BANCO_PROBLEMAS.md`](BANCO_PROBLEMAS.md) y
   [`ARQUITECTURA.md`](ARQUITECTURA.md).
4. Llena `Banco` con al menos 15-20 problemas para que la selección del LLM
   tenga margen real de elegir.

## 2. Apps Script

1. Desde la Sheet: **Extensiones → Apps Script**.
2. Borra el `Code.gs` de ejemplo y crea/pega cada archivo de `apps-script/`
   de esta carpeta con el mismo nombre:
   `appsscript.json`, `Constantes.gs`, `Banco.gs`, `Perfil.gs`,
   `Conversaciones.gs`, `LLM.gs`, `Test.gs`, `Code.gs`.
   - `appsscript.json` se edita desde **Configuración del proyecto → Mostrar
     archivo "appsscript.json" en el editor**.
3. **Configuración del proyecto → Propiedades del script → Agregar
   propiedad del script**: `GEMINI_API_KEY` = tu clave de
   https://ai.google.dev/ (Gemini API, tier gratuito).
4. Guarda todo (Ctrl/Cmd+S).
5. **Implementar → Nueva implementación → tipo "Aplicación web"**:
   - Ejecutar como: **Yo (tu cuenta)**.
   - Quién tiene acceso: **Cualquier usuario** (o "Cualquier usuario de tu
     organización" si es un dominio de Google Workspace del colegio).
6. Autoriza los permisos solicitados (Sheets, Forms, llamadas externas a
   `generativelanguage.googleapis.com`).
7. Copia la **URL de la aplicación web** que te entrega — la necesitas en el
   paso 3.

### Reimplementar tras editar código
Cada vez que cambies el código después de la primera implementación, usa
**Implementar → Administrar implementaciones → editar (lápiz) → Nueva
versión** para que la URL existente sirva el código actualizado (crear una
implementación nueva te daría una URL distinta).

## 3. Frontend (GitHub Pages)

1. Abre `frontend/script.js` y reemplaza `WEB_APP_URL` por la URL del paso
   anterior.
2. Sube la carpeta `frontend/` (o todo `BotDinamica/`) a un repositorio de
   GitHub.
3. En el repo: **Settings → Pages → Source**: rama y carpeta donde está
   `index.html` (ej. `main` / `/BotDinamica/frontend` o `/frontend` si es un
   repo dedicado).
4. Abre la URL de GitHub Pages resultante desde el celular para probar.

## 4. Prueba de humo

1. Abre el chat, escribe un `Estudiante_ID` de prueba (ej. `EST-TEST`) y
   pulsa "Iniciar sesión".
2. Deberías recibir un saludo + diagnóstico + primera pregunta.
3. Responde un par de mensajes de forma libre y confirma que el bot sigue el
   estilo socrático (no da la respuesta directa).
4. Pide "generar test" (o el botón correspondiente) y confirma que llega un
   link de Google Form.
5. Responde ese Form con la cuenta de prueba y revisa que aparezcan filas
   nuevas en `Resultados`.

## Problemas comunes

- **`Exception: Address not found` o similar al llamar a Gemini**: revisa que
  `GEMINI_API_KEY` esté bien copiada en Propiedades del script (sin espacios)
  y que la API esté habilitada en tu proyecto de Google Cloud/AI Studio.
- **El frontend recibe un error de red / respuesta vacía**: confirma que la
  implementación web tiene acceso "Cualquier usuario" (si el Form/Sheet son
  de una cuenta de colegio con políticas restrictivas, puede requerir
  aprobación del administrador de Workspace).
- **CORS**: `frontend/script.js` envía el `fetch` con
  `headers: {'Content-Type': 'text/plain;charset=utf-8'}` a propósito — esto
  evita que el navegador dispare un preflight `OPTIONS`, que Apps Script Web
  Apps no maneja bien. `Code.gs` parsea el body como JSON de todas formas
  desde `e.postData.contents`. No cambies ese `Content-Type` a
  `application/json` en el frontend o el fetch fallará por CORS.
- **Las respuestas del Form no aparecen en `Resultados`**: el trigger
  `onFormSubmit` se instala por-Form dentro de `crearFormularioTest()`; si
  copiaste/moviste el Form manualmente después de crearlo, el trigger se
  pierde. Vuelve a generarlo desde el bot.
