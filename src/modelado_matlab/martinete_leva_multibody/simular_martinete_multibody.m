function [out, resumen] = simular_martinete_multibody()
%SIMULAR_MARTINETE_MULTIBODY Simula la maza sobre un piso que se hunde.

[p, perfil, referencias] = preparar_martinete();
modelName = "martinete_leva_multibody";

in = Simulink.SimulationInput(modelName);
in = in.setVariable("p", p);
in = in.setVariable("perfil", perfil);
in = in.setModelParameter("StopTime", num2str(p.stopTime, "%.12g"));
out = sim(in);

theta = out.yout.get("theta_deg").Values;
omega = out.yout.get("omega_rad_s").Values;
camTorque = out.yout.get("cam_torque_Nm").Values;
rollerForce = out.yout.get("roller_force_N").Values;
rawCamForce = out.yout.get("raw_contact_force_N").Values;
groundPosition = out.yout.get("ground_position_m").Values;
impactForce = out.yout.get("impact_force_N").Values;
camLeverPenetration = ...
    out.yout.get("cam_lever_penetration_m").Values;

camOmega = 2 * pi * p.simulationRpm / 60;
period = 2 * pi / camOmega;
releaseTimes = (0:(p.simRevolutions - 1))' * period + period / 2;
impactThreshold = 500;

impactTimes = nan(p.simRevolutions, 1);
impactPeaks = nan(p.simRevolutions, 1);
impactAngles = nan(p.simRevolutions, 1);
groundAtImpact = nan(p.simRevolutions, 1);

for k = 1:p.simRevolutions
    searchStart = releaseTimes(k) + 0.05;
    searchEnd = min(releaseTimes(k) + 0.95 * period, p.stopTime);
    window = impactForce.Time >= searchStart & ...
        impactForce.Time <= searchEnd;
    if ~any(window)
        continue
    end

    indices = find(window);
    [peakForce, localIndex] = max(impactForce.Data(window));
    if peakForce < impactThreshold
        continue
    end

    eventIndex = indices(localIndex);
    impactTimes(k) = impactForce.Time(eventIndex);
    impactPeaks(k) = peakForce;
    impactAngles(k) = interp1(theta.Time, theta.Data, impactTimes(k));
    groundAtImpact(k) = interp1(groundPosition.Time, ...
        groundPosition.Data, impactTimes(k));
end

impactDetected = isfinite(impactTimes);
contactReach = hypot(p.Lh, p.headContactOffset);
contactPhase = atan2(p.headContactOffset, p.Lh);
requiredArgument = (groundPosition.Data - p.pivotHeight + ...
    p.headContactRadius) / contactReach;
requiredArgument = max(-1, min(1, requiredArgument));
requiredTheta = rad2deg(contactPhase + asin(requiredArgument));
groundOnThetaGrid = interp1(groundPosition.Time, ...
    groundPosition.Data, theta.Time);
thetaRad = deg2rad(theta.Data);
headBottom = p.pivotHeight + p.Lh * sin(thetaRad) - ...
    p.headContactOffset * cos(thetaRad) - p.headContactRadius;
numericalPenetration = max(0, groundOnThetaGrid - headBottom);

phase = mod(camTorque.Time, period);
riseMask = phase >= 0.02 & phase <= period / 2;
pickupPhase = mod(rawCamForce.Time, period);
pickupDuration = p.pickupBlendAngle / (2 * pi) * period;
pickupMask = pickupPhase >= period - pickupDuration | ...
    pickupPhase <= 0.30;
nominal = referencias(referencias.rpm == p.nominalRpm, :);

impactTable = table((1:p.simRevolutions)', releaseTimes, ...
    impactTimes, impactPeaks, impactAngles, 1e3 * groundAtImpact, ...
    VariableNames=["turn", "releaseTime_s", "impactTime_s", ...
    "peakImpactForce_N", "impactAngle_deg", "groundLevel_mm"]);

resumen = struct;
resumen.product = p.productManufacturer + " " + p.productReference;
resumen.simulationRpm = p.simulationRpm;
resumen.revolutionsRequested = p.simRevolutions;
resumen.initialTheta_deg = theta.Data(1);
resumen.initialGroundLevel_mm = 1e3 * groundPosition.Data(1);
resumen.initialHeadClearance_mm = ...
    1e3 * (headBottom(1) - groundOnThetaGrid(1));
resumen.impactsDetected = nnz(impactDetected);
resumen.allRevolutionsHit = all(impactDetected);
resumen.minimumTheta_deg = min(theta.Data);
resumen.maximumTheta_deg = max(theta.Data);
resumen.maximumGroundSink_mm = -1e3 * min(groundPosition.Data);
resumen.maximumNumericalPenetration_mm = ...
    1e3 * max(numericalPenetration);
resumen.maximumCamLeverPenetration_mm = ...
    1e3 * max(camLeverPenetration.Data, [], "all");
resumen.maximumImpactForce_N = max(impactForce.Data);
resumen.maximumCamContactForce_N = max(rawCamForce.Data);
resumen.maximumCamPickupForce_N = max(rawCamForce.Data(pickupMask));
resumen.peakCamTorqueRise_Nm = max(abs(camTorque.Data(riseMask)));
resumen.peakFilteredRollerForceAll_N = max(rollerForce.Data);
resumen.catalogNominalPeakCamTorque_Nm = nominal.peakCamTorque_Nm;
resumen.catalogNominalPeakRollerForce_N = nominal.peakRollerForce_N;
resumen.impactTable = impactTable;

fprintf("\nSimscape Multibody — %s\n", resumen.product);
fprintf(['  Caso: %.0f rpm, %d vueltas, asentamiento producido ' ...
    'por los golpes.\n'], p.simulationRpm, p.simRevolutions);
fprintf(['  Inicio: theta=%.3f deg, piso=%.3f mm, ' ...
    'separacion cabeza-piso=%.3f mm.\n'], ...
    resumen.initialTheta_deg, resumen.initialGroundLevel_mm, ...
    resumen.initialHeadClearance_mm);
fprintf("  Golpes principales detectados: %d/%d.\n", ...
    resumen.impactsDetected, p.simRevolutions);
fprintf("  Recorrido angular observado: %.2f a %.2f deg.\n", ...
    resumen.minimumTheta_deg, resumen.maximumTheta_deg);
fprintf("  Fuerza pico cabeza-piso: %.0f N.\n", ...
    resumen.maximumImpactForce_N);
fprintf(['  Toma C2 monótona: %.0f deg previos + %.0f deg de subida; ' ...
    'pico leva-seguidor: %.0f N.\n'], ...
    rad2deg(p.pickupBlendAngle), ...
    rad2deg(p.pickupJoinRiseAngle), ...
    resumen.maximumCamPickupForce_N);
fprintf("  Asentamiento final: %.2f mm; penetracion numerica max.: %.3f mm.\n", ...
    -1e3 * groundPosition.Data(end), ...
    resumen.maximumNumericalPenetration_mm);
fprintf("  Interpenetracion leva-palanca gris: %.6f mm.\n", ...
    resumen.maximumCamLeverPenetration_mm);
disp(impactTable);

figureHandle = figure( ...
    Name="Martinete geofisico - Simscape Multibody", Color="w");
layout = tiledlayout(5, 1, TileSpacing="compact", Padding="compact");

nexttile;
plot(theta.Time, theta.Data, LineWidth=1.1);
hold on;
plot(groundPosition.Time, requiredTheta, "--", LineWidth=1.1);
yline(rad2deg(p.thetaMin + p.mechanismTilt), ":", "tope inferior");
yline(rad2deg(p.thetaMax + p.mechanismTilt), ":", "tope superior");
for time = impactTimes(impactDetected)'
    xline(time, Color=[0.75 0.15 0.10], Alpha=0.35);
end
ylabel("\theta [deg]");
legend("maza", "\theta requerido por el piso", Location="best");
grid on;

nexttile;
plot(omega.Time, omega.Data, LineWidth=1.0);
ylabel("\omega [rad/s]");
grid on;

nexttile;
plot(groundPosition.Time, 1e3 * groundPosition.Data, ...
    LineWidth=1.2);
ylabel("piso [mm]");
grid on;

nexttile;
plot(impactForce.Time, impactForce.Data, ...
    Color=[0.72 0.18 0.10], LineWidth=0.8);
hold on;
scatter(impactTimes(impactDetected), impactPeaks(impactDetected), ...
    18, "filled");
ylabel("F impacto [N]");
grid on;

nexttile;
yyaxis left;
plot(camTorque.Time, camTorque.Data, LineWidth=0.9);
ylabel("T leva [N m]");
yyaxis right;
plot(rollerForce.Time, rollerForce.Data, LineWidth=0.9);
ylabel("F rodillo [N]");
xlabel("Tiempo [s]");
grid on;

title(layout, sprintf( ...
    "%s — %d vueltas a %.0f rpm, suelo compactable", ...
    resumen.product, p.simRevolutions, p.simulationRpm));

generatedDir = martinete_output_dir();
if ~isfolder(generatedDir)
    mkdir(generatedDir);
end
exportgraphics(figureHandle, fullfile(generatedDir, ...
    "resultados_multivuelta_piso.png"), Resolution=160);
save(fullfile(generatedDir, "resumen_multivuelta.mat"), ...
    "resumen", "referencias");
end
