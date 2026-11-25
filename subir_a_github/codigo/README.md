# Gardiáns do Clima

Videojuego educativo en **Python** para **4º de Primaria**, en **gallego**, pensado para **pizarra digital táctil** (todo se juega tocando y arrastrando; no hace falta teclado).

Estilo: formato de RPG de consola portátil (mapa visto desde arriba, diálogos con retrato, batalla por turnos) con **dibujos de estilo infantil** (formas suaves con contorno, sin píxeles), todos originales y dibujados por código.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python main.py
```

- Se abre a **pantalla completa**. Resolución interna 1280×720, escalada con suavizado a la pantalla.
- Para probarlo en ventana: `python main.py --xanela`.
- Botones en las esquinas: ⛶ pantalla completa y 🏠 volver al inicio. La tecla Esc también vuelve al inicio.

## Versión web (jugar en el navegador, sin instalar nada)

El juego se convierte a página web con **pygbag** (Python en WebAssembly).

1. Generar la versión web (desde la carpeta que contiene `videojuego`):
   ```bash
   pip install pygbag
   python -m pygbag --build --archive videojuego
   ```
   Crea `videojuego/build/web` (la página) y `videojuego/build/web.zip` (para subir).
2. Subirla a **itch.io** (gratis): *Upload new project* → *Kind of project: HTML* → subir `web.zip` → marcar *This file will be played in the browser* → *Viewport dimensions* 1280 × 720 → activar *Fullscreen button*. En *Visibility* se puede elegir *Restricted* (con contraseña) o *Public*.
3. Probar en local antes de subir: `python -m http.server 8001 --directory videojuego/build/web` y abrir `http://localhost:8001`.

Notas de la versión web:
- La primera carga tarda unos 30-40 s (el navegador descarga Python). Después queda en caché.
- Se necesita conexión a internet (Python se descarga del CDN de pygbag).
- El sonido empieza tras el primer toque. El récord no se guarda entre sesiones.
- La fuente es **Nunito** (licencia SIL OFL, incluida en `fontes/`).

## Nivel 1: O tempo e o clima (libro, Unidad 2, págs. 26-39)

Una misión por cada apartado del tema. Cada reto se resuelve **aplicando los contenidos**. Al fallar, la Dra. Brisa muestra una pista explicativa.

| Misión | Págs. | Retos |
|---|---|---|
| 1. A atmosfera e o tempo | 26-27 | Clasificar qué hace la atmósfera · Ordenar evaporación → condensación → precipitación · Unir fenómenos con su explicación · Colocar símbolos en el mapa del tiempo según la predicción y leerlo |
| 2. Elementos e factores | 28-29 | Clasificar elementos/factores · Unir cada instrumento con lo que mide · Colocar temperaturas en una montaña (−1 °C cada 100 m) · Preguntas con imágenes (latitud, mar, relieve…) |
| 3. Os climas de España | 30-31 | Colocar las zonas climáticas en el globo y situar España · Colocar los 6 climas en el mapa de España · Unir cada clima con sus características · Preguntas (clima e incendios) |
| 4. Os climogramas | 32-33 | Leer el climograma de Ciudad Real · Completar un climograma con la tabla (tocar la altura de barras y puntos) · Comparar Ciudad Real y Santander |
| 5. As paisaxes | 34-35 | Unir paisajes (imágenes) con su descripción · Clasificar plantas por paisaje · **Ronda arcade**: tocar un fuego → pregunta → si se acierta llueve y se apaga (paisajes, causas y prevención de incendios) |
| 6. O clima de Galicia | 36-37 | Colocar las 3 variedades del clima oceánico en el mapa de Galicia · Clasificar sus características · Para qué sirve una estación meteorológica · Preguntas sobre el riesgo de incendio |
| 7. O clima está cambiando | 38-39 | Clasificar causas/consecuencias · Acciones que ayudan o perjudican · Unir las TIX con su función · **Batalla final** contra el Barón Feluxe con preguntas de todo el tema |

En las tarjetas se puede **arrastrar** o **tocar la tarjeta y después el destino**. Desde el título, **ESCOLLER MISIÓN** permite ir directamente a cualquier misión (útil para trabajar un apartado concreto en clase).

## Personajes
- **Nubi**: la nube protagonista.
- **Dra. Brisa**: meteoróloga; presenta cada misión y da las pistas.
- **Banda Tisne**: el **Barón Feluxe** y su robot **Tubiño**, villanos ambientales (humo, chispas, talas).

## Editar contenidos
Todos los textos están en [`datos.py`](datos.py): diálogos, tarjetas, parejas para unir, datos de los climogramas y **preguntas** (una lista por misión: `P1` … `P7`). Para añadir una pregunta, copia una existente:

```python
{"tipo": "test", "p": "Pregunta?", "ops": ["Correcta", "Incorrecta 1", "Incorrecta 2"], "ok": 0,
 "exp": "Explicación que se muestra después."},
```
- `tipo`: `"test"`, `"vf"` (con `"ok": True/False`) u `"oco"` (frase con `___`).
- `img` (opcional): nombre de una ilustración de [`arte.py`](arte.py) (por ejemplo `termometro`, `paisaxe_canaria`, `latitude`, `arco`, `estacion`).

Los datos de **Ciudad Real** son los del libro; los de **Santander** son aproximados.
Los mapas de España y Galicia son **simplificados** (dibujados por código para 4º de Primaria).

## Estructura del código

| Archivo | Contenido |
|---|---|
| `main.py` | Arranque (pantalla completa) y bucle principal |
| `datos.py` | **Todos los textos y preguntas en gallego** |
| `escenas.py` | Título, menú de misiones, diálogos, misión completada, resultados y flujo |
| `retos.py` | Retos táctiles: clasificar, ordenar, unir, colocar, mapa del tiempo, preguntas, climogramas |
| `preguntas.py` | Panel de preguntas y banco sin repeticiones |
| `lumes.py` | Ronda arcade de los fuegos (misión 5) |
| `batalla.py` | Batalla final por turnos (misión 7) |
| `arte.py` | Personajes, símbolos del tiempo, instrumentos, paisajes, plantas… |
| `mapas.py` | Mapas de España y Galicia, globo de zonas climáticas y montaña |
| `mapa.py` | Mapa del Val Verde |
| `pincel.py` | Herramienta de dibujo con contornos y suavizado |
| `ui.py`, `texto.py`, `entrada.py`, `sonido.py`, `config.py` | Botones, textos, entrada táctil, sonidos y constantes |

El récord se guarda en `record.json` junto al juego.
