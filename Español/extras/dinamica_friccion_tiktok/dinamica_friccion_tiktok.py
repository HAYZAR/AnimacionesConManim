"""
"El angulo que despierta la friccion" - video vertical para TikTok/Reels/Shorts.

Requiere Manim Community Edition (motor distinto al resto del curso,
que usa la version antigua de 3b1b):

    pip install manim

Render vertical 9:16 recomendado:

    manim -pqh --format=mp4 dinamica_friccion_tiktok.py DinamicaFriccionTikTok

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
M = 2.0          # kg
G = 9.8          # m/s^2
MU_S = 0.6       # coeficiente de friccion estatica
MU_K = 0.4       # coeficiente de friccion cinetica
THETA_1 = 30      # grados: el bloque NO desliza
THETA_2 = 35      # grados: el bloque SI desliza

# --- Paleta de color fija (no reasignar) --------------------------------
COLOR_PESO = RED
COLOR_NORMAL = BLUE
COLOR_FRICCION = GREEN
COLOR_NETA = ORANGE


def mg_sin(theta_deg):
    return M * G * np.sin(np.deg2rad(theta_deg))


def mg_cos(theta_deg):
    return M * G * np.cos(np.deg2rad(theta_deg))


def dir_plano(theta_deg):
    """Vector unitario a lo largo del plano, apuntando cuesta ARRIBA."""
    theta = np.deg2rad(theta_deg)
    return np.array([np.cos(theta), np.sin(theta), 0.0])


def dir_normal(theta_deg):
    """Vector unitario normal al plano, hacia AFUERA de la superficie."""
    theta = np.deg2rad(theta_deg)
    return np.array([-np.sin(theta), np.cos(theta), 0.0])


def cap_width(mobject, max_width=3.9):
    """Encoge (nunca agranda) un mobject para que quepa en el frame vertical angosto."""
    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)
    return mobject


class DinamicaFriccionTikTok(Scene):
    def construct(self):
        self.hook()
        self.plantear_problema()
        self.dcl()
        self.descomponer_peso()
        self.comparar_30()
        self.subir_a_35_y_deslizar()
        self.estrategia()
        self.reto_final()

    # ------------------------------------------------------------------
    # 0:00 - 0:06  Hook
    # ------------------------------------------------------------------
    def hook(self):
        self.plano, self.bloque, self.base_line, self.arco_angulo = self.crear_plano_y_bloque(THETA_1)
        grupo_inicial = VGroup(
            self.plano, self.bloque, self.base_line, self.arco_angulo
        ).move_to(ORIGIN)

        hook_text = cap_width(Text(
            "¿Qué ángulo lo hace\nacelerar de golpe?",
            font_size=34, weight=BOLD,
        )).to_edge(UP, buff=1.0)

        self.play(FadeIn(grupo_inicial), Write(hook_text), run_time=1.2)

        angulo_tracker = ValueTracker(0)
        angulo_label = always_redraw(
            lambda: MathTex(f"{angulo_tracker.get_value():.0f}^\\circ")
            .scale(0.8)
            .next_to(self.plano, DOWN, buff=0.3)
        )
        self.add(angulo_label)
        self.play(angulo_tracker.animate.set_value(THETA_1), run_time=1.4, rate_func=rush_from)
        self.play(Wiggle(self.bloque, scale_value=1.05, rotation_angle=0.01 * TAU), run_time=1.0)
        self.wait(1.4)

        self.play(FadeOut(hook_text), FadeOut(angulo_label))
        self.hook_group = grupo_inicial

    # ------------------------------------------------------------------
    # 0:06 - 0:16  Planteamiento de datos
    # ------------------------------------------------------------------
    def plantear_problema(self):
        self.play(self.hook_group.animate.scale(0.75).to_edge(DOWN, buff=1.6))

        datos = VGroup(
            MathTex(r"m = 2\ \text{kg}"),
            MathTex(r"\mu_s = 0.6"),
            MathTex(r"\mu_k = 0.4"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.9)
        cap_width(datos).to_edge(UP, buff=1.3)

        flecha = Arrow(
            start=datos.get_bottom() + DOWN * 0.1,
            end=self.bloque.get_top(),
            color=YELLOW, buff=0.1, stroke_width=3,
        )

        self.play(LaggedStart(*[Write(d) for d in datos], lag_ratio=0.3), run_time=1.6)
        self.play(GrowArrow(flecha), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(flecha))
        self.wait(5.0)

        self.datos = datos

    # ------------------------------------------------------------------
    # 0:16 - 0:26  Diagrama de cuerpo libre (DCL)
    # ------------------------------------------------------------------
    def dcl(self):
        self.play(self.hook_group.animate.scale(1.3).move_to(RIGHT * 0.9), FadeOut(self.datos))

        centro = self.bloque.get_center()
        d = dir_plano(THETA_1)     # cuesta arriba
        n = dir_normal(THETA_1)    # fuera de la superficie

        self.v_peso = Arrow(centro, centro + DOWN * 1.4, color=COLOR_PESO, buff=0, stroke_width=6)
        self.v_normal = Arrow(centro, centro + n * 1.2, color=COLOR_NORMAL, buff=0, stroke_width=6)
        # La friccion estatica se opone a la tendencia de deslizar cuesta abajo -> apunta cuesta arriba.
        self.v_friccion = Arrow(centro, centro + d * 1.0, color=COLOR_FRICCION, buff=0, stroke_width=6)

        etiqueta_peso = MathTex("mg", color=COLOR_PESO).scale(0.7).next_to(self.v_peso.get_end(), DOWN, buff=0.1)
        etiqueta_normal = MathTex("N", color=COLOR_NORMAL).scale(0.7).next_to(self.v_normal.get_end(), n, buff=0.12)
        etiqueta_friccion = MathTex("f", color=COLOR_FRICCION).scale(0.7).next_to(self.v_friccion.get_end(), d, buff=0.12)

        leyenda = VGroup(
            Dot(color=COLOR_PESO).scale(0.6), Text("Peso", font_size=22, color=COLOR_PESO),
            Dot(color=COLOR_NORMAL).scale(0.6), Text("Normal", font_size=22, color=COLOR_NORMAL),
            Dot(color=COLOR_FRICCION).scale(0.6), Text("Fricción", font_size=22, color=COLOR_FRICCION),
        ).arrange_in_grid(rows=3, cols=2, buff=0.2)
        cap_width(leyenda).to_edge(UP, buff=1.0)

        self.play(Write(leyenda), run_time=0.8)
        self.play(GrowArrow(self.v_peso), Write(etiqueta_peso), run_time=0.7)
        self.wait(0.2)
        self.play(GrowArrow(self.v_normal), Write(etiqueta_normal), run_time=0.7)
        self.wait(0.2)
        self.play(GrowArrow(self.v_friccion), Write(etiqueta_friccion), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(leyenda))

        self.dcl_group = VGroup(
            self.v_peso, self.v_normal, self.v_friccion,
            etiqueta_peso, etiqueta_normal, etiqueta_friccion,
        )
        self.wait(4.2)

    # ------------------------------------------------------------------
    # 0:26 - 0:36  Descomposicion del peso
    # ------------------------------------------------------------------
    def descomponer_peso(self):
        centro = self.bloque.get_center()
        d = dir_plano(THETA_1)
        n = dir_normal(THETA_1)

        # Componentes del peso: cuesta abajo (-d) y contra la superficie (-n).
        comp_paralela = DashedVMobject(
            Arrow(centro, centro - d * 1.0, color=COLOR_PESO, buff=0, stroke_width=5)
        )
        comp_perp = DashedVMobject(
            Arrow(centro, centro - n * 0.75, color=COLOR_PESO, buff=0, stroke_width=5)
        )
        eq_paralela = MathTex(r"mg\sin\theta", color=COLOR_PESO).scale(0.6).next_to(comp_paralela, -d, buff=0.15)
        eq_perp = MathTex(r"mg\cos\theta", color=COLOR_PESO).scale(0.6).next_to(comp_perp, -n, buff=0.15)

        self.play(Create(comp_paralela), Write(eq_paralela), run_time=0.9)
        self.play(Create(comp_perp), Write(eq_perp), run_time=0.9)
        self.wait(0.6)

        formula_normal = MathTex(r"N = mg\cos\theta").scale(0.75).to_edge(UP, buff=1.1)
        self.play(TransformMatchingTex(eq_perp.copy(), formula_normal), run_time=0.9)
        self.wait(0.5)
        self.play(
            FadeOut(formula_normal), FadeOut(comp_paralela), FadeOut(comp_perp),
            FadeOut(eq_paralela), FadeOut(eq_perp),
        )
        self.wait(5.2)

    # ------------------------------------------------------------------
    # 0:36 - 0:46  Comparacion a 30 grados: no desliza
    # ------------------------------------------------------------------
    def comparar_30(self):
        desigualdad = cap_width(MathTex(
            r"mg\sin\theta", r"\ \overset{?}{\leq}\ ", r"\mu_s\, mg\cos\theta"
        ).scale(0.85)).to_edge(UP, buff=1.0)
        self.play(Write(desigualdad), run_time=0.8)

        val_izq = ValueTracker(0)
        val_der = ValueTracker(0)
        num_izq = always_redraw(
            lambda: DecimalNumber(val_izq.get_value(), unit="\\,N", color=COLOR_PESO)
            .scale(0.8).next_to(desigualdad, DOWN, buff=0.5).shift(LEFT * 1.2)
        )
        num_der = always_redraw(
            lambda: DecimalNumber(val_der.get_value(), unit="\\,N", color=COLOR_FRICCION)
            .scale(0.8).next_to(desigualdad, DOWN, buff=0.5).shift(RIGHT * 1.2)
        )
        self.add(num_izq, num_der)
        self.play(
            val_izq.animate.set_value(mg_sin(THETA_1)),
            val_der.animate.set_value(MU_S * mg_cos(THETA_1)),
            run_time=1.6, rate_func=rush_into,
        )
        self.wait(0.4)

        resultado = cap_width(Text("NO desliza (por muy poco)", font_size=26, color=GREEN, weight=BOLD))
        resultado.next_to(VGroup(num_izq, num_der), DOWN, buff=0.6)
        marco = SurroundingRectangle(VGroup(num_izq, num_der), color=YELLOW, buff=0.25)

        self.play(Create(marco), run_time=0.5)
        self.play(Write(resultado), Flash(marco.get_center(), color=YELLOW), run_time=0.8)
        self.play(self.bloque.animate.set_stroke(GREEN, width=6), run_time=0.4)
        self.wait(0.6)

        self.play(
            FadeOut(desigualdad), FadeOut(num_izq), FadeOut(num_der),
            FadeOut(resultado), FadeOut(marco),
        )
        self.wait(3.9)

    # ------------------------------------------------------------------
    # 0:46 - 1:03  Se inclina a 35 grados: si desliza -> 2da ley
    # ------------------------------------------------------------------
    def subir_a_35_y_deslizar(self):
        grupo_plano = VGroup(self.plano, self.bloque, self.dcl_group)
        pivote = self.base_line.get_start()

        self.play(FadeOut(self.arco_angulo), run_time=0.3)
        self.play(
            Rotate(grupo_plano, angle=np.deg2rad(THETA_2 - THETA_1), about_point=pivote),
            run_time=1.4,
        )
        self.play(self.bloque.animate.set_stroke(COLOR_NETA, width=6), run_time=0.3)

        desigualdad2 = cap_width(MathTex(
            f"{mg_sin(THETA_2):.2f}", r"\,N", r"\ >\ ",
            f"{MU_S * mg_cos(THETA_2):.2f}", r"\,N",
        ).scale(0.8)).to_edge(UP, buff=1.0)
        self.play(Write(desigualdad2), run_time=0.8)
        self.play(Indicate(desigualdad2, color=COLOR_NETA), run_time=0.6)
        self.wait(0.3)
        self.play(FadeOut(desigualdad2))
        self.wait(2.5)

        ley_general = cap_width(MathTex(r"\sum F = m a").scale(0.9)).to_edge(UP, buff=1.0)
        ley_sustituida = cap_width(MathTex(
            r"mg\sin\theta - \mu_k mg\cos\theta = ma"
        ).scale(0.75)).to_edge(UP, buff=1.0)

        self.play(Write(ley_general), run_time=0.7)
        self.wait(0.3)
        self.play(TransformMatchingTex(ley_general, ley_sustituida), run_time=0.9)
        self.wait(0.4)

        a_valor = (mg_sin(THETA_2) - MU_K * mg_cos(THETA_2)) / M
        resultado_a = cap_width(MathTex(f"a \\approx {a_valor:.2f}\\ m/s^2", color=COLOR_NETA))
        resultado_a.next_to(ley_sustituida, DOWN, buff=0.6)

        self.play(Write(resultado_a), Flash(resultado_a.get_center(), color=COLOR_NETA), run_time=0.9)

        # El bloque acelera cuesta abajo: direccion -d (hacia la base del plano).
        d2 = dir_plano(THETA_2)
        v_aceleracion = Arrow(
            self.bloque.get_center(),
            self.bloque.get_center() - d2 * 1.1,
            color=COLOR_NETA, buff=0.1, stroke_width=6,
        )
        self.play(GrowArrow(v_aceleracion), run_time=0.5)
        self.play(
            self.bloque.animate.shift(-d2 * 0.9),
            v_aceleracion.animate.shift(-d2 * 0.9),
            run_time=1.0, rate_func=rate_functions.ease_in_quad,
        )
        self.wait(0.4)

        self.play(
            FadeOut(ley_sustituida), FadeOut(resultado_a), FadeOut(v_aceleracion),
            FadeOut(grupo_plano), FadeOut(self.base_line),
        )
        self.wait(2.7)

    # ------------------------------------------------------------------
    # 1:03 - 1:13  Estrategia resumida (conclusion)
    # ------------------------------------------------------------------
    def estrategia(self):
        titulo = cap_width(Text("Estrategia para cualquier\nproblema de fricción", font_size=28, weight=BOLD))
        titulo.to_edge(UP, buff=1.2)

        pasos = VGroup(
            Text("1. Diagrama de\ncuerpo libre", font_size=22, line_spacing=1.0),
            Text("2. ¿F ≤ fricción\nestática máxima?", font_size=22, line_spacing=1.0),
            Text("3. Si desliza: 2ª Ley\ncon fricción cinética", font_size=22, line_spacing=1.0),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        cap_width(pasos)

        flechas = VGroup(*[
            Arrow(pasos[i].get_bottom(), pasos[i + 1].get_top(), buff=0.1, stroke_width=3, color=YELLOW)
            for i in range(len(pasos) - 1)
        ])

        self.play(Write(titulo), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in pasos], lag_ratio=0.4), run_time=1.6)
        self.play(*[GrowArrow(f) for f in flechas], run_time=0.6)
        self.wait(6.0)

        self.play(FadeOut(titulo), FadeOut(pasos), FadeOut(flechas))

    # ------------------------------------------------------------------
    # 1:13 - 1:24  Reto final + cierre
    # ------------------------------------------------------------------
    def reto_final(self):
        reto_titulo = cap_width(Text("TU RETO 🧠", font_size=36, weight=BOLD, color=YELLOW)).to_edge(UP, buff=1.3)
        reto_texto = cap_width(Text(
            "¿Cuál es el ángulo\ncrítico exacto en el\nque este bloque\nempieza a deslizar?",
            font_size=26, line_spacing=1.2,
        )).next_to(reto_titulo, DOWN, buff=0.6)

        pista = cap_width(MathTex(r"\tan\theta_c = \mu_s").scale(0.9).set_opacity(0.5))
        pista.next_to(reto_texto, DOWN, buff=0.8)

        self.play(Write(reto_titulo), run_time=0.6)
        self.play(FadeIn(reto_texto, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
        self.play(FadeIn(pista), run_time=0.6)
        self.wait(2.5)

        cierre = cap_width(Text("Física en 60s — Parte 1/2\nSígueme para la Parte 2 👀", font_size=24))
        cierre.next_to(pista, DOWN, buff=0.8)
        self.play(Write(cierre), run_time=1.0)
        self.wait(4.0)

    # ------------------------------------------------------------------
    # Helpers de construccion geometrica
    # ------------------------------------------------------------------
    def crear_plano_y_bloque(self, theta_deg):
        base_line = Line(LEFT * 1.8, RIGHT * 1.8, color=GREY_B, stroke_width=4)
        base_line.to_edge(DOWN, buff=2.0)

        largo = 3.4
        punto_inicio = base_line.get_start()
        d = dir_plano(theta_deg)
        punto_final = punto_inicio + d * largo

        rampa = Line(punto_inicio, punto_final, color=WHITE, stroke_width=5)
        relleno = Polygon(
            punto_inicio, punto_final, punto_inicio + RIGHT * largo,
            color=GREY_D, fill_opacity=0.6, stroke_width=0,
        )
        arco_angulo = Angle(
            base_line, rampa, radius=0.6, other_angle=False, color=YELLOW
        )

        plano = VGroup(relleno, rampa)

        n = dir_normal(theta_deg)
        pos_bloque = punto_inicio + d * (largo * 0.45) + n * 0.28

        bloque = Square(side_length=0.56, color=WHITE, fill_color=BLUE_E, fill_opacity=0.9)
        bloque.rotate(np.deg2rad(theta_deg))
        bloque.move_to(pos_bloque)

        return plano, bloque, base_line, arco_angulo
