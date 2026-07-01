# AI_LOG

## M0

**Herramienta:** ChatGPT

**Uso:**
- Se consultó cómo estructurar el proyecto.
- Se pidió ayuda para entender el uso de Ruff y la organización del repositorio.
- Se pidió ayuda para modificar el diagrama de estructura con lenguaje mermaid.

**Resultado:**
- Se organizó la estructura inicial del proyecto y se corrigieron problemas de estilo.

---

## M1

**Herramienta:** ChatGPT

**Uso:**
| Prompt | Uso | Resultado |
|--------|-----|-----------|
| Implementación del algoritmo de Voss-McCartney | Se consultó sobre la implementación del algoritmo de Voss-McCartney para generar ruido rosa. | Se implementó la función `generar_ruido_rosa` siguiendo el algoritmo propuesto y adaptándola al proyecto. |
| Validación de inputs | Se consultó cómo manejar parámetros inválidos y cuándo utilizar excepciones. | Se incorporaron validaciones y `raise ValueError` en las funciones. |
| Uso de `np.random.seed()` | Se consultó el funcionamiento de `np.random.seed()` y su utilidad en los tests. | Se aclaró su uso para obtener resultados reproducibles durante las pruebas. |
| Modificación de ploteos | Se solicitó ayuda para modificar gráficos utilizados durante la verificación de señales. | Se ajustaron los ploteos para facilitar la interpretacón visual de los resultados. |
| Verificación de la pendiente espectral | Se consultó cómo verificar la pendiente espectral del ruido rosa utilizando el método de Welch. | Se definió un criterio de validación del espectro basado en la estimación mediante Welch. |
| Implementación del test del rango de frecuencias del sine sweep | Se solicitó ayuda para implementar el test basado en el espectrograma. | Se desarrolló un test utilizando el espectrograma y posteriormente se ajustó para contemplar la resolución frecuencial. |
| Corrección de errores en `sine_sweep` | Se utilizó el modelo para identificar errores en la implementación de `generar_sine_sweep` y proponer correcciones. | Se corrigieron aspectos de la implementación y se ajustaron los tests para verificar correctamente su funcionamiento. |
| Correción del test del sine sweep | Se consultó por fallos en la comparación entre la frecuencia dominante y la frecuencia instantánea teórica. | Se identificó que las diferencias se debían a la resolución del espectrograma y se modificó el criterio de validación del test. |
| Adaptación de `reproducir_y_grabar` a la especificación | Se consultó cómo cumplir el requisito de utilizar `sounddevice.sd.playrec()` manteniendo la captura de la cola de reverberación. | Se reemplazó el uso de `sd.rec()` y `sd.play()` por `sd.playrec()`, agregando un post-roll de silencio para completar la duración de grabación. |
| Revisión de la implementación de `reproducir_y_grabar` | Se solicitó una revisión completa del código para detectar errores lógicos y oportunidades de mejora. | Se agregaron validaciones adicionales y se mejoró la legibilidad del código. |
| Actualización de los tests de grabación | Se pidió adaptar los tests a la nueva implementación basada en `sd.playrec()`. | Se actualizaron los *mocks* y se adecuaron los tests al nuevo funcionamiento de la función. |

**Herramienta:** Copilot (VSC)

**Uso:**
- Se estructuró un prompt para realizar la función reproducir_y_grabar en base a los requisitos.
- Se hizo uso del autocompletado para modificar el código de las funciones sine_sweep y pink_noise de forma eficiente. Asimismo, se utilizó la funcion de autocompletado para comentar sobre los procedimientos, lo cual permitó un mejor entendimiento del lenguaje y el código entre los integrantes del grupo.


---

## M2

**Fecha:** 2026-07-01

**Herramienta:** ChatGPT

**Uso:**
- Se pidió ayuda para diseñar tests con `pytest`.

**Resultado:**
- Se implementaron los tests de duración, tipo, normalización y espectro.
