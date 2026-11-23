"""
Intro de marca reutilizable para toda la serie de Fisica en TikTok.

Recrea la pantalla de marca del canal: manzana cayendo (referencia a
Newton) -> flecha -> F=ma -> logo "H2B" con subrayado -> subtitulo con el
tema del video. Se agrega al PRINCIPIO de construct(), antes de hook().

Requiere la fuente "Dancing Script" (Google Fonts, gratis) instalada en
el sistema para el logo -- si no esta instalada, Manim usa una fuente de
reemplazo automaticamente (se ve distinto pero no falla el render). En
Windows se instala haciendo doble clic en el archivo .ttf descargado de
fonts.google.com/specimen/Dancing+Script y eligiendo "Instalar".

Uso, en cualquier escena de la serie:

    import sys
    sys.path.insert(0, "<ruta a esta carpeta assets>")
    from intro_marca import reproducir_intro

    class MiEscena(Scene):
        def construct(self):
            reproducir_intro(self, "Fricción")
            self.hook()
            ...

No requiere narracion.json: es un "beat" sin texto hablado (un sting de
marca de ~4s), asi que generar_audio.py lo salta automaticamente (no
tiene entrada en narracion.json) y la narracion empieza a hablar recien
cuando arranca self.hook().
"""
from manim import *

COLOR_FONDO_INTRO = "#0B0F1A"
COLOR_CREMA = "#F2EAD3"
COLOR_NARANJA = "#E8A33D"
COLOR_SUBTITULO = "#6B7A99"
COLOR_MANZANA = "#D1352B"

FUENTE_LOGO = "Dancing Script"


def _cap_width(mobject, max_width=3.9):
    """Encoge (nunca agranda) un mobject para que quepa en el frame vertical
    angosto -- version local, igual que la de cada escena de la serie."""
    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)
    return mobject


def _crear_fondo_con_grid():
    fondo = Rectangle(
        width=config.frame_width + 0.5, height=config.frame_height + 0.5,
        fill_color=COLOR_FONDO_INTRO, fill_opacity=1, stroke_width=0,
    )
    lineas = VGroup()
    paso = 0.9
    x = -config.frame_width / 2
    while x <= config.frame_width / 2:
        lineas.add(Line(
            [x, -config.frame_height / 2, 0], [x, config.frame_height / 2, 0],
            color=WHITE, stroke_width=0.5, stroke_opacity=0.06,
        ))
        x += paso
    y = -config.frame_height / 2
    while y <= config.frame_height / 2:
        lineas.add(Line(
            [-config.frame_width / 2, y, 0], [config.frame_width / 2, y, 0],
            color=WHITE, stroke_width=0.5, stroke_opacity=0.06,
        ))
        y += paso
    return VGroup(fondo, lineas)


def _crear_manzana():
    cuerpo = Ellipse(
        width=0.95, height=0.85, color=WHITE, fill_color=COLOR_MANZANA,
        fill_opacity=1, stroke_width=4,
    )
    hoja = Ellipse(width=0.16, height=0.32, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=0)
    hoja.rotate(45 * DEGREES).move_to(cuerpo.get_top() + UP * 0.05 + LEFT * 0.15)
    tallo = Line(
        cuerpo.get_top(), cuerpo.get_top() + UP * 0.22 + RIGHT * 0.06,
        color=WHITE, stroke_width=4,
    )
    return VGroup(cuerpo, hoja, tallo)


def reproducir_intro(scene, tema):
    """Reproduce la intro de marca completa y la limpia de la escena al
    terminar. `tema` es el texto que aparece antes de "· Física y
    aplicaciones" (p.ej. "Fricción", "Impulso y momentum")."""
    fondo = _crear_fondo_con_grid()
    scene.add(fondo)

    manzana = _crear_manzana().shift(UP * 2.2)
    lineas_movimiento = VGroup(*[
        Line(UP * (3.3 + i * 0.15), UP * (2.9 + i * 0.15), color=WHITE, stroke_width=2)
        .shift(RIGHT * (i - 1) * 0.22)
        for i in range(3)
    ])

    scene.play(FadeIn(manzana, shift=DOWN * 0.3), FadeIn(lineas_movimiento), run_time=0.5)
    scene.play(
        manzana.animate.shift(DOWN * 0.9), FadeOut(lineas_movimiento),
        run_time=0.4, rate_func=rate_functions.ease_in_quad,
    )

    flecha = Arrow(
        manzana.get_bottom() + DOWN * 0.1, manzana.get_bottom() + DOWN * 0.55,
        color=COLOR_NARANJA, buff=0, stroke_width=6,
    )
    scene.play(GrowArrow(flecha), run_time=0.3)

    formula = MathTex("F", "=", "ma", color=COLOR_CREMA).scale(1.6)
    formula.next_to(flecha, DOWN, buff=0.35)
    scene.play(Write(formula), run_time=0.6)

    logo_h = Text("H", font=FUENTE_LOGO, weight=BOLD, color=COLOR_CREMA).scale(1.6)
    logo_b = Text("B", font=FUENTE_LOGO, weight=BOLD, color=COLOR_CREMA).scale(1.6)
    letras = VGroup(logo_h, logo_b).arrange(RIGHT, buff=0.75, aligned_edge=DOWN)
    exponente = Text("2", font=FUENTE_LOGO, weight=BOLD, color=COLOR_NARANJA).scale(0.8)
    exponente.move_to(logo_h.get_corner(UR) + RIGHT * 0.05 + UP * 0.05)
    logo = VGroup(letras, exponente).next_to(formula, DOWN, buff=0.35)

    subrayado = ArcBetweenPoints(
        logo.get_corner(DL) + LEFT * 0.15, logo.get_corner(DR) + RIGHT * 0.15,
        angle=-0.3, color=COLOR_NARANJA, stroke_width=4,
    ).shift(DOWN * 0.12)

    scene.play(FadeIn(logo, scale=1.1), run_time=0.4)
    scene.play(Create(subrayado), run_time=0.35)

    subtitulo = _cap_width(
        Text(f"{tema} · Física y aplicaciones", font_size=22, color=COLOR_SUBTITULO)
    )
    subtitulo.next_to(subrayado, DOWN, buff=0.55)
    scene.play(FadeIn(subtitulo, shift=UP * 0.15), run_time=0.4)

    scene.wait(0.8)

    scene.play(
        FadeOut(fondo), FadeOut(manzana), FadeOut(flecha), FadeOut(formula),
        FadeOut(logo), FadeOut(subrayado), FadeOut(subtitulo),
        run_time=0.5,
    )
