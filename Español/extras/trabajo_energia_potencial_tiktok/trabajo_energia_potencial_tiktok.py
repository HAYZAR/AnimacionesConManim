"""
"La caja que engaña tu intuición" - video vertical para TikTok/Reels/Shorts.
Quinta entrega de la serie (Trabajo mecánico y Energía Potencial Gravitatoria).

Requiere Manim Community Edition:

    pip install manim

Render vertical 9:16 recomendado:

    manim -pqh --format=mp4 trabajo_energia_potencial_tiktok.py TrabajoEnergiaPotencialTikTok

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
PESO = 300.0      # N
G = 10.0          # m/s^2
MASA = PESO / G    # kg
H = 4.0           # m, altura de la plataforma del camion
L = 10.0          # m, longitud de la rampa
SIN_THETA = H / L  # 0.4
F_RAMPA = PESO * SIN_THETA     # 120 N
W_RAMPA = F_RAMPA * L           # 1200 J
W_VERTICAL = PESO * H            # 1200 J
PE_GANADA = MASA * G * H          # 1200 J (coincide con W)

PESO_RETO = 450.0  # N, caja mas pesada del reto final (no se resuelve en el video)

# --- Paleta de color fija (misma que el resto de la serie) -------------
COLOR_PESO = RED
COLOR_FUERZA = BLUE
COLOR_ENERGIA = ORANGE
COLOR_TRAYECTORIA = GREEN
COLOR_CAJA = "#C98F4B"


def cap_width(mobject, max_width=3.9):
    """Encoge (nunca agranda) un mobject para que quepa en el frame vertical angosto."""
    if mobject.width > max_width:
        mobject.scale(max_width / mobject.width)
    return mobject


class TrabajoEnergiaPotencialTikTok(Scene):
    def construct(self):
        self.crear_escenario()
        self.hook()
        self.plantear_problema()
        self.definir_trabajo()
        self.proporcionalidad()
        self.comparar_caminos()
        self.energia_potencial()
        self.estrategia()
        self.reto_final()
        self.cierre()

    # ------------------------------------------------------------------
    # Construccion geometrica compartida (no es un "beat" narrado)
    # ------------------------------------------------------------------
    def crear_escenario(self):
        H_VIS = 1.6
        L_HORIZ = 2.2
        self.H_VIS = H_VIS

        self.base_line = Line(LEFT * 2.0, RIGHT * 2.0, color=GREY_B, stroke_width=4)
        self.base_line.to_edge(DOWN, buff=2.2)

        punto_base = self.base_line.get_start() + RIGHT * 0.3
        punto_alto = punto_base + RIGHT * L_HORIZ + UP * H_VIS

        self.punto_base = punto_base
        self.punto_alto = punto_alto

        # Angulo de la rampa (invariante bajo escalado/traslado uniforme, asi
        # que es seguro calcularlo una sola vez aqui y reusarlo mas adelante,
        # aunque el escenario completo se mueva/escale despues).
        delta = punto_alto - punto_base
        self.angle_rampa = np.arctan2(delta[1], delta[0])

        # Camion simplificado: cuerpo rectangular + 2 ruedas, plataforma a la
        # altura de punto_alto.
        camion = Rectangle(
            width=1.5, height=H_VIS, stroke_color=WHITE, stroke_width=3,
            fill_color=GREY_D, fill_opacity=0.9,
        )
        camion.shift(punto_alto - camion.get_corner(UL))

        rueda_1 = Circle(radius=0.16, color=BLACK, fill_color=GREY_E, fill_opacity=1, stroke_width=2)
        rueda_1.move_to(camion.get_corner(DL) + RIGHT * 0.35)
        rueda_2 = Circle(radius=0.16, color=BLACK, fill_color=GREY_E, fill_opacity=1, stroke_width=2)
        rueda_2.move_to(camion.get_corner(DR) + LEFT * 0.35)

        self.camion = VGroup(camion, rueda_1, rueda_2)

        # Rampa (verde) y camino vertical punteado (rojo), ambos arrancan
        # desde el mismo punto en el suelo.
        self.rampa = Line(punto_base, punto_alto, color=COLOR_TRAYECTORIA, stroke_width=5)
        self.camino_vertical = DashedLine(
            punto_base, punto_base + UP * H_VIS, color=COLOR_PESO, stroke_width=5,
        )

        # La caja va INCLINADA, alineada con la superficie de la rampa (no
        # parada en vertical) -- se rota una vez y la rotacion persiste en
        # cualquier shift()/move_to() posterior.
        self.caja_rampa = Square(side_length=0.42, color=WHITE, fill_color=COLOR_CAJA, fill_opacity=0.95)
        self.caja_rampa.rotate(self.angle_rampa)
        self.caja_rampa.move_to(punto_base + self.normal_rampa() * 0.21)

        # NOTA: la caja vertical y la linea "misma altura" se crean mas
        # adelante en comparar_caminos(), a partir de la posicion EN VIVO de
        # self.rampa/self.camino_vertical (get_start/get_end) -- nunca de
        # coordenadas absolutas guardadas aqui, porque el escenario completo
        # se escala y se mueve en hook()/plantear_problema() antes de que se
        # usen, y esas coordenadas quedarian obsoletas (mismo tipo de bug que
        # dir_plano()/dir_normal() evitan en el video de friccion).

        self.escenario = VGroup(
            self.base_line, self.camion, self.rampa, self.camino_vertical, self.caja_rampa,
        )

    def normal_rampa(self):
        """Vector unitario perpendicular a la rampa, hacia el lado de ARRIBA
        (el lado donde descansa la caja). Usa self.angle_rampa, que no
        cambia aunque el escenario se escale/mueva despues."""
        theta = self.angle_rampa
        return np.array([-np.sin(theta), np.cos(theta), 0.0])

    # ------------------------------------------------------------------
    # 0:00 - 0:08  Hook
    # ------------------------------------------------------------------
    def hook(self):
        grupo = VGroup(self.base_line, self.camion, self.rampa, self.camino_vertical, self.caja_rampa)
        grupo.move_to(ORIGIN).shift(DOWN * 0.3)

        interrogante = cap_width(Text("?", font_size=64, weight=BOLD, color=YELLOW))
        interrogante.move_to(VGroup(self.rampa, self.camino_vertical).get_center() + UP * 0.2)

        hook_text = cap_width(Text(
            "¿Subir esta caja por la rampa\ncuesta MENOS trabajo que\nlevantarla derecho? 🤔",
            font_size=30, weight=BOLD, line_spacing=1.1,
        )).to_edge(UP, buff=0.9)

        self.play(FadeIn(grupo, scale=1.08, rate_func=rate_functions.ease_out_back), run_time=0.6)
        self.play(
            FadeIn(hook_text, scale=1.15, rate_func=rate_functions.ease_out_back),
            FadeIn(interrogante, scale=1.6, rate_func=rate_functions.ease_out_back),
            run_time=0.9,
        )
        self.play(Wiggle(interrogante, scale_value=1.25, rotation_angle=0.03 * TAU), run_time=0.8)
        self.wait(2.2)

        self.play(FadeOut(hook_text), FadeOut(interrogante))
        self.hook_group = grupo

    # ------------------------------------------------------------------
    # 0:08 - 0:16  Planteamiento de datos
    # ------------------------------------------------------------------
    def plantear_problema(self):
        self.play(self.hook_group.animate.scale(0.8).to_edge(DOWN, buff=1.5))

        datos = VGroup(
            MathTex(r"\text{Peso} = 300\ \text{N}"),
            MathTex(r"h = 4\ \text{m}"),
            MathTex(r"L = 10\ \text{m}"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.85)
        cap_width(datos).to_edge(UP, buff=1.2)

        self.play(LaggedStart(*[Write(d) for d in datos], lag_ratio=0.3), run_time=1.6)
        self.wait(4.5)

        self.datos = datos
        self.play(FadeOut(datos))

    # ------------------------------------------------------------------
    # 0:16 - 0:26  Definicion de trabajo
    # ------------------------------------------------------------------
    def definir_trabajo(self):
        formula = cap_width(MathTex(
            r"\text{Trabajo} = \text{Fuerza} \times \text{Distancia}"
        ).scale(0.75)).to_edge(UP, buff=1.1)
        formula_corta = cap_width(MathTex(r"W = F \cdot d").scale(0.9)).to_edge(UP, buff=1.1)

        self.play(Write(formula), run_time=1.0)
        self.wait(1.0)
        self.play(TransformMatchingTex(formula, formula_corta), run_time=0.8)

        direccion = dir_rampa(self.rampa.get_start(), self.rampa.get_end())

        flecha_empuje = Arrow(
            self.caja_rampa.get_left() + LEFT * 0.5, self.caja_rampa.get_left(),
            color=COLOR_FUERZA, buff=0.05, stroke_width=5,
        )
        self.play(GrowArrow(flecha_empuje), run_time=0.5)
        self.play(
            self.caja_rampa.animate.shift(direccion * 0.5),
            flecha_empuje.animate.shift(direccion * 0.5),
            run_time=0.8,
        )
        self.wait(2.0)

        self.play(FadeOut(flecha_empuje))
        self.caja_rampa.shift(-direccion * 0.5)

        # La formula se encoge y "aterriza" en una tarjeta fija en la esquina
        # superior -- queda ahi como recordatorio visual del resto del video,
        # en vez de desaparecer para siempre.
        mini_w = MathTex(r"W = F \cdot d", color=COLOR_ENERGIA).scale(0.5)
        fondo_w = SurroundingRectangle(mini_w, color=YELLOW, buff=0.15)
        tarjeta_w = VGroup(fondo_w, mini_w).to_corner(UR, buff=0.4)

        self.play(ReplacementTransform(formula_corta, mini_w), FadeIn(fondo_w), run_time=0.8)
        self.formula_card = tarjeta_w
        self.wait(1.7)

    # ------------------------------------------------------------------
    # 0:26 - 0:38  Razonamiento proporcional (ejemplo aparte, abstracto)
    # ------------------------------------------------------------------
    def proporcionalidad(self):
        self.play(FadeOut(self.escenario))

        pesa = VGroup(
            Circle(radius=0.22, color=COLOR_CAJA, fill_color=COLOR_CAJA, fill_opacity=0.9),
            Rectangle(width=0.5, height=0.08, color=GREY_B, fill_color=GREY_B, fill_opacity=1),
            Circle(radius=0.22, color=COLOR_CAJA, fill_color=COLOR_CAJA, fill_opacity=0.9),
        ).arrange(RIGHT, buff=0.05).to_edge(UP, buff=1.0)

        self.play(FadeIn(pesa), run_time=0.5)

        fila_1 = cap_width(MathTex(r"F=50\,N,\ d=2\,m \rightarrow W=100\,J").scale(0.62))
        fila_2 = cap_width(MathTex(r"F=100\,N,\ d=2\,m \rightarrow W=200\,J").scale(0.62))
        fila_3 = cap_width(MathTex(r"F=100\,N,\ d=4\,m \rightarrow W=400\,J").scale(0.62))
        filas = VGroup(fila_1, fila_2, fila_3).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        filas.next_to(pesa, DOWN, buff=0.6)

        self.play(Write(fila_1), run_time=0.9)
        self.wait(0.8)
        marco_1 = SurroundingRectangle(fila_2, color=YELLOW, buff=0.12)
        self.play(Write(fila_2), run_time=0.9)
        self.play(Create(marco_1), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(marco_1))

        marco_2 = SurroundingRectangle(fila_3, color=YELLOW, buff=0.12)
        self.play(Write(fila_3), run_time=0.9)
        self.play(Create(marco_2), run_time=0.4)
        self.wait(2.0)

        self.play(FadeOut(pesa), FadeOut(filas), FadeOut(marco_2))
        self.wait(1.0)

    # ------------------------------------------------------------------
    # 0:38 - 0:52  Comparacion de caminos: rampa vs vertical
    # ------------------------------------------------------------------
    def comparar_caminos(self):
        self.play(FadeIn(self.escenario), run_time=0.6)

        # Se crean aqui, a partir de la posicion EN VIVO de rampa/camino
        # vertical (ya escalados y movidos por hook()/plantear_problema()).
        self.caja_vertical = self.caja_rampa.copy()
        self.caja_vertical.next_to(self.camino_vertical.get_start(), UP, buff=0)
        self.linea_misma_altura = DashedLine(
            self.camino_vertical.get_end(), self.rampa.get_end(), color=GREY_B, stroke_width=2,
        )
        self.play(FadeIn(self.linea_misma_altura), FadeIn(self.caja_vertical), run_time=0.5)

        # --- Camino 1: rampa -------------------------------------------------
        etiqueta_f_rampa = cap_width(MathTex(f"F = {F_RAMPA:.0f}\\,N", color=COLOR_FUERZA).scale(0.6))
        etiqueta_f_rampa.next_to(self.rampa.get_center(), UP, buff=0.15)

        self.play(Write(etiqueta_f_rampa), run_time=0.6)
        self.play(
            self.caja_rampa.animate.move_to(self.rampa.get_end() + self.normal_rampa() * 0.21),
            run_time=1.4,
        )

        w_rampa_tracker = ValueTracker(0)
        w_rampa_num = always_redraw(
            lambda: DecimalNumber(w_rampa_tracker.get_value(), unit="\\,J", color=COLOR_ENERGIA)
            .scale(0.7).to_edge(UP, buff=1.0).shift(LEFT * 1.1)
        )
        self.add(w_rampa_num)
        self.play(w_rampa_tracker.animate.set_value(W_RAMPA), run_time=1.2, rate_func=rush_into)
        self.wait(0.6)

        # --- Camino 2: vertical ----------------------------------------------
        etiqueta_f_vertical = cap_width(MathTex(f"F = {PESO:.0f}\\,N", color=COLOR_PESO).scale(0.6))
        etiqueta_f_vertical.next_to(self.camino_vertical.get_center(), RIGHT, buff=0.15)

        self.play(Write(etiqueta_f_vertical), run_time=0.6)
        self.play(
            self.caja_vertical.animate.move_to(self.camino_vertical.get_end() + DOWN * 0.3),
            run_time=1.0,
        )
        self.wait(0.3)

        w_vertical_tracker = ValueTracker(0)
        w_vertical_num = always_redraw(
            lambda: DecimalNumber(w_vertical_tracker.get_value(), unit="\\,J", color=COLOR_ENERGIA)
            .scale(0.7).to_edge(UP, buff=1.0).shift(RIGHT * 1.1)
        )
        self.add(w_vertical_num)
        self.play(w_vertical_tracker.animate.set_value(W_VERTICAL), run_time=1.2, rate_func=rush_into)
        self.wait(0.6)

        marco = SurroundingRectangle(VGroup(w_rampa_num, w_vertical_num), color=YELLOW, buff=0.25)
        igual = cap_width(Text("¡el mismo trabajo!", font_size=26, color=YELLOW, weight=BOLD))
        igual.next_to(marco, DOWN, buff=0.4)

        self.play(Create(marco), run_time=0.5)
        self.play(
            Write(igual),
            Flash(marco.get_center(), color=YELLOW, flash_radius=1.2, line_length=0.4),
            Indicate(self.escenario, scale_factor=1.04, color=YELLOW),
            run_time=0.9,
        )
        self.wait(2.2)

        self.play(
            FadeOut(etiqueta_f_rampa), FadeOut(etiqueta_f_vertical), FadeOut(w_rampa_num),
            FadeOut(w_vertical_num), FadeOut(marco), FadeOut(igual),
        )
        self.wait(2.0)

    # ------------------------------------------------------------------
    # 0:52 - 1:02  Energia potencial (la formula llega al final)
    # ------------------------------------------------------------------
    def energia_potencial(self):
        self.play(FadeOut(self.escenario), FadeOut(self.linea_misma_altura), FadeOut(self.caja_vertical))

        frase = cap_width(Text(
            "La energía no sabe\nqué camino tomaste",
            font_size=28, weight=BOLD, line_spacing=1.1,
        )).to_edge(UP, buff=1.1)
        self.play(Write(frase), run_time=1.0)
        self.wait(1.5)

        formula_pe = cap_width(MathTex(r"PE = \text{Peso} \times h = mgh").scale(0.85))
        formula_pe.next_to(frase, DOWN, buff=0.7)
        self.play(Write(formula_pe), run_time=1.0)
        self.wait(1.0)

        # Se agrega una segunda linea a la tarjeta de formulas (sigue en la
        # esquina desde definir_trabajo()).
        mini_pe = MathTex(r"PE = mgh", color=COLOR_ENERGIA).scale(0.5)
        mini_w_copia = self.formula_card[1].copy()
        grupo_texto = VGroup(mini_w_copia, mini_pe).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        fondo_nuevo = SurroundingRectangle(grupo_texto, color=YELLOW, buff=0.15)
        tarjeta_nueva = VGroup(fondo_nuevo, grupo_texto).to_corner(UR, buff=0.4)

        self.play(
            FadeOut(self.formula_card),
            TransformFromCopy(formula_pe, mini_pe),
            FadeIn(fondo_nuevo), FadeIn(mini_w_copia),
            run_time=0.9,
        )
        self.formula_card = tarjeta_nueva
        self.wait(0.2)

        joule = cap_width(MathTex(r"1\ J = 1\ N \cdot 1\ m").scale(0.7))
        joule.next_to(formula_pe, DOWN, buff=0.6)
        self.play(FadeIn(joule, shift=UP * 0.2), run_time=0.7)
        self.wait(2.3)

        self.play(FadeOut(frase), FadeOut(formula_pe), FadeOut(joule))
        self.wait(1.0)

    # ------------------------------------------------------------------
    # 1:02 - 1:12  Estrategia resumida
    # ------------------------------------------------------------------
    def estrategia(self):
        titulo = cap_width(Text("Solo importa\nla altura", font_size=30, weight=BOLD))
        titulo.to_edge(UP, buff=1.1)

        pasos = VGroup(
            Text("1. Fuerza aplicada\n× distancia", font_size=22, line_spacing=1.0),
            Text("2. Eso es el\ntrabajo realizado", font_size=22, line_spacing=1.0),
            Text("3. Si solo cambia la\naltura, es energía\npotencial ganada", font_size=22, line_spacing=1.0),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        cap_width(pasos)

        flechas = VGroup(*[
            Arrow(pasos[i].get_bottom(), pasos[i + 1].get_top(), buff=0.1, stroke_width=3, color=YELLOW)
            for i in range(len(pasos) - 1)
        ])

        self.play(Write(titulo), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in pasos], lag_ratio=0.4), run_time=1.6)
        self.play(*[GrowArrow(f) for f in flechas], run_time=0.6)
        self.wait(5.5)

        self.play(FadeOut(titulo), FadeOut(pasos), FadeOut(flechas))

    # ------------------------------------------------------------------
    # 1:12 - 1:22  Reto final
    # ------------------------------------------------------------------
    def reto_final(self):
        reto_titulo = cap_width(Text("TU RETO 🧠", font_size=36, weight=BOLD, color=YELLOW)).to_edge(UP, buff=1.2)

        caja_grande = Square(side_length=0.6, color=WHITE, fill_color=COLOR_CAJA, fill_opacity=0.95)
        interrogante = cap_width(MathTex("?", color=YELLOW).scale(1.4))
        interrogante.next_to(caja_grande, UP, buff=0.15)
        caja_grupo = VGroup(caja_grande, interrogante).next_to(reto_titulo, DOWN, buff=0.6)

        reto_texto = cap_width(Text(
            "Si esta caja pesara\n450 N en vez de 300,\n¿qué fuerza necesitas\npara subirla por la\nmisma rampa a\nvelocidad constante?",
            font_size=24, line_spacing=1.15,
        )).next_to(caja_grupo, DOWN, buff=0.5)

        self.play(Write(reto_titulo), run_time=0.6)
        self.play(FadeIn(caja_grupo, scale=1.3, rate_func=rate_functions.ease_out_back), run_time=0.7)
        self.play(FadeIn(reto_texto, shift=UP * 0.2), run_time=0.8)
        self.wait(3.5)

        self.play(
            FadeOut(reto_titulo), FadeOut(caja_grupo), FadeOut(reto_texto),
            FadeOut(self.formula_card),
        )

    # ------------------------------------------------------------------
    # 1:22 - 1:26  Cierre
    # ------------------------------------------------------------------
    def cierre(self):
        cierre_texto = cap_width(Text(
            "Física en 60s — Parte 5 🔥\nSígueme para más física 👀",
            font_size=24, line_spacing=1.2,
        ))
        self.play(FadeIn(cierre_texto, scale=1.1, rate_func=rate_functions.ease_out_back), run_time=0.8)
        self.wait(3.2)


def dir_rampa(punto_base, punto_alto):
    """Vector unitario a lo largo de la rampa, apuntando cuesta ARRIBA."""
    v = np.array(punto_alto) - np.array(punto_base)
    return v / np.linalg.norm(v)
