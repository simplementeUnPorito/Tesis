# Martinete de leva — Simscape Multibody

Modelo físico de una maza TOTAL THSM61598 accionada por la leva definida en
`Assets/excel/perfil_leva_balistica_12lb.csv`.

## Ejecución

```matlab
cd("C:\Github\Tesis\modelado\matlab\martinete_leva_multibody")
validar_martinete();
[out, resumen] = simular_martinete_multibody();
graficar_transicion_toma();
generar_plano_herrero();
```

La simulación nominal geofísica ejecuta 8 vueltas a 25 rpm. Genera:

- `generated/leva_balistica_12lb.stl`
- `generated/resultados_multivuelta_piso.png`
- `generated/transicion_toma_C2.png`
- `generated/resumen_multivuelta.mat`
- `generated/plano_herrero_martinete_A3.pdf`
- `generated/plano_herrero_martinete_A3.png`
- `generated/plano_herrero_martinete_A3.svg`
- `generated/perfil_leva_1a1_mm.dxf`
- `generated/perfil_leva_1a1_mm.csv`
- `generated/lista_cotas_herrero.csv`

La lámina para el herrero contiene las vistas frontal y lateral, centros,
longitudes, ángulo de la palanca, espesores y separación axial. El DXF y el
CSV del perfil están en milímetros, a escala 1:1 y con origen en el centro
del eje de la leva. No se definen todavía eje/chaveta de la leva, rodamientos,
soldaduras ni bastidor: deben cerrarse mediante cálculo resistente antes de
fabricar.

## Maza incorporada

Datos del producto TOTAL THSM61598:

- cabeza nominal: 12 lb = 5.443 kg;
- material: acero al carbono 45#, forjado y tratado térmicamente;
- mango: fibra de vidrio de 900 mm;
- geometría medida de la cabeza: cilindro de 185 mm × Ø75 mm.

La masa del mango, no publicada por el fabricante, se mantiene como supuesto
de ingeniería de 0.80 kg. La masa total modelada es 6.243 kg y la inercia
de referencia respecto del pivote es 4.149 kg·m². Los sólidos ya no son una
animación sin masa: la cabeza, el mango de fibra de vidrio, la palanca gris,
el rodillo y su eje tienen masa e inercia calculadas desde su geometría. El
reparto supuesto de los 0.80 kg del conjunto de mango es 0.58/0.12/0.06/0.04
kg, respectivamente. El bloque `Inertia` queda sólo con masa residual
numérica, para no contar dos veces la misma maza.

El mango se muestra en azul verdoso para distinguir la fibra de vidrio; no
se modela como madera.

## Suelo y contacto

La condición inicial está referida al mundo:

- mango horizontal: θ = 0°;
- cabeza cilíndrica vertical;
- cara inferior de golpe: y = 0;
- superficie del piso: y = 0;
- asentamiento inicial: 0 mm.

El piso no tiene una trayectoria preprogramada. Su asentamiento se calcula a
partir de la fuerza cabeza–suelo:

```text
velocidad_asentamiento =
    -ganancia_compactación · max(F_impacto_filtrada - F_fluencia, 0)
```

La posición se integra de forma irreversible entre 0 y −100 mm. Los valores
iniciales son:

- fuerza de fluencia: 2 kN;
- ganancia de compactación: 5e-4 m/(N·s);
- rigidez normal de contacto: 100 MN/m;
- amortiguamiento normal: 20 kN·s/m.

Estos parámetros representan un suelo genérico y deben calibrarse con datos
de campo para interpretar fuerzas o asentamientos geofísicos cuantitativos.

Con esos valores, la corrida verificada produce 8 golpes en 8 vueltas y
54.03 mm de asentamiento acumulado. La penetración numérica máxima de la
cabeza en la superficie es 0.462 mm; es la pequeña deformación necesaria para
el método de contacto por penalización, no un cruce geométrico visible.

## Arquitectura

- Leva: `File Solid` para animación y `Point Cloud` para contacto.
- Seguidor: rodillo `Disk` y `Planar Contact Force`.
- Maza: articulación `Revolute Joint`, cabeza/mango/palanca/rodillo/eje como
  cuerpos rígidos con masa distribuida, gravedad en −Y y límites internos
  −30°/+45°, equivalentes a −14°/+61° en la referencia mundial.
- Piso: cuerpo móvil sobre `Prismatic Joint`.
- Compactación: fuerza filtrada, umbral de fluencia, ganancia e integrador
  saturado.
- Impacto: pequeño radio equivalente de 5 mm ubicado en la cara inferior de
  la cabeza, contra un `Line Segment`. El sólido visible conserva las medidas
  reales de 185 mm × Ø75 mm.

La leva es abierta: sólo la cara de elevación participa en el contacto. La
cara de retorno permanece en el sólido visible, pero no bloquea el descenso
cuando el suelo baja.

La toma original tenía un salto radial de 8 mm entre el círculo base y el
inicio de la subida. El modelo sustituye ese cierre por un empalme polinómico
C² que ocupa los últimos 90° del círculo base y los primeros 5° de la subida.
Esta extensión permite conservar posición, pendiente y curvatura sin ningún
máximo local: el radio es estrictamente monótono en toda la toma. El CSV
original no se modifica. Frente al empalme anterior de 30°, la pendiente
radial máxima baja de 26.77 a 9.46 mm/rad. A 25 rpm, los 90° de aproximación
se recorren en 0.60 s.

La leva, el rodillo y sus geometrías de contacto están en el mismo plano,
desplazado 60 mm en Z respecto de la palanca. Un eje cilíndrico material une
el rodillo con el cuerpo gris. La palanca termina tangente al rodillo en vez
de llegar hasta su centro, y queda una holgura axial leva–palanca de 39 mm.
Además, un `Spatial Contact Force` enfrenta la envolvente 3D cerrada de la
leva con la geometría exportada del sólido gris. La corrida de ocho vueltas
mide 0.000000 mm de interpenetración leva–palanca. En una vista frontal sus
proyecciones 2D pueden superponerse; al rotar Mechanics Explorer se observa
la separación axial y el eje que une ambos planos.

## Advertencia de temporización

La tabla original de 65 rpm omite el ascenso balístico entre el disparo y el
ápice. El tiempo real disparo–impacto es aproximadamente 0.625 s, mayor que
los 0.462 s disponibles hasta la siguiente vuelta. Por eso el caso
multivuelta se ejecuta a 25 rpm. El empalme de toma de 90° comienza un cuarto
de vuelta antes; 25 rpm deja tiempo suficiente para completar la caída aun
cuando el suelo ya se ha asentado.
