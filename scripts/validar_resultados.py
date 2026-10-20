import csv, json
from pathlib import Path
r=Path(__file__).resolve().parents[1]
with (r/'datos/original/pseudo_facebook.csv').open(newline='',encoding='utf-8-sig') as f:
 rows=list(csv.DictReader(f))
def group(pred):return [x for x in rows if pred(x)]
def total(items,key):return sum(int(x[key]) for x in items if x[key] not in ('NA',''))
def mean(items,key):return round(total(items,key)/sum(x[key] not in ('NA','') for x in items),2)
young=group(lambda x:13<=int(x['age'])<=25)
older=group(lambda x:int(x['age'])>35)
adult=group(lambda x:int(x['age'])>25)
answer={'16a':[len(rows),len({x['userid'] for x in rows})], '16b':len(adult),
'16c':{g:[len(t:=group(lambda x:x['gender']==g)),mean(t,'friend_count')] for g in ('female','male')},
'16d':{k:[len(v),total(v,'likes_received'),mean(v,'likes_received')] for k,v in [('13 a 25',young),('mayores de 35',older)]},
'16e':{i:len(group(lambda x:int(x['dob_month'])==i)) for i in range(1,13)},
'16f':[len(young),total(young,'mobile_likes'),total(young,'www_likes'),mean(young,'mobile_likes'),mean(young,'www_likes')],
'16g':[len(adult),total(adult,'mobile_likes'),total(adult,'www_likes'),mean(adult,'mobile_likes'),mean(adult,'www_likes')]}
for key,expected in answer.items():
 rec=json.loads((r/'registros'/f'{key}.json').read_text(encoding='utf-8-sig'))
 assert rec['exit_code']==0,key
 def leaves(v):
  if isinstance(v,dict):
   for a,b in v.items():yield str(a);yield from leaves(b)
  elif isinstance(v,list):
   for a in v:yield from leaves(a)
  else:yield str(v)
 for value in leaves(expected):assert value in rec['salida'],(key,value)
print('Las siete consultas de Hive coinciden con el cálculo independiente del CSV.')
print(json.dumps(answer,ensure_ascii=False,indent=2))
(r/'datos/resultados_verificados.json').write_text(json.dumps(answer,ensure_ascii=False,indent=2),encoding='utf-8')
