"""pre: evita que un entorno reutilice un sdkconfig viejo.

ESP-IDF solo aplica los *.defaults a opciones que todavia no estan en el
sdkconfig generado. Si se edita un defaults (o se cambia el rol de un entorno),
un sdkconfig.<entorno> antiguo seguiria mandando. Se guarda un sello con el
hash de los defaults usados; si cambia, se borra el sdkconfig del entorno.
"""
import hashlib
import os
import re
import shutil

Import("env")  # noqa: F821

project = env.subst("$PROJECT_DIR")
pioenv = env.subst("$PIOENV")
args = env.GetProjectOption("board_build.cmake_extra_args", "")
m = re.search(r'-DSDKCONFIG_DEFAULTS="([^"]+)"', args)
if not m:
    raise SystemExit("[fts-guard] %s: falta -DSDKCONFIG_DEFAULTS" % pioenv)
files = m.group(1).split(";")

h = hashlib.sha256(m.group(1).encode())
for f in files:
    path = os.path.join(project, f)
    if not os.path.isfile(path):
        raise SystemExit("[fts-guard] %s: no existe %s" % (pioenv, f))
    h.update(open(path, "rb").read())
digest = h.hexdigest()

stamp = os.path.join(project, "sdkconfig.%s.stamp" % pioenv)
cfg = os.path.join(project, "sdkconfig.%s" % pioenv)
old = open(stamp).read().strip() if os.path.isfile(stamp) else None
if old != digest:
    if os.path.isfile(cfg):
        os.remove(cfg)
        print("[fts-guard] %s: defaults cambiaron, se regenera sdkconfig.%s"
              % (pioenv, pioenv))
    build = os.path.realpath(env.subst("$BUILD_DIR"))
    expected_build = os.path.realpath(os.path.join(project, ".pio", "build", pioenv))
    if os.path.normcase(build) != os.path.normcase(expected_build):
        raise SystemExit("[fts-guard] unexpected build directory: %s" % build)
    if os.path.isdir(build):
        shutil.rmtree(build, ignore_errors=True)
    with open(stamp, "w") as fp:
        fp.write(digest + "\n")
