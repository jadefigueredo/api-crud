from flask import Flask, request, jsonify, render_template
from database import insert, view, update, delete
from models import Clothing, db
from utils import parse_available

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clothings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/api", methods=['POST'])
def postRequest():
    data = request.get_json()
    new_clothing = Clothing.from_dict(data) 
    insert(new_clothing)
    return jsonify({
                'error': '',
                'res': new_clothing.serialize(),
                'status': '200',
                'msg': 'Success creating a new Clothing! 👍😀'
            })

@app.route('/api', methods=['GET'])
def getRequest():
    # data = request.get_json()
    clothings = view()
    
    if not clothings:
            return jsonify({
            'error': 'You have not entered any clothes yet.! 👕👚',
            'res': '',
            'status': '200'
        })
    return jsonify({
            'error': '',
            'res': clothings,
            'status': '200',
            'msg': 'Success getting all clothings in closet! 👍😀'
        })        
            
            
        
@app.route('/api/<int:id>', methods=['GET'])
def getRequestId(id):
    
    clothing = Clothing.query.filter_by(id=id)
    # lembrar de buscar o id específico da rota
    if not clothing:
        return jsonify({
            'error': 'No clothing items found with the specified criteria! ❌',
            'res': '',
            'status': '404'
        })
    return jsonify({
        'error': '',
        'res': clothing,
        'status': '200',
        'msg': 'Success filtering clothings! 👍😀'
    })
    


@app.route("/api/<int:id>", methods=['PUT'])
def putRequest(id):
    data = request.get_json()
    clothing = Clothing.query.get(id)
    if not clothing:
        return jsonify({
            'error': f"Clothing with ID '{id}' not found! ⛔",
            'res': '',
            'status': '404'
        })
    
    clothing.available = parse_available(data.get('available', clothing.available))
    clothing.quantity = data.get('quantity', clothing.quantity)
    clothing.color = data.get('color', clothing.color)
    clothing.modeling = data.get('modeling', clothing.modeling)
    update(clothing)    
    
    return jsonify({
        'error': '',
        'res': clothing.serialize(),
        'status': '200',
        'msg': f"Success updating clothing with ID {id}! 👍😀"
    })
    
@app.route("/api/<int:id>", methods=['DELETE'])
def deleteRequest(id):
    delete(id)
    return jsonify({
        'error': '',
        'res': '',
        'status': '200',
        'msg': f"Success deleting clothing with ID {id}! 👍😀"
    })
    
print("Rodando o script")

if __name__ == '__main__':
    print("Rodando dentro do __main__")
    with app.app_context():
        db.create_all()
    app.run(debug=True)