# Escenas — El bloque que no empujas también siente la fuerza (TikTok)

Cuarto y último video de la serie "Segunda ley de Newton con fuerzas de contacto".
Usa **Manim Community Edition** (igual que los videos 1-3). El guion completo está en
[`GUION.md`](./GUION.md).

## Instalación y render

Ver `.claude/skills/manim-video-fisica-tiktok/SKILL.md` para instalación completa
(Linux/Windows). Resumen del render:

```bash
manim -ql --format=mp4 bloques_contacto_tiktok.py BloquesContactoTikTok   # prueba
manim -qh --format=mp4 --fps 30 bloques_contacto_tiktok.py BloquesContactoTikTok  # final
```

Verificado en esta sesión: 1080×1920, 30fps, 85.8s — dentro del rango 75-86s del
guion. Revisado con contact sheets (1 fotograma/seg) en toda la línea de tiempo, sin
texto cortado ni mobjects que queden en pantalla de más.

Este video reutiliza el helper `cap_size` (ancho + alto) introducido en
`carro_polea_tiktok.py` — ver ese `ESCENAS.md` para el porqué (fracciones `\dfrac{}{}`
angostas pero muy altas).

### `BloquesContactoTikTok`

```python3
class BloquesContactoTikTok(Scene):
```

<p align="center"><img src="./gifs/bloques_contacto_tiktok.gif" /></p>

*(Genera el gif de vista previa con `manim -qm --format=gif ...` una vez que grabes la
voz en off y lo montes con audio.)*

---

Con este video se completan los 5 problemas de `taller_segunda_ley.tex` — ver la
sección 10 de `GUION.md` para el resumen de la serie completa.
