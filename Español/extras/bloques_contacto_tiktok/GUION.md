# "El bloque que no empujas también siente la fuerza" — Guion y ficha de producción

Cuarto y último video de la serie "Segunda ley de Newton con fuerzas de contacto",
basado en el **Problema 5 ("Dos bloques empujados en contacto")** del taller
`taller_segunda_ley.tex`. Cierra la serie: aquí la fuerza de contacto es la que un
bloque le hace directamente a otro (sin cuerda ni polea), y el protagonista es la
**3ª ley de Newton** ($F_{12} = -F_{21}$).

Producido con **Manim Community Edition**, vertical 9:16, mismo patrón que los videos
1-3 (`Español/extras/dinamica_friccion_tiktok/`, `bascula_ascensor_tiktok/`,
`carro_polea_tiktok/`). Usa `.claude/skills/manim-video-fisica-tiktok/` para instalar
el entorno y renderizar.

---

## 0. Ficha técnica rápida

| Parámetro | Valor |
|---|---|
| Resolución | 1080×1920 px (9:16) |
| FPS | 30 |
| Duración objetivo | 75–85 s |
| Motor | Manim Community Edition |
| Escena principal (sugerida) | `BloquesContactoTikTok` (`bloques_contacto_tiktok.py`, aún sin crear) |
| Paleta de color física | Fuerza aplicada = amarillo, fuerza de contacto entre bloques = azul, fricción = verde, aceleración = naranja |
| $g$ | No se usa explícitamente en este problema (superficie horizontal, sin componentes verticales relevantes) |

**Problema numérico fijo** (dos bloques en contacto sobre superficie horizontal;
$m_1=2{,}0\ \mathrm{kg}$, $m_2=1{,}0\ \mathrm{kg}$; $F=12\ \mathrm{N}$):

```
Aceleración del sistema (no depende de a cuál bloque se empuje):
    a = F / (m1+m2) = 12 / 3 = 4.0 m/s²

Caso A — se empuja el bloque GRANDE (m1=2kg), el bloque pequeño (m2=1kg) va detrás:
    Fuerza de contacto sobre m2:  F12 = m2 · a = 1 × 4.0 = 4.0 N

Caso B — se empuja el bloque PEQUEÑO (m2=1kg), el bloque grande (m1=2kg) va detrás:
    Fuerza de contacto sobre m1:  F21 = m1 · a = 2 × 4.0 = 8.0 N   <- ¡el DOBLE!

Verificación de la 3ª ley (aislando el otro bloque en cada caso):
    Caso A: aislar m1 -> F - F_contacto = m1·a -> F_contacto = 12 - 2×4 = 4.0 N  (=F12) ✓
    Caso B: aislar m2 -> F - F_contacto = m2·a -> F_contacto = 12 - 1×4 = 8.0 N  (=F21) ✓

Con fricción total sobre el sistema f = 3.0 N:
    a = (F - f) / (m1+m2) = (12-3)/3 = 3.0 m/s²

Si F fuera igual a la fricción (F = f):
    a = 0  ->  el sistema no acelera (reposo o velocidad constante: 1ª ley de Newton)
```

El giro conceptual del video: **la aceleración del sistema es siempre la misma (4.0
m/s²) sin importar a cuál bloque empujes** — pero la **fuerza de contacto** entre los
bloques cambia según cuál vaya "adelante": empujar el bloque grande transmite 4.0 N al
pequeño; empujar el pequeño transmite 8.0 N al grande, el doble, porque ahora el
contacto tiene que acelerar más masa.

---

## 1. Introducción llamativa (Hook, 0:00–0:07)

**Animación:** dos bloques en contacto (uno grande, uno pequeño) sobre una superficie.
Una mano empuja el bloque grande con $F=12\ \mathrm{N}$; en el punto de contacto
aparece un número: `4.0 N`. Corte: ahora la mano empuja el bloque pequeño con los
mismos 12 N; el número del contacto cambia a `8.0 N`.

**Texto en pantalla:** "Empujas con 12 N... el otro bloque siente 4 N. Cambias de
lado... ¡y siente 8 N! Misma fuerza total."

**Narración (VO):**
> "Empujas estos dos bloques juntos con 12 newtons. El bloque de atrás siente 4
> newtons en el punto de contacto. Pero si empujas del otro lado, con los mismos 12
> newtons... ¡el contacto ahora es de 8! ¿Por qué cambia?"

**Caption quemado:** `MISMOS 12 N → ¿POR QUÉ CAMBIA EL CONTACTO?`

---

## 2. Guion completo con timeline

| Tiempo | En pantalla / animación Manim | Narración (VO) | Caption quemado |
|---|---|---|---|
| 0:00–0:07 | Bloque grande empujado (contacto→4N), corte a bloque pequeño empujado (contacto→8N). | "Empujas estos dos bloques con 12 newtons. El de atrás siente 4. Cambias de lado, mismos 12 newtons... ¡y ahora siente 8!" | MISMOS 12 N → ¿POR QUÉ CAMBIA EL CONTACTO? |
| 0:07–0:15 | `Write` de datos: $m_1=2\ \text{kg}$, $m_2=1\ \text{kg}$, $F=12\ \text{N}$, sin fricción (por ahora). | "Dos bloques en contacto: uno de 2 kilos, otro de 1 kilo, empujados con 12 newtons, sobre una superficie sin fricción." | m1=2kg · m2=1kg · F=12N |
| 0:15–0:26 | Se empuja $m_1$ (grande). `TransformMatchingTex` de $a=F/m_{\text{total}}=12/3=4.0\ \text{m/s}^2$. Los dos bloques se deslizan juntos. | "Tratamos los dos bloques como un solo sistema: la fuerza entre la masa total. 12 entre 3, cuatro metros por segundo cuadrado." | a = F/(m1+m2) = 4.0 m/s² |
| 0:26–0:36 | Se aísla $m_2$ (el bloque de atrás): único vector horizontal = fuerza de contacto. $F_{12}=m_2 \cdot a = 1\times4 = 4.0\ \text{N}$. | "Ahora aislamos solo al bloque de atrás. La única fuerza horizontal que actúa sobre él es el contacto con el otro bloque: 1 kilo por 4, cuatro newtons." | F₁₂ = m2·a = 4.0 N |
| 0:36–0:44 | Se aísla $m_1$: aparecen $F$ (amarillo) y $F_{21}$ (azul, opuesta). $F_{21}=F-m_1 a=12-8=4.0\ \text{N}$ — coincide con $F_{12}$. Texto: "3ª ley: $F_{12}=-F_{21}$". | "Si aíslas el otro bloque, la cuenta da exactamente los mismos 4 newtons en sentido opuesto. Esa es la tercera ley de Newton." | F₁₂ = −F₂₁ (3ª ley) |
| 0:44–0:56 | Se invierte el montaje: ahora se empuja $m_2$ (pequeño), $m_1$ (grande) va detrás. Misma $a=4.0\ \text{m/s}^2$ (el contador NO cambia). Se aísla $m_1$: $F_{21}=m_1\cdot a=2\times4=8.0\ \text{N}$. | "Si en cambio empujas al bloque pequeño, la aceleración del sistema sigue siendo la misma, cuatro. Pero ahora el contacto tiene que acelerar al bloque grande: 2 kilos por 4... ¡8 newtons! El doble." | F contacto = 8.0 N — ¡el doble! |
| 0:56–1:04 | Texto: "La aceleración del sistema no cambia. El contacto sí: depende de qué masa empuja a cuál." | "La aceleración del sistema nunca cambió. Lo que cambió fue cuánta masa tenía que acelerar el contacto en cada caso." | mismo sistema, distinto contacto |
| 1:04–1:14 | Aparece fricción total $f=3\ \text{N}$ sobre el sistema. $a=(F-f)/m_{\text{total}}=(12-3)/3=3.0\ \text{m/s}^2$. | "Si ahora hay una fricción total de 3 newtons sobre el sistema, la aceleración baja a 3 metros por segundo cuadrado." | a = (F−f)/m_total = 3.0 m/s² |
| 1:14–1:22 | Texto de reto: "¿Qué le pasa a la aceleración si F es exactamente igual a la fricción?" con $a=0$ semi-transparente. | "Tu reto: si la fuerza aplicada fuera exactamente igual a la fricción, ¿qué le pasaría a la aceleración? Coméntalo abajo." | 🧠 RETO: ¿F = FRICCIÓN? |
| 1:22–1:26 | Cierre de la serie completa: "Segunda ley de Newton — Serie completa" + resumen de los 4 videos. | (música sube) | Serie completa — gracias por seguirla 🎬 |

Duración total estimada: **~86 s** (ajustable con los mismos márgenes usados en los
videos 1-3).

---

## 3. Aspectos teóricos clave

1. **2ª Ley de Newton sobre un sistema en contacto:** dos bloques que se tocan y se
   mueven juntos (sin resbalar entre sí) pueden tratarse como un solo sistema de masa
   $m_1+m_2$, acelerado por la fuerza externa neta — igual que en el video 3 con la
   cuerda y la polea, pero aquí la ligadura es más simple: los bloques simplemente
   están en contacto y se empujan.
2. **La fuerza de contacto es interna al sistema completo, pero externa a cada bloque
   por separado.** Al aislar un solo bloque, esa fuerza de contacto sí aparece
   explícitamente en su ecuación — es la única forma de calcularla.
3. **3ª Ley de Newton ($F_{12}=-F_{21}$):** el bloque 1 empuja al bloque 2 con la misma
   magnitud de fuerza con la que el bloque 2 empuja de vuelta al bloque 1, en sentido
   contrario. Aislar cualquiera de los dos bloques y despejar la fuerza de contacto da
   el mismo número — es una verificación cruzada, no una coincidencia.
4. **La aceleración del sistema depende solo de la masa total y la fuerza externa
   neta — no de *cuál* bloque se empuja.** Es el mismo principio del video 3 (misma
   fuerza, misma masa total → misma aceleración), llevado a un montaje distinto.
5. **La fuerza de contacto SÍ depende de cuál bloque se empuja**, porque cambia cuánta
   masa tiene que acelerar esa fuerza de contacto: empujar hacia un bloque más pesado
   requiere una fuerza de contacto mayor que empujar hacia uno más liviano, aunque la
   fuerza total aplicada al sistema sea la misma.
6. **Con fricción, se resta del numerador de la misma fórmula** ($a=(F_{\text{neta}}-f)/m_{\text{total}}$)
   — y si la fuerza aplicada iguala exactamente a la fricción, la fuerza neta es cero y
   el sistema no acelera: la 1ª ley de Newton (inercia) como caso límite de la 2ª.

---

## 4. Estrategia de resolución (metodología replicable — cierre de la serie)

1. **¿Los cuerpos se mueven juntos, sin resbalar entre sí?** Si sí, trátalos como un
   solo sistema de masa total, igual que con una cuerda ideal (video 3).
2. **Halla la aceleración del sistema completo**: $a=F_{\text{neta externa}}/m_{\text{total}}$
   (resta la fricción si existe).
3. **Si necesitas una fuerza de contacto interna, aísla solo uno de los cuerpos** y
   aplica la 2ª ley únicamente a él — ahí la fuerza de contacto aparece explícita.
4. **Verifica con la 3ª ley**: aísla el otro cuerpo y confirma que obtienes la misma
   magnitud de fuerza de contacto, en sentido opuesto.
5. **Recuerda que la aceleración del sistema no depende de cuál cuerpo recibe la
   fuerza externa** — pero la fuerza de contacto interna sí, porque cambia cuánta masa
   queda "detrás" de ese contacto.

Este es el mismo esqueleto de 5 pasos que atraviesa toda la serie: identificar
ligadura → tratar como sistema → aislar cuando haga falta una fuerza interna →
verificar con la ley que corresponda (2ª o 3ª) → generalizar.

---

## 5. Instrucciones de animación en Manim (reutilizar de los videos 1-3)

- Código de color: amarillo = fuerza aplicada externa, azul = fuerza de contacto entre
  bloques, verde = fricción (cuando aparece), naranja = aceleración del sistema.
- `cap_width()` y `cap_size()` (esta última definida en `carro_polea_tiktok.py`, ver
  `SKILL.md` sección 4) en todo texto/fórmula — este video vuelve a tener fórmulas con
  varios términos; usar `/` en línea en vez de `\dfrac{}{}` cuando el texto vaya
  apilado cerca de la escena de los bloques, como se hizo en el video 3.
- Los **dos bloques de tamaños visiblemente distintos** (el grande el doble de ancho
  que el pequeño, aproximadamente, ya que $m_1=2m_2$) son el gancho visual central —
  deben leerse como "grande" y "pequeño" de un vistazo, sin necesidad de leer las
  etiquetas.
- Para el "Caso B" (se invierte quién empuja a quién), es más simple y más seguro
  reconstruir el par de bloques en el orden invertido que intentar animar un
  intercambio de posiciones en vivo — menos riesgo de bugs de geometría, y el corte
  funciona igual de bien narrativamente (mismo patrón que el video 2 al pasar de 30° a
  35°, o el video 3 al reiniciar el carro entre casos).
- Revisar la lista de bugs conocidos antes de programar (`SKILL.md` sección 4, más las
  notas añadidas en `ESCENAS.md` del video 3): un solo helper de geometría reutilizado,
  todo `Write`/`FadeIn` con su `FadeOut`, cuidado con `.next_to()` heredando
  desplazamientos, y verificar con contact sheets (no solo leyendo el código) antes de
  dar el render por bueno.

---

## 6. Conclusión (texto exacto para pantalla y VO — cierre de la serie completa)

**Pantalla:** *"Sistema → aceleración común. Aislar un cuerpo → fuerza de contacto. 3ª ley → verificación."*

**VO:**
> "Con esto cerramos la serie: trata los cuerpos conectados como un sistema para
> hallar la aceleración, aísla uno solo cuando necesites la fuerza de contacto, y usa
> la tercera ley para verificar. Fricción, básculas, poleas o bloques en contacto — la
> segunda ley de Newton es siempre la misma herramienta."

---

## 7. Reto final / preguntas para seguir aprendiendo

**Reto principal:**
> "Si la fuerza aplicada fuera exactamente igual a la fricción, ¿qué le pasaría a la
> aceleración? Coméntalo abajo." *(spoiler: la fuerza neta sería cero, así que
> $a=0$ — el sistema se queda en reposo o sigue a velocidad constante, según cómo
> estuviera moviéndose: es la primera ley de Newton, la inercia, como caso límite de
> la segunda cuando $F_{\text{neta}}=0$.)*

**Preguntas adicionales (elige 1-2, buen cierre de serie):**
- De los cuatro videos de la serie (fricción, báscula, polea, bloques en contacto),
  ¿cuál fuerza de contacto fue la normal, cuál la tensión, y cuál el contacto directo
  entre sólidos? Todas son ejemplos del mismo tipo de fuerza.
- ¿Qué pasaría si los dos bloques *no* estuvieran en contacto, sino separados por un
  pequeño espacio? ¿Seguiría teniendo sentido tratarlos como un solo sistema?
- Si agregas un tercer bloque en contacto (empujando en cadena a los otros dos),
  ¿cómo cambiaría la fuerza de contacto en cada unión? (pista: cada contacto solo
  necesita acelerar la masa que tiene "detrás", igual que en este video).

---

## 8. Especificaciones para publicar en TikTok

- Formato: MP4, vertical 1080×1920, sin bordes negros, 30fps.
- Duración: 75-86 s.
- Subtítulos quemados, sincronizados a la VO (columna "Caption quemado" de la tabla).
- Safe zones: nada importante en el 12% superior ni el 15% inferior del frame.
- Portada sugerida: el fotograma del hook con `4.0 N` y `8.0 N` lado a lado — la
  contradicción aparente (misma fuerza, distinto contacto) es la miniatura más
  llamativa, igual que en los videos anteriores de la serie.
- Hashtags sugeridos: `#Fisica #SegundaLeyDeNewton #TerceraLeyDeNewton #Manim #ClaseDeFisica #CienciaTikTok`
- CTA: pedir la respuesta al reto en comentarios + invitar a ver la serie completa
  (enlazar los 4 videos en la bio o en un video fijado).

---

## 9. Checklist antes de programar/publicar

- [ ] Todos los números coinciden con la tabla de la sección 0 (4.0 N / 8.0 N / 3.0 m/s² / a=0)
- [ ] Verificado que $F_{12}=F_{21}$ en magnitud en ambos casos (3ª ley) antes de animarlo
- [ ] El video deja claro que la aceleración del sistema NO cambia entre casos, solo
      el contacto — es el punto que más se presta a confusión
- [ ] Ninguna fórmula ni texto se corta en los bordes del frame vertical (revisar con
      contact sheet, no solo leyendo el código)
- [ ] Duración final entre 75-86 s
- [ ] Reto y su spoiler verificados a mano

---

## 10. Cierre de la serie

Con este video quedan cubiertos los 5 problemas de `taller_segunda_ley.tex`:
Problema 1 (implícito en el video 3, caso de fuerza directa), Problema 2 (video 3,
polea), Problema 3 (video 1, plano inclinado + fricción añadida), Problema 4 (video 2,
báscula en ascensor) y Problema 5 (este video, bloques en contacto). La serie completa
recorre los cuatro tipos de fuerza de contacto más comunes en un curso introductorio:
**fricción, normal, tensión y contacto directo entre sólidos** — todas resueltas con
la misma herramienta: la segunda ley de Newton aplicada con cuidado a un sistema o a un
cuerpo aislado, según lo que se necesite calcular.
