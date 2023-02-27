from app import db
db.clear()

for x in range(1, 4*24+1):
    db.add('pebbles', {'id': str(x), 'status': False})
