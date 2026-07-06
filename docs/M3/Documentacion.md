# Informe de la Medición 3:

### Función suavizar señal: 

En este caso se suavizo la señal para que no tenga grandes fluctuaciones de ruido, se eligió como opción la Envolvente de Hilbert debido a que se aconseja ya que no requiere elegir un tamaño de ventana y preserva mejor la estructura temporal del decaimiento. Se obtendrá una curva suave que sigue la forma del decaimiento sin tener el detalle de las oscilaciones rápidas.

### Función integral de Schroeder:

La integral de Schroeder acumula la energía desde el final hacia el principio, debido a que esta se obtiene mediante la integración inversa y representa la curva de decaimiento de la energía acústica en un recinto. A diferencia de la función anterior está es monotonamente decreciente por lo tanto se le puede aplicar una línea recta. 

<img width="880" height="470" alt="image" src="https://github.com/user-attachments/assets/68ef57a6-f085-4e25-94f2-c372ebb98d43" />

Podemos ver en el grafico anterior de color verde la integral de Schroeder y las extapolaciones de T20, T30 y EDT para la obtencion del T60. 

### Función regresión lineal: 

Con la utilización de mínimos cuadrados, encontramos la mejor recta que se ajustan a los puntos que usamos para extrapolar y lo vemos en el gráfico anterior en las líneas punteadas de los T30 y T20, ya que estas rectas son aproximaciones lineales distintas para cada una. 


### Función calcular parámetros acústicos: 

Debemos considerar que T10, T20 y T30 comienzan a contar el decaimiento luego de 5dB. Por lo tanto EDT no se asemejara tanto al resto debido a que tiene en cuenta las reflexiones tempranas.

El paso a paso que realizamos para obtener los parámetros acústicos fue: 

[x] Filtra por bandas de octavas.
[x] Suavizado por Hilbert
[x] Integración de Schroeder.
[x] Ajusta regresiones sobre cada tramo (EDT: 0 a -10 dB, T20: -5 a -25 dB,T30: -5 a -35 dB). 
[x] Extrapola los datos. 

### VALIDACIÓN: 

Para comprobar la efectividad de nuestra RIR-API comparamos RI conocidas (extraidas de OPEN AIR). Elegimos la API de la Cátedra (https://rir-api-frontend.onrender.com/) proporcionada por el profesor, el programa REW (https://rir-api-frontend.onrender.com) como software profesional y la información proporcionada en las mismas RI por OPEN AIR (https://www.openair.hosted.york.ac.uk/).

Las RI seleccionas pueden encontrarse en trabajo-practico-ss/docs/M3/RI, las cuales son: 1a_marble_hall.wav y 3a_hats_cloacks_the_lord.wav (extraidas de https://www.openair.hosted.york.ac.uk/?page_id=602), mh3_000_wx_48k.wav (extraida de https://www.openair.hosted.york.ac.uk/?page_id=459) y las RI sintetizadas con nuestra RIR-API (RI_Sintetizada.wav y RI_Sintetizada2.wav).

Para comprobar la efectividad de nuestro método decidimos ponernos un margen de ± 0.5 s respecto al software profesional y/o a la API de la cátedra.

Las comparaciones pueden observarse en las siguientes cinco figuras donde se pueden ver seis bandas normalizadas [125 Hz, 250 Hz, 500 Hz, 1000 Hz, 2000 Hz y 4000 Hz] en el eje X y el tiempo en segundos en el eje Y. Para cada una de las comparaciones hay un gráfico donde se ve el EDT, T20 y T30.

En la siguiente figura se puede ver el audio RI_Sintetizada.wav:

<sub>Figura 2. Comparacion EDT, T20 y T30 para la primer RI sintetizada. </sub>

En la figura 2 puede verse en azul nuestra RIR-API, en verde la de la cátedra, en bordó el REW y en celeste el T60 que tabulamos para generar el archivo. Como se puede notar nuestros valores dieron muy próximos a los del REW siendo superada por la API de la cátedra solamente en los 250 Hz del T20.

En la siguiente figura se puede ver el audio RI_Sintetizada2.wav:

<sub> Figura 3. Comparacion EDT, T20 y T30 para la segunda RI sintetizada. </sub>

En la figura 2 puede verse nuestra RIR-API, en verde la API de la cátedra, rel bordó el REW y en celeste el T60 que tabulamos para generar el archivo. En este caso se pude ver como nuestra RIR-API suele tener valores muy próximos al REW salvo en el EDT de 500 y 1000 Hz, en el T20 de 500 Hz y en el T30 de 500 Hz, sin embargo las diferencias son menores a 0.5 segundos por lo que consideramos que son buenas aproximaciones. Además salvo en el EDT de 500 y 1000 Hz las diferencias entre nuestra API y la de la cátedra son mínimas.

En la siguiente figura se puede ver el audio 1a_marble_hall.wav:

<sub>Figura 4. Comparacion EDT, T20 y T30 para la primer sala de Elveden Hall. </sub>

En azul puede verse nuestra RIR-API, rel bordó el REW y en amarillo los datos suministrados por OPEN AIR que tabulamos para generar el archivo. En este caso el archivo no era soportado por la API de la cátedra. Los valores obtenidos estan dentro de los esperados salvo en el T30 de 125 Hz donde OPEN AIR proporciona un valor con mas de 5 segundos de diferencia, sin embargo el valor calculado por el REW es similar al nuestro por lo que consideremos que esa diferencia se debe a que no tuvimos en cuenta las primeras dos bandas de octava y que estas presentan valores muy altos (T30 de 40,51 segundos para 31,25 Hz y de 22,68 segundos para 62.5 Hz).

En la siguiente figura se puede ver el audio 3a_hats_cloaks_the_lord.wav:

<sub> Figura 5. Comparacion EDT, T20 y T30 para la segunda sala de Elveden Hall.</sub>

En azul puede verse nuestra RIR-API, en verde la API de la cátedra, rel bordó el REW. En este caso no tenemos datos suministrados por OPEN AIR. Los valores que obtuvimos son consistentes con los del REW a excepción del T20 para 2000 Hz, sin embargo la diferencia entre estos es menor a 0,5 segundos por lo que consideramos que la diferencia es aceptable.

En la siguiente figura se puede ver el audio mh3_000_wx_48k.wav:

<sub>Figura 6. Comparacion EDT, T20 y T30 para Maes Howe. </sub>

En azul puede verse nuestra RIR-API, en verde la API de la cátedra, rel bordó el REW y en amarillo los datos suministrados por OPEN AIR que tabulamos para generar el archivo. Los tiempos de reverberación de esta sala son bajos por lo que en los casos más extremos puede verse como la diferencia entre nuestros valores y los obtenidos mediante REW no difieren más de 0,5 para ningún valor. No obstante nuestros valores generalmente se encontraron más cerca de la referencia de OPEIN AIR que los otros (salvo por el T20 en 2000 y 4000 Hz y el T30 en 125, 1000 y 2000 Hz donde alguno de los otros programas dio resultados mas cercanos a los proporcionados por la fuente.




Para facilitar la obtencion de los datos obtenidos por nuestra RIR-API se utlizo: 

 ```python
from app.services.signal_utils import cargar_audio, sintetizar_ri
from app.services.acoustic_parameters import calcular_parametros_acusticos
from app.services.acoustic_parameters import 
from app.services.reproducir_grabar import reproducir_y_grabar

bandas = [125, 250, 500, 1000, 2000, 4000]
T60 = {
    125: 2,
    250: 2.4,
    500: 0.8,
    1000: 0.11,
    2000: 1.15,
    4000: 2,
}

# Para crear una RI ustar este codigo
# ri = sintetizar_ri(T60, 44100, 3)
# Para reproducir y grabar un archivo utilizar este codigo
# reproducir_y_grabar(ri_sintetizada, 44100, 3.5)

# Para cargar un audio utilizar este codigo
# ri = cargar_audio(r"docs\RI\grabacion_1.wav")

# NOTA deberá usarse sintetizar_ri y reproducir_y_grabar para crear uno nuevo
# en caso de querer usar un audio existente solo coloque cargar_audio

pa = calcular_parametros_acusticos(ri[0], 44100, bandas, 8)

print(
    f" {'':<4}|{'':<5}{'125 Hz':<9} |     {'250 Hz':<9} |     {'500 Hz':<9} |"
    f"{'':<4}{'1000 Hz':<9} |     {'2000 Hz':<9} |     {'4000 Hz':<9}|"
)
print("-" * 102)
print(
    f" {'EDT'}{'':<1}|{'':<5}{round(pa['EDT'][125], 3)}{'':<5}|"
    f"{'':<5}{round(pa['EDT'][250], 3)}{'':<5}|"
    f"{'':<5}{round(pa['EDT'][500], 3)}{'':<5}|"
    f"{'':<5}{round(pa['EDT'][1000], 3)}{'':<5}|{'':<5}{round(pa['T20'][2000], 3)}{'':<5}|"
    f"{'':<5}{round(pa['EDT'][4000], 3)}{'':<5}|"
)

print(
    f" {'T20'}{'':<1}|{'':<5}{round(pa['T20'][125], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T20'][250], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T20'][500], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T20'][1000], 3)}{'':<5}|{'':<5}{round(pa['T20'][2000], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T20'][4000], 3)}{'':<5}|"
)
print(
    f" {'T30'}{'':<1}|{'':<5}{round(pa['T30'][125], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T30'][250], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T30'][500], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T30'][1000], 3)}{'':<5}|{'':<5}{round(pa['T30'][2000], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T30'][4000], 3)}{'':<5}|"
)
print(
    f" {'T10'}{'':<1}|{'':<5}{round(pa['T10'][125], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T10'][250], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T10'][500], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T10'][1000], 3)}{'':<5}|{'':<5}{round(pa['T20'][2000], 3)}{'':<5}|"
    f"{'':<5}{round(pa['T10'][4000], 3)}{'':<5}|"
)
print("-" * 102)


 ```
Para realizar lo ploteos de los graficos de banda comparativos se utilizo lo siguiente: 

 ```python

import matplotlib.pyplot as plt
import numpy as np

bandas = ["125 Hz", "250 Hz", "500 Hz", "1 kHz", "2 kHz", "4 kHz"]

# NOTA los valores colocados son de referencia

# Valores Gráfico 1 (EDT)
nuestro0 = [1.81, 2.329, 0.827, 0.286, 1.133, 1.974]
catedra0 = [1.857, 2.352, 1.411, 0.837, 1.2, 2.01]
rew0 = [1.824, 2.352, 1.039, 0.660, 1.252, 1.951]
referencia0 = [2, 2.4, 0.8, 0.11, 1.15, 2]

# Valores Gráfico 2 (T20)
nuestro1 = [1.845, 2.368, 1.006, 0.901, 1.133, 2.029]
catedra1 = [1.82, 2.325, 1.081, 0.775, 1.151, 2.027]
rew1 = [1.871, 2.359, 1.428, 0.889, 1.22, 2.023]
referencia1 = [2, 2.4, 0.8, 0.11, 1.15, 2]

# Valores Gráfico 3 (T30)
nuestro2 = [1.914, 2.421, 1.547, 0.978, 1.194, 2.012]
catedra2 = [1.865, 2.36, 1.501, 0.868, 1.204, 2.012]
rew2 = [1.939, 2.418, 2.011, 1.021, 1.344, 2.009]
referencia2 = [2, 2.4, 0.8, 0.11, 1.15, 2]

bar_width = 0.25
x = np.arange(len(bandas))
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Subgráficos de Barras
axes[0].bar(x - 0.75 * bar_width, nuestro0, bar_width / 2, label="RIR-API", color="steelblue")
axes[0].bar(x - bar_width * 0.25, catedra0, bar_width / 2, label="API CÁTEDRA", color="lightgreen")
axes[0].bar(x + bar_width * 0.25, rew0, bar_width / 2, label="REW", color="darkred")
axes[0].bar(x + bar_width * 0.75, referencia0, bar_width / 2, label="OPEN AIR", color="lightblue")

axes[1].bar(x - 0.75 * bar_width, nuestro1, bar_width / 2, label="RIR-API", color="steelblue")
axes[1].bar(x - bar_width * 0.25, catedra1, bar_width / 2, label="API CÁTEDRA", color="lightgreen")
axes[1].bar(x + bar_width * 0.25, rew1, bar_width / 2, label="REW", color="darkred")
axes[1].bar(x + bar_width * 0.75, referencia1, bar_width / 2, label="OPEN AIR", color="lightblue")

axes[2].bar(x - 0.75 * bar_width, nuestro2, bar_width / 2, label="RIR-API", color="steelblue")
axes[2].bar(x - bar_width * 0.25, catedra2, bar_width / 2, label="API CÁTEDRA", color="lightgreen")
axes[2].bar(x + bar_width * 0.25, rew2, bar_width / 2, label="REW", color="darkred")
axes[2].bar(
    x + bar_width * 0.75, referencia2, bar_width / 2, label="Referencia T60", color="lightblue"
)

# Informacion por Gráfico
axes[0].set_title("EDT")
axes[0].set_xlabel("Bandas")
axes[0].set_ylabel("Segundos")
axes[1].set_title("T20")
axes[1].set_ylabel("Segundos")
axes[1].set_xlabel("Bandas")
axes[2].set_title("T30")
axes[2].set_ylabel("Segundos")
axes[2].set_xlabel("Bandas")

# Sin esto 1 y 2 no tienen datos
for n, ax in enumerate(axes):
    ax.plot(x, x / 3, color="w", alpha=0)
    if n <= 2:
        ax.set_xticks(x, bandas)
        ax.grid(alpha=0.2)
    else:
        ax.set_title("Automatic ticks")

plt.tight_layout()
plt.legend()
plt.show()

 ```


Obtuvimos como comparación con una RI sintetizada y con una RI en el recinto Maes Howe, obtenida de la pagina (https://www.openairlib.net/) los siguientes resultados:

PONER RESULTADOS. 
Análisis breve

### ENDPOINTS: 
En este sección también realizamos los endpoint, como un criterio de diseño para el endpoint que filtra por bandas de octavas, los http solo devuelve un archivo, por lo tanto elegimos que devuelva una carpeta zip para que el cliente pueda descargar todos los audios para cada banda de octava y no tenga que elegir descargar uno por uno.

