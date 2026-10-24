"""
"La bascula que no dice tu peso real" - video vertical para TikTok/Reels/Shorts.
Segundo video de la serie (ver Español/extras/dinamica_friccion_tiktok/ para el primero).

Requiere Manim Community Edition:  pip install manim
Render de prueba:  manim -ql --format=mp4 bascula_ascensor_tiktok.py BasculaAscensorTikTok
Render final:      manim -qh --format=mp4 --fps 30 bascula_ascensor_tiktok.py BasculaAscensorTikTok

El guion completo (narracion VO, timings, specs de TikTok) esta en GUION.md
(misma carpeta).
"""

from manim import *

# --- Formato vertical real (9:16) --------------------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 8.0
config.frame_width = config.frame_height * (config.pixel_width / config.pixel_height)

# --- Datos fisicos del problema (deben coincidir con GUION.md) ---------
# OJO: este video usa g=10 m/s^2 (el del taller), NO 9.8 como el video 1.
M = 60.0   # kg
G = 10.0   # m/s^2

# --- Paleta de color fija (no reasignar) --------------------------------
COLOR_PESO = RED
COLOR_NORMAL = BLUE
COLOR_ACEL = ORANGE


def n_de(a):
    """Lectura de la bascula (normal) para una aceleracion 'a' del ascensor
    (positiva hacia arriba)."""
    return M * (G + a)


def cap_width(mobject, max_width=3.9):
    """Encoge (nunca agranda) un mobject para que quepa en el frame vertical angosto."""
    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)
    return mobject


class BasculaAscensorTikTok(Scene):
    def construct(self):
        self.crear_escenario()
        self.hook()
        self.plantear_problema()
        self.dcl()
        self.segunda_ley()
        self.reposo_y_velocidad_constante()
        self.sube_acelerando()
        self.baja_frenando_comparacion()
        self.baja_acelerando()
        self.caida_libre()
        self.resumen_formula()
        self.reto_final()

    # ------------------------------------------------------------------
    # Escenario persistente: cabina + bascula + persona + vectores + N grande
    # ------------------------------------------------------------------
    def crear_escenario(self):
        cabina_ancho, cabina_alto = 2.2, 4.2
        self.cabina = Rectangle(
            width=cabina_ancho, height=cabina_alto,
            color=WHITE, stroke_width=3, fill_color=GREY_E, fill_opacity=0.12,
        ).to_edge(DOWN, buff=0.5)
        cable = Line(
            self.cabina.get_top(), self.cabina.get_top() + UP * 0.4,
            color=GREY_B, stroke_width=3,
        )
        etiqueta_ascensor = Text("el ascensor", font_size=18, color=GREY_B)
        etiqueta_ascensor.next_to(self.cabina, DOWN, buff=0.15)

        bascula = Rectangle(
            width=1.0, height=0.2, color=WHITE, stroke_width=2,
            fill_color=GREY_B, fill_opacity=1,
        )
        bascula.move_to(self.cabina.get_bottom() + UP * (0.2 / 2 + 0.08))
        self.bascula = bascula

        torso = RoundedRectangle(
            width=0.46, height=0.85, corner_radius=0.1,
            color=WHITE, stroke_width=2, fill_color=BLUE_E, fill_opacity=0.9,
        )
        torso.move_to(bascula.get_top() + UP * (0.85 / 2))
        cabeza = Circle(radius=0.16, color=WHITE, stroke_width=2, fill_color=BLUE_E, fill_opacity=0.9)
        cabeza.move_to(torso.get_top() + UP * (0.16 + 0.02))
        self.persona = VGroup(torso, cabeza)
        self.origen_vectores = torso.get_center()

        self.n_tracker = ValueTracker(n_de(0))  # arranca en reposo: N = mg

        self.v_peso = Arrow(
            self.origen_vectores, self.origen_vectores + DOWN * 0.9,
            color=COLOR_PESO, buff=0, stroke_width=6,
        )
        self.v_normal = Arrow(
            self.origen_vectores, self.origen_vectores + UP * 0.9,
            color=COLOR_NORMAL, buff=0, stroke_width=6,
        )
        etiqueta_peso = MathTex("mg", color=COLOR_PESO).scale(0.6).next_to(self.v_peso, LEFT, buff=0.2)
        etiqueta_normal = MathTex("N", color=COLOR_NORMAL).scale(0.6).next_to(self.v_normal, RIGHT, buff=0.2)
        self.etiquetas_vectores = VGroup(etiqueta_peso, etiqueta_normal)

        self.n_display = always_redraw(
            lambda: VGroup(
                DecimalNumber(self.n_tracker.get_value(), unit="\\,N", color=COLOR_NORMAL, num_decimal_places=0)
                .scale(1.3)
            ).next_to(self.cabina, UP, buff=0.5)
        )

        self.escenario = VGroup(
            self.cabina, cable, etiqueta_ascensor, bascula, self.persona,
            self.v_peso, self.v_normal, self.etiquetas_vectores,
        )

        # Flecha de aceleracion del ascensor (aparece/cambia segun el caso).
        self.v_acel = None
        self.etiqueta_acel = None

    def actualizar_normal(self, nuevo_valor, run_time=1.4):
        """Anima el brazo N (largo proporcional al valor) y el numero grande
        hasta 'nuevo_valor', reemplazando la flecha vieja por una nueva."""
        largo_nuevo = 0.9 * max(nuevo_valor, 1.0) / n_de(0)
        nueva_flecha = Arrow(
            self.origen_vectores, self.origen_vectores + UP * largo_nuevo,
            color=COLOR_NORMAL, buff=0, stroke_width=6,
        )
        self.play(
            Transform(self.v_normal, nueva_flecha),
            self.n_tracker.animate.set_value(nuevo_valor),
            run_time=run_time,
        )

    def mostrar_flecha_aceleracion(self, valor_a, etiqueta_tex, direccion_arriba, run_time=0.6):
        """Crea o reorienta la flecha naranja de aceleracion del ascensor,
        a la derecha de la cabina."""
        punto_base = self.cabina.get_right() + RIGHT * 0.3
        vector = UP * 0.7 if direccion_arriba else DOWN * 0.7
        nueva = Arrow(punto_base, punto_base + vector, color=COLOR_ACEL, buff=0, stroke_width=6)
        nueva_etiqueta = cap_width(MathTex(etiqueta_tex, color=COLOR_ACEL).scale(0.5), max_width=0.95)
        lado = DOWN if direccion_arriba else UP
        nueva_etiqueta.next_to(nueva, lado, buff=0.1)

        if self.v_acel is None:
            self.v_acel = nueva
            self.etiqueta_acel = nueva_etiqueta
            self.play(GrowArrow(self.v_acel), Write(self.etiqueta_acel), run_time=run_time)
        else:
            self.play(
                Transform(self.v_acel, nueva),
                Transform(self.etiqueta_acel, nueva_etiqueta),
                run_time=run_time,
            )

    # ------------------------------------------------------------------
    # 0:00 - 0:06  Hook
    # ------------------------------------------------------------------
    def hook(self):
        hook_text = cap_width(Text(
            "¿Sientes que pesas más\nen el ascensor?",
            font_size=32, weight=BOLD,
        )).to_edge(UP, buff=0.9)

        self.play(FadeIn(self.escenario), Write(hook_text), run_time=1.0)
        self.add(self.n_display)
        self.play(Wiggle(self.persona, scale_value=1.05, rotation_angle=0.01 * TAU), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(hook_text))

    # ------------------------------------------------------------------
    # 0:06 - 0:14  Planteamiento de datos
    # ------------------------------------------------------------------
    def plantear_problema(self):
        datos = VGroup(
            MathTex(r"m = 60\ \text{kg}"),
            MathTex(r"g = 10\ \text{m/s}^2"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.9)
        cap_width(datos).to_edge(UP, buff=1.0)

        flecha = Arrow(
            datos.get_bottom() + DOWN * 0.1, self.persona.get_top(),
            color=YELLOW, buff=0.1, stroke_width=3,
        )
        self.play(LaggedStart(*[Write(d) for d in datos], lag_ratio=0.3), run_time=1.3)
        self.play(GrowArrow(flecha), run_time=0.6)
        self.wait(2.6)
        self.play(FadeOut(flecha), FadeOut(datos))
        self.wait(0.6)

    # ------------------------------------------------------------------
    # 0:14 - 0:22  Diagrama de cuerpo libre
    # ------------------------------------------------------------------
    def dcl(self):
        leyenda = VGroup(
            Dot(color=COLOR_PESO).scale(0.6), Text("Peso real (constante)", font_size=20, color=COLOR_PESO),
            Dot(color=COLOR_NORMAL).scale(0.6), Text("Normal (lo que marca la báscula)", font_size=20, color=COLOR_NORMAL),
        ).arrange_in_grid(rows=2, cols=2, buff=0.2, col_alignments=["r", "l"])
        cap_width(leyenda).to_edge(UP, buff=1.0)

        self.play(Write(leyenda), run_time=0.9)
        self.play(GrowArrow(self.v_peso), Write(self.etiquetas_vectores[0]), run_time=0.6)
        self.wait(0.2)
        self.play(GrowArrow(self.v_normal), Write(self.etiquetas_vectores[1]), run_time=0.6)
        self.wait(1.6)
        self.play(FadeOut(leyenda))
        self.wait(2.0)

    # ------------------------------------------------------------------
    # 0:22 - 0:30  Segunda ley -> N = m(g+a)
    # ------------------------------------------------------------------
    def segunda_ley(self):
        ley_general = cap_width(MathTex(r"\sum F = ma").scale(0.9)).to_edge(UP, buff=1.0)
        ley_persona = cap_width(MathTex(r"N - mg = ma").scale(0.85)).to_edge(UP, buff=1.0)
        formula_final = cap_width(MathTex(r"N = m(g + a)").scale(0.9)).to_edge(UP, buff=1.0)

        self.play(Write(ley_general), run_time=0.7)
        self.wait(0.4)
        self.play(FadeOut(ley_general), FadeIn(ley_persona), run_time=0.7)
        self.wait(0.6)
        self.play(FadeOut(ley_persona), FadeIn(formula_final), run_time=0.7)
        self.wait(2.2)
        self.play(FadeOut(formula_final))
        self.wait(0.5)

    # ------------------------------------------------------------------
    # 0:30 - 0:38  Reposo y velocidad constante dan la misma lectura
    # ------------------------------------------------------------------
    def reposo_y_velocidad_constante(self):
        texto = cap_width(Text(
            "Reposo = velocidad constante\n(mientras a = 0)",
            font_size=24, line_spacing=1.1,
        )).to_edge(UP, buff=1.0)
        self.play(Write(texto), run_time=0.8)
        self.play(Indicate(self.n_display, color=COLOR_NORMAL), run_time=0.8)
        self.wait(2.8)
        self.play(FadeOut(texto))
        self.wait(0.5)

    # ------------------------------------------------------------------
    # 0:38 - 0:50  Sube acelerando (a = +2)
    # ------------------------------------------------------------------
    def sube_acelerando(self):
        texto = cap_width(Text("Sube acelerando: te sientes\nmás pesado", font_size=24, line_spacing=1.1))
        texto.to_edge(UP, buff=1.0)
        self.play(Write(texto), run_time=0.7)
        self.mostrar_flecha_aceleracion(2, "a = +2\\,\\text{m/s}^2", direccion_arriba=True)
        self.actualizar_normal(n_de(2))
        self.play(Flash(self.n_display.get_center(), color=COLOR_ACEL), run_time=0.6)
        self.wait(2.6)
        self.play(FadeOut(texto))
        self.wait(0.4)

    # ------------------------------------------------------------------
    # 0:50 - 0:58  Baja frenando: misma cuenta que "sube acelerando"
    # ------------------------------------------------------------------
    def baja_frenando_comparacion(self):
        texto = cap_width(Text(
            "Baja frenando: la aceleración\ntambién apunta hacia arriba",
            font_size=22, line_spacing=1.1,
        )).to_edge(UP, buff=1.0)
        igual = cap_width(Text("= mismos 720 N", font_size=24, color=COLOR_NORMAL, weight=BOLD))
        igual.next_to(texto, DOWN, buff=0.4)

        self.play(Write(texto), run_time=0.8)
        self.play(Indicate(self.v_acel, color=COLOR_ACEL), run_time=0.6)
        self.play(Write(igual), run_time=0.6)
        self.wait(2.6)
        self.play(FadeOut(texto), FadeOut(igual))
        self.wait(0.4)

    # ------------------------------------------------------------------
    # 0:58 - 1:06  Baja acelerando (a = -2)
    # ------------------------------------------------------------------
    def baja_acelerando(self):
        texto = cap_width(Text("Baja acelerando: te sientes\nmás liviano", font_size=24, line_spacing=1.1))
        texto.to_edge(UP, buff=1.0)
        self.play(Write(texto), run_time=0.7)
        self.mostrar_flecha_aceleracion(-2, "a = -2\\,\\text{m/s}^2", direccion_arriba=False)
        self.actualizar_normal(n_de(-2))
        self.wait(2.6)
        self.play(FadeOut(texto))
        self.wait(0.4)

    # ------------------------------------------------------------------
    # 1:06 - 1:18  Caida libre: N = 0 (climax)
    # ------------------------------------------------------------------
    def caida_libre(self):
        texto = cap_width(Text("Caída libre: la aceleración\nes exactamente g", font_size=24, line_spacing=1.1))
        texto.to_edge(UP, buff=1.0)
        self.play(Write(texto), run_time=0.7)
        self.mostrar_flecha_aceleracion(-G, "a = -g", direccion_arriba=False, run_time=0.8)
        self.actualizar_normal(0.0, run_time=1.8)
        self.wait(0.3)

        ingravidez = cap_width(Text("¡INGRAVIDEZ!", font_size=40, weight=BOLD, color=COLOR_NORMAL))
        ingravidez.next_to(self.n_display, UP, buff=0.35)
        self.play(Write(ingravidez), Flash(self.persona.get_center(), color=COLOR_NORMAL, flash_radius=0.6), run_time=0.9)
        self.wait(3.2)

        self.play(
            FadeOut(texto), FadeOut(ingravidez), FadeOut(self.escenario),
            FadeOut(self.v_acel), FadeOut(self.etiqueta_acel), FadeOut(self.n_display),
        )
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 1:18 - 1:28  Resumen: N = m(g+a) en una recta numerica
    # ------------------------------------------------------------------
    def resumen_formula(self):
        titulo = cap_width(Text("Un solo modelo,\ntodos los casos", font_size=28, weight=BOLD))
        titulo.to_edge(UP, buff=1.1)
        formula = cap_width(MathTex(r"N = m(g + a)").scale(1.0))
        formula.next_to(titulo, DOWN, buff=0.5)

        recta = NumberLine(
            x_range=[-G, G, G / 2], length=2.8, color=GREY_B,
            include_numbers=False, include_tip=True,
        ).next_to(formula, DOWN, buff=0.6)
        etiqueta_izq = cap_width(
            Text("a = -g\n(caída libre)", font_size=16, color=COLOR_NORMAL, line_spacing=1.0),
            max_width=1.3,
        )
        etiqueta_izq.next_to(recta.get_left(), DOWN, buff=0.2).shift(RIGHT * 0.35)
        etiqueta_der = cap_width(
            Text("a = +g\n(el doble de N)", font_size=16, color=COLOR_NORMAL, line_spacing=1.0),
            max_width=1.3,
        )
        etiqueta_der.next_to(recta.get_right(), DOWN, buff=0.2).shift(LEFT * 0.35)
        marcador = Dot(recta.n2p(0), color=COLOR_ACEL)

        self.play(Write(titulo), Write(formula), run_time=1.0)
        self.play(Create(recta), FadeIn(etiqueta_izq), FadeIn(etiqueta_der), run_time=0.8)
        self.play(FadeIn(marcador), run_time=0.4)
        self.play(marcador.animate.move_to(recta.n2p(-G)), run_time=1.0)
        self.play(marcador.animate.move_to(recta.n2p(G)), run_time=1.4)
        self.play(marcador.animate.move_to(recta.n2p(0)), run_time=1.0)
        self.wait(2.4)

        self.play(
            FadeOut(titulo), FadeOut(formula), FadeOut(recta),
            FadeOut(etiqueta_izq), FadeOut(etiqueta_der), FadeOut(marcador),
        )
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 1:28 - 1:33  Reto final + cierre
    # ------------------------------------------------------------------
    def reto_final(self):
        reto_titulo = cap_width(Text("TU RETO 🧠", font_size=36, weight=BOLD, color=YELLOW)).to_edge(UP, buff=1.3)
        reto_texto = cap_width(Text(
            "¿Qué aceleración del\nascensor haría que la báscula\nmarcara el DOBLE de tu peso?",
            font_size=24, line_spacing=1.2,
        )).next_to(reto_titulo, DOWN, buff=0.6)
        pista = cap_width(MathTex(r"N = 2mg").scale(0.9).set_opacity(0.5))
        pista.next_to(reto_texto, DOWN, buff=0.7)

        self.play(Write(reto_titulo), run_time=0.6)
        self.play(FadeIn(reto_texto, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
        self.play(FadeIn(pista), run_time=0.6)
        self.wait(2.4)

        cierre = cap_width(Text(
            "Segunda ley de Newton — Parte 2\nSígueme para la Parte 3 👀",
            font_size=22,
        ))
        cierre.next_to(pista, DOWN, buff=0.7)
        self.play(Write(cierre), run_time=1.0)
        self.wait(3.5)
