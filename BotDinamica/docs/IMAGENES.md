# Diagramas para las preguntas (TikZ → PNG → GitHub)

Inspirado en cómo [`Evaluaciones-Saber-11`](https://hayzar.github.io/Evaluaciones-Saber-11/)
resuelve esto (SVG dibujado a mano dentro de cada pregunta). Aquí se usa
TikZ compilado a PNG en vez de SVG a mano porque es más rápido de producir
para diagramas de física (fuerzas, DCL) sin dibujar vector por vector, y un
PNG vía `<img>` funciona igual de bien tanto en el chat como en el test —
ambos viven ahora en la misma página HTML (ver `docs/ARQUITECTURA.md`; el
test ya no se resuelve en un Google Form aparte). El flujo es: **autoría en
TikZ → build automático a PNG → hosting en GitHub → URL en la columna
`Imagen_URL` del Banco**.

## 1. Autoría: escribe el diagrama en TikZ

Crea un archivo en `BotDinamica/imagenes/tikz/<ID>.tex`, donde `<ID>` es
exactamente el `ID` de la fila del Banco a la que pertenece (ej. `DIN-001.tex`
para el problema `DIN-001`). Usa la clase `standalone` para que el PDF
resultante sea solo el dibujo, sin márgenes de página:

```latex
\documentclass[tikz,border=3pt]{standalone}
\begin{document}
\begin{tikzpicture}
  % tu diagrama aquí
\end{tikzpicture}
\end{document}
```

Hay un ejemplo completo y comentado en
[`../imagenes/tikz/EJEMPLO-DIN-001.tex`](../imagenes/tikz/EJEMPLO-DIN-001.tex)
— un diagrama de cuerpo libre con fuerza aplicada, normal, peso y fricción.
Cópialo como punto de partida para tus propios diagramas.

## 2. Build automático: GitHub Actions compila TikZ → PNG

El workflow
[`.github/workflows/build-imagenes-dinamica.yml`](../../.github/workflows/build-imagenes-dinamica.yml)
(en la raíz del repositorio) se dispara en cada push que toque
`BotDinamica/imagenes/tikz/**.tex`:

1. Corre en un contenedor `texlive/texlive` (TeX Live completo, incluye
   `pdflatex` y `pdftoppm`).
2. Compila cada `.tex` a `.pdf` y lo convierte a `.png` (200 dpi) en
   `BotDinamica/imagenes/render/<ID>.png`.
3. Commitea los PNG generados de vuelta al repositorio automáticamente.

> **Nota de transparencia:** este workflow sigue el patrón estándar para
> compilar TikZ en CI (imagen `texlive/texlive` + `pdflatex` + `pdftoppm`),
> pero no pude ejecutarlo en este entorno de desarrollo (no tiene `pdflatex`
> instalado) para verificarlo end-to-end. Después de hacer el primer push
> con un `.tex` nuevo, revisa la pestaña **Actions** del repositorio para
> confirmar que corrió bien; si el contenedor `texlive/texlive` resulta muy
> pesado/lento para tu caso, una alternativa simple es compilar en tu propia
> máquina (o en [Overleaf](https://overleaf.com)) y subir el PNG resultante
> a mano a `imagenes/render/`.

Si prefieres no depender de CI, puedes compilar localmente con cualquier
distribución TeX (TeX Live, MacTeX, MiKTeX):
```bash
cd BotDinamica/imagenes/tikz
pdflatex DIN-001.tex
pdftoppm -png -r 200 DIN-001.pdf ../render/DIN-001
mv ../render/DIN-001-1.png ../render/DIN-001.png
```

## 3. Hosting: cómo obtener la URL pública

Una vez el PNG está commiteado en `BotDinamica/imagenes/render/`, tienes dos
opciones para la URL (ambas gratuitas, sin configuración adicional de
servidor):

- **`raw.githubusercontent.com` (recomendado, cero configuración):**
  ```
  https://raw.githubusercontent.com/<usuario>/<repo>/<rama>/BotDinamica/imagenes/render/DIN-001.png
  ```
  Funciona apenas el archivo está commiteado en esa rama, sin habilitar nada
  más. Es la opción más simple si el repositorio es público.

- **GitHub Pages** (si ya la usas para `frontend/`, puede ser más prolijo
  tener todo bajo el mismo dominio):
  ```
  https://<usuario>.github.io/<repo>/BotDinamica/imagenes/render/DIN-001.png
  ```
  Requiere que Pages esté habilitado para la rama/carpeta que incluye
  `BotDinamica/imagenes/render/`.

Copia la URL elegida en la columna `Imagen_URL` de la fila correspondiente
en el Banco.

## 4. Cómo se usa `Imagen_URL` en el bot

- **Chat** (`LLM.gs` + `frontend/script.js`): el banco completo (incluyendo
  `Imagen_URL`) se envía al LLM. `INSTRUCCION_IMAGENES` (en `Constantes.gs`)
  le indica que, si el problema que va a presentar tiene `Imagen_URL`, la
  incluya en su mensaje como Markdown `![Diagrama](URL)`. El frontend
  detecta ese patrón y lo convierte en una etiqueta `<img>` real
  (`script.js::renderizarMensajeBot`).
- **Test adaptativo** (`Test.gs::obtenerProblemasTest`): el campo
  `imagen_url` se incluye tal cual en cada problema que se envía al
  frontend; `script.js::crearTarjetaPreguntaTest` la agrega como `<img>`
  arriba de las opciones.

## Por qué no SVG inline (como en Evaluaciones-Saber-11)

Ese enfoque es válido ahora que todo (chat y test) vive en la misma página
HTML — ya no hay una restricción técnica que lo impida, como sí la había
mientras el test se generaba como un Google Form real (que no puede
renderizar SVG/HTML arbitrario). Se mantiene TikZ → PNG porque ya está
construido y probado, y porque compilar diagramas de fuerzas/DCL en TikZ es
más rápido que dibujarlos vector por vector a mano en SVG. Si en el futuro
se quiere ese nivel de control fino sobre el dibujo, migrar a SVG inline
siguiendo el patrón de `Evaluaciones-Saber-11` sigue siendo una opción
razonable — ya no exigiría rehacer el resto de la arquitectura.
