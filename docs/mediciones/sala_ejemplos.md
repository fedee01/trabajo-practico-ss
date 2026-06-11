# Informe de la Medición 1:
Generamos Ruido Rosa debido a que este suele escogerse por encima del Ruido blanco por la similitud de percepción que tiene al oído humano, precisamente  a que reduce la energía en altas frecuencias. Como característica este tiene una “densidad espectral inversamente proporcional a la frecuencia. En la escala logarítmica esto equivale a una caída de -3 dB por octava” (citar info M). 

Para poder llevar a cabo la elaboración del ruido rosa tomamos como decisión de diseño el algoritmo Voss-McCartney, el cual consiste en “una suma de múltiples generadores de ruido blanco que se actualiza a tasas 2^i. El generador se actualiza cuando el bit del índice cambia. La suma produce una señal cuyo espectro se aproxima a la inversa de la frecuencia (1/f)”. 

En el momento de llevar esto a cabo surgió como dificultad la comprensión de la tasa de refresco de los generadores de ruido blanco. Al consultar con los docentes se aclaró sobre el orden, que los generadores de índice bajo se actualizan más seguido a diferencia que los del final. Luego fue necesario la ayuda para ciertos acabados del autocompletado inteligente del Visual Studio Code. Asimismo se utilizó como prompt en el copilot: “Generar una función de ruido rosa a través del algoritmo Voss McCartney de forma tal que devuelva un array normalizado entre -1 y 1, que el generador de ruido blanco sea de 16 bits, que para cada n muestras determina cuándo debe actualizarse y que sume las salidas de los generadores”. 

GRÁFICO RUIDO ROSA:  (PSD vs FRECUENCIA)

{INSERTAR GRAFICO} 

La PSD (Densidad Espectral de Potencia) se expresa en dB/Hz para describir cómo se distribuye la potencia o energía de una señal en un espectro de frecuencias, es decir, a lo largo de las distintas frecuencias que la componen. 

Podemmos ver que hay una caida de -3dB por banda de banda de octava.

CHEQUEAR A PARTIR DE ACA: 

Sine Sweep (barrido sinusoidal) es una oscilación sinusoidal en la cual la frecuencia de oscilación no se mantiene constante sino que aumenta continuamente.  En el caso del sine sweep logarítmico o exponencial aumenta continuamente pero divide el tiempo por octavas de bandas. Esto es por que buscamos igual energía por octava. ACA ES LO DE LA NORMA IEC 61260. 

Se le aplica un filtro inverso invirtiendo temporalmente el sweep y se compensa la distribución no uniforme de energía cuando le aplicamos una corrección de amplitud, esto es debido a que se concentra por más tiempo la energía en las frecuencias bajas. Se realiza la convolución del sweep con el filtro inverso y se produce un impulso ideal. 

