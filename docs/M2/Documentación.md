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

Forma de onda líneal. Eje horizontal tiempo y Eje vertical amplitud.

Se concentra en el tiempo t=0 s con una amplitud máxima de 1 (debido a que fue normalizada la respuesta al impulso entre esos valores), y esta decae de forma exponencial a cero de forma natural. Podemos observar que el pico más alto es la señal directa y luego tenemos las reflexiones primarias y las reflexiones secundarias que van decayendo con el tiempo, la energía decrece de forma muy rapida.

También quisimos observan la respuesta al impulso con escala logarítmica para poder observar el comportamiento en el tiempo de forma más detallada. Se normalizó a RMS para obtener un promedio de energía y ver la tendencia general. 
INSERTAR GRÁFICO DE LA ENVOLVENTE: 

Podemos observar que es una recta por lo tanto confirma que es un decaimiento exponencial. Asimismo la recta debe tener como punto que a 60 dB los segundos deben ser 1,2 ya que fue lo establecido. Nosotros obtuvimos (PONER EL PUNTO QUE VEMOS EN EL GRÁFICO), podemos considerar un pequeño error debido a que el test de sintetizar RI acepta un error menor a 10%, es decir, nuestro T60 podía estar entre 1,08 segundos a 1,32 segundos. 

A continuación con el sine sweep que se obtuvo con anterioridad:


https://github.com/valentinadepiero/trabajo-practico-ss/blob/69a072043316a4f56c9fed7fd7772973395e8ceb/app/services/sine_sweep.py

Se convoluciono con su filtro inverso (realizado anteriormente) y se obtuvo un impulso perfecto. ( Recordemos que $x(t)$= sine sweep * filtro inverso= impulso no perfecto).

Debemos tener en cuenta que como diseño se eligió crear canales separados para el sine sweep y otro para su filtro inverso, para que el usuario pueda utilizarlos por separado de ser necesario. 


Para obtener nuestra respuesta al impulso $h(t)$ asumimos que el recinto se comporta como un sistema Lineal e Invariante en el Tiempo (LTI). Por lo tanto, se puede plantear que $x(t)$ es la sala la cual saldrá modificada como una grabación $y(t)$ que es el resultado de la convolución matemática: 

$y(t)=h(t)* x(t)$

Cómo logramos reproducir un pulso casi perfecto con nuestro sine sweep y su inverso entonces podemos decir que $x(t)=\delta(x)$ en consecuencia $y(t)=h(t)$ en otras palabras nuestra grabación sería directamente nuestra respuesta al impulso.

Debemos tener en cuenta que la respuesta al impulso obtenida por el sweep tenía recortada la información anterior al pico máximo, por lo tanto cuando buscamos la correlación entre ambas RI (la sintetizada con la obtenida con la convolución), se alinearon y se debió eliminar las primeros picos hasta el máximo de la RI sintetizada. De esta forma cumplio con el objetivo requerido por el test OBETENER_RI_DESDE_SWEEP que tenía como criterio la correlación cruzada con RI original (sintetizada) debe ser mayor a 0,9. 

Podemos observar en los siguientes gráficos la correlación entre ambas respuestas al impulso: 

<img width="1200" height="500" alt="image" src="https://github.com/user-attachments/assets/eb2b22de-a004-4966-b3b6-29e178b1cc62" />

En el eje Y se encuentra la amplitud y en el eje X el tiempo. En naranaja tenemos la RI recueprada que es la obtenida mediante la convolución y en celeste la RI original que es la sinteitzada. Podemos ver que se obtuvo una correlación del 0,9955 

En la siguiente figura observamos un grafico más adetalle de la correlacion en los primeros 100ms. 

<img width="1200" height="500" alt="image" src="https://github.com/user-attachments/assets/ce5b1fc3-7368-49b2-8637-aa65f819ad21" />





sintetizar_ri: T60 medido dentro del 10% del especificado por banda
<img width="422" height="318" alt="image" src="https://github.com/user-attachments/assets/0b7ca016-be15-4420-bcb7-b8bcaa40465f" />

Sintetizar RI con T60=2.0s a 1000Hz.Filtrar la RI sintetizada en la banda de 1000 Hz.Calcular la curva de decaimiento en dB (Schroeder).Medir el tiempo en que la curva cruza -60 dB.

Deconvolución: Correlación cruzada con RI original > 0.9.
