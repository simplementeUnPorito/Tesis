"""Registro de la telemetria del control del PSoC (via USB del ESP esclavo).

Uso:  py -3 ctl_log.py COM8 <segundos> <salida.txt> ["ctl report" ...]

Abre el puerto SIN tocar DTR/RTS (no resetea el ESP), manda los comandos
opcionales y escribe una fila por snapshot (clave 0x1ff):
  t_s up_s state prof band I0 I1 I2 I3 SEo BPo OPA SUMo LPo valid sum_age_ms
Tensiones en mV del dominio del ADC de control (ctl_dc), NO del tap fisico;
state: 0 falta aprender, 1 aprendiendo, 2 corriendo, 3 pausa, 4 fallo.
Lineas que empiezan con '#' son mensajes del ESP (p. ej. [CAL] ESTOY_EN_BANDA).
"""
import serial, sys, time, re
port=sys.argv[1]; secs=float(sys.argv[2]); out=sys.argv[3]
cmds=sys.argv[4:]
s=serial.Serial()
s.port=port; s.baudrate=115200; s.timeout=0.5; s.dtr=False; s.rts=False
s.open(); time.sleep(0.7); s.reset_input_buffer()
for c in cmds:
    s.write((c+'\n').encode()); time.sleep(0.3)
v={}; t0=time.time(); last=None
with open(out,'w',encoding='utf-8') as f:
    f.write('t_s up_s state prof band I0 I1 I2 I3 SEo BPo OPA SUMo LPo valid\n')
    while time.time()-t0<secs:
        line=s.readline().decode('utf-8','replace').strip()
        if not line: continue
        m=re.match(r'^#CTL 0 (\d+) (-?\d+)',line)
        if not m:
            if not line.startswith('#CTL'):
                f.write('# '+line+'\n'); f.flush()
            continue
        k=int(m.group(1)); val=int(m.group(2)); v[k]=val
        if k==511:
            dc=[v.get(0x120+4*i,0)//1000 for i in range(5)]
            vl=''.join(str(v.get(0x121+4*i,0)) for i in range(5))
            row=(v.get(256),v.get(257),v.get(258),v.get(272),v.get(273),v.get(274),v.get(275),*dc,vl,v.get(302))
            f.write(f"{time.time()-t0:7.1f} {v.get(261,0)/1000:8.1f} "+' '.join(str(x) for x in row)+'\n'); f.flush()
s.close()
