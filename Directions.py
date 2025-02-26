from flask import Flask,jsonify,request
from flask_cors import CORS, cross_origin

import backend.Functions as CallMethood
import backend.GlobalInfo.ResponseMessages as ResponseMessage

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

@app.route("/mensaje", methods= ['GET'])
@cross_origin(allow_headers=['Content_Type'])
def mensaje():
    try:
        objResult=CallMethood.fnMensaje()
        return objResult
    except Exception as e:
        print("Error en mensaje", e)
        return jsonify(ResponseMessage.err500)
    
@app.route("/mensaje/<id>", methods= ['GET'])
@cross_origin(allow_headers=['Content_Type'])
def mensajeId(id):
    try:
        objResult=CallMethood.fnMensajeId(id)
        return objResult
    except Exception as e:
        print("Error en mensaje", e)
        return jsonify(ResponseMessage.err500)
@app.route('/insert_user', methods=['POST'])
def insert_user():
    user_data = request.json
    return CallMethood.insertUser(user_data)
@app.route('/insert_sector1', methods=['POST'])
def insert_sector():
    sector_data = request.json
    return CallMethood.insertSector(sector_data)
@app.route('/config1', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])  # Corregido Content_Type
def find_config1():
    try:
        objResult = CallMethood.configSec1()  # Asegúrate de que CallMethood está bien importado
        return objResult
    except Exception as e:
        print(f"Error en find_config1: {str(e)}")  # Mensaje más claro
        objResponse = ResponseMessage.err500.copy()
        objResponse["error"] = str(e)  # Incluir el error en la respuesta
        return jsonify(objResponse)

# app.run(host="0.0.0.0",port=5000,debug=True,threaded=True)