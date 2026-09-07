# Escenas — La báscula en el ascensor (TikTok)

Segundo video de la serie "Segunda ley de Newton con fuerzas de contacto". Usa
**Manim Community Edition** (igual que el video 1, `dinamica_friccion_tiktok/`). El
guion completo está en [`GUION.md`](./GUION.md).

## Instalación y render

Ver `.claude/skills/manim-video-fisica-tiktok/SKILL.md` para instalación completa
(Linux/Windows). Resumen del render:

```bash
manim -ql --format=mp4 bascula_ascensor_tiktok.py BasculaAscensorTikTok   # prueba
manim -qh --format=mp4 --fps 30 bascula_ascensor_tiktok.py BasculaAscensorTikTok  # final
```

Verificado en esta sesión: 1080×1920, 30fps, 80.1s — dentro del rango 80-90s del
guion. Revisado con contact sheets (1 fotograma/seg) en toda la línea de tiempo, sin
texto cortado ni mobjects que queden en pantalla de más.

### `BasculaAscensorTikTok`

```python3
class BasculaAscensorTikTok(Scene):
```

<p align="center"><img src="./gifs/bascula_ascensor_tiktok.gif" /></p>

*(Genera el gif de vista previa con `manim -qm --format=gif ...` una vez que grabes la
voz en off y lo montes con audio.)*
