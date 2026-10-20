import csv, hashlib, json
from pathlib import Path
r = Path(__file__).resolve().parents[1]
source = r/'datos/original/pseudo_facebook.csv'
target = r/'datos/pseudo_facebook_ronald.csv'
with source.open(newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    columns = next(reader)
    rows = list(reader)
assert len(columns) == 15
assert all(len(row)==15 for row in rows)
with target.open('w',newline='',encoding='utf-8') as f:
    csv.writer(f,lineterminator='\n').writerows(rows)
meta = {'origen':'https://www.kaggle.com/api/v1/datasets/download/sheenabatra/facebook-data','columnas':columns,'filas':len(rows),'usuarios_unicos':len({row[0] for row in rows}),'sha256_original':hashlib.sha256(source.read_bytes()).hexdigest(),'sha256_sin_encabezado':hashlib.sha256(target.read_bytes()).hexdigest(),'archivo_preparado':str(target)}
(r/'datos/metadata.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(meta,indent=2,ensure_ascii=False))
print('Primera fila sin encabezado:', ','.join(rows[0]))
