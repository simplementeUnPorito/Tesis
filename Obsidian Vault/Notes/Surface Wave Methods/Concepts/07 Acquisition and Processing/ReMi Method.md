# ReMi Method (Refraction Microtremor)

> **Contexto:** Método pasivo de adquisición de ondas superficiales usando ruido ambiental y un arreglo lineal.
> **Fuente:** Foti et al. Cap. 3 (p. 179–181), Cap. 4, Cap. 8.

## Principio

El **método ReMi** (*Refraction Microtremor*, Louie 2001) extrae la velocidad de fase de ondas superficiales a partir del **ruido sísmico ambiental** (*microtremors*), registrado con un arreglo lineal de geófonos estándar de adquisición.

La idea central: el campo de ruido ambiental contiene ondas superficiales que se propagan en todas las direcciones. En el espectro f-k de un arreglo lineal, estas ondas producen energía que puede usarse para estimar la [[Dispersion Relation|curva de dispersión]], bajo la hipótesis de que el campo de ruido es **aproximadamente isotrópico** (fuentes distribuidas uniformemente alrededor del arreglo) o que al menos contiene ondas propagándose en la dirección del arreglo.

## Procesamiento

1. Registrar ruido ambiental con un arreglo lineal de geófonos (típicamente 24–48 canales).
2. Calcular el espectro f-k de los registros de ruido (típicamente mediante la transformada p-τ o f-k directa).
3. Identificar el **borde mínimo de velocidad** en el espectro f-k: los puntos de mínimo número de onda para cada frecuencia corresponden a la velocidad de fase de Rayleigh.
4. Trazar la curva de dispersión a lo largo de ese borde.
5. Invertir la curva para obtener el perfil Vs(z).

## Hipótesis y limitaciones

- **Hipótesis de isotropía del ruido:** si las fuentes de ruido dominan en una sola dirección, el espectro f-k mostrará la velocidad aparente (proyectada sobre el arreglo) que puede ser mayor que la velocidad real. Esto produce **sobreestimación de la velocidad de fase**.
- **Arreglo lineal:** no permite estimar el vector número de onda completo. Solo aprovecha componentes de ruido alineadas con el arreglo.
- **Sin separación modal clara:** el espectro f-k de ruido no tiene la misma definición que el espectro de un experimento activo.

## Ventaja vs. métodos activos y vs. interferometría

| Característica | ReMi | Activo (MASW) | Interferometría pasiva |
|---|---|---|---|
| Fuente | Ruido ambiental | Fuente controlada | Ruido ambiental |
| Geometría | Lineal | Lineal | 2D/lineal |
| Validación hipótesis | Difícil | No aplica | Por correlogram gather |
| Velocidad aparente | Sí (posible sobrestimación) | No (fuente en extremo) | No (cancelación de contribuciones) |
| Frecuencias bajas | Buenas (ruido natural) | Limitadas por fuente | Buenas |

La **interferometría sísmica pasiva** (Cap. 8) supera la limitación de la velocidad aparente: el proceso de cross-correlación cancela las contribuciones de fuentes opuestas y el espectro f-k del interferograma tiene máximos en el número de onda verdadero. El ReMi es más simple pero menos riguroso cuando el campo de ruido no es isotrópico.

## Aplicaciones

- Zonas urbanas donde fuentes activas son impracticables.
- Cuando se requieren profundidades de investigación > 30 m y no hay energía suficiente con sledgehammer.
- Ensayos sísmicos de sitio (Vs30) combinados con refracción de primeros arrivals.

## Referencias

- Louie (2001), *Seismological Research Letters*.
- Foti et al. (2014), Cap. 3 Sec. 3.4.3.3, Cap. 4, Cap. 8 Sec. 8.4.
