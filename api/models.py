from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Clothing(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    available = db.Column(db.Boolean, default=True)
    quantity = db.Column(db.Integer)
    color = db.Column(db.String(50))
    modeling = db.Column(db.String(100))
    
    def update_from_dict(self, data):
        if 'available' in data:
            self.available = bool(data['available'])
        if 'color' in data:
            self.color = data['color']
        if 'modeling' in data:
            self.modeling = data['modeling']
        if 'quantity' in data:
            self.quantity = int(data['quantity'])

        
    def __repr__(self): #método especial usado para definir a representação oficial de um objeto
        return f'<Clothing id={self.id}, modeling={self.modeling}>'

    def serialize(self):
        return {
            'id': self.id,
            'available': self.available,
            'quantity': self.quantity,
            'color': self.color,
            'modeling': self.modeling,
    }