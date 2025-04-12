from models import db, Clothing

def populate_database():
    clothings = [
        {'available': True, 'modeling': 'dress', 'color': 'orange', 'quantity': 1, 'id': 1},
        {'available': True, 'modeling': 'short', 'color': 'brown', 'quantity': 1, 'id': 2},
        {'available': True, 'modeling': 'panty', 'color': 'blue', 'quantity': 3, 'id': 3},
        {'available': True, 'modeling': 'blouse', 'color': 'white', 'quantity': 4, 'id': 4},
        {'available': True, 'modeling': 'dress', 'color': 'white', 'quantity': 3, 'id': 5},
    ]

    for item in clothings:
        clothing = Clothing(
            available=item['available'],
            quantity=item['quantity'],
            color=item['color'],
            modeling=item['modeling'],
            id=item['id']
        )
        db.session.add(clothing)
    
    db.session.commit()  

    
# CREATE
def insert(clothing):
    db.session.add(clothing)
    db.session.commit()
    return 

# READ # pega todas as roupas e mostra a lista do que está no banco
def view():
    return Clothing.query.all()

#  UPDATE
def update(clothing):
    db.session.commit()

#  DELETE
def delete(clothing):
    db.session.delete(clothing)
    db.session.commit()
    return
