"""post: verifica que el sdkconfig generado del entorno tenga lo esperado.

Si el rol, el pin o el modo de red no coinciden con el entorno, el build falla
antes de compilar (no se llega a flashear una imagen con otro perfil).
"""
import os
import re

Import("env")  # noqa: F821

pioenv = env.subst("$PIOENV")
role = env.GetProjectOption("custom_fts_role")
cfg = os.path.join(env.subst("$PROJECT_DIR"), "sdkconfig.%s" % pioenv)

values = {}
for line in open(cfg, encoding="utf-8"):
    line = line.strip()
    if line.startswith("CONFIG_") and "=" in line:
        k, v = line.split("=", 1)
        values[k] = v
    elif line.startswith("# CONFIG_") and line.endswith("is not set"):
        values[line.split()[1]] = "n"

expected = {
    "CONFIG_FTS_ROLE_MASTER": "y" if role == "master" else "n",
    "CONFIG_FTS_ROLE_SLAVE": "y" if role == "slave" else "n",
    "CONFIG_APP_PROJECT_VER": '"fts-pio-%s"' % pioenv,
    "CONFIG_FTS_MODE_INTERNAL_AP": "y",
    "CONFIG_FTS_MODE_USB_NCM": "n",
    "CONFIG_FTS_MQTT_ENABLED": "n",
    "CONFIG_FTS_PULSE_MCPWM_GPIO_ENABLE": "y",
    "CONFIG_FTS_PULSE_MCPWM_GPIO": "7",
    "CONFIG_FTS_LED_ENABLED": "y",
    "CONFIG_FTS_LED_GPIO": "48",
    "CONFIG_FTS_LED_WS2812": "y",
    "CONFIG_ESP_WIFI_FTM_ENABLE": "y",
    "CONFIG_ESPTOOLPY_FLASHSIZE_16MB": "y",
    "CONFIG_SPIRAM": "n",
    "CONFIG_ESP_CONSOLE_UART_DEFAULT": "y",
    "CONFIG_ESP_CONSOLE_UART_BAUDRATE": "115200",
}
# GPIO and LED settings remain editable in sdkconfig.defaults.
defaults = os.path.join(env.subst("$PROJECT_DIR"), "sdkconfig.defaults")
configurable = {
    "CONFIG_FTS_PULSE_MCPWM_GPIO", "CONFIG_FTS_LED_ENABLED",
    "CONFIG_FTS_LED_GPIO", "CONFIG_FTS_LED_WS2812",
}
for line in open(defaults, encoding="utf-8"):
    match = re.match(r"^(CONFIG_[A-Z0-9_]+)=(.*)$", line.strip())
    if match and match.group(1) in configurable:
        expected[match.group(1)] = match.group(2)
if expected["CONFIG_FTS_LED_ENABLED"] == "n":
    expected.pop("CONFIG_FTS_LED_GPIO", None)
    expected.pop("CONFIG_FTS_LED_WS2812", None)
bad = ["%s: esperado %s, hay %s" % (k, v, values.get(k, "<ausente>"))
       for k, v in expected.items() if values.get(k, "n") != v]
if bad:
    raise SystemExit("[fts-verify] %s: sdkconfig.%s no coincide:\n  %s"
                     % (pioenv, pioenv, "\n  ".join(bad)))
print("[fts-verify] %s: sdkconfig OK (rol=%s, GPIO/LED segun defaults, 16MB, sin PSRAM/MQTT/NCM)"
      % (pioenv, role))
