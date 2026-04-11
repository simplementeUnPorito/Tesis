---
name: Shear Damping Ratio
description: Parámetro de amortiguamiento material del suelo (Ds) estimado a partir de [[Surface Waves|ondas superficiales]] — mide la disipación de energía en ciclos de deformación
type: reference
---

# Shear Damping Ratio (Ds) — Amortiguamiento al Corte Material

> [!CONCEPT] Definición
> El **Shear Damping Ratio** $D_s$ cuantifica la disipación de energía en un suelo bajo deformación cíclica de corte. En el modelo [[Viscoelastic Media|viscoelástico]] lineal, $D_s = G''/(2G')$ donde $G^* = G'(1+2iD_s)$ es el módulo de corte complejo. En métodos de [[Surface Waves|ondas superficiales]], $D_s$ se estima a partir de la **curva de atenuación** $\alpha_R(f)$ de las [[Rayleigh Waves]]: $D_s \approx \alpha_R V_R/(2\pi f)$. Es el parámetro de amortiguamiento dinámico a pequeña deformación, relevante para cálculos de amplificación sísmica de sitio.
>
> — Foti et al. (2018), Caps. 2, 5, 7; Lai & Rix (1998).

## Intuición física

Cuando un suelo se deforma y se recupera cíclicamente (como ocurre durante el paso de una onda sísmica), parte de la energía mecánica se disipa en calor por fricción interna entre partículas. Esta disipación no es nula incluso para deformaciones muy pequeñas (rango elástico). El **shear damping ratio** Ds cuantifica esta capacidad disipativa: es la fracción de energía elástica almacenada en un ciclo que se pierde como calor.

Un suelo con alto Ds disipa las ondas sísmicas rápidamente → menor amplificación. Un suelo con bajo Ds actúa casi elásticamente → la onda viaja sin grandes pérdidas.

## Definición técnica

Para un material [[Viscoelastic Media|viscoelástico]] lineal en el dominio de la frecuencia, el módulo de corte complejo se escribe:

$$G^* = G' + i G'' = G'(1 + 2iD_s)$$

donde:
- $G'$ = módulo de almacenamiento (parte elástica, real)
- $G''$ = módulo de pérdida (parte disipativa, imaginaria)
- $D_s = G''/(2G')$ = shear damping ratio

El vínculo con el [[Attenuation|coeficiente de atenuación]] de la [[Rayleigh Waves|onda de Rayleigh]] es:

$$D_s \approx \frac{\alpha_R \cdot V_R}{2\pi f}$$

donde $\alpha_R$ es el coeficiente de atenuación espacial (1/m) y $V_R$ la [[Phase Velocity|velocidad de fase]]. Esta relación surge de la propagación en un semiespacio viscoelástico (Ecuación del libro, cap. 2 y 5).

También se expresa como $D_s = 1/(2Q)$, donde $Q$ es el factor de calidad del material.

## Obtención desde [[Surface Waves|ondas superficiales]]

El procedimiento experimental para determinar el perfil Ds(z) desde mediciones de superficie involucra tres pasos:

1. **Medición de la curva de atenuación experimental:** se registra el decaimiento de amplitud de las [[Rayleigh Waves|ondas de Rayleigh]] en función de la distancia y la frecuencia. Esto requiere separar la atenuación geométrica ($\propto 1/\sqrt{r}$) de la [[Attenuation|atenuación material]]. Los métodos disponibles incluyen:
   - Regresión de la función de transferencia compleja (Capítulo 5, Sección 5.3)
   - Regresión amplitud–offset (Capítulo 5, Sección 5.2)

2. **Inversión de la curva de atenuación:** se ajusta el coeficiente de atenuación teórico de Rayleigh (calculado para un modelo de capas viscoelástico) a la curva experimental mediante mínimos cuadrados. Esta inversión puede realizarse **simultáneamente** con la inversión de la [[Dispersion Curve|curva de dispersión]] para obtener Vs(z) y Ds(z) en el mismo proceso.

3. **Validación:** se comparan los perfiles Ds(z) con datos independientes: ensayo de columna resonante (RCT) en laboratorio o perfiles disponibles de literatura.

## Incertidumbres y limitaciones

- La estimación de Ds es más incierta que la de Vs porque la curva de atenuación tiene mayor varianza experimental.
- En **capas superficiales**, el SWM tiende a **sobreestimar Ds** por:
  - Scattering de energía en heterogeneidades (produce atenuación aparente no material)
  - Disipación por fricción de contacto entre partículas, no modelada en el medio viscoelástico
  - Alta frecuencia → mayor dependencia con la rugosidad del medio
- El Ds obtenido desde [[Surface Waves|ondas superficiales]] representa el **amortiguamiento dinámico a pequeña deformación** (small-strain), coherente con las condiciones de propagación de ondas sísmicas.
- La hipótesis del **modo fundamental** de Rayleigh puede no ser satisfecha si hay modos superiores presentes, lo que afecta tanto la [[Dispersion Curve|curva de dispersión]] como la de atenuación.

## Relevancia en ingeniería sísmica

El perfil Ds(z) entra directamente en los cálculos de **respuesta sísmica local** (amplificación de sitio), ya que controla el amortiguamiento de los picos de amplificación en el espectro de respuesta del suelo. Un error en Ds produce errores en la forma espectral predicha. Por esta razón, la estimación in situ de Ds es valiosa comparada con valores tomados de tablas genéricas.

## Diferencias con damping de laboratorio

| Característica | Ensayo de laboratorio (RCT) | [[Surface Waves|Ondas superficiales]] (SWM) |
|---|---|---|
| Volumen representativo | Pequeño (muestra) | Grande (columna de suelo) |
| Perturbación del suelo | Extracción de muestra | No invasivo |
| Separación atenuación geométrica | No aplicable | Necesaria |
| Estimación de capas superficiales | Posible con muestras superficiales | Tendencia a sobreestimar |
| Consistencia con datos sísmicos | Posible | Directa |

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — validación Ds en sitios Pisa y Memphis
> Foti et al. (2018, §7.3) presentan la inversión simultánea de la [[Dispersion Curve|curva de dispersión]] (para $V_S$) y la curva de atenuación (para $D_s$) en dos sitios de referencia: la Torre de Pisa y el sitio de Memphis. Los perfiles $D_s(z)$ obtenidos por [[Surface Waves|ondas superficiales]] ([[MASW Method|MASW]] activo + pasivo) muestran acuerdo razonable con ensayos de columna resonante (RCT) independientes, con diferencias típicas de 0.5–1.5% en $D_s$ absoluto. El estudio confirma que la inversión de la curva de atenuación de Rayleigh es una estimación in situ válida del amortiguamiento dinámico a pequeña deformación, aunque con mayor incertidumbre que la estimación de $V_S$.
>
> — Foti et al. (2018), §7.3, pp. 375–380, Figs. 7.25–7.29.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | Caps. 2, 5, 7 — definición, estimación e inversión de $D_s$ |
| Lai & Rix (1998), *Georgia Tech Research Report* | Inversión simultánea $c_R$ + $\alpha_R$ para $V_S$ y $D_s$ |
| Foti (2003), *Géotechnique* 53 | $D_s$ de arcilla de Pisa desde [[Surface Waves|ondas superficiales]] |
