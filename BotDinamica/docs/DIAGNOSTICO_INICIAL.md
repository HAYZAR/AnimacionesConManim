# Diagnóstico inicial (6 problemas)

Set inicial de problemas para el primer test que responde un estudiante,
antes de que empiece la intervención socrática. Cubre un aprendizaje por
problema, con contexto (situación reconocible) y diagrama donde aporta
claridad — ver `docs/BANCO_PROBLEMAS.md` (columna `Contexto`) y
`docs/IMAGENES.md` (columna `Imagen_URL`).

Archivo listo para importar a la hoja `Banco`:
[`banco/Banco_Diagnostico.csv`](../banco/Banco_Diagnostico.csv).

## Los 6 aprendizajes cubiertos

| ID | Aprendizaje | Nivel | Demanda cognitiva | Contexto | Diagrama |
|---|---|---|---|---|---|
| `DIAG-01` | Peso vs Masa | 1 | Interpretar | Astronauta Tierra/Luna | No |
| `DIAG-02` | Diagrama de cuerpo libre | 2 | Modelar | Balón de fútbol en reposo | Sí (`DIAG-02.png`) |
| `DIAG-03` | Primera Ley de Newton (equilibrio) | 2 | Aplicar | Bus a velocidad constante | No |
| `DIAG-04` | Segunda Ley de Newton (F=ma) | 2 | Aplicar | Ciclista empujando su bicicleta | No |
| `DIAG-05` | Tercera Ley de Newton (acción-reacción) | 2 | Interpretar | Tira y afloja | Sí (`DIAG-05.png`) |
| `DIAG-06` | Fricción (cinética vs. aplicada) | 2 | Aplicar | Empujar una caja de libros | Sí (`DIAG-06.png`) |

Las fuentes TikZ de los 3 diagramas están en `imagenes/tikz/DIAG-02.tex`,
`DIAG-05.tex` y `DIAG-06.tex`. Al hacer push, el workflow de GitHub Actions
los compila a `imagenes/render/DIAG-0X.png` automáticamente (ver
`docs/IMAGENES.md`); el `Imagen_URL` de cada fila del CSV ya apunta a esa
ruta esperada.

## Pendiente de definir con el docente

Estas preguntas quedaron planteadas pero **sin resolver todavía** — no se
implementó ninguna automatización de esto en el código hasta que se
confirmen, para no imponer un criterio no acordado:

- **Umbral de prioridad de intervención**: ¿qué desempeño en este
  diagnóstico marca a un estudiante como prioritario? (ej. `<50%` global,
  o fallar por completo 2+ aprendizajes).
- **Aprendizaje mínimo aceptable** para continuar sin intervención
  obligatoria (ej. dominar Peso vs Masa + DCL + Segunda Ley, dejando
  Fricción/Tercera Ley como refuerzo paralelo no bloqueante).
- **Criterio de cierre de la intervención** por estudiante (hasta alcanzar
  un umbral, número fijo de sesiones, o decisión manual del docente).

Una vez definidos, se pueden reflejar en `Perfil.gs` (ej. un campo
`prioridad` calculado en `construirPerfilEstudiante`) y/o en un reporte
para el docente — no implementado aún.
