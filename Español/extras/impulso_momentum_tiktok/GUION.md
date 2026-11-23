# "No evitas el golpe. Lo estiras." — Guion y ficha de producción

Video corto de física (Cantidad de movimiento e impulso, teorema impulso-momentum) para
TikTok/Reels/Shorts, producido con **Manim Community Edition**, renderizado en vertical
9:16. Sexta entrega de la serie.

Decisiones ya tomadas con el usuario:
- Motor: **ManimCE**, mismo pipeline que el resto de la serie.
- Formato: **explicativo medio, 80–90 s**.
- Enfoque pedagógico: mismo espíritu Hewitt de la serie (intuición antes que fórmula),
  más dos recursos nuevos tomados de un video de referencia de Instagram sobre este
  mismo tema (bolsas de aire e impulso), **adaptados con problema, números, wording y
  analogía propios — no se copia texto, cifras ni la frase de cierre de ese video**:
  1. Una sección "LA TRAMPA" que nombra y desmiente explícitamente el error conceptual
     más común del tema (creer que el impulso cambia cuando en realidad es fijo).
  2. Dos barras que crecen/achican en proporción inversa (Tiempo vs. Fuerza) para
     visualizar el intercambio — mismo tipo de recurso que ya usamos para las barras de
     trabajo en el video 5, ahora aplicado a tiempo/fuerza.
- Escenario propio: conductor de 80 kg a 20 m/s (72 km/h) que debe detenerse por
  completo — no los 70 kg / 50 km/h del video de referencia.

---

## 0. Ficha técnica rápida

| Parámetro | Valor |
|---|---|
| Resolución | 1080×1920 px (9:16) |
| FPS | 30 |
| Duración objetivo | 80–90 s |
| Motor | Manim Community Edition ≥ 0.18 |
| Escena principal | `ImpulsoMomentumTikTok` (`impulso_momentum_tiktok.py`) |
| Audio | Voz en off (TTS local o edge-tts) + música instrumental de fondo |
| Paleta de color física | Momentum/impulso = `ORANGE`, Fuerza = `RED`, Tiempo = `BLUE`, Trayectoria/auxiliar = `GREEN` |

**Problema numérico fijo (verificado a mano antes de animar):**

```
Conductor: m = 80 kg
Velocidad inicial: v = 20 m/s  (= 72 km/h)
Debe detenerse por completo: Δv = 20 m/s

Cantidad de movimiento (momentum) inicial:
  p = m·v = 80 × 20 = 1600 kg·m/s

Teorema impulso-momentum:  Δp = F · Δt   →   F = Δp / Δt
Δp = 1600 kg·m/s SIEMPRE (fijo por la masa y el cambio de velocidad,
     no depende de cómo se detenga el conductor)

Caso 1 — Golpea el volante directamente (Δt corto):
  Δt = 0.02 s
  F = 1600 / 0.02 = 80 000 N

Caso 2 — Lo detiene la bolsa de aire (Δt 10 veces más largo):
  Δt = 0.2 s
  F = 1600 / 0.2 = 8 000 N   (10 veces menos fuerza, mismo Δp)

Reto final (NO se resuelve en el video):
  Si el Δt de la bolsa fuera el doble (0.4 s), ¿cuánto vale F?
  F = 1600 / 0.4 = 4000 N  (la mitad otra vez — queda como pregunta)
```

---

## 1. Introducción llamativa (Hook, 0:00–0:08)

**Animación:** un auto (ícono simple) se acerca a una pared a velocidad constante.
Texto grande con la pregunta central.

**Texto en pantalla:** "¿Por qué una bolsa de aire te golpea con 10 VECES menos fuerza, si chocas exactamente igual de fuerte?"

**Narración (VO):**
> "¿Por qué una bolsa de aire te golpea con diez veces menos fuerza... si chocaste exactamente igual de fuerte?"

---

## 2. Guion completo con timeline

| Sección (beat) | En pantalla / animación Manim | Narración (VO) |
|---|---|---|
| `hook` | Auto acercándose a una pared, pregunta central. | "¿Por qué una bolsa de aire te golpea con diez veces menos fuerza, si chocaste exactamente igual de fuerte?" |
| `plantear_problema` | Datos: m=80 kg, v=20 m/s (72 km/h), debe quedar en reposo. | "Un conductor de 80 kilos viaja a 20 metros por segundo y tiene que quedar completamente detenido." |
| `concepto_momentum` | `p = m·v` aparece, con flecha de velocidad sobre el auto. | "Todo lo que se mueve tiene cantidad de movimiento: su masa por su velocidad." |
| `concepto_impulso` | `Δp = F·Δt` aparece debajo. Se calcula Δp=1600 kg·m/s (fijo). | "Para detenerlo hay que quitarle ese movimiento, y eso se paga con fuerza multiplicada por el tiempo que dura el frenado. Ese impulso, 1600, es siempre el mismo." |
| `comparar_volante_bolsa` | Barras Tiempo/Fuerza inversas: Δt=0.02s→F=80 000 N (volante) vs Δt=0.2s→F=8 000 N (bolsa). | "Si frena en dos centésimas de segundo contra el volante, la fuerza es de 80 mil newtons. Si la bolsa estira ese frenado a dos décimas, la fuerza baja a solo 8 mil: diez veces menos." |
| `la_trampa` | Texto "LA TRAMPA" + tachar la idea errónea, mostrar la correcta. | "La trampa es pensar que la bolsa reduce el golpe total. Falso: el impulso, 1600, es el mismo siempre. Lo único que cambia es cuánto tiempo tarda en aplicarse." |
| `analogia` | Caja cayendo sobre piso duro (rebote brusco) vs. colchón (hundimiento lento). | "Por eso un colchón duele menos que el piso: el golpe es el mismo, pero tienes más tiempo para frenar." |
| `estrategia` | 3 pasos resumidos: calcula Δp (fijo) → elige Δt → F=Δp/Δt. | "La estrategia: calculas el impulso con la masa y el cambio de velocidad, decides cuánto tiempo dura el frenado, y de ahí sale la fuerza." |
| `reto_final` | Pregunta: ¿y si Δt de la bolsa fuera el doble, 0.4 s? | "Tu reto: si la bolsa tardara el doble, 0.4 segundos, ¿cuánto valdría la fuerza? Coméntalo abajo." |
| `cierre` | Frase final + marca de serie. | "No evitas el golpe. Lo estiras en el tiempo. Física en 60 segundos, parte 6." |

Duración total estimada: **~85 s** (se ajusta con el timing real del render, igual que el resto de la serie).

---

## 3. Aspectos teóricos clave

1. **Cantidad de movimiento (momentum):** `p = m·v`. Depende de la masa y la velocidad del objeto.
2. **Teorema impulso-momentum:** `Δp = F·Δt`. El cambio de momentum (impulso) es igual a la fuerza neta multiplicada por el tiempo durante el cual actúa.
3. **El impulso necesario para detener un objeto es fijo** una vez que se conocen su masa y su cambio de velocidad — no depende de CÓMO se detenga.
4. **La fuerza es inversamente proporcional al tiempo de frenado**, para un impulso fijo: `F = Δp/Δt`. Estirar el tiempo de frenado reduce la fuerza pico, aunque el "golpe total" (impulso) sea idéntico.
5. **Error común a corregir explícitamente ("la trampa"):** confundir "menos fuerza" con "menos impulso". El impulso no cambia; lo que cambia es cómo se reparte en el tiempo.

---

## 4. Estrategia de resolución (metodología replicable)

1. **Calcula el impulso necesario**: `Δp = m·Δv`. Este valor es fijo una vez que conoces la masa y el cambio de velocidad.
2. **Identifica (o elige) el tiempo de frenado** `Δt` para el escenario que te interesa.
3. **Calcula la fuerza**: `F = Δp/Δt`. A mayor `Δt`, menor `F`, para el mismo impulso.
4. **Verifica con un segundo escenario**: si cambias `Δt` pero no `Δp`, la fuerza debe cambiar en proporción inversa (si `Δt` se multiplica por 10, `F` se divide entre 10).

---

## 5. Instrucciones precisas de animación en Manim

- Paleta: Momentum/impulso = `ORANGE`, Fuerza = `RED`, Tiempo = `BLUE`, auxiliar = `GREEN`.
- `cap_width()`/`cap_size()` en todo texto y fórmula, igual que el resto de la serie.
- **Barras de intercambio (Tiempo vs. Fuerza)**: dos `Rectangle` con altura animada vía `ValueTracker` + `always_redraw`, que crecen/achican en proporción inversa al pasar del caso "volante" al caso "bolsa" — mismo patrón ya usado para las barras de trabajo en el video 5 (`DecimalNumber` + `ValueTracker`), aplicado aquí a dos barras simultáneas en vez de un solo contador.
- **Sección "LA TRAMPA"**: texto de la idea errónea con `Line` tachándola (`Cross` o una línea diagonal roja sobre el texto), seguido de `FadeIn` de la idea correcta debajo — debe sentirse como una corrección explícita, no solo información nueva.
- **Analogía piso vs. colchón**: una caja (`Square`) cae con `rate_functions.ease_in_quad` y rebota bruscamente sobre una línea gris (piso), comparado con una caja que se hunde lentamente en un rectángulo verde más grueso (colchón) — reutilizar el patrón de caja ya establecido en el video 5 (mismo `COLOR_CAJA`).
- Reutilizar `mostrar_fase()` del video 5 (etiquetas DATOS/FÓRMULA/DESARROLLO/RESULTADO en la esquina) para mantener consistencia visual entre videos de la serie.
- Zonas seguras: nada importante en el 12% superior ni el 15% inferior del frame.

---

## 6. Conclusión (texto exacto para pantalla y VO)

**Pantalla:** *"No evitas el golpe. Lo estiras en el tiempo."*

**VO:**
> "No evitas el golpe. Lo estiras en el tiempo."

---

## 7. Reto final

**Reto principal (en pantalla + VO):**
> "Tu reto: si la bolsa tardara el doble, 0.4 segundos, ¿cuánto valdría la fuerza? Coméntalo abajo."

**Preguntas adicionales para pie/comentarios (elige 1–2):**
- ¿Por qué duele más chocar contra algo rígido que contra algo que cede?
- Si el conductor pesara el doble, ¿el impulso necesario también se duplica? (sí — y por eso los autos grandes necesitan bolsas más "lentas" para absorber igual de bien)

---

## 8. Especificaciones para publicar en TikTok

- Formato: MP4, vertical 1080×1920, sin bordes negros.
- Duración: 80–90 s.
- Portada (cover): el momento de la comparación de barras Tiempo/Fuerza (la revelación de "10 veces menos").
- Hashtags sugeridos: `#Fisica #ImpulsoYMomentum #CantidadDeMovimiento #FisicaFacil #SeguridadVial #CienciaTikTok #ClaseDeFisica #AprendeEnTikTok`

---

## 9. Checklist antes de publicar

- [ ] Duración final dentro de 80-90 s
- [ ] Resolución 1080×1920, sin franjas negras
- [ ] Hook comprensible con el sonido apagado
- [ ] Ningún texto cortado en los bordes (hoja de contacto)
- [ ] Ningún mobject "fantasma"
- [ ] Números coherentes: m=80kg, v=20m/s, Δp=1600, Δt=0.02s→F=80000N, Δt=0.2s→F=8000N
- [ ] CTA + pregunta de reto presentes en el cierre
