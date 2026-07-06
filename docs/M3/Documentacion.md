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
