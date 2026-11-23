# "El ángulo que despierta la fricción" — Guion y ficha de producción

Video corto de física (2ª ley de Newton + fricción estática/cinética) para TikTok/Reels/Shorts, producido con **Manim Community Edition**, renderizado en vertical 9:16.

Decisiones ya tomadas con el usuario:
- Motor: **ManimCE** (moderno, `pip install manim`). El resto del curso usa la versión antigua de 3b1b (`big_ol_pile_of_manim_imports`); este proyecto es independiente y no depende de esos módulos.
- Formato: **explicativo medio, 60–90 s** (duración objetivo: **~76 s**).
- Escenario físico: **plano inclinado con fricción** (estática → cinética).
- Producción: incluye **guion de narración en voz en off** con timing.

---

## 0. Ficha técnica rápida

| Parámetro | Valor |
|---|---|
| Resolución | 1080×1920 px (9:16) |
| FPS | 30 (`-qh`, `--fps 30`) |
| Duración objetivo | 74–78 s |
| Motor | Manim Community Edition ≥ 0.18 |
| Escena principal | `DinamicaFriccionTikTok` (`dinamica_friccion_tiktok.py`) |
| Audio | Voz en off (grabada o TTS) + música instrumental de fondo, mezclada en edición externa (no en Manim) |
| Subtítulos | Quemados en video (burned-in), sincronizados a la VO |
| Paleta de color física | Peso = rojo (`RED`), Normal = azul (`BLUE`), Fricción = verde (`GREEN`), Fuerza neta/aceleración = naranja (`ORANGE`), texto de apoyo = blanco/amarillo |

**Problema numérico fijo (para que teoría y animación coincidan exactamente):**

- Bloque: `m = 2 kg`, `g = 9.8 m/s²`
- Coeficientes: `μs = 0.6` (estático), `μk = 0.4` (cinético)
- Ángulo 1: `θ = 30°` → el bloque **no** desliza (margen pequeño, tensión dramática)
- Ángulo 2: `θ = 35°` → el bloque **sí** desliza, se calcula la aceleración

Verificación (para que el guion sea físicamente correcto):

```
θ = 30°:  mg·sinθ = 9.80 N   |  μs·mg·cosθ = 10.19 N   → 9.80 < 10.19 → NO desliza
θ = 35°:  mg·sinθ = 11.24 N  |  μs·mg·cosθ = 9.63 N    → 11.24 > 9.63  → SÍ desliza
          f_k = μk·mg·cosθ = 6.42 N
          a = (mg·sinθ − f_k)/m = (11.24 − 6.42)/2 ≈ 2.41 m/s²
Ángulo crítico: θc = arctan(μs) = arctan(0.6) ≈ 30.96°  (el "reto" final)
```

Este par de ángulos (30° casi no desliza, 35° sí) es lo que genera el gancho: existe un **ángulo crítico** exacto donde el bloque pasa de estático a dinámico.

---

## 1. Introducción llamativa (Hook, 0:00–0:06)

**Regla de oro TikTok: el 100% del gancho debe pasar en los primeros 2 segundos, en pantalla, sin depender del audio** (mucha gente ve sin sonido). Por eso el texto del hook debe aparecer escrito y grande simultáneo a la voz.

**Animación:** el plano inclinado y el bloque ya están dibujados desde el frame 0 (sin intro lenta). Un contador de ángulo (`DecimalNumber`) sube rápido de 0° a 30° mientras el bloque tiembla levemente (`Wiggle`) pero no se mueve.

**Texto en pantalla (grande, centrado):** "¿Qué ángulo hace que este bloque pase de quieto... a acelerar de golpe?"

**Narración (VO):**
> "¿Qué ángulo exacto hace que este bloque pase de estar completamente quieto... a acelerar de golpe?"

**Caption quemado (corto, sincronizado):** `¿QUÉ ÁNGULO...` → `...LO HACE ACELERAR?`

---

## 2. Guion completo con timeline

| Tiempo | En pantalla / animación Manim | Narración (VO) | Caption quemado |
|---|---|---|---|
| 0:00–0:06 | Plano inclinado + bloque ya listos. Contador de ángulo sube a 30°. `Wiggle` en el bloque. | "¿Qué ángulo exacto hace que este bloque pase de estar completamente quieto... a acelerar de golpe?" | ¿QUÉ ÁNGULO LO HACE ACELERAR? |
| 0:06–0:16 | `Write` de los datos del problema en tarjeta lateral: m=2kg, μs=0.6, μk=0.4. Flecha señala el bloque. | "Tenemos un bloque de 2 kilos sobre un plano inclinado, con fricción estática de 0.6 y cinética de 0.4." | m=2kg · μs=0.6 · μk=0.4 |
| 0:16–0:26 | Zoom tipo "cámara" al bloque → aparece el Diagrama de Cuerpo Libre (DCL). `Create` de vectores: Peso (rojo, hacia abajo), Normal (azul, perpendicular al plano), Fricción (verde, sobre el plano). | "Para saber si se mueve, dibujamos el diagrama de cuerpo libre: peso, normal y fricción." | 🔴 Peso 🔵 Normal 🟢 Fricción |
| 0:26–0:36 | `TransformMatchingTex`: el vector Peso se descompone en dos componentes punteadas: `mg·sinθ` (paralela al plano) y `mg·cosθ` (perpendicular). | "El peso se descompone en dos partes: una lo empuja plano abajo, y la otra lo aprieta contra la superficie." | mg·senθ ↓ · mg·cosθ → |
| 0:36–0:46 | Aparece la desigualdad `mg·sinθ  vs  μs·mg·cosθ`. Se sustituyen los números con efecto de "conteo" (`DecimalNumber` animado): 9.8 N vs 10.19 N. `SurroundingRectangle` amarillo en el resultado. Bloque queda con borde verde (quieto). | "A 30 grados, la fuerza que lo empuja es de 9.8 newtons, pero la fricción estática máxima aguanta 10.19. Por muy poco... no se mueve." | 9.8 N < 10.19 N → NO desliza |
| 0:46–0:58 | El plano gira de 30° a 35° (`Rotate`, animado y suave). Se repite la comparación: ahora `11.24 N > 9.63 N`. El bloque cambia a borde rojo/naranja y `Indicate` + empieza a deslizar con `MoveAlongPath` sobre el plano. Aparece la 2ª ley de Newton: `ΣF = m·a` → `mg·sinθ − μk·mg·cosθ = m·a`. | "Pero si inclinamos solo 5 grados más, a 35, la fuerza ya supera a la fricción estática. Ahora usamos la segunda ley de Newton con la fricción cinética..." | 11.24 N > 9.63 N → ¡DESLIZA! |
| 0:58–1:03 | El resultado `a ≈ 2.41 m/s²` aparece en grande con `Write` + `Flash`. El bloque acelera visiblemente plano abajo, con vector de aceleración naranja creciendo. | "...y el bloque acelera a 2.41 metros por segundo, cada segundo." | a ≈ 2.41 m/s² |
| 1:03–1:13 | Se reduce todo a un mini-diagrama de flujo de 3 pasos (`VGroup` con flechas): 1) DCL → 2) Comparar F vs fricción máxima → 3) 2ª ley con μ correspondiente. | "Esta es la estrategia para cualquier problema de fricción: diagrama de cuerpo libre, comparas con la fricción estática máxima, y si se mueve, aplicas la segunda ley con la cinética." | DCL → Comparar → 2ª Ley |
| 1:13–1:22 | Texto de reto en pantalla, plano vuelve a 30° con un signo de interrogación grande sobre el ángulo. | "Tu reto: ¿cuál es el ángulo crítico exacto en el que este bloque empieza a deslizar? Coméntalo abajo — en la parte 2 lo resolvemos." | 🧠 RETO: ¿ÁNGULO CRÍTICO? |
| 1:22–1:24 | Cierre con marca/serie ("Física en 60s — Parte 1/2") y llamada a seguir. | (silencio o música sube) | Sígueme para la Parte 2 👀 |

Duración total: **~84 s** incluyendo el cierre (ajustable a 76–80 s recortando el paso 0:16–0:26 si se necesita más corto).

---

## 3. Aspectos teóricos clave (los que el video *debe* dejar claros)

1. **2ª Ley de Newton:** `ΣF = m·a`. Todo el video es una aplicación directa: se identifican todas las fuerzas, se proyectan sobre los ejes del plano inclinado (paralelo/perpendicular), y se resuelve para la incógnita.
2. **Fuerza normal en un plano inclinado:** `N = mg·cosθ`. Es la que "aprieta" al bloque contra la superficie y de la que depende la fricción.
3. **Fricción estática (antes de moverse):** se opone al deslizamiento inminente, es **variable** (no siempre vale `μs·N`), y solo alcanza su **valor máximo** `f_s,max = μs·N` justo en el instante en que el objeto está a punto de deslizar. Mientras `F_aplicada ≤ f_s,max`, el sistema permanece en equilibrio (`a = 0`).
4. **Fricción cinética (ya en movimiento):** una vez que desliza, la fricción se vuelve prácticamente constante: `f_k = μk·N`, y típicamente `μk < μs` (por eso cuesta más "arrancar" un objeto que mantenerlo en movimiento).
5. **Ángulo crítico (condición de deslizamiento):** el punto exacto donde `mg·sinθ = μs·mg·cosθ` simplifica a `tanθc = μs`, es decir, **el ángulo crítico depende solo del coeficiente estático, no de la masa**. Esto es matemáticamente elegante y es el gancho perfecto para el reto final.
6. **Ligadura/vínculo del plano:** el bloque está restringido a moverse (o no) *sobre* la superficie del plano — de ahí que se trabaje en un sistema de ejes rotado (paralelo/perpendicular al plano) en vez de horizontal/vertical puro. Esto es la idea de "fuerza de contacto/ligadura" que pidió el usuario: la normal y la fricción son las dos fuerzas de contacto que el plano ejerce sobre el bloque.

---

## 4. Estrategia de resolución (metodología replicable, mostrada como "fórmula" reutilizable)

1. **Dibuja el DCL** — identifica *todas* las fuerzas de contacto (normal, fricción) y de acción a distancia (peso).
2. **Elige ejes convenientes** — paralelo y perpendicular a la superficie de contacto (no siempre horizontal/vertical).
3. **Descompón el peso** en esos ejes: `mg·sinθ` (paralelo) y `mg·cosθ` (perpendicular).
4. **Calcula la normal** desde el equilibrio perpendicular: `N = mg·cosθ` (si no hay otras fuerzas verticales).
5. **Compara la fuerza que intenta mover el objeto contra la fricción estática máxima** (`μs·N`). Si es menor o igual → sistema en reposo, `a = 0`. Si es mayor → el objeto se mueve.
6. **Si se mueve, cambia a fricción cinética** (`μk·N`, μk < μs) y aplica la 2ª ley de Newton sobre el eje de movimiento para hallar `a`.

Este bloque de 6 pasos es el que se muestra comprimido en el minuto 1:03–1:13 como "fórmula para cualquier problema de fricción" — es el valor pedagógico central del video y lo que lo hace reutilizable como plantilla para una serie.

---

## 5. Instrucciones precisas de animación en Manim (nivel de detalle)

Objetivo: que la animación *sea* la explicación, no una ilustración decorativa. Reglas concretas:

- **Código de color fijo y consistente** en todo el video (definido arriba): rojo=peso, azul=normal, verde=fricción, naranja=neta/aceleración. Nunca reasignar un color a otro concepto.
- **`TransformMatchingTex`** para pasar de la ecuación general (`ΣF = ma`) a la ecuación sustituida con números — así el espectador *ve* de dónde sale cada término, no un corte seco.
- **`Create`/`GrowArrow`** para cada vector de fuerza, uno a la vez, con una pausa corta (`self.wait(0.3)`) entre cada uno — nunca todos a la vez la primera vez que aparecen.
- **`Angle` mobject** para dibujar el arco del ángulo θ en el plano, con su `MathTex` de etiqueta pegado (`.next_to`).
- **`DecimalNumber` + `ValueTracker`** para animar el conteo de 0 a 9.8 N y de 0 a 10.19 N (efecto "contador subiendo") en vez de que el número aparezca estático — genera tensión visual antes de la comparación.
- **`SurroundingRectangle` + `Flash`** en el instante del resultado clave (desliza / no desliza) para marcar el "momento de pago" visualmente, sincronizado con el pico de la narración.
- **Zoom simulado** (no cámara 3D, es innecesario aquí): agrupar el bloque+DCL en un `VGroup` y usar `.animate.scale(...).move_to(ORIGIN)` para simular acercamiento al DCL en el segundo 0:16.
- **Rotación real del plano** (`Rotate` sobre el `VGroup` del plano inclinado) al pasar de 30° a 35°, con el bloque como hijo del mismo grupo para que se mueva junto con la superficie — refuerza físicamente que estamos cambiando la geometría real, no solo el número.
- **Todo el texto explicativo secundario entra y sale rápido** (`FadeIn`/`FadeOut` con `run_time≤0.4`) para mantener el ritmo típico de TikTok; solo las fórmulas centrales se quedan en pantalla más de 2 segundos.
- **Formato vertical real**, no un video horizontal recortado: configurar `config.pixel_width = 1080`, `config.pixel_height = 1920` *antes* de definir la escena, y diseñar el layout pensando en una columna angosta (frame_width ≈ 4.5 unidades de Manim).
- **Zonas seguras (safe zones):** no colocar texto ni elementos clave en el 12% superior ni el 15% inferior del frame (ahí TikTok superpone usuario, descripción, botones de interacción, barra de sonido).

---

## 6. Conclusión (texto exacto para pantalla y VO)

**Pantalla:** *"DCL → Compara con fricción estática máxima → 2ª Ley con la fricción correcta"*

**VO:**
> "Esta es la estrategia para cualquier problema de fricción: haces el diagrama de cuerpo libre, comparas la fuerza aplicada con la fricción estática máxima, y si se mueve, aplicas la segunda ley de Newton con la fricción cinética."

---

## 7. Reto final / preguntas para seguir aprendiendo (engagement)

**Reto principal (en pantalla + VO):**
> "Tu reto: ¿cuál es el ángulo crítico exacto en el que este bloque empieza a deslizar? Coméntalo abajo — en la parte 2 lo resolvemos."

(Pista visual: `tanθc = μs` aparece semi-transparente un instante, sin resolverla — la resolución completa queda para el video de la "parte 2", generando retención de audiencia.)

**Preguntas adicionales para pie/comentarios (elige 1–2, no todas, para no saturar):**
- ¿Qué pasa si el bloque ya está en movimiento y el plano se vuelve *menos* inclinado? ¿en qué ángulo se detiene?
- Si duplicas la masa del bloque, ¿cambia el ángulo crítico? (spoiler: no — buen segundo reto)
- ¿Qué pasaría si en vez de fricción hubiera una cuerda y una polea sosteniendo el bloque? (gancho natural hacia el escenario de ligaduras con polea, ideal para "Parte 3")

---

## 8. Especificaciones para publicar en TikTok

- **Formato:** MP4, vertical 1080×1920 (9:16), sin bordes negros.
- **Duración:** 74–84 s (dentro del rango medio-explicativo pedido; TikTok no penaliza este largo si la retención es buena gracias al hook fuerte).
- **Subtítulos quemados:** obligatorio — gran parte del público ve sin audio. Tipografía sans-serif bold, tamaño grande, alto contraste (blanco con contorno negro o fondo semitransparente), 2–5 palabras por línea, sincronizados frase a frase con la VO (ver columna "Caption quemado" de la tabla).
- **Safe zones:** ver regla en la sección 5 (evitar 12% superior / 15% inferior, y ~8% en cada lateral para no chocar con el ícono de "me gusta/compartir" del lado derecho).
- **Portada (cover):** usar el frame del segundo 0:36 (el bloque con borde verde justo antes de la comparación) — es el fotograma más "curioso" (bloque quieto en un ángulo pronunciado) y funciona como miniatura intrigante.
- **Primer segundo = gancho visual, no logo ni intro de marca.** Cualquier intro/branding va *al final*, después del reto.
- **Música:** instrumental de fondo, volumen bajo bajo la voz (~-18 dB relativo a la VO), con un "riser"/impacto sutil en el segundo 0:46 (cuando el bloque empieza a deslizar) para reforzar el clímax.
- **Texto de descripción/caption del post (ejemplo):** "¿Sabes en qué ángulo EXACTO empieza a resbalar un bloque? 📐⚡ Física en 60s, parte 1/2. Reto en los comentarios 👇"
- **Hashtags sugeridos (mezcla de nicho + amplios):** `#Fisica #FisicaFacil #Newton #Friccion #DinamicaDeNewton #Manim #AprendeEnTikTok #CienciaTikTok #EstudiaConmigo #ClaseDeFisica`
- **CTA explícito:** pedir comentario con la respuesta al reto + "sígueme para la parte 2" — maximiza comentarios (señal fuerte para el algoritmo) y watch-time de la siguiente entrega.

---

## 9. Checklist antes de publicar

- [ ] Duración final entre 60–90 s
- [ ] Resolución 1080×1920, sin franjas negras
- [ ] Hook visible y comprensible con el sonido apagado
- [ ] Subtítulos quemados, sin errores, sincronizados
- [ ] Ningún texto clave dentro de las safe zones prohibidas
- [ ] Números coherentes entre guion, animación y VO (9.8 N / 10.19 N / 11.24 N / 9.63 N / 2.41 m/s²)
- [ ] Portada elegida manualmente (no el frame 0 por defecto)
- [ ] CTA + pregunta de reto presentes en el cierre
- [ ] Descripción del post con hashtags y pregunta del reto

---

## 10. Ideas para la serie (retención entre videos)

- **Parte 2:** resolver el ángulo crítico (`tanθc = μs`) planteado como reto, con demostración de por qué no depende de la masa.
- **Parte 3:** el mismo bloque, pero ahora tirado por una cuerda en ángulo (cambia la normal → cambia la fricción disponible) — "trampa" conceptual clásica de examen.
- **Parte 4:** sistema de dos bloques unidos por cuerda y polea, uno con fricción sobre mesa y otro colgando — introduce ligaduras de tensión/aceleración compartida.
