# Informe de la Medición 2:

Como primera acción se realizó la función grabar y se delimitó que está solo funcione con archivos de audio WAV y FLAC,  en el caso que se inserte otro tipo de archivo responderá con error. Asimismo se normalizó a (-1,1) para en un futuro no tener problemas con los ploteos por distorsión. Se delimitó a que solamente acepta audios de 1 o 2 dimensiones, es decir, mono o estéreo. En el caso de que se reciba un audio estéreo se convertirá en mono por: 

 ```python
mean(axis=1) 

   ```
Luego creamos una respuesta al impulso sintetizada a la cual le establecimos los valores de T60 por banda de octava. Esta la utilizaremos para comprobar que nuestra api funcione correctamente cuando utilicemos respuestas al impulso reales.  

El paso a paso para crear la respuesta al impulso sintetizada fue: 

- [x] Generar ruido blanco.
- [x] Filtrar por pasa-banda de octava 
- [x] Normalizar a RMS.
- [x] Multiplicarlo por una envolvente $e^{-at}$ para que decaiga de forma exponencial.
- [x] Se sumaron todas las bandas de octavas.
- [x] Normalizar 


Los parámetros de referencia que se utilizaron para el siguiente gráfico fueron la frecuencia central de 1000 Hz con una duración 4 segundos, frecuencia de sampleo de 44100 Hz y un T60 de 1,2 segundos. 

Grafico de IR sintetica grafico de forma lineal:

<img width="558" height="298" alt="image" src="https://github.com/user-attachments/assets/8e3f0860-d42d-4031-95cd-52b9472c10db" />

Podemos observar que el pico más alto es la señal directa y luego tenemos las reflexiones primarias y las reflexiones secundarias que van decayendo con el tiempo. Asimismo se observa que el grafico va desde 1 a -1 debido a que fue normalizada la respuesta al impulso entre esos valores. 

También quisimos observan la respuesta al impulso con escala logarítmica para poder observar el comportamiento en el tiempo de forma más detallada. Se normalizó a RMS para obtener un promedio de energía y ver la tendencia general. 



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
