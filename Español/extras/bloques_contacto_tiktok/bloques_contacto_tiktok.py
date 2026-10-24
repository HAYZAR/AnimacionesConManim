"""
"El bloque que no empujas tambien siente la fuerza" - video vertical para
TikTok/Reels/Shorts. Cuarto y ultimo video de la serie (ver
Español/extras/dinamica_friccion_tiktok/, bascula_ascensor_tiktok/ y
carro_polea_tiktok/ para los anteriores).

Requiere Manim Community Edition:  pip install manim
Render de prueba:  manim -ql --format=mp4 bloques_contacto_tiktok.py BloquesContactoTikTok
Render final:      manim -qh --format=mp4 --fps 30 bloques_contacto_tiktok.py BloquesContactoTikTok

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
M1 = 2.0   # kg (bloque grande)
M2 = 1.0   # kg (bloque pequeño)
F_APLICADA = 12.0  # N
FRICCION_TOTAL = 3.0  # N


def a_sistema(f_neta):
    return f_neta / (M1 + M2)


def cap_width(mobject, max_width=3.9):
    """Encoge (nunca agranda) un mobject para que quepa en el frame vertical angosto."""
    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)
    return mobject


def cap_size(mobject, max_width=3.9, max_height=0.45):
    """Como cap_width, pero tambien limita la altura: las formulas con fracciones
    grandes son angostas pero muy altas, e invaden otras zonas del frame si solo
    se limita el ancho."""
    factor = min(max_width / mobject.width, max_height / mobject.height, 1.0)
    if factor < 1.0:
        mobject.scale(factor)
    return mobject


# --- Paleta de color fija (no reasignar) --------------------------------
COLOR_FUERZA = YELLOW
COLOR_CONTACTO = BLUE
COLOR_FRICCION = GREEN
COLOR_ACEL = ORANGE


class BloquesContactoTikTok(Scene):
    def construct(self):
        self.crear_escenario()
        self.hook()
        self.plantear_problema()
        self.sistema_completo()
        self.aislar_bloque_pequeno()
        self.tercera_ley()
        self.invertir_orden()
        self.reflexion()
        self.con_friccion()
        self.reto_final()
        self.cierre()

    # ------------------------------------------------------------------
    # Escenario: piso + dos bloques en contacto + contador de contacto
    # ------------------------------------------------------------------
    def crear_escenario(self):
        self.piso_y = -0.6
        self.piso = Line(LEFT * 1.9, RIGHT * 1.9, color=WHITE, stroke_width=4).shift(UP * self.piso_y)
        self.piso_textura = Line(LEFT * 1.9, RIGHT * 1.9, color=GREY_D, stroke_width=1).shift(UP * (self.piso_y - 0.03))

        self.bloque_grande = self._crear_bloque(0.9, 0.7, BLUE_E)
        self.bloque_pequeno = self._crear_bloque(0.55, 0.45, TEAL_E)

        self.a_tracker = ValueTracker(0.0)
        self.a_display = always_redraw(
            lambda: VGroup(
                MathTex("a \\approx", color=COLOR_ACEL),
                DecimalNumber(self.a_tracker.get_value(), num_decimal_places=2, color=COLOR_ACEL),
                MathTex("\\text{m/s}^2", color=COLOR_ACEL),
            ).arrange(RIGHT, buff=0.15).scale(1.1).to_edge(UP, buff=0.6)
        )

        self.piso_grupo = VGroup(self.piso, self.piso_textura)

    def _crear_bloque(self, ancho, alto, color):
        return RoundedRectangle(
            width=ancho, height=alto, corner_radius=0.06,
            color=WHITE, stroke_width=2, fill_color=color, fill_opacity=0.9,
        )

    def colocar_pareja(self, empujar_grande, x_contacto=0.0):
        """Posiciona los dos bloques en contacto sobre el piso. Si
        empujar_grande es True, el bloque grande queda a la izquierda
        (empujado) y el pequeño a la derecha (detras); si es False, al
        reves. Devuelve el punto de contacto entre ambos."""
        if empujar_grande:
            izq, der = self.bloque_grande, self.bloque_pequeno
        else:
            izq, der = self.bloque_pequeno, self.bloque_grande

        izq.move_to(RIGHT * (x_contacto - izq.width / 2) + UP * (self.piso_y + izq.height / 2 + 0.02))
        der.move_to(RIGHT * (x_contacto + der.width / 2) + UP * (self.piso_y + der.height / 2 + 0.02))
        return izq.get_right()

    def crear_flecha_fuerza(self, punto_inicio, hacia_derecha, color, longitud=0.8):
        vector = RIGHT * longitud if hacia_derecha else LEFT * longitud
        return Arrow(punto_inicio, punto_inicio + vector, color=color, buff=0.05, stroke_width=6)

    # ------------------------------------------------------------------
    # 0:00 - 0:07  Hook
    # ------------------------------------------------------------------
    def hook(self):
        hook_text = cap_width(Text(
            "Mismos 12 N...\n¿por qué cambia el contacto?",
            font_size=28, weight=BOLD, line_spacing=1.1,
        )).next_to(self.a_display, DOWN, buff=0.4)

        self.colocar_pareja(empujar_grande=True, x_contacto=-0.3)
        grupo = VGroup(self.piso_grupo, self.bloque_grande, self.bloque_pequeno)
        self.play(FadeIn(grupo), Write(hook_text), run_time=1.0)
        self.add(self.a_display)

        flecha_f = self.crear_flecha_fuerza(self.bloque_grande.get_left() + LEFT * 0.7, True, COLOR_FUERZA)
        etiqueta_f = MathTex("F=12\\,N", color=COLOR_FUERZA).scale(0.55).next_to(flecha_f, UP, buff=0.1)
        punto_contacto = (self.bloque_grande.get_right() + self.bloque_pequeno.get_left()) / 2
        num_contacto = DecimalNumber(4.0, unit="\\,N", color=COLOR_CONTACTO, num_decimal_places=1).scale(0.6)
        num_contacto.next_to(punto_contacto, DOWN, buff=0.5)

        self.play(GrowArrow(flecha_f), Write(etiqueta_f), run_time=0.6)
        self.play(FadeIn(num_contacto, shift=DOWN * 0.1), self.a_tracker.animate.set_value(4.0), run_time=0.9)
        self.wait(1.6)
        self.play(FadeOut(flecha_f), FadeOut(etiqueta_f), FadeOut(num_contacto))
        self.play(FadeOut(grupo))

        self.colocar_pareja(empujar_grande=False, x_contacto=-0.3)
        grupo2 = VGroup(self.bloque_grande, self.bloque_pequeno)
        self.play(FadeIn(VGroup(self.piso_grupo, grupo2)), run_time=0.5)
        flecha_f2 = self.crear_flecha_fuerza(self.bloque_pequeno.get_left() + LEFT * 0.7, True, COLOR_FUERZA)
        etiqueta_f2 = MathTex("F=12\\,N", color=COLOR_FUERZA).scale(0.55).next_to(flecha_f2, UP, buff=0.1)
        punto_contacto2 = (self.bloque_pequeno.get_right() + self.bloque_grande.get_left()) / 2
        num_contacto2 = DecimalNumber(8.0, unit="\\,N", color=COLOR_CONTACTO, num_decimal_places=1).scale(0.6)
        num_contacto2.next_to(punto_contacto2, DOWN, buff=0.5)

        self.play(GrowArrow(flecha_f2), Write(etiqueta_f2), run_time=0.6)
        self.play(FadeIn(num_contacto2, shift=DOWN * 0.1), run_time=0.6)
        self.wait(2.0)

        self.play(
            FadeOut(hook_text), FadeOut(flecha_f2), FadeOut(etiqueta_f2), FadeOut(num_contacto2),
            FadeOut(self.piso_grupo), FadeOut(self.bloque_grande), FadeOut(self.bloque_pequeno),
        )
        self.a_tracker.set_value(0.0)
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 0:07 - 0:15  Planteamiento de datos
    # ------------------------------------------------------------------
    def plantear_problema(self):
        datos = VGroup(
            MathTex(r"m_1 = 2\ \text{kg (grande)}"),
            MathTex(r"m_2 = 1\ \text{kg (pequeño)}"),
            MathTex(r"F = 12\ \text{N, sin fricción}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.7)
        cap_width(datos).next_to(self.a_display, DOWN, buff=0.5).to_edge(LEFT, buff=0.3)

        self.play(LaggedStart(*[Write(d) for d in datos], lag_ratio=0.3), run_time=1.4)
        self.wait(2.2)
        self.play(FadeOut(datos))
        self.wait(0.4)

    # ------------------------------------------------------------------
    # 0:15 - 0:26  Sistema completo: a = F/(m1+m2)
    # ------------------------------------------------------------------
    def sistema_completo(self):
        self.colocar_pareja(empujar_grande=True, x_contacto=-0.3)
        grupo = VGroup(self.piso_grupo, self.bloque_grande, self.bloque_pequeno)
        self.play(FadeIn(grupo), run_time=0.6)

        flecha_f = self.crear_flecha_fuerza(self.bloque_grande.get_left() + LEFT * 0.7, True, COLOR_FUERZA)
        etiqueta_f = MathTex("F=12\\,N", color=COLOR_FUERZA).scale(0.55).next_to(flecha_f, UP, buff=0.1)
        self.play(GrowArrow(flecha_f), Write(etiqueta_f), run_time=0.6)

        formula = cap_size(MathTex(r"a = F/(m_1{+}m_2) = 12/3 = 4.0\ \text{m/s}^2").scale(0.6))
        formula.next_to(self.a_display, DOWN, buff=0.5)
        self.play(Write(formula), run_time=1.1)

        self.play(
            grupo.animate.shift(RIGHT * 0.4),
            self.a_tracker.animate.set_value(4.0),
            run_time=1.3,
        )
        self.wait(3.0)
        self.play(FadeOut(formula), FadeOut(flecha_f), FadeOut(etiqueta_f))
        self.wait(0.4)
        self.flecha_f_actual = None

    # ------------------------------------------------------------------
    # 0:26 - 0:36  Aislar el bloque pequeño -> F12 = m2*a
    # ------------------------------------------------------------------
    def aislar_bloque_pequeno(self):
        texto = cap_width(Text("Aislamos solo al bloque\nde atrás (el pequeño)", font_size=22, line_spacing=1.1))
        texto.next_to(self.a_display, DOWN, buff=0.5)
        self.play(Write(texto), run_time=0.8)
        self.play(self.bloque_grande.animate.set_opacity(0.15), run_time=0.6)

        punto = self.bloque_pequeno.get_left()
        flecha_contacto = self.crear_flecha_fuerza(punto, True, COLOR_CONTACTO, longitud=0.6)
        etiqueta_c = MathTex("F_{12}", color=COLOR_CONTACTO).scale(0.6).next_to(flecha_contacto, UP, buff=0.1)
        self.play(GrowArrow(flecha_contacto), Write(etiqueta_c), run_time=0.6)

        formula = cap_size(MathTex(r"F_{12} = m_2 \cdot a = 1 \times 4.0 = 4.0\ \text{N}").scale(0.6))
        formula.next_to(texto, DOWN, buff=0.3)
        self.play(Write(formula), run_time=1.0)
        self.wait(3.0)

        self.play(FadeOut(texto), FadeOut(formula), FadeOut(flecha_contacto), FadeOut(etiqueta_c))
        self.play(self.bloque_grande.animate.set_opacity(0.9))
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 0:36 - 0:44  3a ley: aislar el bloque grande
    # ------------------------------------------------------------------
    def tercera_ley(self):
        texto = cap_width(Text("Aislamos ahora el bloque\ngrande: F y F₂₁ opuestas", font_size=22, line_spacing=1.1))
        texto.next_to(self.a_display, DOWN, buff=0.5)
        self.play(Write(texto), run_time=0.8)
        self.play(self.bloque_pequeno.animate.set_opacity(0.15), run_time=0.6)

        flecha_f = self.crear_flecha_fuerza(self.bloque_grande.get_left() + LEFT * 0.6, True, COLOR_FUERZA, longitud=0.55)
        etiqueta_f = MathTex("F", color=COLOR_FUERZA).scale(0.6).next_to(flecha_f, UP, buff=0.1)
        flecha_21 = self.crear_flecha_fuerza(self.bloque_grande.get_right(), False, COLOR_CONTACTO, longitud=0.55)
        etiqueta_21 = MathTex("F_{21}", color=COLOR_CONTACTO).scale(0.6).next_to(flecha_21, UP, buff=0.1)
        self.play(
            GrowArrow(flecha_f), Write(etiqueta_f), GrowArrow(flecha_21), Write(etiqueta_21),
            run_time=0.7,
        )

        formula = cap_size(MathTex(r"F_{21} = F - m_1 a = 12 - 8 = 4.0\ \text{N} = F_{12}").scale(0.55))
        formula.next_to(texto, DOWN, buff=0.3)
        self.play(Write(formula), run_time=1.1)
        self.wait(3.0)

        self.play(
            FadeOut(texto), FadeOut(formula), FadeOut(flecha_f), FadeOut(etiqueta_f),
            FadeOut(flecha_21), FadeOut(etiqueta_21),
        )
        self.play(self.bloque_pequeno.animate.set_opacity(0.9))
        self.play(FadeOut(self.piso_grupo), FadeOut(self.bloque_grande), FadeOut(self.bloque_pequeno))
        self.a_tracker.set_value(0.0)
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 0:44 - 0:56  Se invierte el orden: empuja el bloque pequeño
    # ------------------------------------------------------------------
    def invertir_orden(self):
        texto = cap_width(Text("Ahora empujamos\nal bloque PEQUEÑO", font_size=24, line_spacing=1.1))
        texto.next_to(self.a_display, DOWN, buff=0.5)
        self.play(Write(texto), run_time=0.8)

        self.colocar_pareja(empujar_grande=False, x_contacto=-0.3)
        grupo = VGroup(self.piso_grupo, self.bloque_pequeno, self.bloque_grande)
        self.play(FadeIn(grupo), run_time=0.6)

        flecha_f = self.crear_flecha_fuerza(self.bloque_pequeno.get_left() + LEFT * 0.7, True, COLOR_FUERZA)
        etiqueta_f = MathTex("F=12\\,N", color=COLOR_FUERZA).scale(0.55).next_to(flecha_f, UP, buff=0.1)
        self.play(GrowArrow(flecha_f), Write(etiqueta_f), self.a_tracker.animate.set_value(4.0), run_time=0.9)
        self.wait(2.0)

        self.play(self.bloque_pequeno.animate.set_opacity(0.15), run_time=0.5)
        punto = self.bloque_grande.get_left()
        flecha_contacto = self.crear_flecha_fuerza(punto, True, COLOR_CONTACTO, longitud=0.7)
        etiqueta_c = MathTex("F_{21}", color=COLOR_CONTACTO).scale(0.6).next_to(flecha_contacto, DOWN, buff=0.1)
        self.play(GrowArrow(flecha_contacto), Write(etiqueta_c), run_time=0.6)

        formula = cap_size(MathTex(r"F_{21} = m_1 \cdot a = 2 \times 4.0 = 8.0\ \text{N}").scale(0.6))
        formula.next_to(texto, DOWN, buff=0.3)
        self.play(Write(formula), run_time=1.1)
        self.play(Flash(formula.get_center(), color=COLOR_CONTACTO), run_time=0.6)
        self.wait(2.2)

        self.play(
            FadeOut(texto), FadeOut(formula), FadeOut(flecha_f), FadeOut(etiqueta_f),
            FadeOut(flecha_contacto), FadeOut(etiqueta_c),
        )
        self.play(self.bloque_pequeno.animate.set_opacity(0.9))
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 0:56 - 1:04  Reflexion
    # ------------------------------------------------------------------
    def reflexion(self):
        texto = cap_width(Text(
            "La aceleración del sistema\nno cambió. El contacto sí:\ndepende de qué masa empuja a cuál.",
            font_size=22, line_spacing=1.2,
        ))
        texto.next_to(self.a_display, DOWN, buff=0.5)
        self.play(Write(texto), run_time=1.0)
        self.wait(3.0)
        self.play(FadeOut(texto))
        self.play(FadeOut(self.piso_grupo), FadeOut(self.bloque_grande), FadeOut(self.bloque_pequeno))
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 1:04 - 1:14  Con friccion
    # ------------------------------------------------------------------
    def con_friccion(self):
        self.colocar_pareja(empujar_grande=True, x_contacto=-0.3)
        grupo = VGroup(self.piso_grupo, self.bloque_grande, self.bloque_pequeno)
        self.play(FadeIn(grupo), run_time=0.5)

        flecha_f = self.crear_flecha_fuerza(self.bloque_grande.get_left() + LEFT * 0.7, True, COLOR_FUERZA)
        etiqueta_f = MathTex("F=12\\,N", color=COLOR_FUERZA).scale(0.5).next_to(flecha_f, UP, buff=0.08)
        flecha_fric = self.crear_flecha_fuerza(self.bloque_pequeno.get_right() + RIGHT * 0.05, False, COLOR_FRICCION, longitud=0.45)
        etiqueta_fric = MathTex("f=3\\,N", color=COLOR_FRICCION).scale(0.5).next_to(flecha_fric, DOWN, buff=0.08)
        self.play(
            GrowArrow(flecha_f), Write(etiqueta_f), GrowArrow(flecha_fric), Write(etiqueta_fric),
            run_time=0.7,
        )

        formula = cap_size(MathTex(r"a = (F-f)/(m_1{+}m_2) = 9/3 = 3.0\ \text{m/s}^2").scale(0.55))
        formula.next_to(self.a_display, DOWN, buff=0.5)
        self.play(Write(formula), run_time=1.1)
        self.play(self.a_tracker.animate.set_value(3.0), run_time=1.2)
        self.wait(3.0)

        self.play(
            FadeOut(formula), FadeOut(flecha_f), FadeOut(etiqueta_f),
            FadeOut(flecha_fric), FadeOut(etiqueta_fric),
        )
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 1:14 - 1:22  Reto: F = friccion
    # ------------------------------------------------------------------
    def reto_final(self):
        self.play(FadeOut(self.piso_grupo), FadeOut(self.bloque_grande), FadeOut(self.bloque_pequeno))

        reto_titulo = cap_width(Text("TU RETO 🧠", font_size=34, weight=BOLD, color=YELLOW))
        reto_titulo.next_to(self.a_display, DOWN, buff=0.6)
        reto_texto = cap_width(Text(
            "Si F fuera EXACTAMENTE\nigual a la fricción,\n¿qué le pasa a la aceleración?",
            font_size=24, line_spacing=1.2,
        ))
        reto_texto.next_to(reto_titulo, DOWN, buff=0.5)
        pista = cap_size(MathTex(r"a = 0").scale(0.9).set_opacity(0.5), max_height=0.5)
        pista.next_to(reto_texto, DOWN, buff=0.6)

        self.play(Write(reto_titulo), run_time=0.6)
        self.play(FadeIn(reto_texto, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
        self.play(FadeIn(pista), run_time=0.6)
        self.wait(3.0)
        self.play(FadeOut(reto_titulo), FadeOut(reto_texto), FadeOut(pista), FadeOut(self.a_display))
        self.wait(0.3)

    # ------------------------------------------------------------------
    # 1:22 - 1:26  Cierre de la serie completa
    # ------------------------------------------------------------------
    def cierre(self):
        titulo = cap_width(Text("Serie completa", font_size=32, weight=BOLD, color=YELLOW))
        titulo.to_edge(UP, buff=1.2)
        resumen = VGroup(
            Text("1. Fricción — plano inclinado", font_size=20),
            Text("2. Normal — báscula en ascensor", font_size=20),
            Text("3. Tensión — carro y polea", font_size=20),
            Text("4. Contacto — bloques empujados", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        cap_width(resumen)
        resumen.next_to(titulo, DOWN, buff=0.6)

        self.play(Write(titulo), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in resumen], lag_ratio=0.3), run_time=1.6)
        self.wait(2.0)

        cierre = cap_width(Text("Gracias por seguir la serie 🎬", font_size=24))
        cierre.next_to(resumen, DOWN, buff=0.6)
        self.play(Write(cierre), run_time=1.0)
        self.wait(3.5)
