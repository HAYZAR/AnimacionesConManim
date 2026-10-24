"""
Plantilla de escena para un video vertical de fisica (TikTok/Reels/Shorts).

Copia este archivo a Español/extras/<nombre_del_video>/<nombre_del_video>.py y
adapta las secciones marcadas con TODO. Los helpers de las secciones 1-2 ya
resuelven los bugs mas comunes descritos en SKILL.md (seccion 4) -- no los
borres ni los reescribas por metodo, son de uso compartido en toda la escena.

Requiere Manim Community Edition:  pip install manim
Render de prueba:   manim -ql --format=mp4 <archivo>.py <NombreEscena>
Render final:        manim -qh --format=mp4 --fps 30 <archivo>.py <NombreEscena>
"""

from manim import *

# --- 1. Formato vertical real (9:16) ------------------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 8.0
config.frame_width = config.frame_height * (config.pixel_width / config.pixel_height)

# --- Datos fisicos del problema (deben coincidir con el GUION.md) -------
# TODO: reemplaza por las variables reales del problema y verifica a mano
# (o con un print()) que los numeros que vas a mostrar en pantalla sean
# correctos ANTES de animarlos.
M = 1.0          # kg
G = 9.8          # m/s^2

# --- Paleta de color fija (no reasignar un color a otro concepto) -------
COLOR_PESO = RED
COLOR_NORMAL = BLUE
COLOR_FRICCION = GREEN
COLOR_NETA = ORANGE


# --- 2. Helpers anti-bugs (ver SKILL.md seccion 4) -----------------------
def cap_width(mobject, max_width=3.9):
    """Encoge (nunca agranda) un mobject para que quepa en el frame vertical
    angosto (~4.5 unidades). Envuelve con esto cualquier Text/MathTex que no
    sea una etiqueta pequena junto a un vector."""
    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)
    return mobject


def dir_plano(theta_deg):
    """Vector unitario a lo largo de una superficie inclinada, apuntando
    cuesta ARRIBA. Reutiliza esto en toda la escena en vez de recalcular
    sin/cos por separado en cada metodo -- asi el signo nunca queda
    inconsistente entre, por ejemplo, el dibujo de la rampa y los vectores
    del diagrama de cuerpo libre."""
    theta = np.deg2rad(theta_deg)
    return np.array([np.cos(theta), np.sin(theta), 0.0])


def dir_normal(theta_deg):
    """Vector unitario normal a la superficie, hacia AFUERA de ella."""
    theta = np.deg2rad(theta_deg)
    return np.array([-np.sin(theta), np.cos(theta), 0.0])


# --- 3. Escena -------------------------------------------------------------
class NombreEscena(Scene):
    def construct(self):
        # TODO: una llamada por "beat" del guion, en el mismo orden que la
        # tabla de timeline del GUION.md. Cada metodo debe dejar la escena
        # limpia al terminar (todo Write/FadeIn con su FadeOut) salvo lo que
        # explicitamente continua a la siguiente escena.
        self.hook()
        # self.plantear_problema()
        # ...
        # self.conclusion()
        # self.reto_final()

    # ------------------------------------------------------------------
    # 0:00 - 0:06  Hook
    # ------------------------------------------------------------------
    def hook(self):
        # TODO: el gancho debe entenderse solo con el texto en pantalla,
        # sin depender del audio (regla de oro de TikTok, ver SKILL.md 5).
        hook_text = cap_width(Text(
            "TODO: pregunta o afirmacion que enganche\nen la primera linea",
            font_size=34, weight=BOLD,
        )).to_edge(UP, buff=1.0)

        self.play(Write(hook_text), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(hook_text))

    # ------------------------------------------------------------------
    # TODO: agrega un metodo por cada fila del timeline del GUION.md,
    # copiando el patron de dinamica_friccion_tiktok.py cuando el problema
    # se parezca (DCL, comparacion de fuerzas, 2da ley, estrategia resumida,
    # reto final) -- ese archivo es la referencia canonica de esta skill.
    # ------------------------------------------------------------------
