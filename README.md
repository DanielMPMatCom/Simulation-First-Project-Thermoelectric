# Primer Proyecto de Simulación. Termoeléctricas.

# Problema

Se tiene un conjunto de termoeléctricas y circuitos a los que deben alimentar. Se sabe que el tiempo entre roturas distribuye Weibull y el tiempo que toma una reparación distribuye Log-Normal. Se desea analizar que conjunto de reparaciones realizar para afectar la menor cantidad de circuitos posible. Además se sabe que existe una posibilidad de que un circuito salga de circulación con una cierta probabilidad y se tiene que el consumo eléctrico de un circuito tiene una determinada distribución.

Como no se tienen datos suficientes, se estarán comparando los enfoques macroscópicos y mesoscópicos, en el primero se modelarán los eventos enfocados a cada termoeléctrica en particular y en el mesoscópico se modelaran los distintos componentes de la termoeléctrica. Vamos a realizar una comparación entre las dos formas de abordar el problema.

El planificador puede tomar 3 decisiones distintas

1. Decidir el apagón
2. Decidir mantenimientos
3. Decidir que cantidad de electricidad debe mantener de reserva
