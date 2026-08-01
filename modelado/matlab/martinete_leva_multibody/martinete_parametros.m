function [p, perfil] = martinete_parametros(csvPath)
%MARTINETE_PARAMETROS Parametros y perfil del martinete de leva de 12 lb.
%
%   [P, PERFIL] = MARTINETE_PARAMETROS() carga el CSV de la leva balistica
%   respecto de la ubicacion de este archivo. Las longitudes de P se
%   expresan en metros, los angulos en radianes y las magnitudes dinamicas
%   en unidades SI.

arguments
    csvPath (1, 1) string = defaultCsvPath()
end

if ~isfile(csvPath)
    error("Martinete:CsvNoEncontrado", ...
        "No se encontro el perfil de leva: %s", csvPath);
end

datos = readtable(csvPath, TextType="string");
required = ["sector", "phi_deg", "theta_deg", "gamma_deg", ...
    "rho_paso_mm", "x_perfil_mm", "y_perfil_mm", ...
    "radio_perfil_mm", "mu_deg"];
missing = setdiff(required, string(datos.Properties.VariableNames));
if ~isempty(missing)
    error("Martinete:CsvInvalido", ...
        "Faltan columnas requeridas en el CSV: %s", join(missing, ", "));
end

% Geometria congelada.
p.Lh = 0.850;
p.Hp = 0.215;
p.beta = deg2rad(127.5);
p.Lt = 0.0;
p.Ht = 0.220;
p.rollerRadius = 0.020;
p.theta0 = deg2rad(-16.0);
p.thetaRel = deg2rad(16.0);
p.thetaMin = deg2rad(-30.0);
p.thetaMax = deg2rad(45.0);
p.mechanismTilt = -p.theta0;
p.worldTheta0 = p.theta0 + p.mechanismTilt;
p.worldThetaRel = p.thetaRel + p.mechanismTilt;
p.dphiRise = deg2rad(180.0);
p.clearance = 0.008;
p.pickupBlendAngle = deg2rad(90.0);
p.pickupJoinRiseAngle = deg2rad(5.0);
p.pickupBlendPoints = 181;
p.camThickness = 0.018;
p.camAxialOffset = 0.060;
p.rollerThickness = 0.014;

% Maza comercial TOTAL THSM61598. El catalogo publica 12 lb para la
% cabeza, acero al carbono 45# forjado/tratado y mango de fibra de vidrio
% de 900 mm. La masa del mango no esta publicada: 0.80 kg es un supuesto
% de ingenieria que puede sustituirse por una medicion del ejemplar real.
p.productManufacturer = "TOTAL";
p.productReference = "THSM61598";
p.headRatedMass_lb = 12.0;
p.headMass = p.headRatedMass_lb * 0.45359237;
p.headMaterial = "45# carbon steel, drop-forged and heat-treated";
p.handleMaterial = "fiberglass";
p.handleLength = 0.900;
p.handleMassAssumed = true;
p.handleMass = 0.80;

% Reparto de la masa no publicada del conjunto de mango. Los cuatro
% componentes suman exactamente p.handleMass, de modo que no se duplica
% masa al convertir los solidos graficos en cuerpos rigidos reales.
p.handleShaftMass = 0.58;
p.bellCrankMass = 0.12;
p.rollerMass = 0.06;
p.rollerAxleMass = 0.04;
if abs(p.handleShaftMass + p.bellCrankMass + p.rollerMass + ...
        p.rollerAxleMass - p.handleMass) > 1e-12
    error("Martinete:RepartoMasaInvalido", ...
        "Las masas del conjunto de mango deben sumar p.handleMass.");
end

% Modelo concentrado: cabeza puntual en Lh y mango uniforme desde el
% pivote. Mantiene la inercia fisica independiente de la geometria visual.
p.mass = p.headMass + p.handleMass;
p.Lcg = (p.headMass * p.Lh + ...
    p.handleMass * p.handleLength / 2) / p.mass;
p.Jpivot = p.headMass * p.Lh^2 + ...
    p.handleMass * p.handleLength^2 / 3;
p.g = 9.80665;
p.K = p.mass * p.g * p.Lcg;
p.IzzCg = p.Jpivot - p.mass * p.Lcg^2;
if p.IzzCg <= 0
    error("Martinete:InerciaInvalida", ...
        "La inercia en el centro de gravedad debe ser positiva.");
end
p.inertiaCg = [0.020, p.IzzCg, p.IzzCg];

% Operacion y contacto.
p.nominalRpm = 65.0;
p.maxRpm = 65.0;
p.simulationRpm = 25.0;
p.simRevolutions = 8;
p.contactStiffness = 5.0e6;
p.contactDamping = 2.0e3;
p.contactTransition = 1.0e-4;
p.camLeverContactStiffness = 2.0e8;
p.camLeverContactDamping = 4.0e4;
p.camLeverContactTransition = 1.0e-5;
p.hardStopStiffness = 2.0e6;
p.hardStopDamping = 1.0e3;
p.restitution = 0.10;
p.stopTime = p.simRevolutions * 60 / p.simulationRpm;
p.maxStep = 2.0e-4;

% Geometria medida de la cabeza: cilindro de 185 mm de largo y 75 mm de
% diametro. En el contacto planar se usa su radio como huella equivalente.
p.headLength = 0.185;
p.headDiameter = 0.075;
p.headContactRadius = 0.005;
p.headContactOffset = p.headLength / 2 - p.headContactRadius;

% Piso geofisico. La cara inferior de la cabeza y la superficie del piso
% comienzan exactamente en y=0; el hundimiento posterior surge de impactos.
p.pivotHeight = p.headLength / 2;
p.camCenterWorldX = cos(p.mechanismTilt) * p.Lt - ...
    sin(p.mechanismTilt) * p.Ht;
p.camCenterWorldY = sin(p.mechanismTilt) * p.Lt + ...
    cos(p.mechanismTilt) * p.Ht;
p.groundInitialY = 0.0;
p.groundMaxSink = 0.100;
p.groundLength = 2.0;
p.groundThickness = 0.050;
p.groundDepth = 0.300;
p.groundContactStiffness = 1.0e8;
p.groundContactDamping = 2.0e4;
p.groundContactTransition = 2.0e-5;

% Ley fenomenologica de compactacion irreversible:
%   y_piso_dot = -ganancia * max(F_impacto - F_fluencia, 0)
% El filtro evita que el chatter numerico de contacto active la ley.
p.soilYieldForce = 2.0e3;
p.soilCompactionGain = 5.0e-4;
p.soilForceFilterTau = 2.0e-3;
p.openCamReturn = true;

% Geometria rigida real. La leva y el rodillo trabajan en un plano axial
% separado del mango; un eje material une el rodillo con la palanca gris.
% El extremo de la palanca llega solo hasta la tangencia del rodillo, por
% lo que ya no invade el volumen barrido por la leva.
p.visualMass = 1.0e-6;
p.handleGraphicLength = p.handleLength;
p.handleGraphicWidth = 0.030;
p.handleGraphicDepth = 0.030;
p.headGraphicDimensionsAssumed = false;
p.bellCrankLength = p.Hp - p.rollerRadius;
p.bellCrankWidth = 0.024;
p.bellCrankDepth = 0.024;
p.rollerAxleRadius = 0.008;
p.rollerAxleLength = p.camAxialOffset + ...
    max(p.bellCrankDepth, p.rollerThickness) / 2;
p.rollerAxleCenterZ = p.camAxialOffset / 2;
p.camLeverAxialClearance = p.camAxialOffset - ...
    (p.camThickness + p.bellCrankDepth) / 2;
if p.camLeverAxialClearance <= 0
    error("Martinete:InterferenciaAxial", ...
        "La leva y la palanca gris se intersectan en direccion axial.");
end

% Perfil en el sistema solidario a la leva. El CSV se conserva como
% referencia y se reemplaza solamente el cierre radial de 8 mm por una
% transicion de toma C2 sobre los ultimos 90 grados del circulo base y los
% primeros 5 grados de subida. Extender el empalme elimina el sobrepaso y
% garantiza un radio estrictamente monotono.
perfil.table = datos;
perfil.xy_original_m = [datos.x_perfil_mm, datos.y_perfil_mm] * 1e-3;
perfil.riseMask = datos.sector == "subida";
perfil.fallMask = datos.sector == "caida";
perfil.rise_xy_original_m = perfil.xy_original_m(perfil.riseMask, :);
perfil.fall_xy_original_m = perfil.xy_original_m(perfil.fallMask, :);
[perfil.pickup_xy_m, perfil.fall_xy_m, perfil.rise_xy_m, ...
    pickupMetrics] = smoothPickupTransition( ...
    perfil.rise_xy_original_m, perfil.fall_xy_original_m, ...
    deg2rad(datos.phi_deg(perfil.riseMask)), p);
perfil.xy_m = [perfil.rise_xy_m; perfil.fall_xy_m; ...
    perfil.pickup_xy_m(1:(end - 1), :)];
if p.openCamReturn
    % La cara de retorno queda en el solido visual, pero no en la nube de
    % contacto, salvo la transicion C2 de toma. Esto evita que el circulo
    % base limite el descenso cuando el terreno se hunde.
    perfil.contact_xy_m = densifyPolyline([ ...
        perfil.pickup_xy_m; perfil.rise_xy_m(2:end, :)], 8.0e-4);
else
    perfil.contact_xy_m = densifyPolyline(perfil.xy_m, 8.0e-4);
end
% Envolvente cerrada y densa usada exclusivamente para impedir que el
% solido completo de la leva atraviese la palanca gris. A diferencia del
% contacto funcional leva-rodillo, aqui tambien se incluye la cara de
% retorno.
collisionXY = densifyPolyline([ ...
    perfil.xy_m; perfil.xy_m(1, :)], 1.0e-3);
collisionXY = unique(collisionXY, "rows", "stable");
collisionCount = size(collisionXY, 1);
perfil.collision_xyz_m = [ ...
    collisionXY, -p.camThickness / 2 * ones(collisionCount, 1); ...
    collisionXY, +p.camThickness / 2 * ones(collisionCount, 1)];

% Metricas geometricas usadas por la validacion.
rise = perfil.riseMask;
fall = perfil.fallMask;
perfil.metrics.rhoMinPitch_m = min(datos.rho_paso_mm(rise)) * 1e-3;
perfil.metrics.rhoMaxPitch_m = max(datos.rho_paso_mm(rise)) * 1e-3;
perfil.metrics.baseRadius_m = mean(datos.radio_perfil_mm(fall)) * 1e-3;
perfil.metrics.maxRadius_m = max(datos.radio_perfil_mm) * 1e-3;
perfil.metrics.maxPressureAngle_rad = deg2rad(max(abs(datos.mu_deg(rise))));
perfil.metrics.baseRadiusStd_m = std(datos.radio_perfil_mm(fall)) * 1e-3;
perfil.metrics.pitchRatio = perfil.metrics.rhoMaxPitch_m / ...
    perfil.metrics.rhoMinPitch_m;
perfil.metrics.pickupBlendAngle_rad = p.pickupBlendAngle;
perfil.metrics.pickupJoinRiseAngle_rad = p.pickupJoinRiseAngle;
perfil.metrics.pickupTakePolarAngle_rad = ...
    pickupMetrics.takePolarAngle_rad;
perfil.metrics.pickupJoinPolarAngle_rad = ...
    pickupMetrics.joinPolarAngle_rad;
perfil.metrics.pickupRadiusStart_m = pickupMetrics.radiusStart_m;
perfil.metrics.pickupRadiusEnd_m = pickupMetrics.radiusEnd_m;
perfil.metrics.pickupMaxRadialSlope_m_rad = ...
    pickupMetrics.maxRadialSlope_m_rad;
perfil.metrics.pickupPositionError_m = pickupMetrics.positionError_m;
perfil.metrics.pickupSlopeError_m_rad = pickupMetrics.slopeError_m_rad;
perfil.metrics.pickupCurvatureError_m_rad2 = ...
    pickupMetrics.curvatureError_m_rad2;
end

function [pickup, fallTrimmed, riseTrimmed, metrics] = ...
    smoothPickupTransition(rise, fall, risePhi, p)
%SMOOTHPICKUPTRANSITION Sustituye el escalon de toma por un empalme C2.

riseAngle = unwrap(atan2(rise(:, 2), rise(:, 1)));
riseRadius = vecnorm(rise, 2, 2);
fallAngle = unwrap(atan2(fall(:, 2), fall(:, 1)));
fallRadius = vecnorm(fall, 2, 2);

[~, joinIndex] = min(abs(risePhi - p.pickupJoinRiseAngle));
fitIndices = max(1, joinIndex - 4):min(size(rise, 1), joinIndex + 4);
localAngle = riseAngle(fitIndices) - riseAngle(joinIndex);
fitCoefficients = polyfit(localAngle, riseRadius(fitIndices), 3);
radialSlopeEnd = fitCoefficients(3);
radialCurvatureEnd = 2 * fitCoefficients(2);

angleEnd = riseAngle(joinIndex);
angleStart = riseAngle(1) + p.pickupBlendAngle;
angleSpan = angleEnd - angleStart;
radiusStart = median(fallRadius);
radiusEnd = riseRadius(joinIndex);

radialSlopeUend = radialSlopeEnd * angleSpan;
radialCurvatureUend = radialCurvatureEnd * angleSpan^2;
systemMatrix = [1, 1, 1; 3, 4, 5; 6, 12, 20];
rightHandSide = [ ...
    radiusEnd - radiusStart; ...
    radialSlopeUend; ...
    radialCurvatureUend];
highOrderCoefficients = systemMatrix \ rightHandSide;

u = linspace(0, 1, p.pickupBlendPoints)';
radius = radiusStart + ...
    highOrderCoefficients(1) * u.^3 + ...
    highOrderCoefficients(2) * u.^4 + ...
    highOrderCoefficients(3) * u.^5;
angle = angleStart + angleSpan * u;
pickup = radius .* [cos(angle), sin(angle)];

fallTrimmed = fall(fallAngle > angleStart, :);
riseTrimmed = rise(joinIndex:end, :);
radialSlope = gradient(radius, angle);
metrics.radiusStart_m = radiusStart;
metrics.radiusEnd_m = radiusEnd;
metrics.maxRadialSlope_m_rad = max(abs(radialSlope));
metrics.positionError_m = norm(pickup(end, :) - riseTrimmed(1, :));
metrics.takePolarAngle_rad = riseAngle(1);
metrics.joinPolarAngle_rad = angleEnd;
metrics.slopeError_m_rad = abs( ...
    (3 * highOrderCoefficients(1) + ...
    4 * highOrderCoefficients(2) + ...
    5 * highOrderCoefficients(3)) / angleSpan - radialSlopeEnd);
metrics.curvatureError_m_rad2 = abs( ...
    (6 * highOrderCoefficients(1) + ...
    12 * highOrderCoefficients(2) + ...
    20 * highOrderCoefficients(3)) / angleSpan^2 - ...
    radialCurvatureEnd);

if any(diff(radius) < -1e-12)
    error("Martinete:TransicionTomaNoMonotona", ...
        "La transicion C2 de toma debe crecer monotonamente.");
end
end

function dense = densifyPolyline(points, maxSpacing)
%DENSIFYPOLYLINE Densifica un tramo sin cruzar discontinuidades radiales.

if size(points, 1) < 2
    dense = points;
    return
end

segmentLength = vecnorm(diff(points, 1, 1), 2, 2);
pieces = cell(size(segmentLength));
for k = 1:numel(segmentLength)
    count = max(1, ceil(segmentLength(k) / maxSpacing));
    alpha = (0:(count - 1))' / count;
    pieces{k} = points(k, :) + alpha .* (points(k + 1, :) - points(k, :));
end
dense = [vertcat(pieces{:}); points(end, :)];
end

function csvPath = defaultCsvPath()
thisDir = fileparts(mfilename("fullpath"));
repoRoot = fileparts(fileparts(fileparts(thisDir)));
csvPath = fullfile(repoRoot, "Assets", "excel", ...
    "perfil_leva_balistica_12lb.csv");
end
