---
name: Green Function
description: Función de respuesta del medio elástico a una fuente puntual impulsiva — G(x,t;x₀,τ) describe la propagación de ondas desde la fuente hasta el receptor y es el núcleo del modelo convolucional sísmico y de la [[Seismic Interferometry|interferometría sísmica]]
type: reference
---

# Green Function — Función de Green

> [!CONCEPT] Definición
> La **función de Green** $G(\mathbf{x}, t; \mathbf{x}_0, \tau)$ es la respuesta del medio elástico a una fuente puntual impulsiva aplicada en $\mathbf{x}_0$ en el instante $\tau$:
> $$\mathcal{L}[G(\mathbf{x}, t; \mathbf{x}_0, \tau)] = \delta(\mathbf{x} - \mathbf{x}_0) \, \delta(t - \tau)$$
> donde $\mathcal{L}$ es el operador diferencial de la ecuación de onda elástica. La función de Green codifica **toda la información sobre la estructura del medio** entre la fuente y el receptor: velocidades de onda, estratificación, [[Attenuation|atenuación]], geometría de la fuente. La señal observada en [[MASW Method|MASW]] es la convolución de la función de Green con la señal de la fuente real:
> $$u(\mathbf{x}, t) = \int_{-\infty}^{\infty} G(\mathbf{x}, t; \mathbf{x}_0, \tau) \, s(\tau) \, d\tau = G(\mathbf{x}, t - \tau; \mathbf{x}_0, 0) * s(t)$$
> La función de Green del [[Lamb's Problem|problema de Lamb]] (semiespacio elástico homogéneo con carga superficial) incluye contribuciones de la onda Rayleigh que dominan en campo lejano y decaen como $r^{-1/2}$ (véase [[Hankel Function]]). En la **[[Seismic Interferometry|interferometría sísmica]]**, la [[Cross-Correlation|correlación cruzada]] entre dos receptores recupera la función de Green entre ellos: $G(\mathbf{x}_1, t; \mathbf{x}_2, 0) \approx -\frac{d}{dt} [u(\mathbf{x}_1, t) \star u(\mathbf{x}_2, t)] / S(f)$ — principio que permite usar ruido ambiental como fuente virtual.
>
> — Foti et al. (2018), §2.4.3, §8.4, pp. 107–111, 427–435; Aki & Richards (2002), §4; Lamb (1904).

## Función de Green para Rayleigh en campo lejano

Para el [[Lamb's Problem|problema de Lamb]], la componente Rayleigh de la función de Green en superficie libre en campo lejano es (Foti Ec. 2.75):

$$G_{Rayleigh}(r, \omega) \approx A_R(\omega) \cdot \frac{e^{-i k_R r}}{\sqrt{k_R r}} \cdot e^{i\pi/4}$$

donde $k_R = \omega/V_R(\omega)$ y $A_R(\omega)$ contiene la información sobre la partición de energía entre modos y la amplitud de excitación. Esta expresión es la base del análisis de amplitudes en [[MASW Method|MASW]] para estimar el [[Shear Damping Ratio|factor de amortiguamiento]] $D_S$ a partir del decaimiento espacial (método de [[Joint Inversion|inversión conjunta]] $V_S + D_S$).

## Reciprocidad y simetría

La función de Green satisface el principio de reciprocidad:
$$G_{ij}(\mathbf{x}, t; \mathbf{x}_0, \tau) = G_{ji}(\mathbf{x}_0, t; \mathbf{x}, \tau)$$

Esto significa que fuente y receptor pueden intercambiarse — principio que justifica la [[Seismic Interferometry|interferometría sísmica]] y la tomografía de ruido ambiental.

## Relación con la [[Seismic Interferometry|interferometría sísmica]]

Wapenaar (2004, *PRL*) demuestra que la función de Green entre dos receptores puede extraerse de la correlación cruzada del campo difuso:
$$G(\mathbf{x}_1, \mathbf{x}_2, t) + G(\mathbf{x}_1, \mathbf{x}_2, -t) \propto C(\mathbf{x}_1, \mathbf{x}_2, t)$$

donde $C$ es la [[Cross-Correlation|correlación cruzada]] entre los campos registrados en $\mathbf{x}_1$ y $\mathbf{x}_2$. Esta relación permite medir la dispersión de [[Rayleigh Waves|ondas Rayleigh]] sin fuente activa — base del [[ReMi Method|método ReMi]] y el [[SPAC Method|método SPAC]].

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — función de Green por correlación de ruido en el sitio La Salle
> Foti et al. (2018, §8.4.2, pp. 430–436) demuestran la extracción de la función de Green por correlación de ruido ambiental en el sitio La Salle usando 6 sensores en configuración circular con radio 10–50 m. La correlación cruzada entre pares de receptores acumula durante 30 minutos de registro pasivo. La función de Green emergente muestra un frente de onda Rayleigh con tiempo de llegada $t = r/V_R(f)$ consistente con $V_R$ entre 160 y 320 m/s (4–20 Hz). La [[Dispersion Curve|curva de dispersión]] extraída de la función de Green coincide con la obtenida por [[MASW Method|MASW]] activo dentro del 5% en el rango 6–18 Hz — validando la equivalencia de ambos métodos para sitios con campo difuso isotrópico.
>
> — Foti et al. (2018), §8.4.2, pp. 430–436; Wapenaar (2004), *Phys. Rev. Lett.* 93(25).

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §2.4.3, §8.4 — función de Green en [[MASW Method|MASW]] e interferometría |
| Aki & Richards (2002), *Quantitative Seismology* | §4 — función de Green en elastodinámica |
| Lamb, H. (1904), *Phil. Trans. R. Soc. A* 203 | Función de Green original para semiespacio |
| Wapenaar, K. (2004), *Phys. Rev. Lett.* 93(25) | Extracción de G por correlación de ruido |
