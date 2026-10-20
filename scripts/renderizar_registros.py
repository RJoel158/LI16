"""Renderiza registros auténticos como imágenes; no simula capturas de pantalla."""
from pathlib import Path
from datetime import datetime
import json,textwrap,math
from PIL import Image,ImageDraw,ImageFont
from contenido_informe import POINTS

root=Path(__file__).resolve().parents[1]
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',25)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
bold=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',29)
def wrap(s,width=99):
 result=[]
 for line in s.splitlines():result.extend(textwrap.wrap(line,width=width,replace_whitespace=False,drop_whitespace=False) or [''])
 return result
def clean(s):
 return [l.rstrip() for l in s.splitlines() if l.strip() and not l.startswith(('SLF4J:','[WARN] Failed to create directory:','No such file or directory'))]
manifest=[]
for old in (root/'evidencias').glob('*-registro-*.png'):old.unlink()
for key,title,_ in POINTS:
 file=root/'registros'/f'{key}.json'
 if not file.exists():continue
 rec=json.loads(file.read_text(encoding='utf-8-sig'));assert rec['exit_code']==0,(key,rec['exit_code'])
 output=clean(rec['salida']);sections=[]
 query=root/'proyecto/sql'/f'{key}.sql'
 sql=query.read_text(encoding='utf-8') if query.exists() else ''
 if key=='05':
  output=output[:5]+[l for l in output[5:] if l.strip().startswith(('Live datanodes','Hostname:','Num of Blocks:','Missing blocks:','Blocks with corrupt replicas:'))]
  output.insert(0,'Extracto del registro; reporte completo conservado en JSON.')
 if key=='11':
  meta,_=json.JSONDecoder().raw_decode(rec['salida'].lstrip())
  output=['Resumen del registro; salida completa conservada en JSON.',f'Filas: {meta["filas"]}',f'Usuarios únicos: {meta["usuarios_unicos"]}','Columnas: '+', '.join(meta['columnas']),'SHA256 original: '+meta['sha256_original'],'SHA256 preparado: '+meta['sha256_sin_encabezado'],'Archivo: '+meta['archivo_preparado']]+[l for l in output if l.startswith('Primera fila')]
 if key=='15d':
  output=['Extracto pertinente; DESCRIBE completo conservado en JSON.']+[l for l in output if l.lstrip().startswith(('Database:','Owner:','Location:','Table Type:','SerDe Library:','InputFormat:','OutputFormat:','serialization.null.format'))]
 if key=='15e':
  verify=json.loads((root/'registros/15e-verificacion.json').read_text(encoding='utf-8-sig'))
  output=['LOAD DATA finalizó con código de salida 0.','', 'Verificación posterior: '+verify['fecha'],verify['comando']]+clean(verify['salida'])
 elif not output:output=['Sin salida estándar. Código de salida registrado: 0.']
 if key=='15f':
  cells=[l.split('\t') for l in output]
  for a,b in [(0,8),(8,15)]:
   block=[row[a:b] for row in cells]
   headers=[h.replace('fb_ronald.','') for h in block[0]]
   header_lines=[textwrap.wrap(h,13) for h in headers]
   widths=[max(len(h) for h in hs) for hs in header_lines]
   widths=[max(w,max(len(row[i]) for row in block[1:])) for i,w in enumerate(widths)]
   header=[' | '.join((hs[n] if n<len(hs) else '').ljust(widths[i]) for i,hs in enumerate(header_lines)) for n in range(max(map(len,header_lines)))]
   lines=header+['-+-'.join('-'*w for w in widths)]+[' | '.join(c.ljust(widths[i]) for i,c in enumerate(row)) for row in block[1:]]
   sections.append((f'Columnas {a+1} a {b} del mismo SELECT',lines))
 elif output and '\t' in output[0] and key!='15d':
  cells=[l.split('\t') for l in output]
  if len(cells)==2:
   lines=[f'{h}: {v}' for h,v in zip(cells[0],cells[1])]
  else:
   n=len(cells[0]);cells=[row+['']*(n-len(row)) for row in cells]
   widths=[max(len(row[i]) for row in cells) for i in range(n)]
   lines=[' | '.join(v.ljust(widths[i]) for i,v in enumerate(row)) for row in cells]
  sections.append(('Resultado',lines))
 else:sections.append(('Salida registrada',output))
 prefix=['Comando ejecutado']+wrap(rec['comando'])+['']
 if sql and key!='15c':prefix+=['SQL ejecutado']+wrap(sql)+['']
 if key=='15f':
  chunks=[prefix+[label]+wrap('\n'.join(lines)) for label,lines in sections]
 else:
  full=prefix
  for label,lines in sections:full+=[label]+wrap('\n'.join(lines))+['']
  chunks=[full[i:i+30] for i in range(0,len(full),30)]
 for index,chunk in enumerate(chunks,1):
  w=1600;h=360+36*len(chunk)
  im=Image.new('RGB',(w,h),'white');draw=ImageDraw.Draw(im)
  draw.text((45,25),'LI16  EVIDENCIA DE UN REGISTRO REAL',font=bold,fill='#111111')
  draw.text((45,70),'Registro renderizado · No es una captura de terminal',font=small,fill='#333333')
  draw.text((45,110),f'Punto {title}   |   Parte {index} de {len(chunks)}',font=small,fill='#111111')
  draw.text((45,150),'Hora del sistema al ejecutar: '+rec['fecha'],font=small,fill='#111111')
  draw.text((45,188),f'Código de salida: {rec["exit_code"]}   |   Fuente: registros/{key}.json',font=small,fill='#111111')
  draw.line((45,230,w-45,230),fill='#888888',width=2)
  for n,line in enumerate(chunk):draw.text((45,252+n*36),line,font=font,fill='#111111')
  draw.text((45,h-58),'Advertencias de logging omitidas en esta vista; salida íntegra conservada en JSON.',font=small,fill='#444444')
  path=root/'evidencias'/f'{key}-registro-{index}.png';im.save(path)
  manifest.append({'punto':key,'archivo':path.name,'tipo':'registro_renderizado','fuente':f'registros/{key}.json','fecha_ejecucion':rec['fecha']})
(root/'evidencias/manifiesto_registros.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(manifest)} imágenes de registros reales generadas; identificadas expresamente como renderizados.')
