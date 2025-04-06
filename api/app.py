from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import Clothing
from utils import parse_available

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clothings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/request", methods=['POST'])
def postRequest():
    data = request.get_json()

    new_clothing = Clothing.from_dict(data) 
    print('new clothing: ', new_clothing.serialize())
    db.session.add(new_clothing)
    db.session.commit()
    return jsonify({
                'error': '',
                'res': new_clothing.serialize(),
                'status': '200',
                'msg': 'Success creating a new Clothing! 👍😀'
            })

@app.route('/request', methods=['GET'])
def getRequest():
    # data = request.get_json()
    clothings = Clothing.query.all()
    
    if not clothings:
            return jsonify({
            'error': 'You have not entered any clothes yet.! 👕👚',
            'res': '',
            'status': '200'
        })
    return jsonify({
            'error': '',
            'res': [c.serialize() for c in clothings],
            'status': '200',
            'msg': 'Success getting all clothings in closet! 👍😀'
        })        
            
            
        
@app.route('/request/<int:id>', methods=['GET'])
def getRequestId(id):
    color = request.args.get('color')
    modeling = request.args.get('modeling')
    available = request.args.get('available')
    
    query = Clothing.query
    
    if color:
        query = query.filter_by(color=color)
    if modeling:
        query = query.filter_by(modeling=modeling)
    if available is not None:
        available_bool = available.lower() == 'true'
        query = query.filter_by(available=available_bool)    
        
    results = query.all()
    
    if not results:
        return jsonify({
            'error': 'No clothing items found with the specified criteria! ❌',
            'res': '',
            'status': '404'
        })
    return jsonify({
        'error': '',
        'res': [c.serialize() for c in results],
        'status': '200',
        'msg': 'Success filtering clothings! 👍😀'
    })
    


@app.route("/request/<int:id>", methods=['PUT'])
def putRequest(id):
    data = request.get_json(id)
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
    
    db.session.commit()
    
    
    return jsonify({
        'error': '',
        'res': clothing.serialize(),
        'status': '200',
        'msg': f"Success updating clothing with ID {id}! 👍😀"
    })

if __name__ == '__main__':
    app.run(debug=True)