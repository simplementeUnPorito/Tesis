# Interferometría Sísmica Pasiva (Seismic Interferometry)

> [!CONCEPT] Definición
> La **interferometría sísmica** recupera la **función de Green** entre dos receptores — equivalente a la respuesta de impulso que se observaría si uno de los receptores fuera una fuente virtual — mediante la **cross-correlación** de sus registros de ruido ambiental. La base teórica (Weaver & Lobkis 2001; Wapenaar 2004; Snieder 2004) establece que en un campo difuso isótropo, la cross-correlación entre señales en $R_1$ y $R_2$ converge a la función de Green $G(R_1, R_2)$. El resultado puede procesarse exactamente como datos activos con el receptor fuente virtual en $R_1$. Su principal ventaja sobre el [[ReMi Method|método ReMi]] es que al sumar contribuciones de fuentes en posiciones opuestas se cancelan las velocidades aparentes — el espectro f-k del interferograma presenta máximos en el **[[Wavenumber|número de onda]] verdadero**, no en el aparente. Además, el *correlogram gather* permite validar la hipótesis de campo difuso: fuentes localizadas producen eventos no lineales detectables.
>
> — Foti et al. (2018), Cap. 8.4, pp. 427–430; Wapenaar et al. (2010); Shapiro & Campillo (2004).

## Principio

La **interferometría sísmica** designa el proceso de generar trazas sísmicas desde fuentes virtuales mediante la **cross-correlación** (o convolución) de observaciones en diferentes receptores. Estudios teóricos demostraron que el campo difuso de ruido ambiental puede transformarse en una respuesta de impulso sísmica determinista —la **función de Green** entre receptores— mediante este procedimiento (Weaver y Lobkis 2001, 2002; Snieder 2004; Wapenaar 2004).

En sismología global, la componente de onda superficial de la función de Green entre dos receptores puede recuperarse de la cross-correlación de sus registros de ruido (Campillo y Paul 2003; Shapiro y Campillo 2004). El mismo principio fue posteriormente validado en el rango de frecuencias de ingeniería sísmica (1–100 Hz).

## Procedimiento

1. **Cross-correlación por fuente**: considérense dos receptores $R_1$ y $R_2$ que observan señales de [[Surface Waves|ondas superficiales]] provenientes de fuentes $S_j$ distribuidas alrededor del array. Para cada fuente se cross-correlacionan las señales $T(S_j, R_1)$ y $T(S_j, R_2)$, produciendo una traza correlacionada $T_{12}(S_j)$. La correlación depende de la posición relativa de la fuente y de las propiedades del subsuelo entre los receptores (Fig. 8.28, p. 427).

2. **Correlogram gather**: las trazas correlacionadas para todas las fuentes se ordenan según el **azimut de la fuente**, formando un gather análogo al shot gather en sísmica activa (Fig. 8.29, p. 428). Este gather es regular y suave a pesar de las diferentes distancias de las fuentes, porque la cross-correlación cancela los efectos de trayectoria desde la fuente hasta los receptores.

3. **Suma sobre fuentes**: al sumar las trazas correlacionadas, las contribuciones de fuentes en posiciones opuestas entre sí se anulan. Solo las fuentes en los **puntos estacionarios** —casi alineadas con los dos receptores— contribuyen constructivamente. El resultado es una traza causal/anticausal equivalente a la respuesta de impulso entre $R_1$ y $R_2$: se puede interpretar como si $R_1$ fuera una **fuente virtual** registrada en $R_2$.

## Aplicación en [[Surface Waves|ondas superficiales]]

Las señales extraídas pueden procesarse exactamente como datos activos virtuales. La aplicación principal es la **recuperación de la [[Phase Velocity|velocidad de fase]] de [[Surface Waves|ondas superficiales]]** a partir de ruido ambiental (Shapiro y Campillo 2004). La mayoría de los estudios actuales usa arrays 2D dispersos para obtener una **distribución tomográfica** de las velocidades de [[Surface Waves|ondas superficiales]].

En arrays lineales, el interferograma permite usar un receptor de referencia como fuente virtual, generando un shot gather que se procesa con análisis [[MASW Method|f-k]] estándar.

## Interferograma vs. [[ReMi Method|ReMi]]

El método [[ReMi Method|ReMi]] (*Refraction Microtremor*) procesa directamente los registros de ruido en el dominio f-k, asumiendo que el mínimo de la curva de slowness corresponde a la dispersión real. La interferometría sísmica ofrece ventajas prácticas respecto a [[ReMi Method|ReMi]]:

- En un campo de ondas **no isotrópico**, [[ReMi Method|ReMi]] puede llevar a velocidades **sobreestimadas** porque el análisis utiliza la velocidad aparente. El interferograma, al cancelar las contribuciones de direcciones opuestas, extrae el [[Wavenumber|número de onda]] verdadero (Fig. 8.31, p. 429).
- El espectro f-k del interferograma muestra los máximos **exactamente sobre el [[Wavenumber|número de onda]] teórico verdadero** (Fig. 8.30, p. 429), mientras que el espectro [[ReMi Method|ReMi]] del mismo dataset sintético muestra los máximos sobre el [[Wavenumber|número de onda]] aparente.
- La hipótesis de campo difuso isotrópico puede **validarse con el interferograma**: si existe una fuente dominante a distancia limitada, el interferograma muestra eventos no lineales que advierten sobre la invalidez de los resultados (Fig. 8.32, p. 430). [[ReMi Method|ReMi]] no ofrece este diagnóstico directo.

## Hipótesis fundamentales

- **Campo difuso**: el ruido ambiental debe ser estadísticamente isótropo (fuentes distribuidas en todas las direcciones con energía similar). Esta condición se degrada en entornos urbanos con fuentes direccionales dominantes.
- **[[Surface Waves|Ondas superficiales]] dominantes**: la mayor parte de la energía del ruido ambiental en frecuencias de ingeniería corresponde a [[Surface Waves|ondas superficiales]] (ondas de [[Rayleigh Waves|Rayleigh]] y [[Love Waves|Love]]).
- **Medio homogéneo lateral**: el subsuelo entre los receptores se aproxima como un modelo 1D; variaciones laterales fuertes violan la hipótesis.

## Relación con [[SPAC Method|SPAC]]/ESAC

La interferometría sísmica y la [[Dispersion Relation|autocorrelación espacial]] ([[SPAC Method|SPAC]]/ESAC, Aki 1957) comparten la misma base física: ambas explotan la coherencia espacial del campo de ruido para estimar la [[Phase Velocity|velocidad de fase]]. La interferometría trabaja en el dominio temporal (función de Green) mientras que [[SPAC Method|SPAC]]/ESAC trabaja en el dominio frecuencial (coherencia espacial). En la práctica, el método ESAC puede verse como una implementación en frecuencia del mismo principio interferométrico.

## Limitaciones

- Requiere registros largos (minutos a horas) para acumular suficiente estadística del campo difuso.
- La recuperación correcta de la función de Green requiere distribución casi uniforme de fuentes alrededor del array.
- La contaminación por fuentes transitorias fuertes (tráfico, maquinaria) degrada el resultado; se requiere selección de ventanas o robustización estadística.
- Los modos superiores de [[Surface Waves|ondas superficiales]] son más difíciles de aislar que con métodos activos.

> [!EXAMPLE] Evidencia empírica: Shapiro & Campillo (2004) — tomografía de ondas de Rayleigh por interferometría de ruido ambiental
> Shapiro & Campillo (2004) demuestran que la cross-correlación de registros de ruido sísmico ambiental entre pares de estaciones de la red USArray produce la componente de onda de Rayleigh de la función de Green con suficiente coherencia para medir velocidades de fase en el rango 5–150 s. Las [[Dispersion Curve|curvas de dispersión]] extraídas coinciden con las obtenidas por análisis de terremotos convencionales. El trabajo establece que el **ruido ambiental** (dominado por interacciones océano-atmósfera en ese rango de períodos) actúa como campo difuso suficientemente isótropo para que la hipótesis de la interferometría sea válida globalmente. En el rango de frecuencias de ingeniería (1–100 Hz), el mismo principio se aplica con ruido de tráfico y actividad urbana, aunque la isotropía es menor y requiere más cuidado en la selección de ventanas.
>
> — Shapiro & Campillo (2004), *GRL* 31, L07614; Foti et al. (2018), Cap. 8.4, pp. 427–430.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Cap. 8.4, pp. 427–430 — interferometría en ingeniería |
| Shapiro & Campillo (2004), *GRL* 31 | Demostración de tomografía Rayleigh por cross-correlación de ruido |
| Wapenaar et al. (2010), *Geophysics* | Marco teórico unificado de interferometría sísmica |
| Weaver & Lobkis (2001) | Base termodinámica — campo difuso → función de Green |
