# Primer Proyecto de Simulación. Termoeléctricas.

# Problema

Se tiene un conjunto de termoeléctricas y circuitos a los que deben alimentar. Se sabe que el tiempo entre roturas distribuye Weibull y el tiempo que toma una reparación distribuye Log-Normal. Se desea analizar que conjunto de reparaciones realizar para afectar la menor cantidad de circuitos posible. Además se sabe que existe una posibilidad de que un circuito salga de circulación con una cierta probabilidad y se tiene que el consumo eléctrico de un circuito tiene una determinada distribución.

Como no se tienen datos suficientes, se estarán comparando los enfoques macroscópicos y mesoscópicos, en el primero se modelarán los eventos enfocados a cada termoeléctrica en particular y en el mesoscópico se modelaran los distintos componentes de la termoeléctrica. Vamos a realizar una comparación entre las dos formas de abordar el problema.

El planificador puede tomar 3 decisiones distintas

1. Decidir el apagón
2. Decidir mantenimientos
3. Decidir que cantidad de electricidad debe mantener de reserva

## Distribución Weibull

$X ∼ Weibull(α, λ)$ con $α, λ > 0$

### Función de densidad:

$f(x)=\lambda \alpha (\lambda x)^{\alpha -1}e^{-(\lambda x)^{\alpha }}\qquad x>0$

Donde α es el parámetro de forma y λ es el parámetro de escala de la distribución.

La distribución modela la distribución de fallos (en sistemas) cuando la tasa de fallos es proporcional a una potencia del tiempo:

- Un valor α < 1 indica que la tasa de fallos decrece con el tiempo.
- Cuando α = 1, la tasa de fallos es constante en el tiempo.
- Un valor α > 1 indica que la tasa de fallos crece con el tiempo.

El parámetro λ es un factor de escala que estira o comprime la distribución. Proporciona una estimación de la "vida característica" del producto, que es el tiempo en el que el 63,2% de los equipos habrá fallado.

El análisis de Weibull ayuda a prever el comportamiento futuro de falla de un componente o sistema. Esta capacidad predictiva asiste en la planificación de las actividades de mantenimiento, reduciendo los tiempos de inactividad no planificados y aumentando la eficiencia general del sistema.

### Función de Distribución:

$F(x)=1-e^{-(\lambda x)^{\alpha }}$

para $x > 0$.

#### Media:

$E [X] = \frac {1}{\lambda }\Gamma \left(1+{\frac {1}{\alpha }}\right)$

#### Varianza:

$Var (X)={\frac {1}{\lambda ^{2}}}\left[\Gamma \left(1+{\frac {2}{\alpha }}\right)-\Gamma ^{2}\left(1+{\frac {1}{\alpha }}\right)\right]$


${\displaystyle \Gamma (z)=\int _{0}^{\infty }t^{z-1}e^{-t}\,dt}$
