function carpeta = dir_salida(varargin)
%DIR_SALIDA Carpeta comun para los artefactos generados del proyecto.
%   CARPETA = DIR_SALIDA(PARTE1, ...) crea y devuelve, como char,
%   <raiz>/outputs/PARTE1/... . DIR_SALIDA(..., 'entregable', true) usa
%   <raiz>/docs/... para entregables versionables.
%
%   Convencion: outputs/ contiene todo resultado interno o intermedio y
%   docs/ contiene solamente entregables de tesis. El codigo nunca debe
%   escribir resultados junto a sus fuentes. La raiz se reconoce por
%   .gitmodules; si el submodulo se clono solo, todo cae en outputs/ local,
%   incluso cuando se solicito 'entregable', true.

entregable = false;
if numel(varargin) >= 2 && (ischar(varargin{end-1}) || isstring(varargin{end-1})) ...
        && strcmpi(char(varargin{end-1}), 'entregable')
    entregable = logical(varargin{end});
    varargin(end-1:end) = [];
end

inicios = {pwd, fileparts(mfilename('fullpath'))};
pila = dbstack('-completenames');
if numel(pila) >= 2
    inicios = [{fileparts(pila(2).file)}, inicios];
end

raiz = buscar_marcador(inicios, '.gitmodules');
aislado = isempty(raiz);
if isempty(raiz)
    raiz = buscar_marcador(inicios, '.git');
end
if isempty(raiz)
    raiz = pwd;
end

partes = cellfun(@char, varargin, 'UniformOutput', false);
if entregable && ~aislado
    carpeta = fullfile(raiz, 'docs', partes{:});
else
    carpeta = fullfile(raiz, 'outputs', partes{:});
end
if ~isfolder(carpeta)
    mkdir(carpeta);
end
end


function raiz = buscar_marcador(inicios, marcador)
raiz = '';
for k = 1:numel(inicios)
    actual = char(inicios{k});
    while ~isempty(actual)
        candidato = fullfile(actual, marcador);
        if isfile(candidato) || isfolder(candidato)
            raiz = actual;
            return;
        end
        anterior = actual;
        actual = fileparts(actual);
        if strcmp(actual, anterior)
            break;
        end
    end
end
end
