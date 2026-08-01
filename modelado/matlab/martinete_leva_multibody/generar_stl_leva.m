function stlPath = generar_stl_leva(perfil, p, stlPath)
%GENERAR_STL_LEVA Extruye el perfil CSV para visualizarlo en Multibody.

arguments
    perfil (1, 1) struct
    p (1, 1) struct
    stlPath (1, 1) string = fullfile(fileparts(mfilename("fullpath")), ...
        "generated", "leva_balistica_12lb.stl")
end

outputDir = fileparts(stlPath);
if ~isfolder(outputDir)
    mkdir(outputDir);
end

polygon = polyshape(perfil.xy_m(:, 1), perfil.xy_m(:, 2), ...
    Simplify=true, KeepCollinearPoints=true);
if polygon.NumRegions ~= 1
    error("Martinete:PerfilNoSimple", ...
        "El perfil de leva debe formar una sola region cerrada.");
end

tri2d = triangulation(polygon);
xy = tri2d.Points;
faces2d = tri2d.ConnectivityList;
count = size(xy, 1);
zHalf = p.camThickness / 2;
vertices = [xy, -zHalf * ones(count, 1); ...
    xy, zHalf * ones(count, 1)];

bottom = fliplr(faces2d);
top = faces2d + count;

boundary = freeBoundary(tri2d);
side = zeros(2 * size(boundary, 1), 3);
for k = 1:size(boundary, 1)
    i = boundary(k, 1);
    j = boundary(k, 2);
    side(2 * k - 1, :) = [i, j, j + count];
    side(2 * k, :) = [i, j + count, i + count];
end

mesh = triangulation([bottom; top; side], vertices);
stlwrite(mesh, stlPath, "binary");
end
