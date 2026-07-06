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

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Recomendaciones para validar las funciones del Milestone 2.     | Se consultó qué aspectos funcionales y casos de prueba eran adecuados para verificar cada una de las funciones implementadas.                                    | Se definieron criterios de validación acordes a la funcionalidad de cada servicio y se utilizaron como base para el desarrollo de los tests.                |
| Diseño de tests.                  | Se pidió ayuda para estructurar y redactar tests para las funciones `cargar_audio`, `a_escala_log`, `sintetizar_ri`, `obtener_ri_desde_sweep` y `filtro_octava`. | Se obtuvieron propuestas de tests que luego fueron revisadas y adaptadas antes de incorporarlas al proyecto.                                                |
| Validación del tiempo de reverberación (T60).                   | Se consultó cómo comprobar que la respuesta al impulso sintetizada reproduce el T60 especificado mediante la curva de Schroeder.                                 | Se implementó un procedimiento de validación y un test que estima el T60 y lo compara con el valor esperado dentro de una tolerancia.                       |
| Validación de la recuperación de la respuesta al impulso.       | Se pidió ayuda para verificar que `obtener_ri_desde_sweep` recupera correctamente una RI conocida utilizando un sweep y su filtro inverso.                       | Se definió una comparación basada en correlación normalizada, considerando el alineamiento realizado por la función.                                        |
| Revisión de funciones implementadas.                            | Se solicitaron revisiones del código de las funciones del Milestone 2 para comprobar que la lógica y las validaciones fueran correctas.                          | Se identificaron posibles mejoras y se confirmó el comportamiento esperado de las implementaciones antes de elaborar los tests.                             |
| Reconocimiento y análisis de errores.                           | Se consultó sobre errores detectados durante la ejecución de tests, validaciones manuales y herramientas de análisis estático (Ruff).                            | Se identificó el origen de los errores y se ajustaron los tests y el código para obtener resultados consistentes y cumplir con los estándares del proyecto. |
| Revisión de estrategias de validación para el filtro de octava. | Se consultó cuál era la forma más adecuada de verificar el funcionamiento del filtro solicitado por la consigna.                                                 | Se analizaron distintas alternativas de validación y se evaluó cuál verificaba mejor el comportamiento de la función implementada.                          |


### Herramienta: Claude

Fecha: 27/06/26
| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Implementar tests para `filtro_octava` (frecuencia central, atenuación, respuesta en frecuencia) | Generación de código de test con pytest, reconstruyendo el filtro SOS con `scipy.signal.butter` y analizando su respuesta con `sosfreqz` | Se generaron los 3 tests (`test_filtro_octava_frecuencia_central`, `test_filtro_octava_atenuacion`, `test_filtro_octava_respuesta_frecuencia`) con helpers `_sos_octava` y `_ganancia_db_en` reutilizables |
| Reescribir y reorganizar `test_procesamiento.py` completo integrando todas las clases de test existentes (`TestObtenerRIdesdeSweep`, `TestCargarAudio`, `TestAEscalaLog`, `TestSintetizarRI`, `TestFiltroOctava`) | Reestructuración de archivo de tests para mejorar legibilidad y evitar duplicación de código | Archivo consolidado con imports y helpers al inicio, separadores por bloque, y sin el error de casting complejo |

Fecha: 03/07/26

| Prompt | Uso | Resultados |
|---|---|---|
| Pedido de unificar `sintetizar_ri` y `filtro_octava` | Refactor de `signal_utils.py` para que `sintetizar_ri` reutilice `filtro_octava` en vez de reimplementar el diseño del filtro | `filtro_octava` quedó como única implementación (robusta: soporta multicanal, clipea `Wn`, fallback a `sosfilt` si no hay `sosfiltfilt`); `sintetizar_ri` la importa y la usa, eliminando código de validación de banda duplicado |

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
| Diseñar `/api/v1/filters/band` para que devuelva las 10 bandas de octava (no 6) | Comparación con el JSON de referencia de cátedra (`file_paths`) | Definidas 3 opciones de diseño (paths+download, ZIP, base64); se eligió ZIP en memoria (`io.BytesIO`, sin tocar disco) por ser stateless y más simple en Render |
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
