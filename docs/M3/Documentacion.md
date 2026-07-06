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

[x] 
[x] 
[x] 
[x] 
[x] 
[x] 



### VALIDACIÓN: 

Para realizar los cuadros comparativos se utlizo: 

 ```python
print(f" {'':<4}|{'':<5}{'125 Hz':<9} |     {'250 Hz':<9} |     {'500 Hz':<9} |     {'1000 Hz':<9} |     {'2000 Hz':<9} |     {'4000 Hz':<9}|")
print("-" * 102)
print(f" {'EDT'}{'':<1}|{'':<5}{round(pa['EDT'][125], 3)}{'':<5}|{'':<5}{round(pa['EDT'][250], 3)}{'':<5}|{'':<5}{round(pa['EDT'][500],3)}{'':<5}|{'':<5}{round(pa['EDT'][1000], 3)}{'':<5}|{'':<5}{round(pa['EDT'][2000], 3)}{'':<5}|{'':<5}{round(pa['EDT'][4000], 3)}{'':<5}|")
print(f" {'T20'}{'':<1}|{'':<5}{round(pa['T20'][125], 3)}{'':<5}|{'':<5}{round(pa['T20'][250], 3)}{'':<5}|{'':<5}{round(pa['T20'][500],3)}{'':<5}|{'':<5}{round(pa['T20'][1000], 3)}{'':<5}|{'':<5}{round(pa['EDT'][2000], 3)}{'':<5}|{'':<5}{round(pa['T20'][4000], 3)}{'':<5}|")
print(f" {'T30'}{'':<1}|{'':<5}{round(pa['T30'][125], 3)}{'':<5}|{'':<5}{round(pa['T30'][250], 3)}{'':<5}|{'':<5}{round(pa['T30'][500],3)}{'':<5}|{'':<5}{round(pa['T30'][1000], 3)}{'':<5}|{'':<5}{round(pa['T30'][2000], 3)}{'':<5}|{'':<5}{round(pa['T30'][4000], 3)}{'':<5}|)
print("-" * 102)

 ```

Obtuvimos como comparación con una RI sintetizada y con una RI en el recinto Maes Howe, obtenida de la pagina (https://www.openairlib.net/) los siguientes resultados:

PONER RESULTADOS. 
Análisis breve

### ENDPOINTS: 
En este sección también realizamos los endpoint, como un criterio de diseño para el endpoint que filtra por bandas de octavas, los http solo devuelve un archivo, por lo tanto elegimos que devuelva una carpeta zip para que el cliente pueda descargar todos los audios para cada banda de octava y no tenga que elegir descargar uno por uno.

