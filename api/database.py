# database.py
from models import db, Clothing

# Função para popular o banco de dados com dados iniciais
def populate_database():
    clothings = [
        {'available': True, 'modeling': 'dress', 'color': 'orange', 'quantity': 1},
        {'available': True, 'modeling': 'short', 'color': 'brown', 'quantity': 1},
        {'available': True, 'modeling': 'panty', 'color': 'blue', 'quantity': 3},
        {'available': True, 'modeling': 'blouse', 'color': 'white', 'quantity': 4},
        {'available': True, 'modeling': 'dress', 'color': 'white', 'quantity': 3},
    ]

    for item in clothings:
        clothing = Clothing(
            available=item['available'],
            quantity=item['quantity'],
            color=item['color'],
            modeling=item['modeling']
        )
        db.session.add(clothing)  # adiciona ao banco (em memória)
    
    db.session.commit()  # salva as mudanças no banco

# CREATE
def insert(clothing):
    db.session.add(clothing)
    db.session.commit()

# READ
def view():
    return Clothing.query.all()

#  UPDATE
def update(clothing):
    db.session.commit()

#  DELETE
def delete(clothing_id):
    clothing = Clothing.query.get(clothing_id)
    if clothing:
        db.session.delete(clothing)
        db.session.commit()
