"""
"No evitas el golpe. Lo estiras." - video vertical para TikTok/Reels/Shorts.
Sexta entrega de la serie (Impulso y cantidad de movimiento).

Requiere Manim Community Edition:

    pip install manim

Render vertical 9:16 recomendado:

    manim -pqh --format=mp4 impulso_momentum_tiktok.py ImpulsoMomentumTikTok

El guion completo, la narracion en voz en off y las especificaciones de
publicacion para TikTok estan en GUION.md (misma carpeta).
"""

from manim import *

# --- Formato vertical real (9:16) --------------------------------------
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 8.0
config.frame_width = config.frame_height * (config.pixel_width / config.pixel_height)

# --- Datos fisicos del problema (deben coincidir con GUION.md) ---------
M = 80.0          # kg
V = 20.0          # m/s (72 km/h)
DELTA_P = M * V    # 1600 kg*m/s, fijo

DT_VOLANTE = 0.02  # s
F_VOLANTE = DELTA_P / DT_VOLANTE   # 80 000 N

DT_BOLSA = 0.2     # s
F_BOLSA = DELTA_P / DT_BOLSA         # 8 000 N

# --- Paleta de color fija -------------------------------------------------
COLOR_MOMENTUM = ORANGE
COLOR_FUERZA = RED
COLOR_TIEMPO = BLUE
COLOR_AUX = GREEN
COLOR_CAJA = "#C98F4B"

COLOR_FASE_DATOS = BLUE_C
COLOR_FASE_FORMULA = GREEN_C
COLOR_FASE_DESARROLLO = PURPLE_B
COLOR_FASE_RESULTADO = ORANGE

MAX_BAR_HEIGHT = 1.8


def cap_width(mobject, max_width=3.9):
    """Encoge (nunca agranda) un mobject para que quepa en el frame vertical angosto."""
    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)
    return mobject


def altura_barra(valor, valor_max):
    """Mapea un valor fisico a una altura visual (manim units), normalizada
    contra el valor maximo del par que se esta comparando."""
    return max(0.05, (valor / valor_max) * MAX_BAR_HEIGHT)


class ImpulsoMomentumTikTok(Scene):
    def construct(self):
        self.hook()
        self.plantear_problema()
        self.concepto_momentum()
        self.concepto_impulso()
        self.comparar_volante_bolsa()
        self.la_trampa()
        self.analogia()
        self.estrategia()
        self.reto_final()
        self.cierre()

    # ------------------------------------------------------------------
    # Helpers compartidos
    # ------------------------------------------------------------------
    def crear_auto(self):
        cuerpo = RoundedRectangle(
            width=1.4, height=0.5, corner_radius=0.12,
            stroke_color=WHITE, stroke_width=3, fill_color=BLUE_E, fill_opacity=0.9,
        )
        rueda_1 = Circle(radius=0.14, color=BLACK, fill_color=GREY_E, fill_opacity=1, stroke_width=2)
        rueda_1.move_to(cuerpo.get_corner(DL) + RIGHT * 0.32 + DOWN * 0.03)
        rueda_2 = Circle(radius=0.14, color=BLACK, fill_color=GREY_E, fill_opacity=1, stroke_width=2)
        rueda_2.move_to(cuerpo.get_corner(DR) + LEFT * 0.32 + DOWN * 0.03)
        return VGroup(cuerpo, rueda_1, rueda_2)

    def mostrar_fase(self, texto, color, run_time=0.4):
        """Etiqueta de fase fija en la esquina superior izquierda (Datos /
        Formula / Desarrollo / Resultado), igual que en el video 5."""
        nuevo_texto = Text(texto, font_size=16, weight=BOLD, color=color)
        fondo = SurroundingRectangle(nuevo_texto, color=color, buff=0.12)
        nueva_fase = VGroup(fondo, nuevo_texto).to_corner(UL, buff=0.35)

        animaciones = [FadeIn(nueva_fase, shift=RIGHT * 0.15)]
        if hasattr(self, "fase_actual"):
            animaciones.append(FadeOut(self.fase_actual, shift=RIGHT * 0.15))
        self.play(*animaciones, run_time=run_time)
        self.fase_actual = nueva_fase

    # ------------------------------------------------------------------
    # 0:00 - 0:08  Hook
    # ------------------------------------------------------------------
    def hook(self):
        auto = self.crear_auto().to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        pared = Line(UP * 0.9, DOWN * 0.9, color=GREY_B, stroke_width=10)
        pared.to_edge(RIGHT, buff=0.7).shift(DOWN * 0.3)

        hook_text = cap_width(Text(
            "¿Por qué una bolsa de aire\nte golpea con 10 VECES\nmenos fuerza, si chocas\nigual de fuerte? 🤯",
            font_size=27, weight=BOLD, line_spacing=1.1,
        )).to_edge(UP, buff=0.9)

        self.play(
            FadeIn(auto, scale=1.1, rate_func=rate_functions.ease_out_back),
            FadeIn(pared),
            run_time=0.6,
        )
        self.play(FadeIn(hook_text, scale=1.1, rate_func=rate_functions.ease_out_back), run_time=0.8)
        self.play(auto.animate.next_to(pared, LEFT, buff=0.05), run_time=1.0, rate_func=rate_functions.ease_in_quad)
        self.play(Wiggle(auto, scale_value=1.08, rotation_angle=0.02 * TAU), run_time=0.6)
        self.wait(1.3)

        self.play(FadeOut(hook_text))
        self.auto = auto
        self.pared = pared

    # ------------------------------------------------------------------
    # 0:08 - 0:16  Planteamiento de datos
    # ------------------------------------------------------------------
    def plantear_problema(self):
        self.play(FadeOut(self.pared), self.auto.animate.scale(0.75).to_edge(DOWN, buff=1.6))
        self.mostrar_fase("DATOS", COLOR_FASE_DATOS)

        datos = VGroup(
            MathTex(r"m = 80\ \text{kg}"),
            MathTex(r"v = 20\ \text{m/s}"),
            MathTex(r"\text{debe quedar en reposo}").scale(0.8),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        cap_width(datos).to_edge(UP, buff=1.2)

        self.play(LaggedStart(*[Write(d) for d in datos], lag_ratio=0.3), run_time=1.6)
        self.wait(3.5)

        self.play(FadeOut(datos), FadeOut(self.auto))

    # ------------------------------------------------------------------
    # 0:16 - 0:24  Concepto: momentum
    # ------------------------------------------------------------------
    def concepto_momentum(self):
        self.mostrar_fase("FÓRMULA", COLOR_FASE_FORMULA)

        frase = cap_width(Text(
            "Todo lo que se mueve tiene\ncantidad de movimiento",
            font_size=28, weight=BOLD, line_spacing=1.1,
        )).to_edge(UP, buff=1.1)
        self.play(Write(frase), run_time=1.0)
        self.wait(1.0)

        formula_p = cap_width(MathTex(r"p = m \cdot v", color=COLOR_MOMENTUM).scale(1.0))
        formula_p.next_to(frase, DOWN, buff=0.7)
        self.play(Write(formula_p), run_time=0.8)
        self.wait(1.8)

        self.play(FadeOut(frase), FadeOut(formula_p))
        self.wait(1.0)

    # ------------------------------------------------------------------
    # 0:24 - 0:34  Concepto: impulso (teorema impulso-momentum)
    # ------------------------------------------------------------------
    def concepto_impulso(self):
        formula_impulso = cap_width(MathTex(
            r"\Delta p = F \cdot \Delta t", color=COLOR_MOMENTUM,
        ).scale(0.95)).to_edge(UP, buff=1.1)
        self.play(Write(formula_impulso), run_time=0.9)
        self.wait(1.2)

        calculo = cap_width(MathTex(
            r"\Delta p = 80 \times 20 = 1600\ \text{kg·m/s}", color=COLOR_MOMENTUM,
        ).scale(0.65))
        calculo.next_to(formula_impulso, DOWN, buff=0.6)
        self.play(Write(calculo), run_time=1.0)
        self.wait(0.6)

        fijo = cap_width(Text("ese valor es SIEMPRE el mismo", font_size=22, color=YELLOW, weight=BOLD))
        fijo.next_to(calculo, DOWN, buff=0.5)
        marco = SurroundingRectangle(calculo, color=YELLOW, buff=0.15)
        self.play(Create(marco), FadeIn(fijo, shift=UP * 0.2), run_time=0.8)
        self.wait(1.8)

        # Se encoge a una tarjeta fija en la esquina, igual que W=F*d en el video 5.
        mini_dp = MathTex(r"\Delta p = 1600", color=COLOR_MOMENTUM).scale(0.45)
        fondo_dp = SurroundingRectangle(mini_dp, color=YELLOW, buff=0.15)
        tarjeta_dp = VGroup(fondo_dp, mini_dp).to_corner(UR, buff=0.4)

        self.play(
            FadeOut(formula_impulso), FadeOut(fijo), FadeOut(marco),
            ReplacementTransform(calculo, mini_dp), FadeIn(fondo_dp),
            run_time=0.9,
        )
        self.formula_card = tarjeta_dp
        self.wait(1.0)

    # ------------------------------------------------------------------
    # 0:34 - 0:50  Comparacion volante vs bolsa (barras de intercambio)
    # ------------------------------------------------------------------
    def comparar_volante_bolsa(self):
        self.mostrar_fase("DESARROLLO", COLOR_FASE_DESARROLLO)

        base = Line(LEFT * 1.9, RIGHT * 1.9, color=GREY_B, stroke_width=3)
        base.to_edge(DOWN, buff=1.6)
        self.play(Create(base), run_time=0.4)

        x_t1, x_f1 = -1.3, -0.5
        x_t2, x_f2 = 0.5, 1.3

        t1_tracker = ValueTracker(0.0)
        f1_tracker = ValueTracker(0.0)
        t2_tracker = ValueTracker(0.0)
        f2_tracker = ValueTracker(0.0)

        def crear_barra(x_tracker, color, x_pos):
            return always_redraw(lambda: Rectangle(
                width=0.55, height=x_tracker.get_value(),
                color=color, fill_color=color, fill_opacity=0.85, stroke_width=0,
            ).move_to(base.get_center() + RIGHT * x_pos + UP * x_tracker.get_value() / 2))

        barra_t1 = crear_barra(t1_tracker, COLOR_TIEMPO, x_t1)
        barra_f1 = crear_barra(f1_tracker, COLOR_FUERZA, x_f1)
        barra_t2 = crear_barra(t2_tracker, COLOR_TIEMPO, x_t2)
        barra_f2 = crear_barra(f2_tracker, COLOR_FUERZA, x_f2)
        self.add(barra_t1, barra_f1, barra_t2, barra_f2)

        etiqueta_1 = cap_width(Text("Volante", font_size=20, weight=BOLD))
        etiqueta_1.next_to(base, DOWN, buff=0.15).shift(LEFT * 0.9)
        etiqueta_2 = cap_width(Text("Bolsa de aire", font_size=20, weight=BOLD))
        etiqueta_2.next_to(base, DOWN, buff=0.15).shift(RIGHT * 0.9)
        self.play(Write(etiqueta_1), Write(etiqueta_2), run_time=0.6)

        # --- Caso 1: volante (Δt chico, F grande) ---------------------------
        self.play(
            t1_tracker.animate.set_value(altura_barra(DT_VOLANTE, DT_BOLSA)),
            f1_tracker.animate.set_value(altura_barra(F_VOLANTE, F_VOLANTE)),
            run_time=1.2, rate_func=rush_into,
        )
        valor_t1 = cap_width(MathTex(f"{DT_VOLANTE:.2f}\\,s", color=COLOR_TIEMPO).scale(0.55))
        valor_t1.next_to(barra_t1, UP, buff=0.15)
        valor_f1 = cap_width(MathTex(f"{F_VOLANTE:,.0f}\\,N", color=COLOR_FUERZA).scale(0.5))
        valor_f1.next_to(barra_f1, UP, buff=0.15)
        self.play(Write(valor_t1), Write(valor_f1), run_time=0.6)
        self.wait(1.0)

        # --- Caso 2: bolsa (Δt grande, F chica) ------------------------------
        self.play(
            t2_tracker.animate.set_value(altura_barra(DT_BOLSA, DT_BOLSA)),
            f2_tracker.animate.set_value(altura_barra(F_BOLSA, F_VOLANTE)),
            run_time=1.2, rate_func=rush_into,
        )
        valor_t2 = cap_width(MathTex(f"{DT_BOLSA:.1f}\\,s", color=COLOR_TIEMPO).scale(0.55))
        valor_t2.next_to(barra_t2, UP, buff=0.15)
        valor_f2 = cap_width(MathTex(f"{F_BOLSA:,.0f}\\,N", color=COLOR_FUERZA).scale(0.5))
        valor_f2.next_to(barra_f2, UP, buff=0.15)
        self.play(Write(valor_t2), Write(valor_f2), run_time=0.6)
        self.wait(0.8)

        conclusion = cap_width(Text("10× más tiempo → 10× menos fuerza", font_size=22, color=YELLOW, weight=BOLD))
        conclusion.to_edge(UP, buff=1.0)
        self.play(Write(conclusion), Flash(barra_f2.get_center(), color=YELLOW, flash_radius=0.8), run_time=0.9)
        self.wait(1.8)

        self.play(
            FadeOut(base), FadeOut(barra_t1), FadeOut(barra_f1), FadeOut(barra_t2), FadeOut(barra_f2),
            FadeOut(etiqueta_1), FadeOut(etiqueta_2), FadeOut(valor_t1), FadeOut(valor_f1),
            FadeOut(valor_t2), FadeOut(valor_f2), FadeOut(conclusion),
        )
        self.wait(1.0)

    # ------------------------------------------------------------------
    # 0:50 - 1:00  La trampa (error conceptual comun)
    # ------------------------------------------------------------------
    def la_trampa(self):
        titulo = cap_width(Text("LA TRAMPA 🚫", font_size=34, weight=BOLD, color=RED)).to_edge(UP, buff=1.1)
        self.play(Write(titulo), run_time=0.7)

        idea_falsa = cap_width(Text(
            "\"La bolsa reduce\nel golpe total\"",
            font_size=26, line_spacing=1.1,
        )).next_to(titulo, DOWN, buff=0.6)
        self.play(FadeIn(idea_falsa, shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)

        tachon = Line(
            idea_falsa.get_left() + LEFT * 0.1, idea_falsa.get_right() + RIGHT * 0.1,
            color=RED, stroke_width=6,
        )
        self.play(Create(tachon), run_time=0.5)
        self.wait(0.8)

        idea_correcta = cap_width(Text(
            "El impulso (1600) es\nSIEMPRE el mismo.\nSolo cambia cuánto\ntiempo tarda.",
            font_size=24, line_spacing=1.15, color=GREEN,
        )).next_to(idea_falsa, DOWN, buff=0.7)
        self.play(FadeIn(idea_correcta, shift=UP * 0.2), run_time=0.8)
        self.wait(2.3)

        self.play(
            FadeOut(titulo), FadeOut(idea_falsa), FadeOut(tachon), FadeOut(idea_correcta),
        )

    # ------------------------------------------------------------------
    # 1:00 - 1:09  Analogia: piso duro vs colchon
    # ------------------------------------------------------------------
    def analogia(self):
        self.mostrar_fase("RESULTADO", COLOR_FASE_RESULTADO)

        base = Line(LEFT * 1.9, RIGHT * 1.9, color=GREY_B, stroke_width=3).to_edge(DOWN, buff=1.6)
        self.play(Create(base), run_time=0.4)

        piso_pos = base.get_center() + LEFT * 1.1
        colchon_pos = base.get_center() + RIGHT * 1.1

        colchon = Rectangle(width=1.1, height=0.3, color=GREEN, fill_color=GREEN, fill_opacity=0.6, stroke_width=0)
        colchon.move_to(colchon_pos + UP * 0.15)

        caja_piso = Square(side_length=0.4, color=WHITE, fill_color=COLOR_CAJA, fill_opacity=0.95)
        caja_piso.move_to(piso_pos + UP * 2.5)
        caja_colchon = Square(side_length=0.4, color=WHITE, fill_color=COLOR_CAJA, fill_opacity=0.95)
        caja_colchon.move_to(colchon_pos + UP * 2.5)

        etiqueta_piso = cap_width(Text("Piso", font_size=20, weight=BOLD)).next_to(base, DOWN, buff=0.15).shift(LEFT * 1.1)
        etiqueta_colchon = cap_width(Text("Colchón", font_size=20, weight=BOLD)).next_to(base, DOWN, buff=0.15).shift(RIGHT * 1.1)

        self.play(FadeIn(colchon), Write(etiqueta_piso), Write(etiqueta_colchon), run_time=0.5)
        self.play(FadeIn(caja_piso), FadeIn(caja_colchon), run_time=0.4)

        self.play(
            caja_piso.animate.move_to(piso_pos + UP * 0.2),
            run_time=0.5, rate_func=rate_functions.ease_in_quad,
        )
        self.play(Wiggle(caja_piso, scale_value=1.1, rotation_angle=0.015 * TAU), run_time=0.4)

        self.play(
            caja_colchon.animate.move_to(colchon_pos + UP * 0.25),
            run_time=1.3, rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.6)

        frase = cap_width(Text(
            "Mismo golpe. Más tiempo\npara frenar = menos fuerza.",
            font_size=24, line_spacing=1.1, weight=BOLD,
        )).to_edge(UP, buff=1.1)
        self.play(Write(frase), run_time=0.9)
        self.wait(2.0)

        self.play(
            FadeOut(base), FadeOut(colchon), FadeOut(caja_piso), FadeOut(caja_colchon),
            FadeOut(etiqueta_piso), FadeOut(etiqueta_colchon), FadeOut(frase),
        )

    # ------------------------------------------------------------------
    # 1:09 - 1:18  Estrategia resumida
    # ------------------------------------------------------------------
    def estrategia(self):
        titulo = cap_width(Text("La estrategia", font_size=30, weight=BOLD)).to_edge(UP, buff=1.1)

        pasos = VGroup(
            Text("1. Calcula Δp\n(fijo: m × Δv)", font_size=22, line_spacing=1.0),
            Text("2. Elige o mide\nel tiempo Δt", font_size=22, line_spacing=1.0),
            Text("3. F = Δp / Δt", font_size=22, line_spacing=1.0),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        cap_width(pasos)

        flechas = VGroup(*[
            Arrow(pasos[i].get_bottom(), pasos[i + 1].get_top(), buff=0.1, stroke_width=3, color=YELLOW)
            for i in range(len(pasos) - 1)
        ])

        self.play(Write(titulo), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in pasos], lag_ratio=0.4), run_time=1.6)
        self.play(*[GrowArrow(f) for f in flechas], run_time=0.6)
        self.wait(5.0)

        self.play(FadeOut(titulo), FadeOut(pasos), FadeOut(flechas))

    # ------------------------------------------------------------------
    # 1:18 - 1:27  Reto final
    # ------------------------------------------------------------------
    def reto_final(self):
        reto_titulo = cap_width(Text("TU RETO 🧠", font_size=36, weight=BOLD, color=YELLOW)).to_edge(UP, buff=1.2)

        reto_texto = cap_width(Text(
            "Si la bolsa tardara\nel doble, 0.4 segundos,\n¿cuánto valdría\nla fuerza?",
            font_size=26, line_spacing=1.15,
        )).next_to(reto_titulo, DOWN, buff=0.7)

        self.play(Write(reto_titulo), run_time=0.6)
        self.play(FadeIn(reto_texto, shift=UP * 0.2, scale=1.1, rate_func=rate_functions.ease_out_back), run_time=0.8)
        self.wait(3.3)

        self.play(
            FadeOut(reto_titulo), FadeOut(reto_texto),
            FadeOut(self.formula_card), FadeOut(self.fase_actual),
        )

    # ------------------------------------------------------------------
    # 1:27 - 1:31  Cierre
    # ------------------------------------------------------------------
    def cierre(self):
        cierre_texto = cap_width(Text(
            "No evitas el golpe.\nLo estiras en el tiempo. 💥\nFísica en 60s — Parte 6",
            font_size=26, line_spacing=1.2, weight=BOLD,
        ))
        self.play(FadeIn(cierre_texto, scale=1.1, rate_func=rate_functions.ease_out_back), run_time=0.8)
        self.wait(4.5)
