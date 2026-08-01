function resultados = calcular_referencias(p, perfil, rpm)
%CALCULAR_REFERENCIAS Calcula la referencia analitica balistica y de carga.

arguments
    p (1, 1) struct
    perfil (1, 1) struct
    rpm (:, 1) double {mustBePositive} = p.nominalRpm
end

rpm = rpm(:);
count = numel(rpm);
omegaCam = 2 * pi * rpm / 60;
kRel = 2 * (p.thetaRel - p.theta0) / p.dphiRise;
omegaRelease = kRel .* omegaCam;
sinApex = sin(p.thetaRel) + p.Jpivot .* omegaRelease.^2 / (2 * p.K);
thetaApex = asin(min(sinApex, 1));

fallTime = nan(count, 1);
releaseToImpactTime = nan(count, 1);
impactEnergy = nan(count, 1);
impactSpeed = nan(count, 1);
timeMargin = nan(count, 1);
fullCycleMargin = nan(count, 1);
peakCamTorque = nan(count, 1);
meanCamTorque = nan(count, 1);
peakRollerForce = nan(count, 1);

riseRows = perfil.riseMask;
thetaRise = deg2rad(perfil.table.theta_deg(riseRows));
muRise = deg2rad(perfil.table.mu_deg(riseRows));
s = perfil.table.phi_deg(riseRows) / rad2deg(p.dphiRise);
kProfile = kRel .* s;

for idx = 1:count
    if sinApex(idx) >= 1
        continue
    end

    options = odeset(RelTol=1e-9, AbsTol=1e-11, ...
        Events=@(t, state) impactEvent(t, state, p.theta0));
    [tFall, ~] = ode45(@(~, state) [state(2); ...
        -(p.K / p.Jpivot) * cos(state(1))], ...
        [0, 2], [thetaApex(idx); 0], options);
    fallTime(idx) = tFall(end);

    [tFullCycle, ~] = ode45(@(~, state) [state(2); ...
        -(p.K / p.Jpivot) * cos(state(1))], ...
        [0, 2], [p.thetaRel; omegaRelease(idx)], options);
    releaseToImpactTime(idx) = tFullCycle(end);

    impactEnergy(idx) = p.K * (sin(thetaApex(idx)) - sin(p.theta0));
    impactOmega = sqrt(2 * impactEnergy(idx) / p.Jpivot);
    impactSpeed(idx) = impactOmega * p.Lh;
    sectorTime = (2 * pi - p.dphiRise) / (2 * pi) * 60 / rpm(idx);
    timeMargin(idx) = sectorTime / fallTime(idx) - 1;
    fullCycleMargin(idx) = sectorTime / releaseToImpactTime(idx) - 1;

    alphaCam = 2 * (p.thetaRel - p.theta0) / p.dphiRise^2 * ...
        omegaCam(idx)^2;
    hammerTorque = p.K * cos(thetaRise) + p.Jpivot * alphaCam;
    camTorque = hammerTorque .* kProfile;
    rollerForce = hammerTorque / p.Hp ./ cos(muRise);
    peakCamTorque(idx) = max(camTorque);
    meanCamTorque(idx) = trapz(s, camTorque);
    peakRollerForce(idx) = max(rollerForce);
end

resultados = table(rpm, omegaCam, repmat(kRel, count, 1), ...
    omegaRelease, thetaApex, impactEnergy, impactSpeed, fallTime, ...
    releaseToImpactTime, timeMargin, fullCycleMargin, peakCamTorque, ...
    meanCamTorque, peakRollerForce, ...
    VariableNames=["rpm", "omegaCam_rad_s", "kRel", ...
    "omegaRelease_rad_s", "thetaApex_rad", "impactEnergy_J", ...
    "impactSpeed_m_s", "fallTime_s", "releaseToImpactTime_s", ...
    "timeMargin", "fullCycleMargin", "peakCamTorque_Nm", ...
    "meanCamTorque_Nm", "peakRollerForce_N"]);
end

function [value, isTerminal, direction] = impactEvent(~, state, theta0)
value = state(1) - theta0;
isTerminal = 1;
direction = -1;
end
