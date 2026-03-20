---
name: Ground Roll
description: Ondas superficiales registradas en datos de reflexión sísmica — tratadas como ruido en reflexión pero explotables para caracterización de Vs superficial
type: reference
---

# Ground Roll — Ondas Superficiales en Datos de Reflexión Sísmica

> **Fuente:** Sebastiano Foti, Chapter 7, Sección 7.5 · pp. 384–392

## Intuición física

Cuando se genera una fuente sísmica en superficie para un levantamiento de reflexión, la energía se propaga en todas las direcciones. La mayor parte de la energía viaja como [[Rayleigh Waves|ondas de Rayleigh]] a lo largo de la superficie (ground-roll), mientras que las [[Body Waves|ondas de cuerpo]] (reflexiones) viajan hacia las capas profundas y regresan. En el registro sísmico, el ground-roll aparece como un tren de ondas de gran amplitud, baja frecuencia y velocidad lenta, que se propaga con pendiente característica en el sismograma (tiempo-offset).

Desde la perspectiva de reflexión, el ground-roll **contamina** las reflexiones útiles (P-waves). Desde la perspectiva de ondas superficiales, el ground-roll **contiene información** sobre la rigidez del suelo superficial.

## Características del ground-roll en registros de reflexión

- **Alta amplitud:** las fuentes de reflexión (explosivos, vibroseis) son muy potentes → SNR alto del ground-roll incluso a grandes distancias de la fuente.
- **Baja velocidad:** llega antes que las reflexiones en offsets cortos; en offsets largos se separa bien de las reflexiones.
- **Baja frecuencia dominante:** típicamente 5–30 Hz, con penetración de decenas a cientos de metros.
- **Coherencia espacial:** se propaga con número de onda bien definido en función de la frecuencia → apto para análisis f-k.
- **Alta dispersión:** en suelos blandos superficiales, la [[Dispersion Curve|curva de dispersión]] es fuertemente dispersiva y bien definida.

## Prácticas de supresión y sus efectos sobre las ondas superficiales

En la adquisición de reflexión, se aplican varias técnicas para atenuar el ground-roll:
- **Arreglos de geófonos:** promedian señales de múltiples receptores en una posición, cancelando las longitudes de onda cortas del ground-roll pero preservando las reflexiones.
- **Geófonos de alta frecuencia:** reducen la sensibilidad en las bajas frecuencias donde domina el ground-roll.
- **Fuentes de alta frecuencia** (vibroseis con sweep mínimo alto): reducen la energía inyectada en la banda del ground-roll.
- **Filtros f-k en procesamiento:** aplican máscaras en el dominio f-k para eliminar el cono de velocidades del ground-roll.

Estas prácticas, desde la perspectiva del análisis de ondas superficiales, **limitan el ancho de banda** disponible e introducen distorsiones de fase. Sin embargo, si la geometría de adquisición no fue demasiado agresiva, el ground-roll puede recuperarse con calidad suficiente para análisis.

## Ventajas sobre levantamientos dedicados de ondas superficiales

| Característica | Levantamiento dedicado MASW | Ground-roll de reflexión |
|---|---|---|
| Fuente | Sledgehammer / caída de peso | Explosivo / vibroseis (mucho más potente) |
| SNR a largo offset | Moderado | Alto |
| Rango de offset | Limitado por tamaño del arreglo | Potencialmente kilométrico |
| Cobertura espacial | Puntual o transecto | 2D o 3D completo |
| Redundancia estadística | Baja–media | Extremadamente alta (high-fold) |
| Costo adicional | Levantamiento independiente | Reutilización de datos existentes |

## Flujo de trabajo para análisis de ground-roll

1. **Recuperación de los datos originales** (antes de filtrado agresivo si están disponibles).
2. **Selección de ventanas** de análisis: se usan ventanas deslizantes en tiempo-offset para extraer subconjuntos del sismograma (Figura 7.33 del libro, p. 386).
3. **Extracción de la curva de dispersión** por ventana: análisis f-k o τ-p, extracción del máximo espectral.
4. **Inversión de la curva de dispersión**: puede ser 1D local por ventana, o con restricciones laterales para generar modelos 2D/3D.
5. **Validación**: comparación con datos de downhole, MASW dedicado o ensayos geotécnicos independientes.

## Aplicaciones en 2D y 3D

- **2D:** generación de pseudosecciones de Vs a lo largo de líneas sísmicas (Socco et al. 2008, 2009). Resolución lateral = longitud de la ventana deslizante.
- **3D:** con configuraciones point-receiver, el ground-roll está no-aliaseado y densamente muestreado. Se construyen **volúmenes de dispersión** (velocidad de fase como función de posición geográfica y longitud de onda). Cortes a λ constante producen mapas 2D de velocidad que revelan estructuras geológicas superficiales (Strobbia et al. 2011).

## Limitaciones

- La **profundidad de investigación** está limitada por el contenido de baja frecuencia, que a su vez depende de los geófonos usados. En reflexión de ingeniería (geófonos de 100 Hz), la profundidad puede ser solo 20–50 m. En reflexión de exploración con geófonos de 10 Hz, puede alcanzar cientos de metros.
- La necesidad de separar el ground-roll de reflexiones y refracciones requiere que los datos tengan suficiente separación en el espacio f-k.
- La calibración del modelo de [[Attenuation|atenuación]] es difícil porque la fuente introduce distorsiones de amplitud.

## Referencias
- Socco, L.V. et al. (2008). Seismic characterization of an alpine valley. *Near Surf Geophys*, 6(8), 255–267.
- Socco, L.V. et al. (2009). Laterally constrained inversion of ground roll from seismic reflection records. *Geophysics*, 74, G35–G45.
- Strobbia, C. et al. (2010). Surface waves from continuous profiling. *First Break* 28, 85–91.
- Strobbia, C. et al. (2011). Integrated near-surface model building from surface wave data. *Near Surf Geophys*, 9, 503–514.
- Foti, S. et al. (2014). *Surface Wave Methods for Near-Surface Site Characterization*, CRC Press. Cap. 7, Sección 7.5.
