import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Test
from dotenv import load_dotenv

load_dotenv()

PATH = os.path.abspath('instance')

app = Flask(__name__, instance_path=PATH)
app.config['DEBUG'] = True 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
CORS(app)


@app.route('/')
def main():
    return jsonify({ "status": "Server Running Successfully!"}), 200

# Consultado todos los registro de la tabla tests
@app.route('/tests', methods=['GET'])
def get_tests():
    
    # buscamos los datos
    tests_messages = Test.query.all() # SELECT * FROM tests # [<Test 1>, <Test 2>]

    # Transformamos los datos en un tipo de dato que puedan ser serializar (json)
    #tests_messages = [ test.serialize() for test in tests_messages]
    tests_messages = list(map(lambda test: test.serialize(), tests_messages))

    return jsonify(tests_messages)

# Ruta para crear o insertar un nuevo mensaje de test
@app.route('/tests', methods=['POST'])
def save_test():

    #capturando los datos enviados por el usuario 
    datos = request.json

    #creamos una nueva instancia para crear un nuevo Test
    test = Test()
    test.message = datos.get('message')
    test.author = datos.get('author')

    # Guardamos los datos en la base de datos
    db.session.add(test)
    db.session.commit()

    #devolvemos los datos en formato que puede ser seriaalizdo 
    return jsonify(test.serialize()), 200


@app.route('/tests/<int:id>', methods=['PUT'])
def update_trests(id):
    #capturando los datos enviados por el usuario 
    datos = request.json
    
    test = Test.query.filter_by(id=id).first() # [] => {}

    test.message = datos.get('message')
    test.author = datos.get('author')

    # Guardamos los datos en la base de datos
    db.session.commit()

    return jsonify(test.serialize()), 200

@app.route('/tests/<int:id>', methods=['DELETE'])
def delete_test(id):


    return id

if __name__ == '__main__':
    app.run()