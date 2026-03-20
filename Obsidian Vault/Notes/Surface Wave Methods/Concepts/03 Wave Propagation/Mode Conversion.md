---
name: Mode Conversion
description: Fenómeno por el que una onda incidente sobre una interfaz elástica genera ondas reflejadas y transmitidas de distinto tipo; clave para la formación de ondas superficiales en medios estratificados
type: reference
---

# Conversión de Modos (Mode Conversion)

> **Contexto:** Cuando una onda elástica (P o S) incide sobre una interfaz entre dos medios con propiedades elásticas diferentes, parte de su energía se refleja y parte se transmite — y en ambos casos pueden generarse ondas de tipo distinto al incidente. Este fenómeno es fundamental para entender la formación de [[Rayleigh Waves]] (acoplamiento P–SV) y la ausencia de [[Love Waves]] en semiespacios homogéneos.
> **Fuente:** Foti et al. (2014), Cap. 2.1.3, pp. 46–50.

## Intuición física

En la interfaz entre dos medios elásticos, las condiciones de continuidad de desplazamiento y esfuerzo deben satisfacerse para todas las componentes del campo. Dado que los esfuerzos de compresión (relacionados con P) y los de corte (relacionados con S) están acoplados en la condición de frontera, una onda P incidente debe generar tanto ondas P como ondas SV en reflexión y transmisión para que el sistema de ecuaciones de frontera tenga solución.

La excepción son las ondas SH: sus condiciones de frontera están desacopladas de las P–SV (solo involucran el esfuerzo de corte horizontal), por lo que una onda SH incidente solo genera ondas SH.

## Reglas de conversión

| Onda incidente | Reflexiones generadas | Transmisiones generadas |
|---|---|---|
| P | P + SV | P + SV |
| SV | P + SV | P + SV |
| SH | SH | SH |

La dirección y amplitud de cada onda generada se determinan por las **ecuaciones de Zoeppritz**, que aplican las condiciones de continuidad de cuatro cantidades en la interfaz: desplazamientos normales y tangenciales, y esfuerzos normales y de corte.

## Relación con las ondas superficiales

### Formación de ondas de Rayleigh

Las [[Rayleigh Waves]] surgen del acoplamiento entre ondas P y SV en la superficie libre. La condición de superficie libre ($\sigma_{zz} = \sigma_{xz} = 0$ en $z = 0$) hace que las reflexiones P y SV en la superficie se refuercen constructivamente para ciertas velocidades de fase, produciendo el modo de Rayleigh. Sin conversión P–SV, las ondas de Rayleigh no existirían.

En términos prácticos: una fuente superficial vertical genera inicialmente ondas P y SV; estas se acoplan en la superficie libre y a lo largo de la propagación horizontal producen el tren de ondas de Rayleigh dominante en los registros sísmicos de superficie.

### Formación de ondas de Love

Las [[Love Waves]] son ondas SH guiadas en una capa superficial. No involucran conversión P–SV: la propagación de SH es independiente. La condición para que existan Love waves es la reflexión total de ondas SH en la interfaz capa–semiespacio, que requiere $V_{S,\text{capa}} < V_{S,\text{semiespacio}}$.

### Modos superiores de Rayleigh

En medios [[Layered Media|estratificados]], las múltiples reflexiones P–SV en distintas interfaces dan lugar a los [[Surface Wave Modes|modos superiores de Rayleigh]]. La conversión de modos en cada interfaz determina cuánta energía se transfiere entre modos, condicionando la amplitud relativa del modo fundamental y los superiores en el registro del arreglo de geófonos.

## Importancia para la adquisición

La conversión de modos tiene consecuencias prácticas en el diseño del arreglo:

1. **Contaminación de registros**: si la fuente genera ondas P, en las interfaces del subsuelo se generan ondas SV convertidas que llegan a los geófonos con diferentes moveouts. En ciertos casos pueden interferir con el tren de ondas superficiales.

2. **Separación en procesamiento**: el análisis f-k permite separar ondas con diferentes velocidades de fase (y por tanto diferentes pendientes en el sismograma). Las ondas de cuerpo convertidas tienen velocidades mayores que las ondas superficiales y se distinguen en el espectro f-k.

3. **Fuentes horizontales y Love**: las fuentes horizontales generan principalmente ondas SH, minimizando la conversión a P y SV. Esto es ventajoso para la adquisición de [[Love Waves]] con menor contaminación de componentes P–SV.

## Referencias

- Foti et al. (2014), Cap. 2.1.3, pp. 46–50 — condiciones de frontera y conversión P–SV–SH.
- Foti et al. (2014), Cap. 2.2, pp. 50–62 — formación de ondas de Rayleigh por acoplamiento P–SV.
