# Informe de la Medición 2:

Asumimos que el recinto se comporta como un sistema Lineal e Invariante en el Tiempo (LTI). Bajo esta hipótesis, la sala queda completamente caracterizada por una única función: su Respuesta al Impulso (h(t)). 
Cualquier sonido que se reproduzca en la sala (x(t)) saldrá modificado como una grabación (y(t)) que es el resultado de la convolución matemática: 

y(t)=h(t)* x(t)

Si se pudiera reproducir un impulso ideal, es decir, x(T)= delta de dirac. ENTONCES, NOS TERMINARÍA QUEDANDO QUE Y(T)=H(T),  es decir, que nuestra grabación sería directamente nuestra respuesta al impulso.

Recordemos que generamos un impulso con el sine sweep convolucionado con sul filtro inverso. (M1).

Hay que realizar la deconvolución. Recordemos que x(t)= sine sweep * filtro inverso= impulso no perfecto.

Se utilizó la transformada rápida de Fourier.

Grafico de IR sintetica:

<img width="558" height="298" alt="image" src="https://github.com/user-attachments/assets/8e3f0860-d42d-4031-95cd-52b9472c10db" />

Forma de onda líneal. Eje horizontal tiempo y Eje vertical amplitud. 

Se concentra en el tiempo t=0 s con una amplitud máxima de 1 y esta decae de forma exponencial a cero de forma natural. La energía decrece de forma muy rapida

FALTA GRAFICO ESPECTRAL!
En este es la misma señal pero promediado RMS y luego escalado a escala logartimica, esto se da para poder observar la pendiente de como deae la energia de forma linealmente. 


sintetizar_ri: T60 medido dentro del 10% del especificado por banda
<img width="422" height="318" alt="image" src="https://github.com/user-attachments/assets/0b7ca016-be15-4420-bcb7-b8bcaa40465f" />

Sintetizar RI con T60=2.0s a 1000Hz.Filtrar la RI sintetizada en la banda de 1000 Hz.Calcular la curva de decaimiento en dB (Schroeder).Medir el tiempo en que la curva cruza -60 dB.

Deconvolución: Correlación cruzada con RI original > 0.9.
