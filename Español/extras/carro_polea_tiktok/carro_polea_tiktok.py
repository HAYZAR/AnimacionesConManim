"""
"La misma fuerza, la mitad de aceleracion" - video vertical para TikTok/Reels/Shorts.
Tercer video de la serie (ver Español/extras/dinamica_friccion_tiktok/ y
Español/extras/bascula_ascensor_tiktok/ para los anteriores).

Requiere Manim Community Edition:  pip install manim
Render de prueba:  manim -ql --format=mp4 carro_polea_tiktok.py CarroPoleaTikTok
Render final:      manim -qh --format=mp4 --fps 30 carro_polea_tiktok.py CarroPoleaTikTok

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
# g=10 m/s^2, igual que el video 2 (NO 9.8 como el video 1).
G = 10.0
M_CARRO = 1.0   # kg
M_PESA = 1.0    # kg (cada pesa pesa 10 N)


def a_de(n_pesas):
    """Aceleracion del sistema carro+pesas colgantes para n pesas colgando."""
    m_total = M_CARRO + n_pesas * M_PESA
    f_neta = n_pesas * M_PESA * G
    return f_neta / m_total


def cap_width(mobject, max_width=3.9):
    """Encoge (nunca agranda) un mobject para que quepa en el frame vertical angosto."""
    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)
    return mobject


def cap_size(mobject, max_width=3.9, max_height=0.45):
    """Como cap_width, pero tambien limita la altura: las formulas con \\dfrac
    (fracciones grandes) son angostas pero MUY altas, e invaden el area de la
    mesa/carro mas abajo si solo se limita el ancho."""
    factor = min(max_width / mobject.width, max_height / mobject.height, 1.0)
    if factor < 1.0:
        mobject.scale(factor)
    return mobject


# --- Paleta de color fija (no reasignar) --------------------------------
COLOR_FUERZA = YELLOW
COLOR_PESO = RED
COLOR_ACEL = ORANGE


class CarroPoleaTikTok(Scene):
    def construct(self):
        self.crear_escenario()
        self.hook()
        self.plantear_problema()
        self.caso_a_fuerza_directa()
        self.introducir_polea()
        self.caso_b_una_pesa()
        self.por_que_es_la_mitad()
        self.montaje_mas_pesas()
        self.reto_limite()
        self.estrategia()
        self.cierre()

    # ------------------------------------------------------------------
    # Escenario persistente: mesa + carro + polea + pesas + contador
    # ------------------------------------------------------------------
    def crear_escenario(self):
        self.mesa_y = -0.1
        mesa = Line(LEFT * 1.5, RIGHT * 1.2, color=WHITE, stroke_width=4).shift(UP * self.mesa_y)
        patas = VGroup(
            Line(LEFT * 1.3, LEFT * 1.3 + DOWN * 0.3, color=GREY_B, stroke_width=3),
            Line(RIGHT * 1.0, RIGHT * 1.0 + DOWN * 0.3, color=GREY_B, stroke_width=3),
        ).shift(UP * self.mesa_y)
        etiqueta_mesa = cap_width(Text("mesa sin fricción", font_size=16, color=GREY_B), max_width=1.8)
        etiqueta_mesa.next_to(mesa, DOWN, buff=0.05)
        self.mesa_grupo = VGroup(mesa, patas, etiqueta_mesa)

        self.punto_polea = RIGHT * 1.2 + UP * self.mesa_y
        polea = Circle(radius=0.15, color=WHITE, stroke_width=3, fill_color=GREY_D, fill_opacity=1)
        polea.move_to(self.punto_polea)
        soporte = Line(self.punto_polea, self.punto_polea + UP * 0.3, color=GREY_B, stroke_width=3)
        self.polea_grupo = VGroup(polea, soporte)

        self.carro = RoundedRectangle(
            width=0.6, height=0.4, corner_radius=0.06,
            color=WHITE, stroke_width=2, fill_color=BLUE_E, fill_opacity=0.9,
        )
        self.carro_x_inicial = -0.9
        self.carro.move_to(RIGHT * self.carro_x_inicial + UP * (self.mesa_y + 0.2 + 0.02))

        self.cuerda_horizontal = always_redraw(
            lambda: Line(
                self.carro.get_right(), self.punto_polea,
                color=GREY_A, stroke_width=2.5,
            )
        )

        self.pesas = VGroup()  # pesas colgantes (se llenan mas adelante)
        self.cuerda_vertical = always_redraw(lambda: self._cuerda_vertical_actual())

        self.a_tracker = ValueTracker(0.0)
        self.a_display = always_redraw(
            lambda: VGroup(
                MathTex("a \\approx", color=COLOR_ACEL),
                DecimalNumber(self.a_tracker.get_value(), num_decimal_places=2, color=COLOR_ACEL),
                MathTex("\\text{m/s}^2", color=COLOR_ACEL),
            ).arrange(RIGHT, buff=0.15).scale(1.1).to_edge(UP, buff=0.6)
        )

        self.escenario = VGroup(
            self.mesa_grupo, self.polea_grupo, self.carro,
            self.cuerda_horizontal, self.cuerda_vertical,
        )

    def _cuerda_vertical_actual(self):
        fin = self.pesas.get_top() if len(self.pesas) > 0 else self.punto_polea + DOWN * 1.2
        return Line(self.punto_polea, fin, color=GREY_A, stroke_width=2.5)

    def crear_pesa(self):
        return Square(side_length=0.35, color=WHITE, stroke_width=2, fill_color=RED_E, fill_opacity=0.9)

    def agregar_pesas(self, n_total, run_time=0.8):
        """Ajusta self.pesas para que tenga exactamente n_total pesas apiladas
        colgando bajo la polea, animando las que se agreguen."""
        nuevas = VGroup()
        y_tope = self.punto_polea[1] - 0.5
        for i in range(len(self.pesas), n_total):
            pesa = self.crear_pesa()
            pesa.move_to(self.punto_polea + RIGHT * 0.0)
            pesa.move_to([self.punto_polea[0], y_tope - i * 0.37, 0])
            nuevas.add(pesa)
        if len(nuevas) > 0:
            self.pesas.add(*nuevas)
            self.play(*[FadeIn(p, shift=DOWN * 0.2) for p in nuevas], run_time=run_time)

    def mover_carro_y_actualizar_a(self, nuevo_valor_a, distancia_carro=0.35, run_time=1.4):
        self.play(
            self.carro.animate.shift(RIGHT * distancia_carro),
            self.a_tracker.animate.set_value(nuevo_valor_a),
            run_time=run_time,
        )

    # ------------------------------------------------------------------
    # 0:00 - 0:07  Hook
    # ------------------------------------------------------------------
    def hook(self):
        hook_text = cap_width(Text(
            "Misma fuerza...\n¿distinta aceleración?",
            font_size=30, weight=BOLD, line_spacing=1.1,
        )).next_to(self.a_display, DOWN, buff=0.4)

        flecha_mano = Arrow(
            self.carro.get_left() + LEFT * 0.9, self.carro.get_left(),
            color=COLOR_FUERZA, buff=0.05, stroke_width=6,
        )
        etiqueta_f = MathTex("F=10\\,N", color=COLOR_FUERZA).scale(0.6)
        etiqueta_f.next_to(flecha_mano, UP, buff=0.1)

        self.play(FadeIn(VGroup(self.mesa_grupo, self.carro)), Write(hook_text), run_time=1.0)
        self.play(GrowArrow(flecha_mano), Write(etiqueta_f), run_time=0.6)
        self.add(self.a_display)
        self.play(self.a_tracker.animate.set_value(10.0), self.carro.animate.shift(RIGHT * 0.3), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(flecha_mano), FadeOut(etiqueta_f))
        self.play(self.a_tracker.animate.set_value(5.0), run_time=1.0)
        self.wait(2.2)
        self.play(FadeOut(hook_text))
        self.carro.move_to(RIGHT * self.carro_x_inicial + UP * (self.mesa_y + 0.2 + 0.02))
        self.a_tracker.set_value(0.0)
        self.wait(0.4)

    # ------------------------------------------------------------------
    # 0:07 - 0:15  Planteamiento de datos
    # ------------------------------------------------------------------
    def plantear_problema(self):
        datos = VGroup(
            MathTex(r"m_{\text{carro}} = 1\ \text{kg}"),
            MathTex(r"\text{cada pesa} = 10\ \text{N}"),
            MathTex(r"\text{polea ideal}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.75)
        cap_width(datos).next_to(self.a_display, DOWN, buff=0.5).to_edge(LEFT, buff=0.35)

        self.play(LaggedStart(*[Write(d) for d in datos], lag_ratio=0.3), run_time=1.4)
        self.wait(3.3)
        self.play(FadeOut(datos))
        self.wait(0.5)

    # ------------------------------------------------------------------
    # 0:15 - 0:24  Caso A: mano hala el carro directamente
    # ------------------------------------------------------------------
    def caso_a_fuerza_directa(self):
        texto = cap_width(Text("Caso A: una mano hala\ndirectamente el carro", font_size=22, line_spacing=1.1))
        texto.next_to(self.a_display, DOWN, buff=0.5)

        flecha_mano = Arrow(
            self.carro.get_left() + LEFT * 0.9, self.carro.get_left(),
            color=COLOR_FUERZA, buff=0.05, stroke_width=6,
        )
        etiqueta_f = MathTex("F=10\\,N", color=COLOR_FUERZA).scale(0.6)
        etiqueta_f.next_to(flecha_mano, UP, buff=0.1)

        formula = cap_size(MathTex(r"a = F / m_{\text{carro}} = 10/1 = 10.0\ \text{m/s}^2").scale(0.65))
        formula.next_to(texto, DOWN, buff=0.3)

        self.play(Write(texto), run_time=0.7)
        self.play(GrowArrow(flecha_mano), Write(etiqueta_f), run_time=0.6)
        self.wait(0.4)
        self.play(Write(formula), run_time=1.0)
        self.mover_carro_y_actualizar_a(10.0, distancia_carro=0.4)
        self.wait(3.0)
        self.play(FadeOut(texto), FadeOut(formula), FadeOut(flecha_mano), FadeOut(etiqueta_f))
        self.carro.move_to(RIGHT * self.carro_x_inicial + UP * (self.mesa_y + 0.2 + 0.02))
        self.a_tracker.set_value(0.0)
        self.wait(0.5)

    # ------------------------------------------------------------------
    # 0:24 - 0:34  Se reemplaza la mano por la polea + 1 pesa
    # ------------------------------------------------------------------
    def introducir_polea(self):
        texto = cap_width(Text(
            "La cuerda no se estira:\nel carro y la pesa siempre\ntienen la misma aceleración",
            font_size=22, line_spacing=1.15,
        ))
        texto.next_to(self.a_display, DOWN, buff=0.5)

        self.play(Write(texto), run_time=0.9)
        self.play(
            FadeIn(self.polea_grupo), FadeIn(self.cuerda_horizontal), FadeIn(self.cuerda_vertical),
            run_time=0.5,
        )
        self.agregar_pesas(1, run_time=0.8)
        self.wait(3.2)
        self.play(FadeOut(texto))
        self.wait(0.4)

    # ------------------------------------------------------------------
    # 0:34 - 0:46  Caso B: 1 pesa colgante -> a = 5.0
    # ------------------------------------------------------------------
    def caso_b_una_pesa(self):
        formula = cap_size(
            MathTex(r"a = F_{\text{neta}} / m_{\text{total}} = 10/(1{+}1) = 5.0\ \text{m/s}^2").scale(0.6)
        )
        formula.next_to(self.a_display, DOWN, buff=0.5)

        self.play(Write(formula), run_time=1.1)
        self.wait(0.5)
        self.mover_carro_y_actualizar_a(5.0, distancia_carro=0.3, run_time=1.8)
        self.wait(3.0)
        self.play(FadeOut(formula))
        self.wait(0.4)

    # ------------------------------------------------------------------
    # 0:46 - 0:52  ¿Por que es la mitad?
    # ------------------------------------------------------------------
    def por_que_es_la_mitad(self):
        texto = cap_width(Text(
            "¡Esos 10 N también tienen\nque acelerar a la pesa\nque los produce!",
            font_size=22, line_spacing=1.15, color=COLOR_PESO,
        ))
        texto.next_to(self.a_display, DOWN, buff=0.5)
        self.play(Write(texto), run_time=0.9)
        self.play(Indicate(self.pesas, color=COLOR_PESO), run_time=0.8)
        self.wait(3.0)
        self.play(FadeOut(texto))
        self.wait(0.4)

    # ------------------------------------------------------------------
    # 0:52 - 1:02  Montaje: 2 pesas, luego 3 pesas
    # ------------------------------------------------------------------
    def montaje_mas_pesas(self):
        texto = cap_width(Text("Cada pesa nueva empuja\nmás... pero también pesa más", font_size=20, line_spacing=1.1))
        texto.next_to(self.a_display, DOWN, buff=0.5)
        self.play(Write(texto), run_time=0.7)

        self.agregar_pesas(2, run_time=0.6)
        self.play(self.a_tracker.animate.set_value(a_de(2)), run_time=1.1)
        self.wait(1.0)

        self.agregar_pesas(3, run_time=0.6)
        self.play(self.a_tracker.animate.set_value(a_de(3)), run_time=1.1)
        self.wait(2.6)

        self.play(FadeOut(texto))
        self.play(FadeOut(self.escenario), FadeOut(self.pesas))
        self.wait(0.4)

    # ------------------------------------------------------------------
    # 1:02 - 1:12  Reto: el limite cuando n -> infinito
    # ------------------------------------------------------------------
    def reto_limite(self):
        reto_titulo = cap_width(Text("TU RETO 🧠", font_size=34, weight=BOLD, color=YELLOW))
        reto_titulo.next_to(self.a_display, DOWN, buff=0.6)
        reto_texto = cap_width(Text(
            "Si cuelgas MUCHÍSIMAS pesas,\n¿a qué valor se acerca\nla aceleración?",
            font_size=24, line_spacing=1.2,
        ))
        reto_texto.next_to(reto_titulo, DOWN, buff=0.5)
        pista = cap_size(
            MathTex(r"a = \dfrac{10n}{1+n}").scale(0.9).set_opacity(0.5), max_height=0.5,
        )
        pista.next_to(reto_texto, DOWN, buff=0.6)

        self.play(Write(reto_titulo), run_time=0.6)
        self.play(FadeIn(reto_texto, shift=UP * 0.2), run_time=0.8)
        self.wait(1.6)
        self.play(FadeIn(pista), run_time=0.6)
        self.wait(3.2)
        self.play(FadeOut(reto_titulo), FadeOut(reto_texto), FadeOut(pista))
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 1:12 - 1:20  Estrategia resumida
    # ------------------------------------------------------------------
    def estrategia(self):
        self.play(FadeOut(self.a_display))
        titulo = cap_width(Text("Un sistema conectado =\nuna sola masa total", font_size=28, weight=BOLD))
        titulo.to_edge(UP, buff=1.1)

        pasos = VGroup(
            Text("1. ¿Están unidos por\nuna cuerda ideal?", font_size=22, line_spacing=1.0),
            Text("2. Suma TODAS las masas\nconectadas", font_size=22, line_spacing=1.0),
            Text("3. Solo cuenta la fuerza\nexterna neta (no la tensión)", font_size=22, line_spacing=1.0),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        cap_width(pasos)
        pasos.next_to(titulo, DOWN, buff=0.6)

        flechas = VGroup(*[
            Arrow(pasos[i].get_bottom(), pasos[i + 1].get_top(), buff=0.1, stroke_width=3, color=YELLOW)
            for i in range(len(pasos) - 1)
        ])

        self.play(Write(titulo), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in pasos], lag_ratio=0.4), run_time=1.6)
        self.play(*[GrowArrow(f) for f in flechas], run_time=0.6)
        self.wait(3.0)

        self.play(FadeOut(titulo), FadeOut(pasos), FadeOut(flechas))
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 1:20 - 1:24  Cierre
    # ------------------------------------------------------------------
    def cierre(self):
        cierre = cap_width(Text(
            "Segunda ley de Newton — Parte 3\nSígueme para la Parte 4 👀",
            font_size=24,
        ))
        self.play(Write(cierre), run_time=1.0)
        self.wait(3.5)
