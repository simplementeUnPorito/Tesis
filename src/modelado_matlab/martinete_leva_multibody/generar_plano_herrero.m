function archivos = generar_plano_herrero()
%GENERAR_PLANO_HERRERO Genera una lamina minima para fabricar el martinete.
%
% La lamina no reemplaza el calculo resistente ni define soldaduras,
% rodamientos o ajustes. Todas las cotas geometricas se obtienen del mismo
% conjunto de parametros utilizado por el modelo Simscape Multibody.

[p, perfil] = martinete_parametros();
outputDirectory = martinete_output_dir();
if ~isfolder(outputDirectory)
    mkdir(outputDirectory);
end

archivos.png = fullfile(outputDirectory, ...
    "plano_herrero_martinete_A3.png");
archivos.pdf = fullfile(outputDirectory, ...
    "plano_herrero_martinete_A3.pdf");
archivos.svg = fullfile(outputDirectory, ...
    "plano_herrero_martinete_A3.svg");
archivos.dxf = fullfile(outputDirectory, ...
    "perfil_leva_1a1_mm.dxf");
archivos.csvPerfil = fullfile(outputDirectory, ...
    "perfil_leva_1a1_mm.csv");
archivos.csvCotas = fullfile(outputDirectory, ...
    "lista_cotas_herrero.csv");

camCenter = 1e3 * [p.camCenterWorldX, p.camCenterWorldY];
pivot = [0, 0];
rollerCenter = 1e3 * p.Hp * [cos(p.beta), sin(p.beta)];
rotation = [cos(p.mechanismTilt), -sin(p.mechanismTilt); ...
    sin(p.mechanismTilt), cos(p.mechanismTilt)];
camLocal = 1e3 * perfil.xy_m;
camWorld = camLocal * rotation.' + camCenter;

figureHandle = figure( ...
    Name="Plano minimo para herrero", ...
    Color="w", ...
    Units="centimeters", ...
    Position=[1, 1, 42, 29.7]);
layout = tiledlayout(figureHandle, 2, 3, ...
    TileSpacing="compact", Padding="compact");

frontAxes = nexttile(layout, 1, [2, 2]);
drawFrontView(frontAxes, p, camWorld, camCenter, pivot, ...
    rollerCenter);

sideAxes = nexttile(layout, 3);
drawSideView(sideAxes, p);

camAxes = nexttile(layout, 6);
drawCamDetail(camAxes, perfil);

title(layout, "MARTINETE DE LEVA — PLANO GEOMÉTRICO MÍNIMO", ...
    FontWeight="bold", FontSize=16);

exportgraphics(figureHandle, archivos.png, Resolution=300);
exportgraphics(figureHandle, archivos.pdf, ContentType="vector");
exportgraphics(figureHandle, archivos.svg, ContentType="vector");

writeCamDxf(archivos.dxf, camLocal);
writetable(array2table(camLocal, ...
    VariableNames=["x_mm", "y_mm"]), archivos.csvPerfil);
writeDimensionsTable(archivos.csvCotas, p, perfil, ...
    camCenter, rollerCenter);

fprintf("Plano PNG: %s\n", archivos.png);
fprintf("Plano PDF vectorial: %s\n", archivos.pdf);
fprintf("Plano SVG vectorial: %s\n", archivos.svg);
fprintf("Perfil de leva 1:1 DXF: %s\n", archivos.dxf);
fprintf("Perfil de leva 1:1 CSV: %s\n", archivos.csvPerfil);
fprintf("Lista de cotas: %s\n", archivos.csvCotas);
end

function drawFrontView(ax, p, camWorld, camCenter, pivot, ...
        rollerCenter)
hold(ax, "on");

% El martillo comercial se representa solo como interfaz existente.
plot(ax, [0, 390], [0, 0], ...
    Color=[0.04, 0.48, 0.52], LineWidth=9);
plot(ax, [330, 342], [-12, 12], "w-", LineWidth=4);
plot(ax, [344, 356], [-12, 12], "w-", LineWidth=4);
text(ax, 195, -23, "martillo existente", ...
    HorizontalAlignment="center", FontSize=9, ...
    Color=[0.02, 0.34, 0.37]);

% Palanca gris real, terminada tangente al rodillo.
leverLength = 1e3 * p.bellCrankLength;
leverWidth = 1e3 * p.bellCrankWidth;
direction = [cos(p.beta), sin(p.beta)];
normal = [-direction(2), direction(1)];
leverCorners = [ ...
    pivot - leverWidth / 2 * normal; ...
    pivot + leverWidth / 2 * normal; ...
    pivot + leverLength * direction + leverWidth / 2 * normal; ...
    pivot + leverLength * direction - leverWidth / 2 * normal];
patch(ax, leverCorners(:, 1), leverCorners(:, 2), ...
    [0.35, 0.35, 0.40], EdgeColor="k", LineWidth=1.0);

% Leva y rodillo.
patch(ax, camWorld(:, 1), camWorld(:, 2), ...
    [0.06, 0.65, 0.67], EdgeColor=[0, 0.25, 0.30], ...
    LineWidth=1.5, FaceAlpha=0.82);
rollerRadius = 1e3 * p.rollerRadius;
rectangle(ax, Position=[rollerCenter - rollerRadius, ...
    2 * rollerRadius, 2 * rollerRadius], Curvature=[1, 1], ...
    FaceColor=[0.78, 0.36, 0.10], EdgeColor="k", LineWidth=1.2);
rectangle(ax, Position=[rollerCenter - 0.40 * rollerRadius, ...
    0.80 * rollerRadius, 0.80 * rollerRadius], Curvature=[1, 1], ...
    FaceColor=[0.30, 0.30, 0.32], EdgeColor="none");

% Centros y ejes constructivos.
plot(ax, pivot(1), pivot(2), "ko", MarkerFaceColor="k", MarkerSize=6);
plotCenterMark(ax, camCenter, 10);
plotCenterMark(ax, rollerCenter, 7);
plot(ax, [pivot(1), rollerCenter(1)], ...
    [pivot(2), rollerCenter(2)], "--", ...
    Color=[0.25, 0.25, 0.25], LineWidth=0.8);

% Cotas principales de la estructura a fabricar.
drawAlignedDimension(ax, pivot, rollerCenter, 48, ...
    sprintf("P–R  %.0f mm", 1e3 * p.Hp));
drawAngleDimension(ax, pivot, 92, 0, p.beta, ...
    sprintf("\\beta = %.1f°", rad2deg(p.beta)));

text(ax, camCenter(1) + 12, camCenter(2) + 16, ...
    "eje de leva", FontSize=9, BackgroundColor="w");
text(ax, pivot(1) + 8, pivot(2) - 20, "P  pivote", ...
    FontSize=9, BackgroundColor="w");
text(ax, min(camWorld(:, 1)) + 8, max(camWorld(:, 2)) + 16, ...
    "LEVA", FontWeight="bold", BackgroundColor="w");

axis(ax, "equal");
xlim(ax, [-330, 420]);
ylim(ax, [-145, 390]);
grid(ax, "on");
ax.XMinorGrid = "on";
ax.YMinorGrid = "on";
ax.GridAlpha = 0.16;
ax.MinorGridAlpha = 0.08;
ax.TickDir = "out";
ax.FontName = "Arial";
ax.FontSize = 9;
ax.Toolbar.Visible = "off";
xlabel(ax, "x [mm]");
ylabel(ax, "y [mm]");
title(ax, "GEOMETRÍA DE MONTAJE — posición inicial");
hold(ax, "off");
end

function drawSideView(ax, p)
hold(ax, "on");

zLever = 1e3 * [-p.bellCrankDepth / 2, p.bellCrankDepth / 2];
zCam = 1e3 * (p.camAxialOffset + ...
    [-p.camThickness / 2, p.camThickness / 2]);
zRoller = 1e3 * (p.camAxialOffset + ...
    [-p.rollerThickness / 2, p.rollerThickness / 2]);
zAxle = 1e3 * (p.rollerAxleCenterZ + ...
    [-p.rollerAxleLength / 2, p.rollerAxleLength / 2]);

% Corte real por el eje del rodillo. Las piezas se dibujan en su posicion
% axial, no separadas como una lista.
rectangle(ax, Position=[zLever(1), -12, diff(zLever), 24], ...
    FaceColor=[0.35, 0.35, 0.40], EdgeColor="k", LineWidth=1.2);
rectangle(ax, Position=[zCam(1), 20, diff(zCam), 90], ...
    FaceColor=[0.06, 0.65, 0.67], EdgeColor="k", LineWidth=1.2);
rectangle(ax, Position=[zRoller(1), -20, diff(zRoller), 40], ...
    FaceColor=[0.78, 0.36, 0.10], EdgeColor="k", LineWidth=1.2);
rectangle(ax, Position=[zAxle(1), -8, diff(zAxle), 16], ...
    FaceColor=[0.27, 0.28, 0.31], EdgeColor="k", LineWidth=1.2);

plot(ax, [-18, 78], [0, 0], "k-.", LineWidth=0.6);

text(ax, mean(zLever), -16, "PALANCA", ...
    HorizontalAlignment="center", VerticalAlignment="top", ...
    FontSize=8.5, FontWeight="bold");
text(ax, mean(zCam), 67, "LEVA", Rotation=90, ...
    HorizontalAlignment="center", FontWeight="bold", Color="w");
text(ax, mean(zRoller), -25, "RODILLO", ...
    HorizontalAlignment="center", VerticalAlignment="top", ...
    FontSize=8.2, FontWeight="bold");
text(ax, mean(zAxle), 1, "EJE", ...
    HorizontalAlignment="center", VerticalAlignment="bottom", ...
    FontSize=8, FontWeight="bold", Color="w");

drawHorizontalDimension(ax, zLever(2), zCam(1), -36, ...
    sprintf("holgura en palanca  %.0f mm", ...
    1e3 * p.camLeverAxialClearance));

xlim(ax, [-20, 80]);
ylim(ax, [-48, 120]);
axis(ax, "off");
ax.FontName = "Arial";
ax.FontSize = 9;
ax.Toolbar.Visible = "off";
title(ax, "CORTE POR EL EJE DEL RODILLO");
hold(ax, "off");
end

function drawCamDetail(ax, perfil)
hold(ax, "on");

cam = 1e3 * perfil.xy_m;
radii = vecnorm(cam, 2, 2);
[maximumRadius, maximumIndex] = max(radii);
minimumRadius = 1e3 * perfil.metrics.baseRadius_m;
maximumPoint = cam(maximumIndex, :);
minimumPoint = [-minimumRadius, 0];

patch(ax, cam(:, 1), cam(:, 2), [0.06, 0.65, 0.67], ...
    EdgeColor=[0, 0.24, 0.29], LineWidth=1.5, FaceAlpha=0.82);

circleAngle = linspace(0, 2 * pi, 300);
plot(ax, minimumRadius * cos(circleAngle), ...
    minimumRadius * sin(circleAngle), "k:", LineWidth=1.1);
plot(ax, [0, maximumPoint(1)], [0, maximumPoint(2)], ...
    Color=[0.78, 0.12, 0.08], LineWidth=1.5);
plot(ax, [0, minimumPoint(1)], [0, minimumPoint(2)], ...
    Color=[0.20, 0.20, 0.20], LineWidth=1.2);
plotCenterMark(ax, [0, 0], 9);

maximumUnit = maximumPoint / maximumRadius;
maximumNormal = [-maximumUnit(2), maximumUnit(1)];
maximumLabelPoint = 0.63 * maximumPoint + 15 * maximumNormal;
text(ax, maximumLabelPoint(1), maximumLabelPoint(2), ...
    sprintf("R máx = %.2f cm", maximumRadius / 10), ...
    Rotation=atan2d(maximumPoint(2), maximumPoint(1)), ...
    HorizontalAlignment="center", BackgroundColor="w", ...
    FontWeight="bold", FontSize=9);
text(ax, minimumPoint(1) - 12, minimumPoint(2) - 12, ...
    sprintf("R mín = %.2f cm", minimumRadius / 10), ...
    HorizontalAlignment="right", BackgroundColor="w", ...
    FontWeight="bold", FontSize=9);

axis(ax, "equal");
xlim(ax, [-215, 205]);
ylim(ax, [-190, 190]);
grid(ax, "on");
ax.GridAlpha = 0.15;
ax.TickDir = "out";
ax.FontName = "Arial";
ax.FontSize = 8;
ax.Toolbar.Visible = "off";
xlabel(ax, "x local [mm]");
ylabel(ax, "y local [mm]");
title(ax, "DETALLE DE LEVA");
hold(ax, "off");
end

function plotCenterMark(ax, center, sizeValue)
plot(ax, center(1) + [-sizeValue, sizeValue], ...
    center(2) + [0, 0], "k-", LineWidth=0.9);
plot(ax, center(1) + [0, 0], ...
    center(2) + [-sizeValue, sizeValue], "k-", LineWidth=0.9);
end

function drawHorizontalDimension(ax, x1, x2, y, label)
color = [0.15, 0.15, 0.15];
tick = 7;
plot(ax, [x1, x2], [y, y], "-", Color=color, LineWidth=0.8);
plot(ax, [x1, x1], y + [-tick, tick], "-", Color=color);
plot(ax, [x2, x2], y + [-tick, tick], "-", Color=color);
text(ax, mean([x1, x2]), y - 7, label, ...
    HorizontalAlignment="center", VerticalAlignment="top", ...
    FontSize=8.5, BackgroundColor="w");
end

function drawAlignedDimension(ax, point1, point2, offset, label)
color = [0.15, 0.15, 0.15];
direction = point2 - point1;
direction = direction / norm(direction);
normal = [-direction(2), direction(1)];
dimensionPoint1 = point1 + offset * normal;
dimensionPoint2 = point2 + offset * normal;
plot(ax, [point1(1), dimensionPoint1(1)], ...
    [point1(2), dimensionPoint1(2)], "-", Color=color);
plot(ax, [point2(1), dimensionPoint2(1)], ...
    [point2(2), dimensionPoint2(2)], "-", Color=color);
plot(ax, [dimensionPoint1(1), dimensionPoint2(1)], ...
    [dimensionPoint1(2), dimensionPoint2(2)], ...
    "-", Color=color, LineWidth=0.8);
tick = 7 * normal;
plot(ax, dimensionPoint1(1) + [-tick(1), tick(1)], ...
    dimensionPoint1(2) + [-tick(2), tick(2)], "-", Color=color);
plot(ax, dimensionPoint2(1) + [-tick(1), tick(1)], ...
    dimensionPoint2(2) + [-tick(2), tick(2)], "-", Color=color);
labelPoint = mean([dimensionPoint1; dimensionPoint2], 1) + 8 * normal;
text(ax, labelPoint(1), labelPoint(2), label, ...
    Rotation=atan2d(direction(2), direction(1)), ...
    HorizontalAlignment="center", VerticalAlignment="middle", ...
    FontSize=8.5, BackgroundColor="w");
end

function drawAngleDimension(ax, center, radius, startAngle, endAngle, label)
angles = linspace(startAngle, endAngle, 120);
plot(ax, center(1) + radius * cos(angles), ...
    center(2) + radius * sin(angles), "k-", LineWidth=0.8);
plot(ax, center(1) + [0, radius * cos(startAngle)], ...
    center(2) + [0, radius * sin(startAngle)], "k:");
plot(ax, center(1) + [0, radius * cos(endAngle)], ...
    center(2) + [0, radius * sin(endAngle)], "k:");
middleAngle = mean([startAngle, endAngle]);
text(ax, center(1) + (radius + 18) * cos(middleAngle), ...
    center(2) + (radius + 18) * sin(middleAngle), label, ...
    HorizontalAlignment="center", FontWeight="bold", ...
    FontSize=9, BackgroundColor="w");
end

function writeDimensionsTable(filePath, p, perfil, ~, ~)
camRadii = 1e3 * vecnorm(perfil.xy_m, 2, 2);
minimumCamRadius = 1e3 * perfil.metrics.baseRadius_m;
maximumCamRadius = max(camRadii);
names = [
    "pivote_a_rodillo"
    "angulo_palanca"
    "palanca_gris_longitud"
    "palanca_gris_ancho"
    "palanca_gris_espesor"
    "eje_rodillo_diametro"
    "eje_rodillo_longitud"
    "leva_radio_minimo"
    "leva_radio_maximo"
    "separacion_planos"
    "holgura_axial_leva_palanca"
    ];
values = [
    1e3 * p.Hp
    rad2deg(p.beta)
    1e3 * p.bellCrankLength
    1e3 * p.bellCrankWidth
    1e3 * p.bellCrankDepth
    2e3 * p.rollerAxleRadius
    1e3 * p.rollerAxleLength
    minimumCamRadius / 10
    maximumCamRadius / 10
    1e3 * p.camAxialOffset
    1e3 * p.camLeverAxialClearance
    ];
units = [
    "mm"
    "deg"
    "mm"
    "mm"
    "mm"
    "mm"
    "mm"
    "cm"
    "cm"
    "mm"
    "mm"
    ];
writetable(table(names, values, units, ...
    VariableNames=["cota", "valor", "unidad"]), filePath);
end

function writeCamDxf(filePath, camCoordinatesMm)
fileIdentifier = fopen(filePath, "w");
if fileIdentifier < 0
    error("Martinete:NoSePuedeEscribirDXF", ...
        "No se pudo crear el archivo DXF: %s", filePath);
end
cleanup = onCleanup(@() fclose(fileIdentifier));

fprintf(fileIdentifier, "0\nSECTION\n2\nHEADER\n");
fprintf(fileIdentifier, "9\n$INSUNITS\n70\n4\n");
fprintf(fileIdentifier, "0\nENDSEC\n");
fprintf(fileIdentifier, "0\nSECTION\n2\nENTITIES\n");
fprintf(fileIdentifier, "0\nPOLYLINE\n8\nLEVA\n66\n1\n70\n1\n");
for index = 1:size(camCoordinatesMm, 1)
    fprintf(fileIdentifier, ...
        "0\nVERTEX\n8\nLEVA\n10\n%.9f\n20\n%.9f\n30\n0.0\n", ...
        camCoordinatesMm(index, 1), camCoordinatesMm(index, 2));
end
fprintf(fileIdentifier, "0\nSEQEND\n");
fprintf(fileIdentifier, "0\nPOINT\n8\nCENTROS\n10\n0.0\n20\n0.0\n30\n0.0\n");
fprintf(fileIdentifier, "0\nENDSEC\n0\nEOF\n");
end
