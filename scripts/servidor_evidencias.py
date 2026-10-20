from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import json, html
from datetime import datetime
from zoneinfo import ZoneInfo
root=Path(__file__).resolve().parents[1]
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  key=self.path.split('?')[0].strip('/')
  if key=='reloj':
   body=datetime.now(ZoneInfo('America/La_Paz')).strftime('%d/%m/%Y %H:%M:%S %z').encode()
   self.send_response(200);self.end_headers();self.wfile.write(body);return
  if not key:key='01'
  path=root/'registros'/f'{key}.json'
  if not path.is_file():self.send_error(404);return
  rec=json.loads(path.read_text(encoding='utf-8-sig'))
  e=html.escape
  raw=rec['salida']
  lines=[line.rstrip() for line in raw.splitlines() if line.strip() and not line.startswith(('SLF4J:', '[WARN] Failed to create directory:', 'No such file or directory'))]
  clean='\n'.join(lines)
  query=root/'proyecto/sql'/f'{key}.sql'
  sql=f'<p><b>SQL ejecutado</b></p><pre>{e(query.read_text(encoding="utf-8"))}</pre>' if query.exists() else ''
  if lines and '\t' in lines[0] and key not in ('15d',):
   cells=[line.split('\t') for line in lines]
   result='<table>'+''.join('<tr>'+''.join(f'<{"th" if i==0 else "td"}>{e(c)}</{"th" if i==0 else "td"}>' for c in row)+'</tr>' for i,row in enumerate(cells))+'</table>'
  else:
   result=f'<pre>{e(clean) if clean else "Sin salida estándar. Consultar el código de salida y la verificación del punto."}</pre>'
  content=f'''<!doctype html><html lang="es"><meta charset="utf-8"><title>{e(rec['titulo'])}</title>
  <style>body{{margin:24px;font:16px Arial;color:#172334;background:#fff}}h1{{font-size:23px}}.meta{{font-size:14px;color:#35485b}}pre{{font:14px Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f4f6;padding:14px;border:1px solid #ccd3da}}header{{display:flex;justify-content:space-between;gap:20px}}#clock{{font-weight:bold;white-space:nowrap}}footer{{font-size:13px;color:#475569;margin-top:20px}}table{{border-collapse:collapse;width:100%;font-size:{'11' if key=='15f' else '15'}px}}td,th{{border:1px solid #cbd5e1;padding:10px 7px;text-align:left;overflow-wrap:anywhere}}th{{background:#e2e8f0}}details{{margin-top:18px}}</style>
  <header><b>LI16 · Ronald Joel Saavedra Vargas</b><span id="clock"></span></header>
  <h1>{e(rec['titulo'])}</h1><p class="meta">Registro real de ejecución · {e(rec['fecha'])} · Código de salida {rec.get('exit_code')}</p>
  <p><b>Comando ejecutado</b></p><pre>{e(rec['comando'])}</pre>
  {sql}<p><b>Resultado del registro real</b></p>{result}
  <details><summary>Salida original completa incluidas advertencias</summary><pre>{e(raw)}</pre></details>
  <footer>Captura de un visor local de registros reales, no de una terminal interactiva. Las advertencias de logging se conservan en el original. El reloj muestra la hora actual del sistema en Bolivia; la ejecución tiene su propia fecha arriba.</footer>
  <script>async function tick(){{document.getElementById('clock').textContent='Hora del sistema: '+await(await fetch('/reloj')).text()}}tick();setInterval(tick,1000)</script></html>'''
  self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(content.encode())
ThreadingHTTPServer(('0.0.0.0',8766),Handler).serve_forever()
