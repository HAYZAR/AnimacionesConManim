# "<Título llamativo>" — Guion y ficha de producción

<Una frase describiendo el video: tema de física, formato, duración objetivo.>

Producido con **Manim Community Edition**, renderizado en vertical 9:16.

---

## 0. Ficha técnica rápida

| Parámetro | Valor |
|---|---|
| Resolución | 1080×1920 px (9:16) |
| FPS | 30 |
| Duración objetivo | <rango, ej. 60-90 s> |
| Motor | Manim Community Edition |
| Escena principal | `<NombreEscena>` (`<archivo>.py`) |
| Audio | <voz en off / solo texto+música / etc.> |
| Paleta de color física | Peso = rojo, Normal = azul, Fricción = verde, Neta/aceleración = naranja |

**Problema numérico fijo (verificado a mano antes de animar):**

```
<Escribe aquí las cuentas del problema con los números finales, igual que en
Español/extras/dinamica_friccion_tiktok/GUION.md. Si los números no cuadran
aquí, no van a cuadrar en el video.>
```

---

## 1. Introducción llamativa (Hook, 0:00–0:0X)

**Regla de oro TikTok: el gancho debe entenderse en los primeros 1-2 segundos solo
con el texto en pantalla, sin depender del audio.**

**Animación:** <qué se ve en pantalla desde el frame 0>

**Texto en pantalla:** "<...>"

**Narración (VO):** "<...>"

---

## 2. Guion completo con timeline

| Tiempo | En pantalla / animación Manim | Narración (VO) | Caption quemado |
|---|---|---|---|
| 0:00–0:0X | | | |
| ... | | | |

---

## 3. Aspectos teóricos clave (los que el video *debe* dejar claros)

1. ...

---

## 4. Estrategia de resolución (metodología replicable)

1. ...

---

## 5. Instrucciones precisas de animación en Manim

- Código de color fijo y consistente (ver ficha técnica). Nunca reasignar un color a
  otro concepto.
- Formato vertical real: `config.pixel_width/height` configurados antes de la escena.
- Todo texto/fórmula pasa por `cap_width()` (ver SKILL.md sección 4.1).
- Zonas seguras: nada importante en el 12% superior ni el 15% inferior del frame.

---

## 6. Conclusión (texto exacto para pantalla y VO)

**Pantalla:** "<...>"

**VO:** "<...>"

---

## 7. Reto final / preguntas para seguir aprendiendo

**Reto principal:** "<...>"

**Preguntas adicionales (elige 1-2):**
- ...

---

## 8. Especificaciones para publicar en TikTok

- Formato: MP4, vertical 1080×1920, sin bordes negros.
- Duración: <rango>.
- Subtítulos quemados: <sí/no y estilo>.
- Portada (cover): <qué frame usar>.
- Música: <sugerencia>.
- Hashtags sugeridos: `#... #... #...`

---

## 9. Checklist antes de publicar

- [ ] Duración final dentro del rango objetivo
- [ ] Resolución 1080×1920, sin franjas negras
- [ ] Hook comprensible con el sonido apagado
- [ ] Ningún texto cortado en los bordes (revisado con contact sheet, no solo leyendo el código)
- [ ] Ningún mobject "fantasma" (Write sin su FadeOut correspondiente)
- [ ] Números coherentes entre guion, animación y VO
- [ ] CTA + pregunta de reto presentes en el cierre
