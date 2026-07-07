# AI_LOG

## GENERAL
 
 Se utilizaron distintos modelos durante la construcción de la api para optimizar el desarrollo y aprendizaje:

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Generación preliminar de funciones a partir de las especificaciones del Milestone 2. | Se solicitaron implementaciones iniciales de las funciones para comprender el flujo general del código y contar con una base de trabajo.  | Se obtuvo una primera versión de las funciones, que luego fue revisada y modificada manualmente para adecuarse a los requisitos del proyecto y a criterios de diseño establecidos por los integrantes.                  |

Reflexión: El diseño preliminar de funciones fue escencial para entender la organización del código. Nos permitió entender el proposito de funciones especificas de librerías como Numpy, Sounddevice, entre otras. En base a esto se buscaron y se consultó a los distintos modelos (CHATgpt, Copilot, CLaude) por alternativas mas simples y eficientes para el desarrollo y legibilidad de las funciones.

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Autocompletado de documentación del código. Funciones FIX y EXPLAIN (errores)                                 | Se utilizó el autocompletado de Copilot para generar docstrings y comentarios descriptivos durante el desarrollo.                         | Se documentaron las funciones siguiendo un formato consistente, facilitando la comprensión del código por parte del resto de los integrantes del equipo.    

Reflexión: Además de facilitar tareas repetitivas de escritura y correción, se utilizó para dejar descripciones claras como comentarios durante el desarrollo de las funciones. De esta forma, se facilitó el entendimiento del código entre integrantes. Asimismo, se usaron las funciones FIX y EXPLAIN al obtener errores con el fin de detectar la fuente de los mismos.

A continuación se encuentran los usos especificos durante cada Milestone:

## M0

### Herramienta: ChatGPT

Fecha: 24/04/26

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Modificación del diagrama de estructura | Se solicitó ayuda para modificar el diagrama de arquitectura utilizando lenguaje Mermaid. | Se actualizó el diagrama para representar correctamente la estructura del proyecto y facilitar su documentación en el README. |
| Configuración del entorno y ejecución de la API | Se solicitó ayuda para comprender cómo levantar el servidor con Uvicorn e instalar las dependencias necesarias para ejecutar la API y los tests. | Se configuró el entorno de desarrollo, se instalaron las dependencias requeridas y se logró ejecutar correctamente la API y pasar los tests de *health* correspondientes. |

---

## M1

### Herramienta: ChatGPT

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Implementación del algoritmo de Voss-McCartney | Se consultó sobre la implementación del algoritmo de Voss-McCartney para generar ruido rosa. | Se logró un mejor entendimiento sobre la función del algoritmo. |
| Validación de inputs | Se consultó cómo manejar parámetros inválidos y cuándo utilizar excepciones. | Se incorporaron validaciones y `raise ValueError` en las funciones. |
| Modificación de ploteos | Se solicitó ayuda para modificar gráficos de validación manual de las funciones `sine_sweep` y `pink_noise`. | Se ajustaron los ploteos para facilitar la interpretacón visual de los resultados. |
| Verificación de la pendiente espectral | Se consultó cómo verificar la pendiente espectral del ruido rosa utilizando el método de Welch. | Se definió un criterio de validación del espectro basado en la estimación mediante Welch. |
| Corrección de errores en `sine_sweep` | Se utilizó el modelo para identificar errores en la implementación de `generar_sine_sweep` y proponer correcciones. | Se corrigieron aspectos de la implementación y se ajustaron los tests para verificar correctamente su funcionamiento. |
| Implementación del test del rango de frecuencias del sine sweep | Se solicitó ayuda para implementar el test basado en el espectrograma. | Se desarrolló un test utilizando el espectrograma y posteriormente se ajustó para contemplar la resolución frecuencial. |
| Correción del test del sine sweep | Se consultó por fallos en la comparación entre la frecuencia dominante y la frecuencia instantánea teórica. | Se identificó que las diferencias se debían a la resolución del espectrograma y se modificó el criterio de validación del test. |
| Adaptación de `reproducir_y_grabar` a la especificación | Se consultó cómo cumplir el requisito de utilizar `sounddevice.sd.playrec()` manteniendo la captura de la cola de reverberación. | Se reemplazó el uso de `sd.rec()` y `sd.play()` por `sd.playrec()`, agregando un post-roll de silencio para completar la duración de grabación. |
| Revisión de la implementación de `reproducir_y_grabar` | Se solicitó una revisión completa del código para detectar errores lógicos y oportunidades de mejora. | Se agregaron validaciones adicionales y se mejoró la legibilidad del código. |
| Actualización de los tests de grabación | Se pidió adaptar los tests a la nueva implementación basada en `sd.playrec()`. | Se actualizaron los *mocks* y se adecuaron los tests al nuevo funcionamiento de la función. |

---

## M2

**Herramienta:** ChatGPT

Fecha: 11/06/26 al 16/06/26

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Recomendaciones para validar las funciones del Milestone 2.     | Se consultó qué aspectos funcionales y casos de prueba eran adecuados para verificar cada una de las funciones implementadas.                                    | Se definieron criterios de validación acordes a la funcionalidad de cada servicio y se utilizaron como base para el desarrollo de los tests.                |
| Diseño de tests.                  | Se pidió ayuda para estructurar y redactar tests para las funciones `cargar_audio`, `a_escala_log`, `sintetizar_ri`, `obtener_ri_desde_sweep` y `filtro_octava`. | Se obtuvieron propuestas de tests que luego fueron revisadas y adaptadas antes de incorporarlas al proyecto.                                                |
| Validación del tiempo de reverberación (T60).                   | Se consultó cómo comprobar que la respuesta al impulso sintetizada reproduce el T60 especificado mediante la curva de Schroeder.                                 | Se implementó un procedimiento de validación y un test que estima el T60 y lo compara con el valor esperado dentro de una tolerancia.                       |
| Validación de la recuperación de la respuesta al impulso.       | Se pidió ayuda para verificar que `obtener_ri_desde_sweep` recupera correctamente una RI conocida utilizando un sweep y su filtro inverso.                       | Se definió una comparación basada en correlación normalizada, considerando el alineamiento realizado por la función.                                        |

Reflexión: La validación de `obtener_ri_desde_sweep` para que tenga la correlación requerida con un a ri sintetizada fué dificil de formular. Como `obtener_ri_desde_sweep` corta los picos previos al primer pico máximo, los impulsos (original y recuperado) quedaban desalineados. Se aplicó un alineamiento y un pre-roll a la ri original para asegurar que ambas señales tengan la misma duración. Inicialmente esto se hizo porque en general los parametros acústicos toman el pico maximo del impulso como punto inicial.

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Revisión de funciones implementadas.                            | Se solicitaron revisiones del código de las funciones del Milestone 2 para comprobar que la lógica y las validaciones fueran correctas.                          | Se identificaron posibles mejoras y se confirmó el comportamiento esperado de las implementaciones antes de elaborar los tests.                             |
| Reconocimiento y análisis de errores.                           | Se consultó sobre errores detectados durante la ejecución de tests, validaciones manuales y herramientas de análisis estático (Ruff).                            | Se identificó el origen de los errores y se ajustaron los tests y el código para obtener resultados consistentes y cumplir con los estándares del proyecto. |
| Revisión de estrategias de validación para el filtro de octava. | Se consultó cuál era la forma más adecuada de verificar el funcionamiento del filtro solicitado por la consigna.                                                 | Se analizaron distintas alternativas de validación y se evaluó cuál verificaba mejor el comportamiento de la función implementada.                          |


### Herramienta: Claude

Fecha: 27/06/26
| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Implementar tests para `filtro_octava` (frecuencia central, atenuación, respuesta en frecuencia) | Generación de código de test con pytest, reconstruyendo el filtro SOS con `scipy.signal.butter` y analizando su respuesta con `sosfreqz` | Se generaron los 3 tests (`test_filtro_octava_frecuencia_central`, `test_filtro_octava_atenuacion`, `test_filtro_octava_respuesta_frecuencia`) con helpers `_sos_octava` y `_ganancia_db_en` reutilizables |
| Reescribir y reorganizar `test_procesamiento.py` completo integrando todas las clases de test existentes (`TestObtenerRIdesdeSweep`, `TestCargarAudio`, `TestAEscalaLog`, `TestSintetizarRI`, `TestFiltroOctava`) | Reestructuración de archivo de tests para mejorar legibilidad y evitar duplicación de código | Archivo consolidado con imports y helpers al inicio, separadores por bloque |

Fecha: 03/07/26

| Prompt | Uso | Resultados |
|---|---|---|
| Pedido de unificar `sintetizar_ri` y `filtro_octava` | Refactor de `signal_utils.py` para que `sintetizar_ri` reutilice `filtro_octava` en vez de reimplementar el diseño del filtro | `filtro_octava` quedó como única implementación (robusta: soporta multicanal, clipea `Wn`, fallback a `sosfilt` si no hay `sosfiltfilt`); `sintetizar_ri` la importa y la usa, eliminando código de validación de banda duplicado |

Reflexión: Se utilizó la IA para reorganizar y estructurar elementos faltantes o poco robusctos de M2, con el fin de obtener una versión final de la API mucho mas limpia. Se integraron tests que validaran los raises de cada función, y varios tests adicionales que sugirió el modelo con el fin de debuggear resultados.

---

## M3

**Herramienta:** Claude

Fecha: 04/07/26

| Prompt | Uso | Resultados |
|---|---|---|
| Pedido de ayuda para realizar gráfico preliminar de respuesta en frecuencia del banco de filtros de octava | Creación de un script de graficado usando `sosfreqz` sobre el diseño real del filtro | Se generó una figura con las 9-10 bandas IEC 61260 superpuestas en escala log |

Reflexión: Para realizar el gráfico se pidieron alternativas. Una era definir una función dentro de `app.services.filter.py` que implementara `sosfreqz` pero se optó por llevar a cabo este paso en un archivo  independiente a las funciones escenciales del proyecto. 

Fecha: 05/07/26

| Prompt | Uso | Resultado |
|---|---|---|
| Diseñar `/api/v1/filters/band` para que devuelva las 9 bandas de octava (no 6) | Comparación con el JSON de referencia de cátedra (`file_paths`) | Definidas 3 opciones de diseño (paths+download, ZIP, base64); se eligió ZIP en memoria (`io.BytesIO`, sin tocar disco) por ser stateless y más simple en Render |
| Metadata del ZIP (`sample_rate`, `num_samples`, `bandwidth`, `center_frequencies`) | Diseño de schema `BandFilterHeaders` + documentación de headers HTTP en OpenAPI | Router `/filters/band` completo devolviendo ZIP + headers `X-*`; schema Pydantic solo para los headers (el body binario no tiene `response_model`) |
| Agregar `/filters/frequencies` (GET) y `/filters/single-band` (POST) | Extensión del router de filtros utilizando `filtro_octava`  | Dos endpoints nuevos: uno devuelve lista fija de frecuencias, otro filtra una sola banda y devuelve WAV + headers |

Reflexión: Se eligió que el endpoint devuelva un ZIP con archivos de audio WAV filtrados por banda para que sea mas accesible. Como se quería mantener un response body con la metadata se consultó con el modelo y decidimos dejar la informacion en los headers.

| Prompt | Uso | Resultado |
|---|---|---|
| Diseñar `/api/v1/acoustics/parameters/by-bands` | Comparación de campos (`file_info`, `analysis_settings`, `band_results`, `parameters`) contra el `openapi.json` real de referencia | Schema y router completos, con reshape de `dict[parametro][fc]` a las dos vistas (`band_results` transpuesto y `parameters` por tipo) |
| Diseñar `/api/v1/acoustics/parameters` (banda completa, sin filtrar por octava) | Reutilización de `calcular_parametros_acusticos` con flag `sin_filtrar=True` en vez de duplicar función | Único punto de cálculo para banda completa y por bandas; evita reescribir el pipeline Schroeder + regresión |

Reflexión: Se eligió integrar en una misma función ambos casos (señal completa, señal filtrada) a partir de un bool para no duplicar la función.

| Prompt | Uso | Resultado |
|---|---|---|
| Resolver `noise_analysis` (`estimated_noise_level`, `estimated_snr_db`) sin implementar Lundeby | Estimador simplificado por energía de cola de la señal (no es el algoritmo Lundeby) | Función `estimar_ruido_de_fondo` documentada explícitamente como aproximación, no como método de Lundeby |
| Armar `/api/v1/analysis/impulse-response/by-bands` completo | Integración de `calcular_parametros_acusticos` + `estimar_ruido_de_fondo` en un solo endpoint | Endpoint completo con `lundeby_applied: false` y `cutoff_time: null` explícitos, coherente con el JSON de referencia cuando Lundeby no se aplica |

Reflexión: Se integró la función estimar_ruido_de_fondo ya que, al no utilizar Lundeby hay limitaciones en el cálculo de los parámetros. La SNR estimada puede dar información valiosa al momento de determinar la calidad de los parámetros obtenidos. Si se obtiene una SNR alta los parámetros entregados serán mas fieles al comportamiento real de la sala.

Fecha: 06/07/26

| Prompt | Uso | Resultado |
|---|---|---|
| Restructuración del informe final (`informe.md`) con la redacción real de la documentación de M1, M2 y M3, vinculación de las 17 figuras a los archivos del repositorio y eliminación de secciones no deseadas | Se pidió reescribir el informe usando el contenido ya redactado en las documentaciones de cada milestone, reemplazar las rutas de imagen provisorias por las 17 correspondientes al repositorio real, y sacar del informe la columna "¿Cumple?" de la tabla de validación.| Se obtuvo un informe consolidado con el análisis de gráficos y resultados de M1/M2/M3, las 17 imágenes correctamente vinculadas (incluyendo nombres de archivo con espacios, tildes y paréntesis), y las secciones y columna solicitadas eliminadas |

Reflexión: Para esta etapa se priorizó que el informe reflejara fielmente lo que ya estaba documentado en cada milestone, en lugar de generar contenido nuevo, ya que gran parte del análisis de los gráficos y las validaciones ya existía en las documentaciones de M1, M2 y M3. La vinculación de las imágenes resultó más delicada de lo esperado, ya que varios nombres de archivo del repositorio tenían espacios, tildes y paréntesis que rompían la sintaxis de Markdown, por lo que se debió recurrir a la codificación de URL para cada caso particular. 

## M3 · Producto Final — Utils, revisión de código y fixes de integración

| Prompt | Uso | Resultado |
|---|---|---|
| Diseñar `/api/v1/utils/schroeder`, `/log-scale`, `/smoothing` | Comparación de los response bodies de ejemplo (`num_samples`, `t_max`, `file_path`, etc.) contra las funciones ya implementadas (`integral_schroeder`, `a_escala_log`, `suavizar_signal`) | Se decidió devolver `.npy` binario para `schroeder`/`log-scale` (curvas numéricas) y WAV para `smoothing` (sigue siendo una señal temporal), con metadata en headers HTTP |
| Preguntar si conviene devolver un array completo de 192000 valores en JSON | Discusión de downsampling vs. mantener formato de la referencia | Se descartó el downsampling: se decidió mantener consistencia con la cátedra devolviendo `.npy` con el array completo, serializado en memoria sin tocar disco |

Reflexión: Nos resultó mas ordenado en este caso obtener un archivo numpy antes que el array, ya que centraliza toda la información en un archivo y hay menos riesgo de perder data por error.

| Prompt | Uso | Resultado |
|---|---|---|
| Endpoint `/smoothing` con dos opciones implementadas | Revisión de `suavizar_signal` ya implementada (soporta ambos vía el parámetro `ventana`) | Endpoint `/smoothing` expone ambos métodos (`hilbert` por defecto, `moving_average` con `window_ms` requerido); validación 422 si falta `window_ms` |

Para la revisión final:
| Prompt | Uso | Resultado |
|---|---|---|
| Revisión de tests ya escritos (`test_analisis.py`, `test_generacion.py`, `test_procesamiento.py`) | Comparación de cada test contra el código real para detectar redundancia o gaps de cobertura | Detectado un test duplicado en `regresion_lineal` (mismos datos, mismo assert); identificados gaps en `reproducir_y_grabar` (sin tests de validaciones) que se completaron con 3 tests nuevos |
| Debug: 404 en CI de GitHub Actions en todos los endpoints de M3 | Diagnóstico comparando qué rutas fallaban (todas menos `/health` y `/`) | Causa raíz: routers definían `prefix`/`tags` propios en `APIRouter(...)` Y `main.py` volvía a pasarlos en `include_router(...)`, duplicando el path (`/api/v1/utils/api/v1/utils/...`). Corregido en `filters.py`, `acoustics.py`, `analysis.py`, `utils.py`: `router = APIRouter()` sin argumentos |
| Confirmar y ajustar el alcance de bandas por endpoint (6 de validación vs. 9 completas) | Discusión de diseño: `/acoustics/parameters/by-bands` (validación contra REW) vs. `/analysis/impulse-response/by-bands` (diagnóstico exploratorio con SNR) vs. `/filters/band` (filtrado general) | Se fijaron 3 alcances distintos e intencionales: 6 bandas IEC 125–4000 Hz para validación, 9 bandas completas 31.5–8000 Hz para análisis exploratorio y para filtrado general |

Reflexión: Ya que se incorpora el SNR estimado en el response body de los endpoints de análisis, se decidió incorporar también las 9 bandas. De esta manera, el usuario puede determinar si los parametros son fieles a la respuesta real del recinto (si se tiene una SNR mayor a 45 dB aproximadamente, ya que T60 se estima con T30/T20)

| Prompt | Uso | Resultado |
|---|---|---|
| Sumar el filtro inverso del sine sweep como opción, igual que la API de referencia | Comparación contra el schema `SineSweepRequest`/`inverse` de la referencia | Se agregó el campo `inverse: bool` al request; el mismo endpoint `/sine-sweep` devuelve el sweep o el filtro inverso según el flag, sin necesidad de un endpoint separado |
