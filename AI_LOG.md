# AI_LOG

## M0

### Herramienta: ChatGPT

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Modificación del diagrama de estructura | Se solicitó ayuda para modificar el diagrama de arquitectura utilizando lenguaje Mermaid. | Se actualizó el diagrama para representar correctamente la estructura del proyecto y facilitar su documentación en el README. |
| Configuración del entorno y ejecución de la API | Se solicitó ayuda para comprender cómo levantar el servidor con Uvicorn e instalar las dependencias necesarias para ejecutar la API y los tests. | Se configuró el entorno de desarrollo, se instalaron las dependencias requeridas y se logró ejecutar correctamente la API y pasar los tests de *health* correspondientes. |

---

## M1

### Herramienta: ChatGPT

**Uso:**
| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Implementación del algoritmo de Voss-McCartney | Se consultó sobre la implementación del algoritmo de Voss-McCartney para generar ruido rosa. | Se logró un mejor entendimiento sobre la función del algoritmo. |
| Validación de inputs | Se consultó cómo manejar parámetros inválidos y cuándo utilizar excepciones. | Se incorporaron validaciones y `raise ValueError` en las funciones. |
| Uso de `np.random.seed()` | Se consultó el funcionamiento de `np.random.seed()` y su utilidad en los tests. | Se aclaró su uso para obtener resultados reproducibles en los tests. |
| Modificación de ploteos | Se solicitó ayuda para modificar gráficos de validación manual de las funciones `sine_sweep` y `pink_noise`. | Se ajustaron los ploteos para facilitar la interpretacón visual de los resultados. |
| Verificación de la pendiente espectral | Se consultó cómo verificar la pendiente espectral del ruido rosa utilizando el método de Welch. | Se definió un criterio de validación del espectro basado en la estimación mediante Welch. |
| Corrección de errores en `sine_sweep` | Se utilizó el modelo para identificar errores en la implementación de `generar_sine_sweep` y proponer correcciones. | Se corrigieron aspectos de la implementación y se ajustaron los tests para verificar correctamente su funcionamiento. |
| Implementación del test del rango de frecuencias del sine sweep | Se solicitó ayuda para implementar el test basado en el espectrograma. | Se desarrolló un test utilizando el espectrograma y posteriormente se ajustó para contemplar la resolución frecuencial. |
| Correción del test del sine sweep | Se consultó por fallos en la comparación entre la frecuencia dominante y la frecuencia instantánea teórica. | Se identificó que las diferencias se debían a la resolución del espectrograma y se modificó el criterio de validación del test. |
| Adaptación de `reproducir_y_grabar` a la especificación | Se consultó cómo cumplir el requisito de utilizar `sounddevice.sd.playrec()` manteniendo la captura de la cola de reverberación. | Se reemplazó el uso de `sd.rec()` y `sd.play()` por `sd.playrec()`, agregando un post-roll de silencio para completar la duración de grabación. |
| Revisión de la implementación de `reproducir_y_grabar` | Se solicitó una revisión completa del código para detectar errores lógicos y oportunidades de mejora. | Se agregaron validaciones adicionales y se mejoró la legibilidad del código. |
| Actualización de los tests de grabación | Se pidió adaptar los tests a la nueva implementación basada en `sd.playrec()`. | Se actualizaron los *mocks* y se adecuaron los tests al nuevo funcionamiento de la función. |

### Herramienta: Copilot (Visual Studio Code)

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Implementación de `reproducir_y_grabar` | Se estructuró un prompt para generar una primera versión de la función `reproducir_y_grabar` a partir de los requisitos establecidos en la especificación. | Se obtuvo una implementación inicial que luego fue revisada, adaptada y corregida manualmente para cumplir con la especificación del proyecto. |
| Autocompletado en `generar_sine_sweep` | Se utilizó el autocompletado para agilizar la escritura y modificación del código de la función `generar_sine_sweep`. | Se redujo el tiempo de edición del código, manteniendo la lógica definida por el equipo. |
| Autocompletado en `generar_ruido_rosa` | Se utilizó el autocompletado para agilizar la implementación y modificación de la función `generar_ruido_rosa`. | Se facilitaron tareas repetitivas de escritura y refactorización sin modificar el diseño del algoritmo. |
| Generación de comentarios | Se utilizó el autocompletado para sugerir comentarios descriptivos y documentación del código. | Se mejoró la legibilidad del código y la comprensión de los procedimientos implementados por parte de los integrantes del grupo. |

---

## M2

**Herramienta:** ChatGPT

| **Prompt**                                                      | **Uso**                                                                                                                                                          | **Resultado**                                                                                                                                               |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Recomendaciones para validar las funciones del Milestone 2.     | Se consultó qué aspectos funcionales y casos de prueba eran adecuados para verificar cada una de las funciones implementadas.                                    | Se definieron criterios de validación acordes a la funcionalidad de cada servicio y se utilizaron como base para el desarrollo de los tests.                |
| Diseño de tests unitarios para el Milestone 2.                  | Se pidió ayuda para estructurar y redactar tests para las funciones `cargar_audio`, `a_escala_log`, `sintetizar_ri`, `obtener_ri_desde_sweep` y `filtro_octava`. | Se obtuvieron propuestas de tests que luego fueron revisadas y adaptadas antes de incorporarlas al proyecto.                                                |
| Validación del tiempo de reverberación (T60).                   | Se consultó cómo comprobar que la respuesta al impulso sintetizada reproduce el T60 especificado mediante la curva de Schroeder.                                 | Se implementó un procedimiento de validación y un test que estima el T60 y lo compara con el valor esperado dentro de una tolerancia.                       |
| Validación de la recuperación de la respuesta al impulso.       | Se pidió ayuda para verificar que `obtener_ri_desde_sweep` recupera correctamente una RI conocida utilizando un sweep y su filtro inverso.                       | Se definió una comparación basada en correlación normalizada, considerando el alineamiento realizado por la función.                                        |
| Revisión de funciones implementadas.                            | Se solicitaron revisiones del código de las funciones del Milestone 2 para comprobar que la lógica y las validaciones fueran correctas.                          | Se identificaron posibles mejoras y se confirmó el comportamiento esperado de las implementaciones antes de elaborar los tests.                             |
| Reconocimiento y análisis de errores.                           | Se consultó sobre errores detectados durante la ejecución de tests, validaciones manuales y herramientas de análisis estático (Ruff).                            | Se identificó el origen de los errores y se ajustaron los tests y el código para obtener resultados consistentes y cumplir con los estándares del proyecto. |
| Revisión de estrategias de validación para el filtro de octava. | Se consultó cuál era la forma más adecuada de verificar el funcionamiento del filtro solicitado por la consigna.                                                 | Se analizaron distintas alternativas de validación y se evaluó cuál verificaba mejor el comportamiento de la función implementada.                          |


### Herramienta: Claude

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Implementar tests para `filtro_octava` (frecuencia central, atenuación, respuesta en frecuencia) según el Test 4 del enunciado | Generación de código de test con pytest, reconstruyendo el filtro SOS con `scipy.signal.butter` y analizando su respuesta con `sosfreqz` | Se generaron los 3 tests (`test_filtro_octava_frecuencia_central`, `test_filtro_octava_atenuacion`, `test_filtro_octava_respuesta_frecuencia`) con helpers `_sos_octava` y `_ganancia_db_en` reutilizables |
| Corregir `ComplexWarning: Casting complex values to real discards the imaginary part` en los tests de filtro de octava | Debugging de un warning de numpy al castear el array complejo `h` (salida de `sosfreqz`) a `dtype=float` | Se identificó y eliminó el cast `np.asarray(h, dtype=float)`; se usó `np.abs(h)` directamente sobre el complejo para calcular la magnitud en dB |
| Reescribir y reorganizar `test_procesamiento.py` completo integrando todas las clases de test existentes (`TestObtenerRIdesdeSweep`, `TestCargarAudio`, `TestAEscalaLog`, `TestSintetizarRI`, `TestFiltroOctava`) | Reestructuración de archivo de tests para mejorar legibilidad y evitar duplicación de código | Archivo consolidado con imports y helpers al inicio, separadores por bloque, y sin el error de casting complejo |


### Herramienta: Copilot (Visual Studio Code)

| **Prompt**                                                                           | **Uso**                                                                                                                                   | **Resultado**                                                                                                                                                  |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Generación preliminar de funciones a partir de las especificaciones del Milestone 2. | Se solicitaron implementaciones iniciales de las funciones para comprender el flujo general del código y contar con una base de trabajo.  | Se obtuvo una primera versión de las funciones, que luego fue revisada y modificada manualmente para adecuarse a los requisitos del proyecto.                  |
| Simplificación y refactorización del código.                                         | Se consultaron alternativas para reducir complejidad, eliminar pasos repetitivos y mejorar la legibilidad de las funciones implementadas. | Se simplificó la estructura del código, eliminando operaciones redundantes y realizando modificaciones para obtener implementaciones más claras y mantenibles. |
| Autocompletado de documentación del código.                                          | Se utilizó el autocompletado de Copilot para generar docstrings y comentarios descriptivos durante el desarrollo.                         | Se documentaron las funciones siguiendo un formato consistente, facilitando la comprensión del código por parte del resto de los integrantes del equipo.       |

