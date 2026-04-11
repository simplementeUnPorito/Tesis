---
name: Eurocode 8
description: Norma europea de diseño sísmico (EN 1998) que clasifica sitios por VS,30 en clases A–E y establece espectros de respuesta elástica para diseño de estructuras
type: reference
---

# Eurocode 8 — Norma Europea de Diseño Sísmico

> [!CONCEPT]
> El **Eurocode 8** (EN 1998-1, «Design of structures for earthquake resistance») es la norma europea que regula el diseño sísmico de edificaciones e infraestructuras. Su clasificación de sitio se basa en el parámetro [[Vs30|VS,30]] (velocidad de corte promedio en los primeros 30 m):
>
> | Clase | VS,30 (m/s) | Descripción |
> |-------|-------------|-------------|
> | A | > 800 | Roca o formación geológica muy rígida |
> | B | 360–800 | Depósitos de arena muy densa, grava o roca blanda |
> | C | 180–360 | Depósitos de arena densa a media, grava o arcilla rígida |
> | D | < 180 | Depósitos de suelo blando a cohesivo (arcillas blandas) |
> | E | — | Perfil con VS < 360 m/s suprayaciendo roca (h = 5–20 m) |
> | S1, S2 | — | Suelos especiales: turba/arcilla altamente compresible; suelos licuables |
>
> El valor VS,30 se determina preferiblemente mediante métodos no invasivos ([[MASW Method|MASW]], [[SASW Method|SASW]]) o invasivos ([[Downhole Test|downhole]]/[[Cross-Hole Test|cross-hole]]), y define el espectro de respuesta elástica mediante los factores de suelo S, TB, TC, TD.

## Relación con métodos de ondas superficiales

La [[MASW Method|MASW]] es el método más eficiente para determinar VS,30 en la práctica de ingeniería:
1. Adquisición sísmica en superficie (no invasiva, no requiere sondeo)
2. Extracción de la [[Dispersion Curve|curva de dispersión]] experimental
3. Inversión → perfil VS(z) hasta ≥30 m de profundidad
4. Cálculo: VS,30 = 30 / Σ(dᵢ/VS,ᵢ)

## Equivalencias con otros estándares

| Clase EC8 | NEHRP/ASCE 7 | VS,30 (m/s) |
|-----------|--------------|-------------|
| A | A (Roca dura) | > 1500 |
| A–B | B (Roca) | 760–1500 |
| B–C | C (Suelo muy denso) | 360–760 |
| C–D | D (Suelo rígido) | 180–360 |
| D | E (Suelo blando) | < 180 |

La norma chilena NCh 433 utiliza un esquema similar pero con umbrales adaptados a la sismicidad andina.

## Espectros de respuesta

El espectro de diseño horizontal de EC8 (aceleración espectral Sa) depende de la clase de sitio a través del factor de suelo S:

$$S_a(T) = a_g \cdot S \cdot \eta \cdot \Phi(T, T_B, T_C, T_D)$$

donde ag es la aceleración de diseño en roca, η es el factor de amortiguamiento (η=1 para ξ=5%), y Φ es la forma del espectro. Las clases D y E amplifican significativamente el espectro en el rango de períodos largos.

> [!EXAMPLE] Evidencia empírica (Foti et al. 2018, Comina et al. 2002)
> - **Seismic Microzonation, Memphis, TN** (Foti et al. 2018, §7.5): 45 ensayos [[MASW Method|MASW]] cubrieron la ciudad; VS,30 varió entre 160 y 490 m/s. La mayoría de sitios cayó en clase C–D (EC8), con clase E en zonas de llanura aluvial. El costo fue ~×15 inferior al de métodos invasivos para la misma cobertura espacial.
> - **Comina et al. (2002)** — Dique del Po (Italia): [[Joint Inversion|inversión conjunta]] [[MASW Method|MASW]]+ERT produjo perfiles VS(z) coherentes con ensayos CPT. VS,30 = 195–230 m/s → clase C/D en EC8. La clasificación afectó la aceleración de diseño horizontal en +25% respecto al bedrock.
> - **Andrus & Stokoe (2000)** — Base de datos de 26 sitios licuados en terremotos (Loma Prieta, Northridge, Kobe): todos los sitios con VS,30 < 180 m/s (clase D/E en EC8) mostraron evidencia de licuefacción cuando la sacudida superó el umbral CRR. VS,30 emerge como indicador de vulnerabilidad sísmica a nivel de sitio.

## Referencias

| Referencia | Contenido |
|-----------|-----------|
| CEN EN 1998-1 (2004) | Eurocode 8: Design of structures for earthquake resistance, Part 1 |
| NEHRP FEMA P-1050 (2015) | NEHRP Recommended Seismic Provisions: tablas de clasificación VS,30 |
| Foti et al. (2018) | §1.2, §7.5: uso de VS,30 y [[MASW Method|MASW]] para clasificación EC8 |
