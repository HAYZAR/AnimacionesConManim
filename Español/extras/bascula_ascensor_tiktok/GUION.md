# "La báscula que no dice tu peso real" — Guion y ficha de producción

Segundo video de la serie "Segunda ley de Newton con fuerzas de contacto", basado en el
**Problema 4 ("La báscula en el ascensor")** del taller `taller_segunda_ley.tex`. Aquí la
"fuerza de contacto" es la **normal** entre la báscula y la persona, y la **ligadura** es
que la persona se mueve con la *misma aceleración* que el ascensor — no hay fricción en
este problema, pero el concepto de fuerza de contacto + ligadura es el mismo hilo
conductor que en el video 1 (`Español/extras/dinamica_friccion_tiktok/`).

Producido con **Manim Community Edition**, vertical 9:16. Sigue el mismo patrón que el
video 1 — usa la skill `.claude/skills/manim-video-fisica-tiktok/` para instalar el
entorno y renderizar cuando este guion pase a código.

---

## 0. Ficha técnica rápida

| Parámetro | Valor |
|---|---|
| Resolución | 1080×1920 px (9:16) |
| FPS | 30 |
| Duración objetivo | 80–90 s |
| Motor | Manim Community Edition |
| Escena principal (sugerida) | `BasculaAscensorTikTok` (`bascula_ascensor_tiktok.py`, aún sin crear) |
| Paleta de color física | Peso real ($mg$) = rojo, Normal/lectura de báscula ($N$) = azul, aceleración del ascensor = naranja |

**⚠️ Diferencia con el video 1:** ese problema usaba $g=9.8\ \mathrm{m/s^2}$; **este
taller pide explícitamente $g=10\ \mathrm{m/s^2}$** (ver indicaciones del `.tex`). No
mezclar los dos valores al programar la escena.

**Problema numérico fijo** (persona de $m=60\ \mathrm{kg}$ sobre una báscula dentro de un
ascensor; $N$ = lectura de la báscula = fuerza normal sobre la persona):

Ecuación única para todos los casos (eje vertical, positivo hacia arriba):
$$N - mg = ma \quad\Rightarrow\quad N = m(g+a)$$
donde **$a$ es la aceleración del ascensor** (no su velocidad, ni su sentido de
movimiento — ese es el giro conceptual de todo el video).

```
Reposo:                          a = 0        ->  N = 600 N   (= mg)
Sube acelerando (a = +2 m/s²):   a = +2       ->  N = 720 N   (más pesado)
Sube a velocidad constante:      a = 0        ->  N = 600 N   (igual que en reposo)
Baja frenando (decelera):        a = +2       ->  N = 720 N   (misma cuenta que "sube acelerando")
Baja acelerando (a = -2 m/s²):   a = -2       ->  N = 480 N   (más liviano)
Cable cortado / caída libre:     a = -g = -10 ->  N = 0 N     (ingravidez total)
Reto: ¿a para sentir el doble?   N = 2mg      ->  a = +g = +10 m/s²
```

El detalle que sostiene todo el video: **"sube" y "baja" no determinan el signo de
$N$ — lo determina si el ascensor acelera hacia arriba o hacia abajo.** Por eso "subir
acelerando" y "bajar frenando" dan *exactamente* el mismo número (720 N), y por qué
"velocidad constante" (subiendo o no) siempre da lo mismo que estar en reposo.

---

## 1. Introducción llamativa (Hook, 0:00–0:06)

**Animación:** persona de pie sobre una báscula dentro de la cabina de un ascensor, ya
en pantalla. Un número grande (`600 N`) tiembla/parpadea sobre la báscula.

**Texto en pantalla:** "¿Alguna vez sentiste que pesabas más en un ascensor? Tu peso no
cambió... esto sí."

**Narración (VO):**
> "¿Sentiste alguna vez que pesabas más al subir en un ascensor? Tu peso no cambió...
> pero lo que marca la báscula, sí. Y hay un momento en el que marca cero."

**Caption quemado:** `¿POR QUÉ PESAS DISTINTO EN UN ASCENSOR?`

---

## 2. Guion completo con timeline

| Tiempo | En pantalla / animación Manim | Narración (VO) | Caption quemado |
|---|---|---|---|
| 0:00–0:06 | Persona + báscula + cabina de ascensor. Número `600 N` parpadea. | "¿Sentiste alguna vez que pesabas más al subir en un ascensor? Tu peso no cambió, pero lo que marca la báscula sí. Y hay un momento en el que marca cero." | ¿POR QUÉ PESAS DISTINTO EN UN ASCENSOR? |
| 0:06–0:14 | `Write` de los datos: $m=60\ \text{kg}$, $g=10\ \text{m/s}^2$. Flecha señala a la persona sobre la báscula. | "Una persona de 60 kilos se sube a una báscula, dentro de un ascensor." | m = 60 kg |
| 0:14–0:22 | Zoom al DCL de la persona: vector peso $mg$ (rojo, abajo) y normal $N$ (azul, arriba) — el mismo tamaño en reposo. | "La báscula nunca mide tu peso real. Mide la fuerza normal: lo fuerte que empuja hacia arriba para sostenerte." | La báscula mide N, no mg |
| 0:22–0:30 | `TransformMatchingTex`: $\sum F = ma \to N - mg = ma \to N = m(g+a)$. Resaltar que "$a$" es la aceleración del ascensor. | "Aplicamos la segunda ley en el eje vertical: la normal menos el peso es igual a la masa por la aceleración del ascensor. Esa aceleración es la clave de todo." | N = m(g + a) |
| 0:30–0:38 | Ascensor quieto y luego subiendo a velocidad constante (misma velocidad, sin acelerar). Número de la báscula: `600 N` en ambos casos, con un signo "=" grande entre las dos escenas. | "En reposo, la báscula marca 600 newtons. Y si el ascensor sube a velocidad constante... marca exactamente lo mismo. Lo que importa no es moverse, es acelerar." | REPOSO = VELOCIDAD CONSTANTE → 600 N |
| 0:38–0:50 | Ascensor acelerando hacia arriba ($a=+2\ \text{m/s}^2$). Contador sube de 600 a `720 N`. Persona con leve `Indicate` (se siente más pesada). Luego: ascensor bajando pero *frenando* — mismo número `720 N` aparece de nuevo, con un ✓ comparando ambas escenas. | "Si el ascensor acelera hacia arriba, la báscula sube a 720 newtons: te sientes más pesado. Y si el ascensor está bajando pero frenando, su aceleración también apunta hacia arriba... así que marca exactamente los mismos 720 newtons." | 720 N (subir acelerando = bajar frenando) |
| 0:50–0:58 | Ascensor bajando y acelerando hacia abajo ($a=-2\ \text{m/s}^2$). Contador baja a `480 N`. | "Pero si el ascensor baja acelerando, la aceleración apunta hacia abajo, y la báscula marca solo 480 newtons: te sientes más liviano." | 480 N — te sientes más liviano |
| 0:58–1:10 | Clímax: cable cortado / caída libre. El número cae en picada hasta `0 N`, persona "flotando" dentro de la cabina (`Indicate`/leve desplazamiento vertical). | "Y si el ascensor cae libremente, su aceleración es exactamente $g$ hacia abajo... la normal se hace cero. La báscula marca cero, aunque tu masa y tu peso siguen siendo los mismos. Eso es ingravidez." | N = 0 → ¡INGRAVIDEZ! |
| 1:10–1:20 | Resumen visual: fórmula $N=m(g+a)$ con una recta numérica de $a$ (de $-g$ a $+g$) y el valor de $N$ deslizándose sobre ella según el signo de $a$. | "La fórmula es siempre la misma: normal igual a masa por gravedad más aceleración del ascensor. Solo cambia el signo y el valor de esa aceleración." | N = m(g + a) — un solo modelo, todos los casos |
| 1:20–1:30 | Texto de reto: "¿Qué aceleración necesitarías para sentir EL DOBLE de tu peso real?" con la fórmula $N=2mg$ semi-transparente. | "Tu reto: ¿qué aceleración del ascensor haría que la báscula marcara el doble de tu peso real? Coméntalo abajo." | 🧠 RETO: ¿ACELERACIÓN PARA EL DOBLE DE N? |
| 1:30–1:33 | Cierre con marca de serie ("Segunda ley de Newton — Parte 2") y llamada a seguir. | (música sube) | Sígueme para la Parte 3 👀 |

Duración total estimada: **~93 s** (ajustable a 80-85s recortando el paso 0:30–0:38 o
acelerando las transiciones numéricas, igual que se hizo en el video 1).

---

## 3. Aspectos teóricos clave (los que el video *debe* dejar claros)

1. **La báscula mide la normal, no el peso.** El peso ($mg$) es constante mientras la
   masa y $g$ no cambien; lo que la báscula reporta es la fuerza de contacto que ejerce
   sobre la persona, y esa sí cambia con el movimiento del ascensor.
2. **2ª Ley de Newton en un sistema no inercial (el ascensor):** para la persona,
   tomando arriba como positivo, $N - mg = ma$, de donde $N = m(g+a)$. Es la misma
   estructura ("fuerza neta = masa por aceleración") que en el plano inclinado del
   video 1, solo que aquí las dos fuerzas verticales (peso y normal) están alineadas
   con el movimiento, sin necesidad de descomponer nada.
3. **Ligadura:** la persona está *pegada* a la báscula, así que su aceleración es
   siempre igual a la del ascensor — no puede acelerar distinto del suelo que pisa. Esa
   es la restricción (ligadura) que conecta "lo que hace el ascensor" con "lo que siente
   la persona".
4. **La velocidad no importa, la aceleración sí.** Subir, bajar, estar quieto a
   velocidad constante: si $a=0$, la báscula siempre marca $mg$. Es el error conceptual
   más común y el que más "engancha" al espectador porque contradice la intuición
   ("si subo debería pesar más... pero solo si estoy *acelerando* al subir").
5. **Ingravidez no es "falta de gravedad".** Cuando $N=0$ (caída libre, $a=-g$), la
   persona sigue teniendo el mismo peso $mg$ — simplemente no hay ninguna superficie
   empujándola porque ella y el ascensor caen exactamente igual de rápido. Es la misma
   física por la que los astronautas "flotan" en la Estación Espacial: están en caída
   libre continua alrededor de la Tierra, no en un lugar sin gravedad.

---

## 4. Estrategia de resolución (metodología replicable)

1. **Identifica las fuerzas verticales sobre la persona**: peso ($mg$, hacia abajo) y
   normal ($N$, hacia arriba) — no hay más, la báscula no ejerce fricción horizontal
   aquí.
2. **Define un signo positivo** (por convención, arriba) y escribe la 2ª ley sobre ese
   eje: $N - mg = ma$.
3. **Identifica la ligadura**: la aceleración "$a$" en esa ecuación es la del ascensor
   (el vínculo obliga a que sea también la de la persona).
4. **Determina el signo de $a$ a partir de lo que hace el ascensor** — no de si "sube" o
   "baja", sino de hacia dónde apunta su aceleración (acelerando hacia arriba = positivo,
   acelerando hacia abajo = negativo, velocidad constante o reposo = cero).
5. **Despeja y calcula** $N = m(g+a)$. El signo y la magnitud de $N$ frente a $mg$ te
   dicen si la persona se siente más pesada, más liviana, igual, o en ingravidez total
   ($N=0$).

---

## 5. Instrucciones de animación en Manim (reutilizar del video 1)

- Mismo código de color: rojo = peso, azul = normal; aquí se suma **naranja** para la
  aceleración del ascensor (vector junto a la cabina, no sobre la persona).
- `cap_width()` en todo texto/fórmula (ver `SKILL.md` sección 4.1) — el resumen de la
  sección 2 (recta numérica de $a$) es especialmente ancho, cuidar que quepa en las
  ~3.9 unidades seguras del frame vertical.
- `DecimalNumber` + `ValueTracker` para el contador de la báscula (600→720→480→0),
  igual que el contador de fuerzas del video 1 — es el elemento visual que más
  "engancha" porque el espectador ve el número cambiar en vivo con cada escenario.
- La cabina del ascensor puede subir/bajar en pantalla con `ValueTracker` +
  `always_redraw`, pero el **número de la báscula depende de la aceleración, no de la
  posición ni la velocidad** — al programar la escena, cuidado con animar la cabina
  moviéndose a velocidad constante mientras el número cambia: eso contradice
  exactamente el punto central del video. Anima la cabina acelerando (curva, no
  lineal) solo en las escenas donde $a\neq 0$.
- Repasar la lista de bugs conocidos del video 1 antes de programar (`SKILL.md` sección
  4): un solo helper de geometría, todo `Write` con su `FadeOut`, cuidado con
  `.next_to()` heredando desplazamientos.

---

## 6. Conclusión (texto exacto para pantalla y VO)

**Pantalla:** *"N = m(g + a) — la báscula mide la normal, no tu peso real"*

**VO:**
> "La estrategia es siempre la misma: identifica el peso y la normal, escribe la
> segunda ley en el eje vertical, y recuerda que la aceleración es la del ascensor, no
> la velocidad ni el sentido del movimiento."

---

## 7. Reto final / preguntas para seguir aprendiendo

**Reto principal:**
> "¿Qué aceleración del ascensor haría que la báscula marcara el doble de tu peso
> real? Coméntalo abajo — en la parte 3 lo resolvemos." *(spoiler para quien escriba el
> guion de la respuesta: $a=+g$, exactamente $10\ \text{m/s}^2$ hacia arriba, porque
> $N=2mg \Rightarrow m(g+a)=2mg \Rightarrow a=g$.)*

**Preguntas adicionales (elige 1-2):**
- Si la báscula marca 0 N, ¿significa que la persona no pesa nada, o que nada la está
  empujando? ¿Es lo mismo "no pesar" que "no sentir tu peso"?
- ¿Por qué los astronautas en la Estación Espacial Internacional "flotan" si la
  gravedad ahí solo es un poco menor que en la superficie de la Tierra?
- Si en vez de una persona hubiera dos personas abrazadas sobre la misma báscula
  (juntas suman 120 kg), ¿cambia la fórmula? ¿Y si se paran una sobre los hombros de la
  otra? (gancho hacia sistemas de dos cuerpos, como el Problema 5 del taller — bloques en
  contacto).

---

## 8. Especificaciones para publicar en TikTok

- Formato: MP4, vertical 1080×1920, sin bordes negros, 30fps.
- Duración: 80-93 s (recortable; ver nota de la sección 2).
- Subtítulos quemados, sincronizados a la VO (columna "Caption quemado" de la tabla).
- Safe zones: nada importante en el 12% superior ni el 15% inferior del frame.
- Portada sugerida: el fotograma justo cuando el número cae a `0 N` (el momento más
  intrigante — un número en cero es una miniatura muy llamativa).
- Hashtags sugeridos: `#Fisica #SegundaLeyDeNewton #Ascensor #Ingravidez #Manim #ClaseDeFisica #CienciaTikTok`
- CTA: pedir la respuesta al reto en comentarios + "sígueme para la parte 3".

---

## 9. Checklist antes de programar/publicar

- [ ] Todos los números coinciden con la tabla de la sección 0 (600 N / 720 N / 480 N / 0 N)
- [ ] $g=10\ \text{m/s}^2$ en todo el archivo (no 9.8 — ese es el del video 1)
- [ ] El video dice explícitamente que "subir/bajar" no es lo mismo que "acelerar hacia
      arriba/abajo" — es el punto que más se presta a confusión
- [ ] Duración final entre 80-90 s
- [ ] Reto y su spoiler verificados a mano antes de publicar la respuesta en la parte 3

---

## 10. Ideas para la serie (los otros problemas del mismo taller)

El archivo `taller_segunda_ley.tex` trae 5 problemas — este video cubrió el 4. Los
otros tres que aún no tienen video son candidatos naturales para continuar la serie
"Segunda ley de Newton con fuerzas de contacto":

- **Problema 1 (carros halados por una fuerza):** comparación directa de $a=F/m$ —
  buen video introductorio/"parte 0" si se quiere explicar la ley desde cero antes del
  ascensor.
- **Problema 2 (carro + pesas colgantes por una polea):** sistema de dos cuerpos unidos
  por una cuerda ideal — la ligadura aquí es "misma rapidez y misma aceleración en toda
  la cuerda", y permite mostrar cómo la *masa total* del sistema decide la aceleración
  aunque la fuerza motriz venga solo de una parte.
- **Problema 5 (dos bloques en contacto empujados):** fuerza de contacto entre los dos
  bloques ($F_{12}$ vs $F_{21}$) — combina perfectamente con la 3ª ley de Newton y es un
  cierre natural de la serie ("ya viste fricción, ya viste una báscula, ahora viste qué
  pasa cuando dos cuerpos se empujan entre sí").

(El Problema 3 del taller, plano inclinado sin fricción, ya quedó cubierto en esencia
por el video 1, que además le agregó fricción estática/cinética.)
