from flask import Flask, request, jsonify, render_template
from database import *
from models import Clothing, db
from utils import parse_available
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresadmin@localhost:5432/clothings'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clothings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route("/api/post/insert_new_clothing", methods=['POST'])
def postRequest():
    try:
        data = request.get_json()
                     
        new_clothing = Clothing(
            available=data.get('available', True),
            quantity=data.get('quantity', ''),
            color=data.get('color', ''),
            modeling=data.get('modeling', '')
        )
        insert(new_clothing)
        return jsonify({
                    'res': new_clothing.serialize(),
                    'status': '201',
                    'msg': 'Created'
                }), 201
    except Exception as e:
        
        logging.info('Erro ao inserir na tabela')
        return jsonify({
        'error': 'Bad Gateway',
        'details': str(e),
        'status': '502'
        }), 502

@app.route('/api/get/clothings', methods=['GET'])
def getRequest():
    try:
        clothings = view()               
        serialized_clothings = [item.serialize() for item in clothings]
        return jsonify({
                'res': serialized_clothings,
                'status': '200',
                'msg': 'Ok'
            })
    except Exception as e:
        
        logging.info('Não encontrado')   
        return jsonify({
        'error': '',
        'status': '404',
        'details': str(e),
        }), 404  
            
@app.route('/api/get/<int:id>', methods=['GET'])
def getRequestId(id):
    
    try:
        get_clothing_by_id = Clothing.query.get(id)
    
        return jsonify({
            'error': '',
            'res': get_clothing_by_id.serialize(),
            'status': '200',
            'msg': 'Ok'
        }), 200
    except Exception as e:
            return jsonify({
            'error': f'Not Found - No clothing items found with the specified {id}',
            'res': '',
            'status': '404'
        }), 404

    

@app.route("/api/put/<int:id>", methods=['PUT'])
def putRequest(id):
    
    try:
        data = request.get_json()
        clothing = Clothing.query.get(id)
        clothing.available = parse_available(data.get('available', clothing.available))
        clothing.quantity = data.get('quantity', clothing.quantity)
        clothing.color = data.get('color', clothing.color)
        clothing.modeling = data.get('modeling', clothing.modeling)
        clothing = update(clothing)
        
        return jsonify({
        'details': str(e),
        'res': clothing.serialize(),
        'status': '200',
        'msg': "Ok"
    }), 200
    except Exception as e:
            return jsonify({
            'error': f"Clothing with ID '{id}' not found! ⛔",
            'res': '',
            'status': '404'
        }), 404
    
    
@app.route("/api/delete/<int:id>", methods=['DELETE'])
def deleteRequest(id):
    
    try:
        clothing_to_be_deleted = Clothing.query.get(id)        
        delete(clothing_to_be_deleted) 
        
        return jsonify({
            'error': '',
            'res': '',
            'status': '200',
            'msg': "Ok"
        }), 200
    except Exception as e:
        return jsonify({
            'error': f"'{id}' not found",
            'res': '',
            'status': '404'
        }), 404

# tomar cuidado com o app before request pq ele pode causar erros e eu posso não conseguir rodar corretamente
    
# @app.before_request
# def log_request_info():
#     print(f"Request: {request.method} {request.url}")
#     print(f"Request Body: {request.get_json()}")
#     print(f"Request Headers: {request.headers}")

    
print("Rodando o script")

if __name__ == '__main__':
    print("Rodando dentro do __main__")
    with app.app_context():
        db.create_all()
        from database import populate_database
        populate_database()
    app.run(host='0.0.0.0', debug=True)