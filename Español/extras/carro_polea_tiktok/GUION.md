# "La misma fuerza, la mitad de aceleración" — Guion y ficha de producción

Tercer video de la serie "Segunda ley de Newton con fuerzas de contacto", basado en el
**Problema 2 ("Pesas que caen y un carro que acelera")** del taller
`taller_segunda_ley.tex`. Aquí la fuerza de contacto es la **tensión** de la cuerda, y
la **ligadura** es que la cuerda es inextensible y la polea ideal: el carro y las pesas
colgantes se mueven siempre con la *misma rapidez y la misma aceleración*.

Producido con **Manim Community Edition**, vertical 9:16, siguiendo el mismo patrón que
los videos 1 y 2 (`Español/extras/dinamica_friccion_tiktok/`,
`Español/extras/bascula_ascensor_tiktok/`). Usa
`.claude/skills/manim-video-fisica-tiktok/` para instalar el entorno y renderizar.

---

## 0. Ficha técnica rápida

| Parámetro | Valor |
|---|---|
| Resolución | 1080×1920 px (9:16) |
| FPS | 30 |
| Duración objetivo | 75–85 s |
| Motor | Manim Community Edition |
| Escena principal (sugerida) | `CarroPoleaTikTok` (`carro_polea_tiktok.py`, aún sin crear) |
| Paleta de color física | Fuerza aplicada / tensión = amarillo, peso de las pesas = rojo, aceleración = naranja |
| $g$ | $10\ \mathrm{m/s^2}$ (igual que el video 2 — este taller usa $g=10$, no $9.8$) |

**Problema numérico fijo** (carro de $m_{\text{carro}}=1{,}0\ \mathrm{kg}$ sobre una mesa
horizontal *sin fricción*; cada pesa colgante pesa $10\ \mathrm{N}$, es decir
$m_{\text{pesa}}=1{,}0\ \mathrm{kg}$; polea ideal, cuerda inextensible):

```
Caso A — mano hala el carro con F = 10 N directamente:
    a = F / m_carro = 10 / 1  = 10.0 m/s²

Caso B — la fuerza la produce 1 pesa colgante (mismos 10 N, vía polea):
    masa total del sistema = m_carro + m_pesa = 1 + 1 = 2 kg
    F_neta externa = peso de la pesa = 10 N   (la tensión es interna, se cancela)
    a = F_neta / m_total = 10 / 2 = 5.0 m/s²   <- ¡la MITAD que en el caso A!

Con 2 pesas colgando:  m_total = 3 kg,  F_neta = 20 N,  a = 6.67 m/s²
Con 3 pesas colgando:  m_total = 4 kg,  F_neta = 30 N,  a = 7.50 m/s²
Con 10 pesas:                                          a = 9.09 m/s²
Con 100 pesas:                                         a = 9.90 m/s²

Límite cuando el número de pesas n -> infinito:
    a = 10n/(1+n)  ->  10 m/s²  =  g   (se acerca a g, nunca lo alcanza ni lo supera)
```

El giro conceptual de todo el video: **en el caso A y el caso B se aplican
exactamente los mismos 10 N, pero la aceleración NO es la misma** — porque en el caso B
esos 10 N también tienen que acelerar a la propia pesa que los produce, no solo al
carro.

---

## 1. Introducción llamativa (Hook, 0:00–0:07)

**Animación:** carro sobre una mesa, una mano (flecha amarilla) lo hala con
$F=10\ \mathrm{N}$; el número `10.0 m/s²` aparece grande. Corte rápido: la mano
desaparece, en su lugar una cuerda pasa por una polea y de ella cuelga una pesa de
$10\ \mathrm{N}$; el número cambia a `5.0 m/s²`.

**Texto en pantalla:** "10 newtons... 10 m/s². Los MISMOS 10 newtons... 5 m/s². ¿Por qué?"

**Narración (VO):**
> "Halas este carro con 10 newtons y acelera a 10 metros por segundo cuadrado. Ahora
> cuelgas un peso de exactamente 10 newtons de una cuerda... y solo acelera a 5. Misma
> fuerza. Mitad de aceleración. ¿Por qué?"

**Caption quemado:** `MISMOS 10 N → ¿POR QUÉ DISTINTA ACELERACIÓN?`

---

## 2. Guion completo con timeline

| Tiempo | En pantalla / animación Manim | Narración (VO) | Caption quemado |
|---|---|---|---|
| 0:00–0:07 | Carro halado a mano (10N → 10 m/s²), corte a polea+pesa (10N → 5 m/s²). | "Halas este carro con 10 newtons y acelera a 10 m/s². Cuelgas un peso de 10 newtons de una cuerda... y solo acelera a 5. Misma fuerza, mitad de aceleración. ¿Por qué?" | MISMOS 10 N → ¿POR QUÉ DISTINTA ACELERACIÓN? |
| 0:07–0:15 | `Write` de los datos: $m_{\text{carro}}=1\ \text{kg}$, mesa sin fricción, cada pesa = 10 N ($m=1$ kg), polea ideal. | "Un carro de 1 kilo, sobre una mesa sin fricción, conectado por una cuerda y una polea ideal a pesas de 10 newtons cada una." | m_carro = 1 kg · pesa = 10 N c/u |
| 0:15–0:24 | Caso A aislado: solo el carro + flecha $F=10\,\text{N}$. `TransformMatchingTex` de $a=F/m$ con los números. Carro se desliza, contador sube a `10.0 m/s²`. | "Si solo hay una mano halando, la segunda ley es directa: la fuerza entre la masa del carro. Diez entre uno, diez metros por segundo cuadrado." | a = F/m = 10/1 = 10.0 m/s² |
| 0:24–0:34 | Se reemplaza la mano por la polea + 1 pesa colgante. Texto: "la cuerda es inextensible: el carro y la pesa SIEMPRE tienen la misma aceleración". | "Ahora la fuerza la produce una pesa colgante, no una mano. La cuerda no se estira y la polea es ideal: el carro y la pesa se mueven exactamente igual de rápido, siempre." | misma cuerda = misma aceleración |
| 0:34–0:46 | Se dibuja un contorno alrededor de carro+pesa+cuerda ("el sistema completo"). `TransformMatchingTex`: $a = F_{\text{neta}}/m_{\text{total}}$, con $m_{\text{total}}=m_{\text{carro}}+m_{\text{pesa}}=2\ \text{kg}$. Contador baja de 10.0 a `5.0 m/s²`. | "Para resolverlo, tratamos carro y pesa como un solo sistema. La tensión es una fuerza interna, se cancela. Lo único que lo acelera desde afuera es el peso de la pesa: 10 newtons... repartidos entre 2 kilos de masa total. Cinco metros por segundo cuadrado." | a = 10N / 2kg = 5.0 m/s² |
| 0:46–0:52 | Texto: "¡Los mismos 10 N ahora también tienen que acelerarSE a sí mismos!" | "Por eso es la mitad: esos 10 newtons ya no solo mueven al carro, también tienen que acelerar a la pesa que los produce." | la fuerza también se acelera a sí misma |
| 0:52–1:02 | Montaje rápido: se agrega una 2ª pesa (contador a `6.67 m/s²`), luego una 3ª (contador a `7.50 m/s²`). Pesas se apilan colgando. | "Si cuelgas dos pesas, la aceleración sube a 6.67. Con tres, a 7.5. Cada pesa nueva empuja más fuerte... pero también pesa más." | +pesas → 6.67 m/s² → 7.50 m/s² |
| 1:02–1:12 | Texto de reto: "¿A qué valor se acerca la aceleración si cuelgas MUCHÍSIMAS pesas?" con $a=\dfrac{10n}{1+n}$ semi-transparente. | "Tu reto: si cuelgas muchísimas pesas, ¿a qué valor se acerca la aceleración? Coméntalo abajo." | 🧠 RETO: ¿EL LÍMITE CUANDO n→∞? |
| 1:12–1:20 | Resumen: "Trata el sistema conectado como un solo objeto. Solo cuenta la fuerza externa neta." | "La estrategia: si dos cuerpos están conectados por una cuerda ideal, trátalos como un solo sistema. Solo importa la fuerza externa que no se cancela." | un sistema, una sola ecuación |
| 1:20–1:24 | Cierre con marca de serie y llamada a seguir. | (música sube) | Sígueme para la Parte 4 👀 |

Duración total estimada: **~84 s** (ajustable con los mismos márgenes usados en los
videos 1 y 2).

---

## 3. Aspectos teóricos clave

1. **2ª Ley de Newton sobre un sistema conectado:** si dos cuerpos están unidos por una
   cuerda ideal (inextensible, sin masa) que pasa por una polea ideal (sin fricción,
   sin masa), pueden tratarse como **un solo sistema** de masa $m_{\text{total}}$,
   acelerado por la **fuerza externa neta** que actúa sobre el conjunto.
2. **La tensión es una fuerza interna del sistema.** Tira del carro hacia la polea y de
   la pesa hacia arriba con la misma magnitud (3ª ley aplicada a la cuerda ideal) — por
   eso se cancela al sumar fuerzas sobre el sistema completo, y solo sobrevive el peso
   de la parte que cuelga.
3. **Ligadura de la cuerda inextensible:** el carro y la(s) pesa(s) tienen siempre la
   misma rapidez y la misma aceleración en magnitud — la cuerda solo cambia la
   *dirección* de esa restricción (de horizontal a vertical) sin cambiar su valor.
4. **La misma fuerza puede producir aceleraciones muy distintas** según cuánta masa
   tenga que mover — incluida su propia masa, si la fuente de la fuerza también forma
   parte del sistema que se acelera (como la pesa colgante).
5. **La aceleración nunca alcanza ni supera $g$** en este montaje: por más pesas que
   cuelguen, $a=\dfrac{n\, m_{\text{pesa}}\, g}{m_{\text{carro}}+n\, m_{\text{pesa}}}$ se
   acerca a $g$ pero nunca lo alcanza, porque el carro (con masa fija) siempre le resta
   algo de aceleración al sistema.

---

## 4. Estrategia de resolución (metodología replicable)

1. **Identifica qué cuerpos están unidos por una cuerda/ligadura ideal** — si la cuerda
   no se estira y la polea es ideal, esos cuerpos comparten la misma rapidez y
   aceleración.
2. **Dibuja el sistema completo como un solo contorno** que encierre a todos los
   cuerpos conectados.
3. **Identifica la fuerza externa neta sobre ese contorno** — las tensiones internas
   (que tiran de un cuerpo hacia otro) se cancelan; sobrevive solo lo que "empuja o
   jala" desde afuera del sistema (aquí, el peso de la parte que cuelga).
4. **Suma las masas de todos los cuerpos del sistema** para obtener $m_{\text{total}}$.
5. **Aplica la 2ª ley al sistema completo**: $a = F_{\text{neta externa}}/m_{\text{total}}$.
6. *(Si necesitas la tensión misma, no la aceleración)*: aísla un solo cuerpo del
   sistema y aplica la 2ª ley solo a él — ahí la tensión sí aparece explícitamente.

---

## 5. Instrucciones de animación en Manim (reutilizar de los videos 1 y 2)

- Mismo código de color de la serie, adaptado: amarillo = fuerza aplicada/tensión,
  rojo = peso de las pesas, naranja = aceleración resultante.
- `cap_width()` en todo texto/fórmula — este video tiene fórmulas más largas
  ($a=F_{\text{neta}}/m_{\text{total}}$) que corren más riesgo de desbordar el frame
  angosto que las del video 2.
- **Evitar `TransformMatchingTex` entre fórmulas que no comparten sub-expresiones**
  (lección del video 2, `SKILL.md` sección 4): "$a=F/m$" y
  "$a=F_{\text{neta}}/m_{\text{total}}$" comparten poco texto literal — mejor usar
  `FadeOut` + `FadeIn` explícitos entre ellas, no dejar que Manim intente adivinar la
  correspondencia.
- `DecimalNumber` + `ValueTracker` para el contador de aceleración en vivo (10.0 → 5.0
  → 6.67 → 7.50), igual que el contador de $N$ del video 2 — es otra vez el elemento
  que más "engancha" porque el espectador ve el número cambiar con cada escenario.
- El **carro deslizándose** y las **pesas apilándose** al colgar más son el gancho
  visual central: usa el espacio vertical del frame (angosto pero alto) para apilar
  pesas hacia abajo — encaja naturalmente con el formato 9:16.
- Repasar la lista de bugs conocidos antes de programar (`SKILL.md` sección 4): un
  solo helper de geometría reutilizado (por ejemplo para la posición de cada pesa en la
  pila), todo `Write`/`FadeIn` con su `FadeOut`, cuidado con `.next_to()` heredando
  desplazamientos de un mobject ya desplazado.

---

## 6. Conclusión (texto exacto para pantalla y VO)

**Pantalla:** *"Sistema conectado = una sola masa total, una sola fuerza externa neta"*

**VO:**
> "Cuando dos cuerpos están unidos por una cuerda ideal, trátalos como un solo
> sistema: suma las masas, identifica la única fuerza externa que no se cancela, y
> aplica la segunda ley una sola vez."

---

## 7. Reto final / preguntas para seguir aprendiendo

**Reto principal:**
> "Si cuelgas muchísimas pesas, ¿a qué valor se acerca la aceleración? Coméntalo abajo
> — en la parte 4 lo resolvemos." *(spoiler para quien escriba la respuesta: se acerca
> a $g=10\ \text{m/s}^2$ pero nunca lo alcanza, porque el carro siempre le resta algo de
> aceleración al sistema por más pesas que cuelguen.)*

**Preguntas adicionales (elige 1-2):**
- Si en vez de colgar más pesas, pones 2 pesas *encima* del carro (sin que cuelguen) y
  dejas solo 1 pesa colgando, ¿la aceleración sube o baja respecto al caso de 1 sola
  pesa colgando? Calcúlalo. *(Respuesta: baja — la masa total sube a 4 kg pero la
  fuerza externa neta sigue siendo de solo 1 pesa, 10 N, así que $a=2{,}5\ \text{m/s}^2$,
  la mitad que con 1 pesa colgando y nada encima.)*
- ¿Qué tensión hay en la cuerda cuando cuelga 1 sola pesa? (pista: aísla solo la pesa
  y aplica la 2ª ley únicamente a ella, con la aceleración que ya calculaste para todo
  el sistema.)
- ¿Cambiaría algo si la mesa SÍ tuviera fricción? ¿Qué término habría que restarle a la
  fuerza externa neta? (gancho hacia una posible "parte 5" que combine este montaje con
  fricción, cerrando el círculo con el video 1 de la serie).

---

## 8. Especificaciones para publicar en TikTok

- Formato: MP4, vertical 1080×1920, sin bordes negros, 30fps.
- Duración: 75-85 s.
- Subtítulos quemados, sincronizados a la VO (columna "Caption quemado" de la tabla).
- Safe zones: nada importante en el 12% superior ni el 15% inferior del frame.
- Portada sugerida: el fotograma del hook con los dos números lado a lado, `10.0 m/s²`
  vs `5.0 m/s²` — la contradicción aparente es la miniatura más llamativa.
- Hashtags sugeridos: `#Fisica #SegundaLeyDeNewton #Poleas #Manim #ClaseDeFisica #CienciaTikTok`
- CTA: pedir la respuesta al reto del límite en comentarios + "sígueme para la parte 4".

---

## 9. Checklist antes de programar/publicar

- [ ] Todos los números coinciden con la tabla de la sección 0 (10.0 / 5.0 / 6.67 / 7.50 m/s²)
- [ ] $g=10\ \text{m/s}^2$ en todo el archivo (consistente con el video 2, no 9.8 del video 1)
- [ ] El video deja claro que la tensión es una fuerza *interna* que se cancela al
      tratar el sistema completo — es el punto que más se presta a confusión
- [ ] Ninguna fórmula ni texto se corta en los bordes del frame vertical (revisar con
      contact sheet, no solo leyendo el código)
- [ ] Duración final entre 75-85 s
- [ ] Reto y su spoiler verificados a mano antes de publicar la respuesta en la parte 4

---

## 10. Ideas para la serie (lo que falta del mismo taller)

Con este video quedan cubiertos los Problemas 1 (implícito, en el Caso A de este mismo
video), 2, 3 (video 1) y 4 (video 2) de `taller_segunda_ley.tex`. Queda pendiente:

- **Problema 5 (dos bloques en contacto empujados):** fuerza de contacto entre los dos
  bloques ($F_{12}$ vs $F_{21}$), 3ª ley de Newton — cierre natural de la serie, y buen
  candidato para la "Parte 4" que este video ya promete en el cierre.
