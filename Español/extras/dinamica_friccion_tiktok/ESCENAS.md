# Escenas — Dinámica con fricción para TikTok

Proyecto independiente del resto del curso: usa **Manim Community Edition**
(el resto del repositorio usa la versión antigua de 3b1b/manim). El guion
completo (narración, timings, especificaciones para TikTok) está en
[`GUION.md`](./GUION.md).

## Instalación (distinta a `0_instalacion/`)

```bash
# Linux (Debian/Ubuntu) — dependencias del sistema que ManimCE necesita
sudo apt-get install libcairo2-dev libpango1.0-dev ffmpeg texlive-full

pip install manim
```

Ver la guía oficial si tu sistema no es Debian/Ubuntu:
https://docs.manim.community/en/stable/installation.html

## Render

```bash
cd Español/extras/dinamica_friccion_tiktok
manim -pqh --format=mp4 dinamica_friccion_tiktok.py DinamicaFriccionTikTok
```

- `-p` reproduce el video al terminar, `-qh` calidad alta (1080p base, aquí
  reconfigurado a 1080×1920 vertical dentro del propio script).
- Usa `-ql` (calidad baja) mientras iteras el timing, y `-qh` o `-qk` para
  la versión final que subirás a TikTok.

### 

```python3
class DinamicaFriccionTikTok(Scene):
```

<p align="center"><img src="./gifs/dinamica_friccion_tiktok.gif" /></p>

*(Genera el gif de vista previa con `manim -qm --format=gif ...` y colócalo
en `gifs/` una vez renderizado el video final.)*
