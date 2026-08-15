---
name: manim-video-fisica-tiktok
description: Instala y usa Manim Community Edition en Windows (PowerShell) para producir videos verticales cortos de física (1080x1920, formato TikTok/Reels/Shorts) con guion, narración y animaciones. Úsala siempre que el usuario pida crear, planear o renderizar un video de física/matemáticas para TikTok o redes sociales, mencione "Manim" junto con un tema de física (dinámica, fricción, cinemática, energía, etc.), pida instalar o configurar el entorno de Manim en su computador con Windows, o quiera generar un nuevo video siguiendo el mismo patrón que "El ángulo que despierta la fricción" (Español/extras/dinamica_friccion_tiktok/). También aplica si el usuario pregunta por qué su animación de Manim se ve cortada en un video vertical, o por qué elementos de texto no desaparecen de la escena.
---

# Video de física para TikTok con Manim (Windows / PowerShell)

Esta skill encapsula el flujo completo que se usó para producir el primer video de la
serie — "El ángulo que despierta la fricción" (dinámica + fricción estática/cinética,
`Español/extras/dinamica_friccion_tiktok/`) — para que sea repetible en Windows con
PowerShell, la máquina del profesor que mantiene este repositorio.

El resto del curso (`Español/1_formato_textos`, etc.) usa la versión antigua de
`3b1b/manim` (`big_ol_pile_of_manim_imports`). **Esta skill usa Manim Community Edition
(`pip install manim`)**, que es el motor mantenido activamente y el que mejor soporta
un flujo moderno de instalación en Windows. No mezcles los dos: un video producido con
esta skill es un proyecto independiente dentro de `Español/extras/<nombre_del_video>/`.

## 1. Instalación del entorno (una sola vez por máquina)

Ejecuta esto en PowerShell, no en cmd.exe ni en bash. Si algo falla, léele el error al
usuario en vez de reintentarlo a ciegas — casi siempre es uno de los tres gotchas de la
sección 1.1.

```powershell
# Python 3.10+ (si `py --version` ya da 3.10+, sáltate esto)
winget install Python.Python.3.12

# Entorno virtual dedicado al proyecto (evita romper otros usos de Python del usuario)
py -m venv .venv
.venv\Scripts\Activate.ps1

# Manim + dependencias Python
pip install --upgrade pip
pip install manim

# FFmpeg (requerido para exportar mp4)
winget install Gyan.FFmpeg

# LaTeX -- MiKTeX es mucho más liviano que TeX Live en Windows y basta para
# MathTex/Tex de Manim
winget install MiKTeX.MiKTeX
```

Verifica al final:

```powershell
python -c "import manim; print(manim.__version__)"
ffmpeg -version
latex --version
```

### 1.1 Gotchas específicos de Windows (revisa esto antes de reportar un fallo)

- **`Activate.ps1` bloqueado por la política de ejecución**: PowerShell por defecto no
  deja correr scripts. Si el error menciona "running scripts is disabled", ejecuta
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` una vez, o activa el venv con
  `powershell -ExecutionPolicy Bypass -File .venv\Scripts\Activate.ps1`.
- **`ffmpeg`/`latex` "no se reconoce como un comando"** justo después de instalarlos
  con winget: winget actualiza el PATH del sistema, pero la terminal ya abierta no lo
  recarga. Cierra y vuelve a abrir PowerShell (o la sesión de Claude Code) antes de
  concluir que la instalación falló.
- **MiKTeX pide instalar un paquete la primera vez que compilas una fórmula**: si
  aparece un diálogo o el render se queda colgado, abre "MiKTeX Console" →
  Settings → activa "Always install missing packages on-the-fly" para que no vuelva a
  bloquear un render no interactivo.

## 2. Flujo para crear un video nuevo

Cada video vive en su propia carpeta `Español/extras/<nombre_del_video>/` con tres
archivos, siguiendo exactamente el patrón de `dinamica_friccion_tiktok/`:

```
Español/extras/<nombre_del_video>/
├── GUION.md              # guion completo: hook, teoría, timeline, specs de TikTok
├── <nombre_del_video>.py # escena de Manim
└── ESCENAS.md            # instalación + comando de render (breve, sigue la convención del curso)
```

Usa `assets/plantilla_escena.py` (en esta skill) como punto de partida para el `.py` —
ya trae resuelto el formato vertical y los helpers anti-bugs de la sección 4. Usa
`assets/GUION_template.md` como esqueleto del guion — respeta las mismas secciones que
`Español/extras/dinamica_friccion_tiktok/GUION.md` (introducción llamativa, aspectos
teóricos clave, estrategia de resolución, conclusión, reto final, specs de TikTok).

Antes de escribir una sola línea de la escena, **fija los números del problema físico y
verifícalos a mano** (o con Python) en el propio GUION.md, igual que se hizo ahí:

```
θ = 30°:  mg·sinθ = 9.80 N   |  μs·mg·cosθ = 10.19 N   → NO desliza
θ = 35°:  mg·sinθ = 11.24 N  |  μs·mg·cosθ = 9.63 N    → SÍ desliza
```

Un guion con números que no cuadran (o que nunca se comprobaron) es el error más caro
de arrastrar hasta el render final, porque el video entero se construye sobre esos
valores.

### 2.1 Ciclo de render — iterar rápido, verificar en serio

1. **Borrador rápido**: `manim -ql --format=mp4 archivo.py NombreEscena` (baja calidad,
   segundos en vez de minutos). Úsalo mientras ajustas geometría y layout.
2. **Verifica visualmente sin pedirle al usuario que abra el video** — usa
   `scripts/contact_sheet.ps1 -Video ruta\al\video.mp4` (bundled en esta skill). Genera
   un contact sheet (una imagen con un fotograma por segundo en cuadrícula) y luego
   **léela con la herramienta de lectura de imágenes**. Un video de Manim se ve
   perfecto en el código y sigue teniendo texto cortado, vectores invertidos o
   elementos que nunca se borran — la única forma confiable de detectarlo es mirando
   los fotogramas reales, no releyendo el `.py`.
3. Corrige lo que encuentres (ver checklist de la sección 4) y vuelve a renderizar en
   baja calidad hasta que el contact sheet se vea limpio en toda la línea de tiempo.
4. **Ajusta el ritmo** para que la duración total caiga en 60-90s (el rango que
   funciona bien en TikTok para contenido explicativo): suma mentalmente los
   `run_time` y `self.wait()` de cada método y añade `self.wait()` extra en los puntos
   donde la narración del GUION.md necesita más tiempo en pantalla.
5. **Render final**: `manim -qh --format=mp4 --fps 30 archivo.py NombreEscena`.
6. **Verifica con ffprobe**, no de oído:
   ```powershell
   ffprobe -v error -show_entries format=duration -show_entries stream=width,height,avg_frame_rate archivo.mp4
   ```
   Debe dar `width=1080`, `height=1920`, `avg_frame_rate=30/1`, y una duración dentro
   del rango que fijaste en el GUION.md.

## 3. Formato vertical real (no un video horizontal recortado)

Al inicio del `.py`, antes de definir la escena:

```python
from manim import *

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 8.0
config.frame_width = config.frame_height * (config.pixel_width / config.pixel_height)
```

Esto deja un frame angosto (~4.5 unidades de Manim de ancho, contra las ~14 de un
frame horizontal normal). Es la causa raíz del bug más frecuente de esta skill — ver
sección 4.1.

## 4. Reglas para que el código no falle en el render (aprendidas a la fuerza)

Estos cuatro problemas aparecieron los cuatro en el primer video de la serie y **no se
detectan leyendo el código** — solo viendo el video renderizado fotograma a fotograma.
Prevenirlos de entrada ahorra una vuelta completa de render + revisión.

### 4.1 Todo texto/fórmula debe pasar por un límite de ancho

`Text`/`MathTex` pensados para un frame horizontal normal (14 unidades) se salen del
frame vertical (4.5 unidades) y quedan cortados en los bordes izquierdo/derecho, sin
ningún error en consola. Define esto una vez y envuelve con él cualquier texto u
fórmula que no sea una etiqueta pequeña junto a un vector:

```python
def cap_width(mobject, max_width=3.9):
    """Encoge (nunca agranda) un mobject para que quepa en el frame vertical angosto."""
    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)
    return mobject
```

Úsalo así: `titulo = cap_width(Text("...", font_size=28)).to_edge(UP, buff=1.2)`.

### 4.2 Un solo helper de geometría, nunca signos recalculados a mano

En escenas con planos inclinados, poleas o superficies en ángulo, es fácil que el
vector de la normal o la fricción apunten al lado equivocado si cada método recalcula
`sin`/`cos` por su cuenta. Define **una sola vez** la dirección del plano y su normal,
y reutilízalos en toda la escena:

```python
def dir_plano(theta_deg):
    """Vector unitario a lo largo del plano, apuntando cuesta ARRIBA."""
    theta = np.deg2rad(theta_deg)
    return np.array([np.cos(theta), np.sin(theta), 0.0])

def dir_normal(theta_deg):
    """Vector unitario normal al plano, hacia AFUERA de la superficie."""
    theta = np.deg2rad(theta_deg)
    return np.array([-np.sin(theta), np.cos(theta), 0.0])
```

Verifica el resultado mirando el contact sheet: la normal debe apuntar hacia afuera de
la superficie (no hacia adentro) y la fricción/componentes del peso deben quedar sobre
la línea del plano, no desviadas.

### 4.3 Todo `Write`/`FadeIn` necesita su `FadeOut` antes de la siguiente escena

Es fácil crear una etiqueta explicativa, mostrarla, y olvidar quitarla — queda flotando
en pantalla durante el resto del video (pasó con las etiquetas `mg·sinθ`/`mg·cosθ` en
el primer video). Antes de pasar de un método/beat al siguiente, repasa: ¿todo lo que
apareció con `Write`/`FadeIn`/`Create` en este bloque tiene un `FadeOut` correspondiente
o sigue siendo necesario en el resto de la escena?

### 4.4 `.next_to(mobject_ya_desplazado, DIRECCION)` hereda el desplazamiento

Si posicionas un texto con `.next_to(x, DOWN)` donde `x` ya está desplazado del centro
(por ejemplo un número que se movió con `.shift(LEFT * 1.2)`), el texto nuevo hereda
ese desplazamiento y puede salirse del frame en vez de quedar centrado. Cuando quieras
centrar un texto respecto a varios elementos, usa el grupo completo:
`resultado.next_to(VGroup(num_izq, num_der), DOWN, buff=0.6)`, no uno de los dos.

## 5. Especificaciones de publicación en TikTok (para el GUION.md)

- Resolución 1080×1920, 30fps, sin franjas negras.
- Duración 60-90s para contenido explicativo (ajustable según el formato que pida el
  usuario: gancho corto, explicativo medio, o serie multi-parte).
- Safe zones: nada importante en el 12% superior ni el 15% inferior del frame (ahí
  TikTok superpone usuario, descripción y botones de interacción).
- Subtítulos quemados recomendados — gran parte de la audiencia ve sin sonido.
- El gancho (primeros 1-2s) debe funcionar solo con el texto en pantalla, sin depender
  del audio.

## 6. Recursos incluidos en esta skill

- `assets/plantilla_escena.py` — esqueleto de escena con el formato vertical y los
  cuatro helpers de la sección 4 ya resueltos; copia y adapta al problema físico nuevo.
- `assets/GUION_template.md` — esqueleto del guion con las mismas secciones que el
  primer video de la serie.
- `scripts/contact_sheet.ps1` — script de PowerShell que renderiza en baja calidad,
  extrae un fotograma por segundo con ffmpeg y arma la cuadrícula de verificación
  visual descrita en la sección 2.1.

## 7. Ejemplo de referencia

`Español/extras/dinamica_friccion_tiktok/` contiene el primer video completo de la
serie (plano inclinado, fricción estática vs. cinética, 2ª ley de Newton) con su
GUION.md, su escena `.py` ya corregida, y el registro de qué bugs reales aparecieron y
cómo se solucionaron. Ante la duda sobre cómo estructurar un video nuevo, ese proyecto
es la referencia canónica — cópiale la forma, no necesariamente el contenido físico.
