# Informe de la Medición 1:
Generamos Ruido Rosa debido a que este suele escogerse por encima del Ruido blanco por la similitud de percepción que tiene al oído humano, precisamente  a que reduce la energía en altas frecuencias. Como característica este tiene una “densidad espectral inversamente proporcional a la frecuencia. En la escala logarítmica esto equivale a una caída de -3 dB por octava” (citar info M). 

Para poder llevar a cabo la elaboración del ruido rosa tomamos como decisión de diseño el algoritmo Voss-McCartney, el cual consiste en “una suma de múltiples generadores de ruido blanco que se actualiza a tasas 2^i. El generador se actualiza cuando el bit del índice cambia. La suma produce una señal cuyo espectro se aproxima a la inversa de la frecuencia (1/f)”. 

En el momento de llevar esto a cabo surgió como dificultad la comprensión de la tasa de refresco de los generadores de ruido blanco. Al consultar con los docentes se aclaró sobre el orden, que los generadores de índice bajo se actualizan más seguido a diferencia que los del final. Luego fue necesario la ayuda para ciertos acabados del autocompletado inteligente del Visual Studio Code. Asimismo se utilizó como prompt en el copilot: “Generar una función de ruido rosa a través del algoritmo Voss McCartney de forma tal que devuelva un array normalizado entre -1 y 1, que el generador de ruido blanco sea de 16 bits, que para cada n muestras determina cuándo debe actualizarse y que sume las salidas de los generadores”. 

GRÁFICO RUIDO ROSA:  (PSD vs FRECUENCIA)

<img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/468cdeab-3dd5-4709-89f6-92fc84e1f1e9" />


La PSD (Densidad Espectral de Potencia) se expresa en dB/Hz para describir cómo se distribuye la potencia o energía de una señal en un espectro de frecuencias, es decir, a lo largo de las distintas frecuencias que la componen. 

Se observa que hay una caída de 3.18dB por banda de banda de octava, es decir, que pasó el test de espectro de ruido rosa, donde se utilizó la función welch y tenía como criterio que la pendiente debía ser dentro de -3dB con un error de 1dB. 
Asimismo, en el grafico hay una especie de meseta (valor que se mantiene constante) desde las primeras frecuencias hasta un poco más que 170 Hz, esto se puede deber a la longitud de la ventana de análisis que se utilizó para el cálculo de la densidad espectral de potencia y el algoritmo de generación de ruido. En muchos casos el algoritmo no tiene la resolución suficiente para distinguir lo que sucede en las frecuencias bajas, por consiguiente se promedian los valores. También al utilizar el filtro digital, como Voss Mc-Carteney, necesitan muchos coeficientes para mantener la precisión en las bajas frecuencias, por lo tanto se aplana la pendiente. 

ACA HAY QUE PONER SI CAMBIAMOS EL ERROR O LO DEJAMOS ASI!

CHEQUEAR A PARTIR DE ACA: 

Sine Sweep (barrido sinusoidal) es una oscilación sinusoidal en la cual la frecuencia de oscilación no se mantiene constante sino que aumenta continuamente.  En el caso del sine sweep logarítmico o exponencial aumenta continuamente pero divide el tiempo por octavas de bandas. Esto es por que buscamos igual energía por octava. ACA ES LO DE LA NORMA IEC 61260. 

Se le aplica un filtro inverso invirtiendo temporalmente el sweep y se compensa la distribución no uniforme de energía cuando le aplicamos una corrección de amplitud, esto es debido a que se concentra por más tiempo la energía en las frecuencias bajas. Se realiza la convolución del sweep con el filtro inverso y se produce un impulso ideal. 

o este texto: 
Sine Sweep (barrido sinusoidal) es una oscilación sinusoidal en la cual la frecuencia de oscilación no se mantiene constante sino que aumenta continuamente. En el caso del sine sweep logarítmico o exponencial aumenta continuamente pero divide el tiempo por octavas de bandas. Debido a que se busca igual energía por octava. ACA ES LO DE LA NORMA IEC 61260. Se inviertio temporalmente el sweep con la aplicación de un filtro inverso para compensar la distribución no uniforme de energía. Esto se realizó aplicando una corrección de amplitud que compensa la distribución no uniforme de energía por frecuencia del sweep logarítmico.

<img width="1000" height="400" alt="image" src="https://github.com/user-attachments/assets/80e32655-4949-4fbe-a564-89206474f889" />


Se observa en el gráfico en el eje vertical las frecuencias y en el eje horizontal el tiempo. La intensidad del amarillo representa la amplitud de energía de la señal. Se observa que se concentra mayor energía en la línea amarilla brillante que tiene como trayectoria curva exponencial ascendente. Asimismo, en el extremo inferior izquierdo del gráfico, la mancha amarilla es muy ancha y se va difuminando de forma vertical debido a la baja resolución en frecuencias bajas por la longitud de la ventana. 

REDACTAR MÁS LINDO LA PARTE DE PROBLEMATICA: 

Cuando se realizó el gráfico de sine sweep surgió como problemática que la resolución del gráfico era demasiado grande, se buscó información en matplotlib y se cambió en el código  plt.yscale(“symlog”),  “log ” por “symlog”. Debido a que este último es de utilidad para rangos muy grandes. 

<img width="1000" height="400" alt="image" src="https://github.com/user-attachments/assets/4a08f7c0-86d1-4da5-826a-3d2394441e42" />


Se puede observar que se obtuvo como resultado de la convolución del sine sweep y su filtro inverso un impulso con lóbulos laterales pequeños que se atenúan de forma drástica y simétrica a los milisegundos, también que dicho impulso obtiene su valor normalizado de amplitud máxima (1) en el tiempo 0s  <img width="992" height="466" alt="image" src="https://github.com/user-attachments/assets/555d67ef-895f-44a8-81ae-caf5a92eaedb" />

Asimismo se validó el test de convolución-impulso, el cual tiene como criterio que la relación pico - piso sea mayor o igual a 40 dB, siendo que se obtuvo un valor de 109.5 dB. 


Grabación y reproducción 
<img width="352" height="326" alt="image" src="https://github.com/user-attachments/assets/ad0f33ec-7663-46e5-a5dd-5f2b34e5263f" />

Para comprobar que las funciones “generar_ruido_rosa” y “reproducir_y_grabar” funcionen correctamente se realizo una prueba de la siguiente manera: 

 ```python
from app.services.pink_noise import generar_ruido_rosa
from app.services.reproducir_grabar import reproducir_y_grabar

prueba = generar_ruido_rosa(3,44100)
reproducir_y_grabar(prueba, 44100, 4)
   ```
de forma tal que se genera un ruido rosa por 3 segundos a una frecuencia de muestreo de 44100 Hz y se grabe por 4 segundos. Luego se coloco el archivo en audacity y se graficó.
Estas pruebas se realizaron diez veces a diferentes intensidades sonoras utilizando para su reproducción y grabación un Noga vintage mic-2030 px cardioide. Se puede observar en el grafico de la figura: X el ruido rosa a una intendidad de COMPLETAR INTENSIDAD, cumple con una caida logaritmica (DESARROLLAR UN POCO MAS) 
En caso de querer repetir este experimento se puede copiar el codigo en un nuevo archivo, ejecutar y arrastrar la grabación realizada (dentro de la carpeta grabaciones) a audacity (para graficar se deberá tocar “Analizar/Trazar espectro”).


# Informe de la Medición 2:

Asumimos que el recinto se comporta como un sistema Lineal e Invariante en el Tiempo (LTI). Bajo esta hipótesis, la sala queda completamente caracterizada por una única función: su Respuesta al Impulso (h(t)). 
Cualquier sonido que se reproduzca en la sala (x(t)) saldrá modificado como una grabación (y(t)) que es el resultado de la convolución matemática: 

y(t)=h(t)* x(t)


