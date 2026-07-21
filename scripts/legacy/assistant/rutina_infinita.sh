#!/bin/bash

LOG_FILE="trabajo_infinito.log"
echo "--- Iniciando Bucle de Producción Nocturna (Hasta que el jefe despierte) ---" > $LOG_FILE

# Entrar al entorno correcto por las dudas
source src/python/geophone_scope/venv/bin/activate 2>/dev/null

iteracion=1

while true; do
    echo "=================================================" >> $LOG_FILE
    echo "🕒 [$(date)] Iniciando Iteración #$iteracion" >> $LOG_FILE
    
    # Aquí llamamos a Claude. Asumo que usas un CLI similar a 'claude' o 'aider'. 
    # Le pasamos el archivo de instrucciones y le decimos que corra libre.
    cat prompt_instrucciones.txt | claude --dangerously-skip-permissions >> $LOG_FILE 2>&1
    
    echo "✅ [$(date)] Iteración #$iteracion terminada. Guardando progreso..." >> $LOG_FILE
    
    # Auto-guardado en Git para que no pierdas nada de lo que hace en cada ciclo
    git add .
    git commit -m "Auto-iteración nocturna #$iteracion: Ajustes de simulación y código" || echo "No hay cambios para commitear"
    git push origin main
    
    echo "💤 Pausando 5 minutos para enfriar la API y evitar bloqueos de tokens..." >> $LOG_FILE
    sleep 300
    
    iteracion=$((iteracion+1))
done
