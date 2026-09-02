function outputDirectory = martinete_output_dir()
%MARTINETE_OUTPUT_DIR Devuelve la carpeta central de resultados ignorados.

modelDirectory = fileparts(mfilename("fullpath"));
repositoryRoot = fileparts(fileparts(fileparts(modelDirectory)));
outputDirectory = fullfile(repositoryRoot, "outputs", "modelado", ...
    "martinete_leva_multibody");
end
