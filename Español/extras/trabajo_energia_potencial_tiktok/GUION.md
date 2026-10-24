# "La caja que engaña tu intuición" — Guion y ficha de producción

Video corto de física (Trabajo mecánico y Energía Potencial Gravitatoria) para TikTok/Reels/Shorts, producido con **Manim Community Edition**, renderizado en vertical 9:16. Quinta entrega de la serie — primera que sale de la 2ª ley de Newton (fuerzas) para entrar a Trabajo y Energía.

Decisiones ya tomadas con el usuario:
- Motor: **ManimCE**, siguiendo el mismo pipeline que los 4 videos anteriores de la serie.
- Formato: **explicativo medio, 75–90 s**.
- Enfoque pedagógico: **estilo "Hewitt-Drew-it!" (Paul Hewitt, Física Conceptual)** — intuición cotidiana antes del diagrama técnico, razonamiento proporcional explícito, la fórmula aparece como "etiqueta" de algo ya entendido (no como punto de partida), y cierre con una pregunta real sin resolver.
- Escenario propio (no el de Hewitt): una caja en una mudanza, subida por una rampa a un camión vs. levantada directo — mismo tipo de "sorpresa" pedagógica (el trabajo no depende del camino), pero con nuestros propios números y nuestra propia narrativa visual.

---

## 0. Ficha técnica rápida

| Parámetro | Valor |
|---|---|
| Resolución | 1080×1920 px (9:16) |
| FPS | 30 |
| Duración objetivo | 80–88 s |
| Motor | Manim Community Edition ≥ 0.18 |
| Escena principal | `TrabajoEnergiaPotencialTikTok` (`trabajo_energia_potencial_tiktok.py`) |
| Audio | Voz en off (TTS local o edge-tts) + música instrumental de fondo |
| Paleta de color física | Peso = rojo (`RED`), Fuerza aplicada = azul (`BLUE`), Trabajo/Energía = naranja (`ORANGE`), Trayectoria/rampa = verde (`GREEN`) — mismo código de color que el resto de la serie |

**Problema numérico fijo (verificado a mano antes de animar):**

```
Caja de mudanza: Peso = 300 N  (m = 30 kg, g = 10 m/s²)
Camión: altura de la plataforma h = 4 m
Rampa: longitud L = 10 m  →  sinθ = h/L = 0.4  →  θ = arcsin(0.4) ≈ 23.6°

Caso 1 — Rampa (sin fricción, velocidad constante):
  F_rampa = Peso · sinθ = 300 × 0.4 = 120 N
  W_rampa = F_rampa × L = 120 × 10 = 1200 J

Caso 2 — Levantar derecho:
  W_vertical = Peso × h = 300 × 4 = 1200 J

→ 1200 J = 1200 J. Mismo trabajo, caminos distintos. Depende solo de h.

Energía potencial ganada:  PE = Peso × h = m·g·h = 300 × 4 = 1200 J  (coincide con W)

Demo de proporcionalidad (ejemplo aparte, abstracto, con una pesa genérica):
  F=50 N, d=2 m  → W=100 J
  F=100 N, d=2 m → W=200 J   (doble fuerza, misma distancia → doble trabajo)
  F=100 N, d=4 m → W=400 J   (doble fuerza Y doble distancia → 4× el trabajo)

Reto final (NO se resuelve en el video):
  Caja más pesada: Peso' = 450 N (m'=45 kg), misma rampa (L=10 m, h=4 m, sinθ=0.4)
  F' = Peso' · sinθ = 450 × 0.4 = 180 N   (queda como pregunta para el espectador)
```

---

## 1. Introducción llamativa (Hook, 0:00–0:08)

**Regla de oro TikTok: el gancho debe entenderse en los primeros 1-2 segundos solo con el texto en pantalla, sin depender del audio.**

**Animación:** una caja junto a un camión de mudanza con la plataforma elevada. Dos trayectorias posibles ya dibujadas y parpadeando: una rampa diagonal (verde) y una flecha vertical recta (roja) hasta la plataforma. Signo de interrogación grande entre ambas.

**Texto en pantalla:** "¿Subir esta caja por la rampa cuesta MENOS trabajo que levantarla derecho?"

**Narración (VO):**
> "¿Subir esta caja por la rampa cuesta menos trabajo que levantarla directo hacia arriba? Tu intuición te va a engañar."

**Caption quemado:** `¿RAMPA = MENOS TRABAJO?`

---

## 2. Guion completo con timeline

| Tiempo | En pantalla / animación Manim | Narración (VO) | Caption quemado |
|---|---|---|---|
| 0:00–0:08 | Caja + camión + rampa (verde) y flecha vertical (roja) ya dibujados. `Wiggle` en el signo de interrogación. | "¿Subir esta caja por la rampa cuesta menos trabajo que levantarla directo hacia arriba? Tu intuición te va a engañar." | ¿RAMPA = MENOS TRABAJO? |
| 0:08–0:16 | `Write` de los datos: Peso=300N, h=4m (altura del camión), L=10m (longitud de rampa). Flechas señalan cada medida sobre el dibujo. | "Esta caja pesa 300 newtons. El camión está a 4 metros de altura, y la rampa mide 10 metros de largo." | 300 N · h=4m · L=10m |
| 0:16–0:26 | Aparece la definición `W = F · d` en grande, con una flecha azul (fuerza aplicada) empujando la caja sobre la rampa una distancia corta, animada con `MoveAlongPath`. | "El trabajo en física es la fuerza que aplicas, multiplicada por la distancia que recorres empujando en esa dirección." | TRABAJO = FUERZA × DISTANCIA |
| 0:26–0:38 | Ejemplo aparte con una pesa genérica (ícono simple), fuera del camión: `F=50N,d=2m→100J`, luego `F=100N,d=2m→200J` (ambos con `DecimalNumber` animado), luego `F=100N,d=4m→400J`. `SurroundingRectangle` resalta cada relación. | "Si duplicas la fuerza con la misma distancia, el trabajo se duplica. Pero si además duplicas la distancia, el trabajo se multiplica por cuatro." | 2× fuerza = 2× trabajo · 2× ambos = 4× |
| 0:38–0:52 | Vuelve el camión. Caja sube por la rampa: `F_rampa=120N` (calculada en pantalla desde `Peso·sinθ`), `W_rampa = 120×10 = 1200J`. Luego, lado a lado, la caja sube derecho: `W_vertical = 300×4 = 1200J`. `Flash` + `SurroundingRectangle` amarillo igualando ambos resultados. | "Por la rampa, la fuerza necesaria es menor, 120 newtons, pero caminas más: 10 metros. El trabajo da 1200 joules. Levantándola derecho, la fuerza es mayor, pero el camino es más corto. El trabajo... también da 1200 joules." | 1200 J = 1200 J 😮 |
| 0:52–1:02 | Texto "la energía no sabe qué camino tomaste" aparece. Se etiqueta el resultado como `PE = Peso × h = m·g·h`, con la unidad `1 J = 1 N·m` apareciendo junto a un ícono simple. | "Esa energía que ganó la caja se llama energía potencial gravitatoria: peso por altura. Y se mide en joules — un joule es el trabajo de 1 newton a lo largo de 1 metro." | PE = m·g·h |
| 1:02–1:12 | Mini diagrama de flujo de 3 pasos: 1) Mide la fuerza aplicada y la distancia 2) Multiplícalas → trabajo 3) Si solo cambia la altura, ese trabajo es la energía potencial ganada. | "Por eso no importa si empujas por una rampa larga o levantas directo: lo único que determina la energía ganada es el cambio de altura." | SOLO IMPORTA LA ALTURA |
| 1:12–1:22 | Camión y rampa vuelven, pero ahora con una caja más grande/oscura. Signo de interrogación sobre su peso. | "Tu reto: si esta caja pesara 450 newtons en vez de 300, ¿qué fuerza necesitarías para subirla por la misma rampa a velocidad constante? Coméntalo abajo." | 🧠 RETO: CAJA DE 450 N |
| 1:22–1:26 | Cierre con marca de serie ("Física en 60s — Parte 5") y llamada a seguir. | (silencio o música sube) | Sígueme para más física 👀 |

Duración total: **~86 s**.

---

## 3. Aspectos teóricos clave (los que el video *debe* dejar claros)

1. **Definición de trabajo mecánico:** `W = F·d`, donde `F` es la componente de la fuerza en la dirección del desplazamiento. Es la puerta de entrada al concepto de energía.
2. **El trabajo es proporcional a fuerza y a distancia por separado:** duplicar una variable duplica el trabajo; duplicar ambas lo multiplica por cuatro. Es razonamiento proporcional, no memorización de la fórmula.
3. **Independencia del camino (para fuerzas conservativas sin fricción):** subir una caja por una rampa larga con poca fuerza, o levantarla directo con más fuerza y menos distancia, produce exactamente el mismo trabajo si la altura final es la misma. Esto es la idea central del video y el "momento sorpresa".
4. **Energía como capacidad de realizar trabajo:** el trabajo hecho sobre un objeto se convierte en energía que ese objeto adquiere (y que puede luego transferir o transformar).
5. **Energía potencial gravitatoria:** `PE = m·g·h` (equivalente a `Peso × h`). Depende solo de la altura respecto a un nivel de referencia, no de la trayectoria recorrida para llegar ahí.
6. **Unidad Joule:** `1 J = 1 N · 1 m`. Útil para que el espectador entienda de dónde sale la unidad, no solo que "así se llama".

---

## 4. Estrategia de resolución (metodología replicable)

1. **Identifica la fuerza aplicada en la dirección del movimiento** y la distancia recorrida en esa misma dirección.
2. **Multiplica fuerza × distancia** para obtener el trabajo realizado.
3. **Si el único cambio relevante es la altura**, ese trabajo equivale a la energía potencial ganada: `PE = Peso × h`.
4. **Compara caminos distintos con el mismo cambio de altura** para verificar: si no hay fricción, el trabajo total debe coincidir — es una forma de comprobar que el problema está bien planteado.

---

## 5. Instrucciones precisas de animación en Manim

- Reutilizar el código de color de la serie: Peso = `RED`, Fuerza aplicada = `BLUE`, Trabajo/Energía = `ORANGE`, Trayectoria/rampa = `GREEN`. Nunca reasignar un color a otro concepto distinto al de los videos anteriores.
- Formato vertical real: `config.pixel_width = 1080`, `config.pixel_height = 1920` antes de definir la escena.
- Todo texto y fórmula pasa por `cap_width()`/`cap_size()` (ver SKILL.md sección 4.1) — especialmente la comparación `1200 J = 1200 J` y la definición `W = F·d`, que deben verse grandes sin desbordar el frame angosto.
- **Nunca usar `TransformMatchingTex` entre fórmulas sin sub-expresiones compartidas** (p. ej. de `W=F·d` a `PE=mgh` son conceptualmente relacionadas pero tipográficamente distintas) — usar `FadeOut`+`FadeIn` explícitos, como se documentó tras los bugs de los videos 1-4.
- **`DecimalNumber` + `ValueTracker`** para el conteo animado de 0 a 1200 J en ambos casos (rampa y vertical), sincronizados para que el espectador vea literalmente que llegan al mismo número.
- **`MoveAlongPath`** para la caja subiendo la rampa (trayectoria diagonal) y una animación recta separada para el levantamiento vertical — mostrar ambas una junto a la otra (`VGroup` partido en dos mitades de pantalla) en el momento de la comparación clave (0:38–0:52).
- Cualquier mobject creado con `always_redraw` (si se usa para la flecha de fuerza variable) debe añadirse explícitamente a la escena — bug ya documentado en la serie.
- Zonas seguras: nada importante en el 12% superior ni el 15% inferior del frame.

---

## 6. Conclusión (texto exacto para pantalla y VO)

**Pantalla:** *"Trabajo = Fuerza × Distancia → Si solo cambia la altura, eso ES la energía potencial"*

**VO:**
> "Por eso no importa si empujas por una rampa larga o levantas directo: lo único que determina la energía ganada es el cambio de altura."

---

## 7. Reto final / preguntas para seguir aprendiendo

**Reto principal (en pantalla + VO):**
> "Tu reto: si esta caja pesara 450 newtons en vez de 300, ¿qué fuerza necesitarías para subirla por la misma rampa a velocidad constante? Coméntalo abajo."

(No se revela la respuesta en este video — queda para generar retención hacia la siguiente entrega de la serie.)

**Preguntas adicionales para pie/comentarios (elige 1–2):**
- Si la rampa fuera más larga pero la altura del camión no cambia, ¿la energía potencial ganada cambia? (spoiler: no — solo cambia la fuerza necesaria)
- ¿Qué pasaría con el trabajo si la rampa tuviera fricción? (gancho natural hacia conectar esta serie con la de fricción ya publicada)

---

## 8. Especificaciones para publicar en TikTok

- Formato: MP4, vertical 1080×1920, sin bordes negros.
- Duración: 80–88 s.
- Subtítulos quemados: sí, mismo estilo que el resto de la serie (sans-serif bold, alto contraste, 2-5 palabras por línea).
- Portada (cover): el frame de la comparación `1200 J = 1200 J` (segundo ~0:50) — es el momento de mayor sorpresa visual.
- Música: instrumental de fondo, bajo volumen, con un pequeño impacto en el segundo 0:44 (cuando se revela que ambos trabajos coinciden).
- Hashtags sugeridos: `#Fisica #FisicaFacil #TrabajoYEnergia #EnergiaPotencial #Newton #Manim #CienciaTikTok #ClaseDeFisica #AprendeEnTikTok #FisicaConceptual`

---

## 9. Checklist antes de publicar

- [ ] Duración final dentro de 80-88 s
- [ ] Resolución 1080×1920, sin franjas negras
- [ ] Hook comprensible con el sonido apagado
- [ ] Ningún texto cortado en los bordes (revisado con contact sheet, no solo leyendo el código)
- [ ] Ningún mobject "fantasma" (Write sin su FadeOut correspondiente)
- [ ] Números coherentes entre guion, animación y VO (300 N / 4 m / 10 m / 120 N / 1200 J)
- [ ] CTA + pregunta de reto presentes en el cierre

---

## 10. Nota de estilo (por qué está ordenado así, no como un libro de texto)

Este guion invierte el orden "clásico" (diagrama técnico → fórmula → ejemplo numérico) por el orden conceptual de Hewitt: analogía cotidiana (mudanza) → definición en palabras simples → razonamiento proporcional con números pequeños → el resultado sorprendente como clímax → la fórmula aparece *después*, como una forma corta de nombrar lo que ya se entendió → cierre con una pregunta real, no solo un dato curioso. La fórmula `PE = mgh` no aparece hasta el minuto 0:52, después de que el espectador ya vio con sus propios ojos que 1200 J = 1200 J por dos caminos distintos.
