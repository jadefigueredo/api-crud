from flask import Flask, request, jsonify, render_template
from database import *
from models import Clothing, db
from utils import parse_available
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clothings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route("/api/insert", methods=['POST'])
def postRequest():
    data = request.get_json()
    
    new_clothing = Clothing(
        available=data.get(('available', True)),
        quantity=data.get('quantity', ''),
        color=data.get('color', ''),
        modeling=data.get('modeling', '')
    )
    insert(new_clothing)
    return jsonify({
                'error': '',
                'res': new_clothing.serialize(),
                'status': '201',
                'msg': 'HTTP 201 Created! Success creating new clothing! 👍😀'
            })

@app.route('/api', methods=['GET'])
def getRequest():
    clothings = view()
    if not clothings:
            return jsonify({
            'error': 'You have not entered any clothes yet.! 👕👚',
            'res': '',
            'status': '200'
        })
            
    serialized_clothings = [item.serialize() for item in clothings]
    return jsonify({
            'error': '',
            'res': serialized_clothings,
            'status': '200',
            'msg': 'HTTP 200 Ok - Success getting all clothings in closet! 👍😀'
        })        
            
            
        
@app.route('/api/<int:id>', methods=['GET'])
def getRequestId(id):
    get_clothing_by_id = Clothing.query.get(id)

    if not get_clothing_by_id:
        return jsonify({
            'error': f'Not Found - No clothing items found with the specified {id}! ❌',
            'res': '',
            'status': '404'
        })
    return jsonify({
        'error': '',
        'res': get_clothing_by_id.serialize(),
        'status': '200',
        'msg': 'HTTP 200 Ok - Success filtering clothings! 👍😀'
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
    
@app.route("/api/delete/<int:id>", methods=['DELETE'])
def deleteRequest(id):
    data = request.get_json()
    
    clothing_to_be_deleted = 
    # buscar id na tabela
    # retornar id e enviar id na requisição
    
    delete(clothing_to_be_deleted) 
    
    if not clothing_to_be_deleted:
        return jsonify({
            'error': f"Clothing with ID '{id}' not found! ⛔",
            'res': '',
            'status': '404'
        })
         
    return jsonify({
        'error': '',
        'res': '',
        'status': '200',
        'msg': f"Success deleting clothing with ID {id}! 👍😀"
    })
    
    
@app.before_request
def log_request_info():
    print(f"Request: {request.method} {request.url}")
#    print(f"Request Body: {request.get_json()}")
    print(f"Request Headers: {request.headers}")

    
print("Rodando o script")

if __name__ == '__main__':
    print("Rodando dentro do __main__")
    with app.app_context():
        db.create_all()
    app.run(debug=True)