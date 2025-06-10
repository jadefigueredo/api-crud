from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import HTTPException, NotFound, BadRequest
from database import *
from models import Clothing, db
from utils import parse_available
from flask_cors import CORS
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify(status="ok", message="API is running"), 200

@app.route("/api/clothing", methods=["POST"])
def postRequest():
    try:
        data = request.get_json()

        if not data:
            raise BadRequest("No data provided")

        new_clothing = Clothing(
            available=data.get("available", True),
            quantity=data.get("quantity", ""),
            color=data.get("color", ""),
            modeling=data.get("modeling", "")
        )
        insert(new_clothing)

        return jsonify({
            "res": new_clothing.serialize(),
            "status": "201",
            "msg": "Created"
        }), 201

    except BadRequest as e:
        return jsonify({
            "error": "Bad Request",
            "details": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)
        }), 500

@app.route("/api/get/clothings", methods=["GET"])
def getRequest():
    try:
        clothings = view()
        serialized_clothings = [item.serialize() for item in clothings]

        if not serialized_clothings:
            raise NotFound("No clothing items found")

        return jsonify({
            "res": serialized_clothings,
            "status": "200"
        }), 200

    except NotFound as e:
        return jsonify({
            "error": "Not Found",
            "details": str(e)
        }), 404

    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)
        }), 500

@app.route("/api/get/<int:id>", methods=["GET"])
def getRequestId(id):
    try:
        clothing = Clothing.query.get(id)

        if not clothing:
            raise NotFound(f"Clothing item with ID {id} not found")

        return jsonify({
            "res": clothing.serialize(),
            "status": "200",
            "msg": "Ok"
        }), 200

    except NotFound as e:
        return jsonify({
            "error": "Not Found",
            "details": str(e)
        }), 404

    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)
        }), 500

@app.route("/api/put/<int:id>", methods=["PUT"])
def putRequest(id):
    try:
        data = request.get_json()
        clothing = Clothing.query.get(id)

        if not clothing:
            raise NotFound(f"Clothing item with ID {id} not found")

        clothing.available = parse_available(data.get("available", clothing.available))
        clothing.quantity = data.get("quantity", clothing.quantity)
        clothing.color = data.get("color", clothing.color)
        clothing.modeling = data.get("modeling", clothing.modeling)

        clothing = update(clothing)

        return jsonify({
            "res": clothing.serialize(),
            "status": "200",
            "msg": "Updated"
        }), 200

    except NotFound as e:
        return jsonify({
            "error": "Not Found",
            "details": str(e)
        }), 404

    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)
        }), 500

@app.route("/api/delete/<int:id>", methods=["DELETE"])
def deleteRequest(id):
    try:
        clothing_to_be_deleted = Clothing.query.get(id)

        if not clothing_to_be_deleted:
            raise NotFound(f"Clothing item with ID {id} not found")

        delete(clothing_to_be_deleted)

        return jsonify({
            "res": "",
            "status": "200",
            "msg": "Deleted"
        }), 200

    except NotFound as e:
        return jsonify({
            "error": "Not Found",
            "details": str(e)
        }), 404

    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e)
        }), 500

print("Rodando o script")

if __name__ == "__main__":
    print("Rodando dentro do __main__")
    with app.app_context():
        db.create_all()
        from database import populate_database
        populate_database()
    app.run(host="0.0.0.0", debug=True)
    
