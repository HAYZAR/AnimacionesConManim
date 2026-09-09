"""
Genera la narracion en voz en off para un video, sincronizada con el timing
real calculado por tts_timing.py, y la mezcla con el video ya renderizado
(copiando el stream de video, sin recomprimir).

Dos backends de sintesis, elegidos con la variable de entorno TTS_BACKEND:

- "espeak" (por defecto): espeak-ng + mbrola, 100% offline, sin internet ni
  cuentas. No existe voz mbrola colombiana; usa mb-vz1 (venezolano) como la
  mas cercana disponible.
- "edge": Microsoft Edge Read Aloud (paquete "edge-tts" de PyPI), gratis y
  sin API key, con voces neuronales reales en espanol colombiano
  (es-CO-GonzaloNeural, es-CO-SalomeNeural). Requiere internet: pip install
  edge-tts. NOTA: el dominio speech.platform.bing.com que usa edge-tts esta
  bloqueado en algunos entornos en la nube (mismo bloqueo que Azure); en una
  maquina Windows/Mac/Linux normal con internet abierto funciona sin problema.

Uso: python3 generar_audio.py <carpeta_video> <archivo.py> <Clase> <video.mp4> <salida.mp4>
Lee el mapeo metodo->texto desde un archivo JSON <carpeta_video>/narracion.json

Ejemplos:
  python3 generar_audio.py carpeta escena.py MiClase in.mp4 out.mp4
  TTS_BACKEND=edge TTS_VOICE=es-CO-GonzaloNeural python3 generar_audio.py carpeta escena.py MiClase in.mp4 out.mp4
  TTS_BACKEND=edge TTS_VOICE=es-CO-SalomeNeural python3 generar_audio.py carpeta escena.py MiClase in.mp4 out.mp4
"""
import ast
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tts_timing import Evaluator  # noqa: E402

BACKEND = os.environ.get("TTS_BACKEND", "espeak")  # "espeak" o "edge"

VOZ_ESPEAK = "mb/mb-vz1"  # español venezolano (la variante mbrola offline mas cercana a
# Colombia disponible; no existe una voz mbrola colombiana). Alternativas:
# mb-mx1/mb-mx2 (mexicano), mb-es4 (España).
VELOCIDAD_ESPEAK = "175"  # palabras por minuto aprox

VOZ_EDGE = os.environ.get("TTS_VOICE", "es-CO-GonzaloNeural")  # o es-CO-SalomeNeural (femenina)
RATE_EDGE = os.environ.get("TTS_RATE", "+0%")  # p.ej "+10%" para hablar mas rapido

# Requiere ffmpeg/ffprobe siempre. Backend "espeak" requiere ademas espeak-ng +
# mbrola + una voz mbrola en español (p.ej. mbrola-es4). En Windows, instala
# espeak-ng con winget y coloca los archivos de voz mbrola (busca "mbrola-es"
# en tu gestor de paquetes o descarga los .deb de Debian y extrae los archivos
# de voz manualmente a la carpeta de espeak-ng si no hay paquete nativo para
# Windows) -- si no consigues mbrola, cambia VOZ_ESPEAK a "es-419" (espeak
# puro, mas robotico pero no necesita nada mas). Backend "edge" requiere
# `pip install edge-tts` e internet.


def calcular_timing(py_path, clase):
    with open(py_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(py_path))
    class_def = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == clase)
    methods = {n.name: n for n in class_def.body if isinstance(n, ast.FunctionDef)}
    construct = methods["construct"]
    ev = Evaluator(methods)

    call_order = []
    for node in construct.body:
        for child in ast.walk(node):
            if (
                isinstance(child, ast.Call)
                and isinstance(child.func, ast.Attribute)
                and isinstance(child.func.value, ast.Name)
                and child.func.value.id == "self"
            ):
                call_order.append(child.func.attr)

    timing = []
    t = 0.0
    for name in call_order:
        if name not in methods:
            continue
        dur = ev.method_duration(methods[name], {})
        timing.append((name, t, dur))
        t += dur
    return timing, t


def sintetizar(texto, out_audio):
    if BACKEND == "edge":
        subprocess.run(
            ["edge-tts", "--voice", VOZ_EDGE, "--rate", RATE_EDGE,
             "--text", texto, "--write-media", str(out_audio)],
            check=True, capture_output=True, text=True,
        )
    else:
        subprocess.run(
            ["espeak-ng", "-v", VOZ_ESPEAK, "-s", VELOCIDAD_ESPEAK, "-w", str(out_audio), texto],
            check=True, capture_output=True, text=True,
        )


def duracion_audio(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def main():
    carpeta, py_file, clase, video_in, video_out = sys.argv[1:6]
    carpeta = Path(carpeta)
    py_path = carpeta / py_file
    narracion = json.loads((carpeta / "narracion.json").read_text(encoding="utf-8"))

    timing, total = calcular_timing(py_path, clase)
    print(f"Backend TTS: {BACKEND}" + (f" (voz {VOZ_EDGE})" if BACKEND == "edge" else f" (voz {VOZ_ESPEAK})"))
    print(f"Duracion total calculada: {total:.2f}s")

    tmp = Path(tempfile.gettempdir()) / "manim_tts_audio" / carpeta.name
    tmp.mkdir(parents=True, exist_ok=True)

    ext = "mp3" if BACKEND == "edge" else "wav"
    clips = []  # (start_seconds_real, audio_path, duration)
    cursor = 0.0  # nunca se agenda un clip antes de que termine el anterior
    for name, start, dur in timing:
        texto = narracion.get(name)
        if not texto:
            continue
        audio_path = tmp / f"{name}.{ext}"
        sintetizar(texto, audio_path)
        d = duracion_audio(audio_path)
        inicio_real = max(start, cursor)
        cursor = inicio_real + d
        clips.append((inicio_real, audio_path, d))

        if d > dur + 0.3:
            nota = f"⚠ excede el beat ({dur:.1f}s) por {d - dur:.1f}s"
        elif inicio_real > start + 0.05:
            nota = f"↪ retrasado {inicio_real - start:.1f}s (el beat anterior se extendió)"
        else:
            nota = "OK"
        print(f"  {name:28s} beat={start:6.2f}s  real={inicio_real:6.2f}s  habla={d:5.2f}s  {nota}")

    # Base de silencio del largo total del video
    silencio = tmp / "silencio_base.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono",
         "-t", f"{total + 1.0:.2f}", str(silencio)],
        check=True, capture_output=True, text=True,
    )

    inputs = ["-i", str(silencio)]
    filtros = []
    mix_labels = ["[0]"]
    for i, (start, wav_path, d) in enumerate(clips, start=1):
        inputs += ["-i", str(wav_path)]
        delay_ms = int(start * 1000)
        filtros.append(f"[{i}]adelay={delay_ms}|{delay_ms}[a{i}]")
        mix_labels.append(f"[a{i}]")
    filtros.append(f"{''.join(mix_labels)}amix=inputs={len(mix_labels)}:duration=first:dropout_transition=0:normalize=0[aout]")
    filtro_completo = ";".join(filtros)

    narracion_wav = tmp / "narracion_completa.wav"
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", filtro_completo, "-map", "[aout]", str(narracion_wav)]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    print(f"Narracion mezclada: {narracion_wav}")

    # Mux con el video (copia el stream de video, codifica audio a aac)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(video_in), "-i", str(narracion_wav),
         "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
         "-shortest", str(video_out)],
        check=True, capture_output=True, text=True,
    )
    print(f"Video con narracion: {video_out}")


if __name__ == "__main__":
    main()
