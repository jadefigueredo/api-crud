from flask import Flask, request, jsonify, render_template
from database import *
from models import Clothing, db
from utils import parse_available
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clothings.db'
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
                })
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
            #     return jsonify({
            #     'res': '',
            #     'status': '200',
            #     'msg': 'Ok'
            # })
                
        serialized_clothings = [item.serialize() for item in clothings]
        return jsonify({
                'res': serialized_clothings,
                'status': '200',
                'msg': 'Ok'
            })
    except Exception as e:
        logging.info('Sem conteúdo')        
            
@app.route('/api/get/<int:id>', methods=['GET'])
def getRequestId(id):
    get_clothing_by_id = Clothing.query.get(id)
    
    

    if not get_clothing_by_id:
        return jsonify({
            'error': f'Not Found - No clothing items found with the specified {id}',
            'res': '',
            'status': '404'
        })
    return jsonify({
        'error': '',
        'res': get_clothing_by_id.serialize(),
        'status': '200',
        'msg': 'Ok'
    })
    

@app.route("/api/put/<int:id>", methods=['PUT'])
def putRequest(id):
    data = request.get_json()
    clothing = Clothing.query.get(id)
    if not clothing:
        return jsonify({
            'error': "Not Found",
            'res': '',
            'status': '404'
        })
    clothing.available = parse_available(data.get('available', clothing.available))
    clothing.quantity = data.get('quantity', clothing.quantity)
    clothing.color = data.get('color', clothing.color)
    clothing.modeling = data.get('modeling', clothing.modeling)
    clothing = update(clothing)
    
    return jsonify({
        'error': '',
        'res': clothing.serialize(),
        'status': '200',
        'msg': "Ok"
    })
    
@app.route("/api/delete/<int:id>", methods=['DELETE'])
def deleteRequest(id):
    clothing_to_be_deleted = Clothing.query.get(id)
    
    if not clothing_to_be_deleted:
        return jsonify({
            'error': f"'{id}' not found",
            'res': '',
            'status': '404'
        })
    delete(clothing_to_be_deleted) 
    return jsonify({
        'error': '',
        'res': '',
        'status': '200',
        'msg': "Ok"
    })

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
    app.run(debug=True)