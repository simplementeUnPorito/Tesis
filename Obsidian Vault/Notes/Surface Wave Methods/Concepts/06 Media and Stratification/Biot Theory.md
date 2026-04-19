---
name: Biot Theory
description: Teoría de la poroelasticidad de Biot (1956) que describe la propagación de ondas en medios porosos saturados — predice tres tipos de ondas (P rápida, P lenta difusiva, S) y la independencia del [[Shear Modulus|módulo de corte]] G respecto a la saturación
type: reference
---

# Biot Theory — Teoría de Biot (Poroelasticidad)

> [!CONCEPT] Definición
> La **teoría de Biot** (Biot 1956) es el marco de referencia para describir la propagación de ondas elásticas en medios porosos saturados con fluido. La teoría acopla las ecuaciones de movimiento del esqueleto sólido con las del fluido intersticial, generando dos conjuntos de ecuaciones:
> $$\rho_{11} \ddot{\mathbf{u}} + \rho_{12} \ddot{\mathbf{U}} = \nabla \cdot \boldsymbol{\sigma} + b(\dot{\mathbf{U}} - \dot{\mathbf{u}})$$
> $$\rho_{12} \ddot{\mathbf{u}} + \rho_{22} \ddot{\mathbf{U}} = -\nabla p - b(\dot{\mathbf{U}} - \dot{\mathbf{u}})$$
> donde $\mathbf{u}$ es el desplazamiento del sólido, $\mathbf{U}$ el del fluido, $\boldsymbol{\sigma}$ el tensor de esfuerzos del esqueleto, $p$ la presión de poros, y $b$ el coeficiente de acoplamiento viscoso. La teoría predice la existencia de **tres tipos de ondas** en medios porosos saturados:
> 1. **Onda P rápida (P₁)**: movimiento en fase fluido-sólido; $V_{P1} > V_P^{drenado}$; baja [[Attenuation|atenuación]] a bajas frecuencias
> 2. **Onda P lenta (P₂, onda de Biot)**: movimiento en contrafase fluido-sólido; $V_{P2} \ll V_{P1}$; muy alta [[Attenuation|atenuación]] — se comporta como onda difusiva a frecuencias sísmicas
> 3. **Onda S**: cizallamiento del esqueleto; $V_S$ **no depende de la saturación** ($G$ es igual en condiciones drenadas y no drenadas)
> La consecuencia más importante para [[MASW Method|MASW]]: $G_{\text{sat}} = G_{\text{drained}}$ ([[Shear Modulus|módulo de corte]] independiente de la saturación), razón por la que $V_S$ es robusta respecto al nivel freático (ver [[Porous Media]]).
>
> — Biot (1956), *J. Acoust. Soc. Am.* 28(2), 168–191; Foti et al. (2018), §2.1.1, pp. 40–45; Gassmann (1951).

## Ecuaciones de Biot-Gassmann para módulos elásticos

La rigidez volumétrica saturada se calcula mediante la ecuación de Gassmann (1951):

$$K_{sat} = K_{sk} + \frac{(1 - K_{sk}/K_s)^2}{n/K_f + (1-n)/K_s - K_{sk}/K_s^2}$$

donde:
- $K_{sk}$: módulo drenado del esqueleto
- $K_s$: módulo del mineral sólido
- $K_f$: módulo del fluido (agua: ~2.25 GPa)
- $n$: porosidad

El [[Shear Modulus|módulo de corte]] es **invariante**: $G_{sat} = G_{sk}$ — consecuencia directa de que el fluido no resiste esfuerzos de corte.

## Implicaciones prácticas para [[Surface Waves|ondas superficiales]]

| Propiedad | Efecto de la saturación |
|-----------|------------------------|
| $V_S$ | Prácticamente nulo ($G$ no cambia) |
| $V_P$ | Drástico: $V_P \to 1500$ m/s cuando $K_f \to K_{agua}$ |
| Coeficiente de Poisson $\nu$ | Salta de ~0.25–0.35 (no saturado) a ~0.45–0.49 (saturado) |
| Onda P lenta | Detectable solo en ultrasonidos (> 100 kHz); difusiva en campo |

La tabla de agua produce un salto discontinuo en $V_P$ visible en perfiles de [[Seismic Refraction|refracción sísmica]] — pero no en $V_S$ medido por [[MASW Method|MASW]] (ver [[Porous Media]]).

## Frecuencia crítica de Biot

La teoría de Biot predice una frecuencia crítica:
$$f_c = \frac{\eta \, n}{2\pi \, k_0 \, \rho_f}$$

donde $\eta$ es la viscosidad del fluido, $k_0$ la permeabilidad intrínseca del suelo, y $\rho_f$ la densidad del fluido. Para $f < f_c$ (rango sísmico típico: < 1 kHz), la onda P lenta es esencialmente difusiva. Para $f > f_c$ (ultrasonidos), se vuelve propagante.

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — validación Biot en sitio La Salle (VP vs VS en tabla de agua)
> Foti et al. (2018, §6.3, pp. 293–298) demuestran experimentalmente la predicción de Biot en el sitio La Salle: el perfil de [[Seismic Refraction|refracción sísmica]] muestra un salto abrupto de $V_P$ de ~500 m/s (suelo no saturado) a ~1500 m/s (suelo saturado) a ~4 m de profundidad — marcando la tabla de agua. En contraste, el perfil $V_S$ ([[MASW Method|MASW]]) varía suavemente de 180 a 280 m/s sin discontinuidad a esa profundidad. El [[Poisson Ratio|razón de Poisson]] efectivo salta de $\nu \approx 0.30$ (no saturado) a $\nu \approx 0.49$ (saturado) — confirma predicción de Biot-Gassmann: $G = G_{sk}$ invariante, pero $K_{sat} \gg K_{sk}$ por la contribución del fluido. Foti concluye que asumir $\nu$ fijo en la inversión de Rayleigh introduce sesgo en $V_S$ si no se conoce la posición de la tabla de agua.
>
> — Foti et al. (2018), §6.3, pp. 293–298; Biot (1956), *J. Acoust. Soc. Am.* 28(2), 168–191.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Biot, M.A. (1956), *J. Acoust. Soc. Am.* 28(2), 168–191 | Teoría original de propagación de ondas en medios porosos |
| Gassmann, F. (1951), *Vierteljahrsschr. Naturf. Ges. Zürich* 96 | Ecuación de Gassmann para módulos saturados |
| Foti et al. (2018), *Surface Wave Methods* | §2.1.1 — implicaciones para [[Surface Waves|ondas superficiales]] |
