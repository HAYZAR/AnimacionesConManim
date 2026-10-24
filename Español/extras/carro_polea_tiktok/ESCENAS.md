# Escenas — La misma fuerza, la mitad de aceleración (TikTok)

Tercer video de la serie "Segunda ley de Newton con fuerzas de contacto". Usa
**Manim Community Edition** (igual que los videos 1 y 2). El guion completo está en
[`GUION.md`](./GUION.md).

## Instalación y render

Ver `.claude/skills/manim-video-fisica-tiktok/SKILL.md` para instalación completa
(Linux/Windows). Resumen del render:

```bash
manim -ql --format=mp4 carro_polea_tiktok.py CarroPoleaTikTok   # prueba
manim -qh --format=mp4 --fps 30 carro_polea_tiktok.py CarroPoleaTikTok  # final
```

Verificado en esta sesión: 1080×1920, 30fps, 75.5s — dentro del rango 75-85s del
guion. Revisado con contact sheets (1 fotograma/seg) en toda la línea de tiempo, sin
texto cortado ni mobjects que queden en pantalla de más.

Bug particular de este video (además de los ya conocidos, ver `SKILL.md` sección 4):
las fórmulas con `\dfrac{}{}` (fracciones grandes) son angostas pero muy **altas** —
`cap_width` no basta, hace falta también limitar la altura (`cap_size` en este
archivo) o evitar `\dfrac` y usar una división en línea ("/") cuando el texto vaya
apilado cerca de otros elementos de la escena.

### `CarroPoleaTikTok`

```python3
class CarroPoleaTikTok(Scene):
```

<p align="center"><img src="./gifs/carro_polea_tiktok.gif" /></p>

*(Genera el gif de vista previa con `manim -qm --format=gif ...` una vez que grabes la
voz en off y lo montes con audio.)*
