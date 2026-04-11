---
name: Resonant Column Test
description: Ensayo de laboratorio que mide VS y DS de pequeña deformación en muestras de suelo — referencia de validación para la estimación de DS mediante [[Surface Waves|ondas superficiales]]
type: reference
---

# Resonant Column Test (RCT) — Ensayo de Columna Resonante

> [!CONCEPT] Definición
> El **Resonant Column Test (RCT)** es un ensayo de laboratorio que mide la **velocidad de onda de corte** $V_S$ y el **coeficiente de amortiguamiento** $D_s$ de una muestra de suelo a pequeña deformación ($\gamma < 10^{-5}$). Se aplica una torsión vibratoria a la columna de suelo y se varía la frecuencia hasta encontrar la **resonancia fundamental** del sistema: $f_r = V_S/(4H)$ donde $H$ es la altura de la muestra. $V_S$ se calcula de $f_r$; $D_s$ se obtiene de la curva de amplificación en resonancia (half-power bandwidth) o del decaimiento libre tras cortar la excitación. Es la referencia de laboratorio estándar para validar las estimaciones in situ de $D_s$ obtenidas por [[MASW Method|MASW]] desde la [[Shear Damping Ratio|curva de atenuación]] de Rayleigh. **Limitaciones**: requiere extracción y transporte de la muestra (perturbación del estado de esfuerzos); el volumen representado es pequeño (muestra cilíndrica ~5–10 cm diámetro × 10–15 cm alto); el estado de esfuerzos in situ es difícil de reproducir exactamente.
>
> — Foti et al. (2018), §7.3; ASTM D4015; Hardin & Drnevich (1972).

## Principio de funcionamiento

La columna de suelo se monta en un aparato que aplica una torsión controlada en la base mientras la cabeza vibra libremente. El sistema mecánico (suelo + cabeza) tiene una frecuencia de resonancia fundamental:

$$f_r = \frac{1}{2\pi}\sqrt{\frac{k_{suelo}}{m_{cabeza}}}$$

donde $k_{suelo} = G \cdot A / H$ es la rigidez al corte del suelo, $G = \rho V_S^2$ el módulo de corte y $m_{cabeza}$ la masa polar de la cabeza vibrante.

La velocidad de onda de corte: $V_S = 2\pi f_r H \cdot C$ donde $C$ es un factor de corrección que depende de la geometría y la masa relativa cabeza/suelo.

El amortiguamiento $D_s$ se mide de dos formas:
1. **Half-power bandwidth**: $D_s = (f_2 - f_1)/(2f_r)$ donde $f_1, f_2$ son las frecuencias a amplitud $1/\sqrt{2}$ del pico
2. **Decaimiento libre**: ajuste de la envolvente de decaimiento $A(t) = A_0 e^{-\pi D_s f_r t}$

## Comparación con estimación in situ por [[Surface Waves|ondas superficiales]]

| Aspecto | Resonant Column Test | [[Surface Waves|Ondas superficiales]] ([[MASW Method|MASW]]) |
|---|---|---|
| Volumen representativo | Pequeño (muestra) | Grande (columna de suelo natural) |
| Perturbación de la muestra | Inevitable | No invasivo |
| Rango de deformación | Pequeña deformación | Pequeña deformación |
| Resultado | $V_S(z)$ y $D_s(z)$ por profundidad de extracción | $V_S(z)$ y $D_s(z)$ del perfil completo |
| Estimación de DS | Alta precisión (±0.5–1%) | Moderada (±1–2%) |
| Consistencia con ensayo sísmico | Posible | Directa |

## Rol en la validación del [[MASW Method|MASW]]-DS

El RCT proporciona la referencia de laboratorio para los perfiles $D_s(z)$ obtenidos por [[Shear Damping Ratio|inversión de la curva de atenuación]] de ondas de Rayleigh. En la práctica:
1. Se extrae muestras a diferentes profundidades del sitio investigado
2. Se realizan RCT en laboratorio a la presión de confinamiento in situ
3. Se comparan los perfiles $D_s^{RCT}(z)$ con los $D_s^{[[MASW Method|MASW]]}(z)$

Acuerdo típico: diferencias de 0.5–1.5% en $D_s$ absoluto — considerado razonable dado que el RCT mide una muestra y el [[MASW Method|MASW]] mide el comportamiento promedio del suelo in situ.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — validación DS [[MASW Method|MASW]] vs RCT en Pisa y Memphis
> Foti et al. (2018, §7.3) comparan el perfil $D_s(z)$ obtenido por inversión de la curva de atenuación de ondas de Rayleigh con ensayos RCT en dos sitios de referencia: la Torre de Pisa (arcilla de alta plasticidad) y el sitio de Memphis (depósitos aluviales). En Pisa, los valores de $D_s$ [[MASW Method|MASW]] oscilan entre 2–6% en los primeros 30 m, con diferencias respecto al RCT de ±1–1.5% en valor absoluto. En Memphis, el acuerdo es similar (±0.5–1%) excepto en la capa más superficial donde el [[MASW Method|MASW]] sobreestima el $D_s$ por efectos de scattering superficial. El estudio confirma que la inversión de la curva de atenuación de Rayleigh es un estimador válido de $D_s$ in situ, aunque con mayor incertidumbre que el RCT.
>
> — Foti et al. (2018), §7.3, pp. 375–380, Figs. 7.25–7.29.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §7.3, pp. 375–380 — validación DS [[MASW Method|MASW]] vs RCT |
| ASTM D4015 | Norma estándar para Resonant Column Test |
| Hardin & Drnevich (1972), *J. Soil Mech.* | Formulación del RCT para suelos |
