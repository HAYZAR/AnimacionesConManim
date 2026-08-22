// Reemplaza esto por la URL de tu implementación de Apps Script Web App.
// Ver docs/DEPLOY.md, paso 2.7.
const WEB_APP_URL = 'https://script.google.com/macros/s/AKfycbyOqKppyyRUCrXHh2bXnEnsvXJ6rbtC2YGPADra7QKQ00Cqn7gWc5OtyJhTDAaVray9Tw/exec';

const pantallaLogin = document.getElementById('pantalla-login');
const pantallaChat = document.getElementById('pantalla-chat');
const inputEstudianteId = document.getElementById('input-estudiante-id');
const btnIniciar = document.getElementById('btn-iniciar');
const loginError = document.getElementById('login-error');

const mensajesEl = document.getElementById('mensajes');
const indicadorCargando = document.getElementById('indicador-cargando');
const formMensaje = document.getElementById('form-mensaje');
const inputMensaje = document.getElementById('input-mensaje');
const btnEnviar = document.getElementById('btn-enviar');
const btnGenerarTest = document.getElementById('btn-generar-test');
const chatError = document.getElementById('chat-error');

let estudianteId = null;

btnIniciar.addEventListener('click', iniciarSesion);
inputEstudianteId.addEventListener('keydown', function (ev) {
  if (ev.key === 'Enter') iniciarSesion();
});
formMensaje.addEventListener('submit', function (ev) {
  ev.preventDefault();
  enviarMensaje();
});
btnGenerarTest.addEventListener('click', generarTest);

async function iniciarSesion() {
  const valor = inputEstudianteId.value.trim();
  if (!valor) {
    mostrarError(loginError, 'Escribe tu identificador de estudiante.');
    return;
  }
  estudianteId = valor;
  ocultarError(loginError);
  btnIniciar.disabled = true;

  try {
    const datos = await llamarWebApp({ accion: 'iniciar', estudiante_id: estudianteId });
    pantallaLogin.hidden = true;
    pantallaChat.hidden = false;
    agregarMensajeBot(datos.mensaje);
  } catch (error) {
    mostrarError(loginError, 'No se pudo iniciar la sesión: ' + error.message);
  } finally {
    btnIniciar.disabled = false;
  }
}

async function enviarMensaje() {
  const texto = inputMensaje.value.trim();
  if (!texto) return;

  agregarMensajeUsuario(texto);
  inputMensaje.value = '';
  ocultarError(chatError);
  establecerCargando(true);

  try {
    const datos = await llamarWebApp({ accion: 'mensaje', estudiante_id: estudianteId, mensaje: texto });
    agregarMensajeBot(datos.mensaje);
  } catch (error) {
    mostrarError(chatError, 'No se pudo enviar el mensaje: ' + error.message);
  } finally {
    establecerCargando(false);
  }
}

async function generarTest() {
  ocultarError(chatError);
  establecerCargando(true);
  btnGenerarTest.disabled = true;

  try {
    const datos = await llamarWebApp({ accion: 'generar_test', estudiante_id: estudianteId });
    agregarMensajeSistema('Nuevo test generado: ' + datos.url_formulario);
  } catch (error) {
    mostrarError(chatError, 'No se pudo generar el test: ' + error.message);
  } finally {
    establecerCargando(false);
    btnGenerarTest.disabled = false;
  }
}

/**
 * Llama al Web App de Apps Script. Usa Content-Type: text/plain a propósito
 * para evitar el preflight CORS (ver docs/DEPLOY.md); el body sigue siendo
 * JSON y Code.gs lo parsea manualmente desde e.postData.contents.
 */
async function llamarWebApp(body) {
  const respuesta = await fetch(WEB_APP_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify(body)
  });

  if (!respuesta.ok) {
    throw new Error('HTTP ' + respuesta.status);
  }

  const datos = await respuesta.json();
  if (!datos.ok) {
    throw new Error(datos.error || 'Error desconocido del servidor.');
  }
  return datos;
}

function agregarMensajeBot(texto) {
  agregarMensaje('bot', renderizarMensajeBot(texto));
}

function agregarMensajeUsuario(texto) {
  agregarMensaje('usuario', escaparHtml(texto));
}

function agregarMensajeSistema(texto) {
  agregarMensaje('sistema', escaparHtml(texto));
}

function agregarMensaje(tipo, htmlSeguro) {
  const burbuja = document.createElement('div');
  burbuja.className = 'mensaje mensaje--' + tipo;
  burbuja.innerHTML = htmlSeguro;
  mensajesEl.appendChild(burbuja);
  mensajesEl.scrollTop = mensajesEl.scrollHeight;
}

/**
 * Escapa HTML y aplica un subconjunto mínimo de Markdown que puede venir en
 * la respuesta del bot: **negrita** y ![alt](url) para diagramas
 * (Imagen_URL del Banco — ver docs/IMAGENES.md). Todo el texto se escapa
 * primero, así que solo se insertan etiquetas controladas por este código.
 */
function renderizarMensajeBot(texto) {
  let html = escaparHtml(texto);

  html = html.replace(/!\[([^\]]*)\]\((https?:\/\/[^\s)]+)\)/g, function (_, alt, url) {
    return '<img src="' + url + '" alt="' + alt + '">';
  });

  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  return html;
}

function escaparHtml(texto) {
  const div = document.createElement('div');
  div.textContent = texto;
  return div.innerHTML;
}

function establecerCargando(cargando) {
  indicadorCargando.hidden = !cargando;
  btnEnviar.disabled = cargando;
}

function mostrarError(el, mensaje) {
  el.textContent = mensaje;
  el.hidden = false;
}

function ocultarError(el) {
  el.hidden = true;
}
