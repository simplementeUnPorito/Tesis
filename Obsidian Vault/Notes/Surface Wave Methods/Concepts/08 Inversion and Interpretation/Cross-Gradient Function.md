---
name: Cross-Gradient Function
description: Función de acoplamiento estructural en inversión conjunta multi-física que penaliza cuando los gradientes de dos modelos (VS y VP, o sísmico y eléctrico) apuntan en direcciones diferentes — impone co-localización de interfaces sin atar los valores
type: reference
---

# Cross-Gradient Function — Función de Gradiente Cruzado

> [!CONCEPT] Definición
> La **función de gradiente cruzado** es un término de acoplamiento en la [[Joint Inversion|inversión conjunta]] de múltiples tipos de datos geofísicos que impone **consistencia estructural** entre dos modelos $m_1(\mathbf{x})$ y $m_2(\mathbf{x})$ sin requerir una relación petrofísica explícita entre ellos. Se define como:
> $$\mathbf{t}(m_1, m_2) = \nabla m_1 \times \nabla m_2$$
> donde $\times$ es el producto vectorial entre los gradientes espaciales. La condición $\mathbf{t} = \mathbf{0}$ significa que los gradientes de ambos modelos son **paralelos o antiparalelos** en todo punto — equivalente a decir que las interfaces (zonas de alto gradiente) de ambos modelos están co-ubicadas espacialmente, aunque los valores en cada modelo pueden ser completamente diferentes. El funcional de inversión conjunta con cross-gradients es:
> $$\Phi_{JI} = \phi_1(\mathbf{d}_1, m_1) + \phi_2(\mathbf{d}_2, m_2) + w_{cg} \|\mathbf{t}(m_1, m_2)\|^2$$
> donde $\phi_i$ son los funcionales de misfit individuales y $w_{cg}$ controla la fuerza del acoplamiento estructural. En inversión sísmica-eléctrica conjunta (velocidad + resistividad), el cross-gradient impone que las capas geológicas que generan contraste de velocidad también generen contraste eléctrico — hipótesis realista sin requerir conocer la ecuación de Archie u otras relaciones petrofísicas.
>
> — Foti et al. (2018), §8.6.2, pp. 450–458; Gallardo & Meju (2003), *GRL* 30(14); Gallardo & Meju (2004), *JGR*.

## Interpretación geométrica

El gradiente cruzado $\mathbf{t} = \nabla m_1 \times \nabla m_2$ es el vector normal al plano definido por ambos gradientes. Minimizar $\|\mathbf{t}\|^2$ equivale a alinear los gradientes:

- $\mathbf{t} = \mathbf{0}$: gradientes paralelos → mismas interfaces en ambos modelos
- $\|\mathbf{t}\|$ grande: gradientes perpendiculares → interfaces en posiciones distintas

Este enfoque es más flexible que las relaciones petrofísicas (que atan valores, no solo estructuras) y más informativo que la inversión independiente (que ignora la co-localización).

## Aplicaciones en caracterización multi-método de sitios

| Combinación de datos | Modelos | Acoplamiento esperado |
|---------------------|---------|----------------------|
| MASW + ERT (eléctrica) | $V_S$ + $\rho_{elec}$ | Capas litológicas simultáneas |
| MASW + GPR | $V_S$ + $\epsilon$ (permitividad) | Tabla de agua, interfaces sedimentarias |
| MASW + P-refracción | $V_S$ + $V_P$ | Estratificación y saturación |
| MASW + gravimetría | $V_S$ + $\rho_{masa}$ | Contraste litológico denso |

> [!EXAMPLE] Evidencia empírica: Foti et al. (2018) — inversión conjunta MASW+ERT con cross-gradients
> Foti et al. (2018, §8.6.2, Figs. 8.43–8.46) presentan la inversión conjunta de datos MASW y ERT (Tomografía de Resistividad Eléctrica) para el sitio de una dique fluvial en el río Po, Italia, usando el método de cross-gradients (Gallardo & Meju 2003). La inversión independiente produce un perfil $V_S$ con 3 capas bien definidas pero una ERT con 5 unidades irregulares — inconsistencia que dificulta la interpretación geológica. Con el acoplamiento de cross-gradients ($w_{cg} = 0.5$), el perfil $V_S$ y la distribución de resistividad convergen a 3 unidades co-localizadas: (1) relleno antrópico superficial (0–2 m: $V_S$ = 180 m/s, alta resistividad), (2) arena aluvial saturada (2–8 m: $V_S$ = 250 m/s, baja resistividad), (3) grava consolidada (>8 m: $V_S$ = 450 m/s, resistividad media). La consistencia estructural mejora la interpretación geológica sin forzar relaciones petrofísicas.
>
> — Foti et al. (2018), §8.6.2, pp. 450–458; Gallardo & Meju (2003), *GRL* 30(14), 1658.

## Referencias

| Fuente | Sección / Página |
|--------|-----------------|
| Foti et al. (2018), *Surface Wave Methods* | §8.6.2 — inversión conjunta multi-física con cross-gradients |
| Gallardo & Meju (2003), *GRL* 30(14), 1658 | Definición del método de cross-gradients |
| Gallardo & Meju (2004), *JGR* 109(B3) | Aplicación a datos sísmicos y eléctricos |
