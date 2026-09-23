"""Vuelca la traza cruda de LPo del PSoC (`ctl get 255`) y la decodifica.

Uso:  py -3 ctl_trace.py COM8 ["ctl set 24 20000" "ctl apply" ...]

El firmware guarda las ultimas 127 lecturas de LPo (promedios de ~20 ms,
SIN mediana ni ventana de silencio) con su tiempo. Imprime `ms  mV` y marca
las muestras a menos de 25 ms del inicio del ultimo reporte de telemetria.
Sirvio para probar que cada rafaga I2C al ESP golpea LPo (2026-09-16).
Codificacion por muestra: (dt_ms<<20) | (mV*100 en 20 bits con signo).
"""
import serial, sys, time, re
port=sys.argv[1]; pre=sys.argv[2:]
s=serial.Serial(); s.port=port; s.baudrate=115200; s.timeout=0.3; s.dtr=False; s.rts=False
s.open(); time.sleep(0.7); s.reset_input_buffer()
for c in pre: s.write((c+'\n').encode()); time.sleep(0.4)
time.sleep(3.0); s.reset_input_buffer()
s.write(b'ctl get 255\n')
v={}; t0=time.time()
while time.time()-t0<4:
    l=s.readline().decode('utf-8','replace').strip()
    m=re.match(r'#CTL 0 (\d+) (-?\d+)',l)
    if m:
        k=int(m.group(1))
        if 0x17D<=k<=0x1FE: v[k]=int(m.group(2))
s.close()
rs,rl,last=v.get(0x17D),v.get(0x17E),v.get(0x17F)
n=max([k-0x180 for k in v if k>=0x180],default=-1)+1
# rebuild times backwards from last
rows=[]
for i in range(n):
    x=v[0x180+i]&0xFFFFFFFF
    dt=x>>20; mv=x&0xFFFFF
    if mv&0x80000: mv-=0x100000
    rows.append([dt,mv/100.0])
tt=[0]*n
for i in range(1,n): tt[i]=tt[i-1]+rows[i][0]
off=last-tt[-1]
print('report_start',rs,'last_report_end',rl,'n',n)
for i in range(n):
    t=tt[i]+off
    mark=' <report' if rs is not None and abs(t-rs)<25 else ''
    print(f'{t:10d} {rows[i][1]:8.2f}{mark}')
