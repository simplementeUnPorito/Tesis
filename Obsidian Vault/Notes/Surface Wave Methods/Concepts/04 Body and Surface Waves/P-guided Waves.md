# P-guided Waves

> **Contexto:** Exploración marina somera, adquisición con hidrófonos en el fondo o en la columna de agua.
> **Fuente:** Foti et al. Cap. 8, pp. 403–412.

## Definición

Las **ondas guiadas de tipo P** (*P-guided waves*) son modos de propagación que existen en el sistema agua-sedimentos. Corresponden a los **modos fugantes** (*leaky modes*) de la ecuación de dispersión: raíces complejas cuya parte real de la velocidad de fase supera la velocidad compresional del agua (~1500 m/s). Físicamente son **ondas P multireflejadas** en la capa de agua (entre la superficie libre del agua y el fondo marino), con energía parcialmente atrapada y parcialmente radiada hacia el subsuelo.

En oceanografía acústica se denominan ondas ULF (*ultra-low frequency*), típicamente en el rango 1–100 Hz en plataformas continentales. En aguas muy someras (ensayos near-shore), el rango se desplaza hacia valores más altos.

## Diferencia con ondas de Scholte

| Característica | [[Scholte Waves|Ondas de Scholte]] | Ondas guiadas P |
|---|---|---|
| Tipo de modo | Modo real (propagante) | Modo fugante (leaky) |
| Velocidad de fase | < Vp_agua | > Vp_agua |
| Parámetro sensoriado | Vs del sedimento | Vp del sedimento y del agua |
| Frecuencia de corte | Sin corte (modo fund.) | Depende de la geometría |
| Visibilidad en registro | Baja velocidad, llegan tarde | Alta velocidad, llegan primero |
| Aplicación | Perfil Vs marino | Perfil Vp marino |

## Condición de existencia y aproximación acústica

Las ondas guiadas P existen cuando la capa de agua puede funcionar como guía acústica, es decir, cuando la velocidad compresional del sedimento supera la del agua. La **aproximación acústica** (tratar el sedimento como un fluido con Vs = 0) es válida cuando el ratio de Poisson es alto, como ocurre en sedimentos saturados blandos (Vs << Vp). Esta aproximación simplifica el modelado directo.

## Información a priori necesaria

Para modelar e invertir ondas guiadas P se necesita:
- **Velocidad del agua:** medible con un sensor de temperatura/salinidad, o asumida ≈ 1500 m/s.
- **Velocidad compresional del subfondo:** estimable del tiempo de llegada del primer arribo en el registro.

## Inversión conjunta con ondas de Scholte

Si se adquieren simultáneamente [[Scholte Waves|ondas de Scholte]] (sensibles a Vs) y ondas guiadas P (sensibles a Vp), la **inversión conjunta** permite estimar ambos perfiles acoplando los modelos geométricos (espesores de capa compartidos). Esta combinación hace posible la caracterización completa del subsuelo marino con un único dataset.

## Referencias

- Foti et al. (2014), Cap. 8, Secciones 8.2.2 y 8.2.3.
