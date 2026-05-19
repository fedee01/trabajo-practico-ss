# Explicacion de EDT
""" 
Early Decay Time (Tiempo de Decaimiento Temprano) determinará cómo será el T60 (Tiempo de reverberacion) del recinto considerando el comportamiento del decaimiento de los primeros 10 dB. Debemos considerar que el tiempo obtenido en el decaimiento de 10 dB lo debemos multiplicar por 6 para obtener la suposición anteriormente nombrada. Se toma la medición entre 0 dB y -10 dB y luego se extrapola el resultado. En algunas fuentes se lo suele nombrar como T10. """

# Explicacion de T20

"""
T20 sigue la misma lógica que el T10,  se toma en cuenta el tiempo que le lleva la señal en caer 20 DB. Debemos tener en cuenta que prácticamente se empieza a contar luego del decaimiento de 5 DB, es decir, que el T20 se toma la medición desde -5 db a -25db. En este caso se debe multiplicar el valor obtenido por 3 para conseguir el T60. Chequear si nosotros prácticamente tenemos esa consideración o no!. """
 
# Explicacion de T30
"""
T30 tiene el mismo razonamiento que los anteriores pero en este caso es el tiempo que tarda la señal en caer 30 DB, midiendo desde la caída de menos 5 DB y el resultado se multiplica por 2 para extrapolarlo y que se asemeja a T60. """

"""
Chequear siguiente info: 
Si la diferencia de nivel es superior a 45 DB, el parámetro T60 puede calcularse utilizando el T10, T20 y T30. """




