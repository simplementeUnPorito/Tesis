function figureHandle = graficar_transicion_toma()
%GRAFICAR_TRANSICION_TOMA Compara el escalon original con el empalme C2.

[p, perfil] = martinete_parametros();
original = 1e3 * perfil.xy_original_m;
smooth = 1e3 * perfil.xy_m;
pickup = 1e3 * perfil.pickup_xy_m;

pickupAngle = unwrap(atan2(pickup(:, 2), pickup(:, 1)));
pickupRadius = vecnorm(pickup, 2, 2);
angleBeforeTake = -rad2deg(pickupAngle - pickupAngle(end));
baseRadius = perfil.metrics.pickupRadiusStart_m * 1e3;
originalRise = 1e3 * perfil.rise_xy_original_m;
originalRiseAngle = unwrap(atan2( ...
    originalRise(:, 2), originalRise(:, 1)));
originalRiseRadius = vecnorm(originalRise, 2, 2);
joinMask = originalRiseAngle >= ...
    perfil.metrics.pickupJoinPolarAngle_rad;
originalRiseAngle = originalRiseAngle(joinMask);
originalRiseRadius = originalRiseRadius(joinMask);
originalRiseCoordinate = -rad2deg(originalRiseAngle - ...
    perfil.metrics.pickupJoinPolarAngle_rad);
takeCoordinate = -rad2deg( ...
    perfil.metrics.pickupTakePolarAngle_rad - ...
    perfil.metrics.pickupJoinPolarAngle_rad);
takeRadius = originalRiseRadius(1);

figureHandle = figure(Name="Transicion C2 de toma", Color="w");
layout = tiledlayout(1, 2, TileSpacing="compact", Padding="compact");

nexttile;
plot(original(:, 1), original(:, 2), ...
    "--", Color=[0.55 0.55 0.55], LineWidth=1.0);
hold on;
plot(smooth(:, 1), smooth(:, 2), ...
    Color=[0.10 0.35 0.65], LineWidth=1.3);
plot(pickup(:, 1), pickup(:, 2), ...
    Color=[0.80 0.20 0.10], LineWidth=2.2);
scatter(pickup([1, end], 1), pickup([1, end], 2), ...
    26, "filled");
axis equal;
xlim([-90, -20]);
ylim([-70, 25]);
xlabel("x [mm]");
ylabel("y [mm]");
legend("perfil CSV", "perfil suavizado", "empalme C2", ...
    Location="best");
grid on;
title("Detalle geométrico de la toma");

nexttile;
originalCoordinate = [angleBeforeTake(1); takeCoordinate; ...
    takeCoordinate; originalRiseCoordinate(2:end)];
originalRadius = [baseRadius; baseRadius; takeRadius; ...
    originalRiseRadius(2:end)];
plot(originalCoordinate, originalRadius, ...
    "--", Color=[0.55 0.55 0.55], LineWidth=1.1);
hold on;
plot(angleBeforeTake, pickupRadius, ...
    Color=[0.80 0.20 0.10], LineWidth=2.0);
xline(takeCoordinate, ":", "\theta=-16 deg");
xline(0, ":", "empalme con subida");
xlabel("Ángulo antes de la toma [deg]");
ylabel("Radio físico [mm]");
legend("escalón original", "empalme C2", Location="best");
grid on;
title("Radio estrictamente monótono");

title(layout, sprintf( ...
    "Toma C2 monótona: %.0f deg previos + %.0f deg de subida", ...
    rad2deg(p.pickupBlendAngle), ...
    rad2deg(p.pickupJoinRiseAngle)));

generatedDir = martinete_output_dir();
if ~isfolder(generatedDir)
    mkdir(generatedDir);
end
axesHandles = findall(figureHandle, Type="axes");
for axesHandle = axesHandles'
    axesHandle.Toolbar.Visible = "off";
end
exportgraphics(figureHandle, fullfile(generatedDir, ...
    "transicion_toma_C2.png"), Resolution=180);
end
