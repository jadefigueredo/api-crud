from models import db, Clothing

def populate_database():
    clothings = [
        {"available": True, "modeling": "dress", "color": "orange", "quantity": 1},
        {"available": True, "modeling": "short", "color": "brown", "quantity": 1},
        {"available": True, "modeling": "panty", "color": "blue", "quantity": 3},
        {"available": True, "modeling": "blouse", "color": "white", "quantity": 4},
        {"available": True, "modeling": "dress", "color": "white", "quantity": 3},
    ]
    print(clothings)
    for item in clothings:
        clothing = Clothing(**item)
        db.session.add(clothing)
    
   db.session.commit()  

    
# CREATE
def insert(clothing):
    db.session.add(clothing)
    db.session.commit()
    return 

# READ 
def view():
    return Clothing.query.all()

#  UPDATE
def update(clothing):
    db.session.commit()
    return clothing

#  DELETE
def delete(clothing):
    db.session.delete(clothing)
    db.session.commit()
    return

print(populate_database())