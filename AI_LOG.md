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

**Uso:**
- Se pidió ayuda para diseñar tests con `pytest`.

**Resultado:**
- Se implementaron los tests de duración, tipo, normalización y espectro.

### Herramienta: Claude
Acá tenés la tabla para tu AI log:

| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Implementar tests para `filtro_octava` (frecuencia central, atenuación, respuesta en frecuencia) según el Test 4 del enunciado | Generación de código de test con pytest, reconstruyendo el filtro SOS con `scipy.signal.butter` y analizando su respuesta con `sosfreqz` | Se generaron los 3 tests (`test_filtro_octava_frecuencia_central`, `test_filtro_octava_atenuacion`, `test_filtro_octava_respuesta_frecuencia`) con helpers `_sos_octava` y `_ganancia_db_en` reutilizables |
| Corregir `ComplexWarning: Casting complex values to real discards the imaginary part` en los tests de filtro de octava | Debugging de un warning de numpy al castear el array complejo `h` (salida de `sosfreqz`) a `dtype=float` | Se identificó y eliminó el cast `np.asarray(h, dtype=float)`; se usó `np.abs(h)` directamente sobre el complejo para calcular la magnitud en dB |
| Reescribir y reorganizar `test_procesamiento.py` completo integrando todas las clases de test existentes (`TestObtenerRIdesdeSweep`, `TestCargarAudio`, `TestAEscalaLog`, `TestSintetizarRI`, `TestFiltroOctava`) | Reestructuración de archivo de tests para mejorar legibilidad y evitar duplicación de código | Archivo consolidado con imports y helpers al inicio, separadores por bloque, y sin el error de casting complejo |
| Consulta sobre error marcado en líneas de `np.interp` (imagen de editor) | Diagnóstico de posible error de sintaxis/ejecución | Se determinó que el subrayado correspondía al corrector ortográfico del editor, no a un error real de Python; se solicitó traceback completo para confirmar |
