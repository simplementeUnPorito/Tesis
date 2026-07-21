#!/bin/bash

# =================================================================
# SCRIPT DE TRABAJO AUTÓNOMO - TESIS (CLAUDE-CODE EDITION)
# =================================================================

# --- CONFIGURACIÓN DE TIEMPOS ---
START_TIME_STR="04:01"
END_TIME_STR="12:00"
LOG_FILE="sesion_nocturna_final.log"

# Convertir tiempos a segundos para comparación
START_TIME=$(date -d "$START_TIME_STR" +%s)
END_TIME=$(date -d "$END_TIME_STR" +%s)

echo "--- Script de Tesis Blindado Iniciado ($(date)) ---" | tee -a "$LOG_FILE"

# 1. LIMPIEZA INICIAL Y PERMISOS
echo "Limpiando bloqueos y preparando entorno..." | tee -a "$LOG_FILE"
rm -f .git/index.lock
pkill -f claude || true
chmod -R 777 . # Asegura que Claude pueda escribir en todo el repo

# 2. ESPERA HASTA LAS 04:01 AM (Reset de tokens)
current_time=$(date +%s)
if [ $current_time -lt $START_TIME ]; then
    seconds_to_wait=$((START_TIME - current_time))
    echo "Estado: En espera. Los tokens se resetean a las 4am." | tee -a "$LOG_FILE"
    echo "Faltan $((seconds_to_wait / 3600))h $(((seconds_to_wait % 3600) / 60))min para arrancar." | tee -a "$LOG_FILE"
    sleep $seconds_to_wait
fi

echo "=== [$(date)] ARRANCANDO RUTINA DE PRODUCCIÓN ===" | tee -a "$LOG_FILE"

# 3. BUCLE DE EJECUCIÓN HASTA LAS 12:00 PM
while [ $(date +%s) -lt $END_TIME ]; do
    echo "--------------------------------------------------------" >> "$LOG_FILE"
    echo "[$(date +%H:%M)] Iniciando ciclo de trabajo..." | tee -a "$LOG_FILE"

    # Definimos el Mega-Prompt con las instrucciones de cierre
    PROMPT_CLAUDE="Urgente: Lee 'historial.txt' y 'prompt_instrucciones.txt'. 
    Tu objetivo es que el sistema de comparación de filtros (TIA vs Opa) en PSoC funcione y que el programa de Python muestre el osciloscopio con las 3 señales (cruda, filtrada analógica, filtrada digital).
    REGLAS ESTRICTAS:
    1. Implementa transparencia USB/UART (responder por donde entre el comando).
    2. Si detectas UART, permite cambio de baudios.
    3. Asegura que los DMAs del PSoC no saturen el buffer.
    4. REGLA DE CIERRE: Cuando consideres que el sistema es estable o si la hora se acerca a las 11:55 AM, haz un COMMIT con mensaje 'Mejoras automáticas Claude' y haz PUSH a origin main obligatoriamente."

    # EJECUCIÓN NO INTERACTIVA (Banderas oficiales)
    # -p: Salida no interactiva (impresión directa)
    # --dangerously-skip-permissions: Ignora pedidos de confirmación de escritura
    claude -p "$PROMPT_CLAUDE" --dangerously-skip-permissions >> "$LOG_FILE" 2>&1

    # Verificación de salida
    if [ $? -eq 0 ]; then
        echo "Ciclo completado con éxito." | tee -a "$LOG_FILE"
    else
        echo "Aviso: Ciclo con errores o límite de tokens alcanzado. Reintentando en 2 minutos..." | tee -a "$LOG_FILE"
        sleep 120
    fi

    # Limpieza de seguridad post-ciclo
    rm -f .git/index.lock
    
    echo "Esperando 60 segundos para el siguiente ciclo de revisión..."
    sleep 60
done

# 4. CIERRE DE SEGURIDAD (Backup final manual)
echo "=== Límite de tiempo alcanzado (12:00 PM). Verificando Git final ===" | tee -a "$LOG_FILE"
git add .
git commit -m "Backup final de emergencia - Fin de sesión Claude" || echo "Nada nuevo que subir"
git push origin main || echo "Error crítico al subir a GitHub"

echo "--- Fin de la jornada nocturna. Revisa $LOG_FILE para ver el progreso. ---" | tee -a "$LOG_FILE"
