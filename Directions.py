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
    
@app.route("/historial", methods= ['GET'])
@cross_origin(allow_headers=['Content_Type'])
def historial():
    try:
        objResult=CallMethood.obtener_historial_riego()
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
@app.route('/update_sector1/<id>', methods=['PUT'])
@cross_origin(allow_headers=['Content-Type'])
def update_sector(id):
    try:
        # Obtenemos los datos del cuerpo de la solicitud (request)
        sector_data = request.json
        print(f"Datos recibidos: {sector_data}")
        
        # Llamamos a la función para actualizar el sector con el id recibido
        return CallMethood.actualizar_sector(id, sector_data)
    
    except Exception as e:
        # Manejo de errores
        print(f"Error al actualizar el sector: {e}")
        return jsonify({"mensaje": "Error al actualizar el sector"}), 500
    
# @app.route('/update_sector2/<id>', methods=['PUT'])
# @cross_origin(allow_headers=['Content-Type'])
# def update_sector(id):
#     try:
#         # Obtenemos los datos del cuerpo de la solicitud (request)
#         sector_data2 = request.json
#         print(f"Datos recibidos: {sector_data2}")
        
#         # Llamamos a la función para actualizar el sector con el id recibido
#         return CallMethood.actualizar_sector(id, sector_data2)
    
#     except Exception as e:
#         # Manejo de errores
#         print(f"Error al actualizar el sector: {e}")
#         return jsonify({"mensaje": "Error al actualizar el sector"}), 500


@app.route('/config1/<id>', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])  # Corregido Content_Type
def find_config1(id):
    try:
        objResult = CallMethood.configRiego(id)  # Asegúrate de que CallMethood está bien importado
        return objResult
    except Exception as e:
        print(f"Error en find_config1: {str(e)}")  # Mensaje más claro
        objResponse = ResponseMessage.err500.copy()
        objResponse["error"] = str(e)  # Incluir el error en la respuesta
        return jsonify(objResponse)
    
@app.route('/estado/<id>', methods=['GET'])
def state(id):
    try:
        objResult = CallMethood.obtener_estado_riego(id)
        return objResult
    except Exception as e:
        print(f"Error en estado: {str(e)}")
        objResponse = ResponseMessage.err500.copy()
        objResponse["error"] = str(e)
        return jsonify(objResponse)
@app.route('/estadoValvula/<id>', methods=['GET'])
def stateValvula(id):
    try:
        objResult = CallMethood.obtener_estado_valvula(id)
        return objResult
    except Exception as e:
        print(f"Error en estado: {str(e)}")
        objResponse = ResponseMessage.err500.copy()
        objResponse["error"] = str(e)
        return jsonify(objResponse)

@app.route('/actualizarEstado/<id>', methods=['PUT'])
@cross_origin(allow_headers=['Content-Type'])  # Asegura que el header Content-Type sea permitido
def update_state(id):
    try:
        # Llamamos a la función para actualizar el estado
        return CallMethood.actualizar_estado_riego(id)
    except Exception as e:
        # Manejo de errores
        print(f"Error al actualizar el estado de riego: {e}")
        return jsonify({"mensaje": "Error al actualizar el estado"}), 500
@app.route('/actualizarEstadoValvula/<id>', methods=['PUT'])
@cross_origin(allow_headers=['Content-Type'])  # Asegura que el header Content-Type sea permitido
def update_state_valvula(id):
    try:
        # Llamamos a la función para actualizar el estado
        return CallMethood.actualizar_estado_valvula(id)
    except Exception as e:
        # Manejo de errores
        print(f"Error al actualizar el estado de riego: {e}")
        return jsonify({"mensaje": "Error al actualizar el estado"}), 500
@app.route('/actualizarEstadoFalse/<id>', methods=['PUT'])
@cross_origin(allow_headers=['Content-Type'])  # Asegura que el header Content-Type sea permitido
def update_state_false(id):
    try:
        # Llamamos a la función para actualizar el estado
        return CallMethood.actualizar_estado_riego_false(id)
    except Exception as e:
        # Manejo de errores
        print(f"Error al actualizar el estado de riego: {e}")
        return jsonify({"mensaje": "Error al actualizar el estado"}), 500
    

@app.route('/restarPausa/<id>', methods=['PUT'])
@cross_origin(allow_headers=['Content-Type'])  # Permite el encabezado Content-Type
def restar_pausa_ruta(id):
    try:
        # Llamamos a la función para restar la pausa
        return CallMethood.restar_pausa(id)
    except Exception as e:
        # Manejo de errores
        print(f"Error al restar la pausa: {e}")
        return jsonify({"mensaje": "Error al restar la pausa"}), 500

    
@app.route('/duracionPausa/<id>', methods=['PUT'])
@cross_origin(allow_headers=['Content-Type'])  # Permite el encabezado Content-Type
def actualizar_duracionpausa_ruta(id):
    try:
        # Llamamos a la función para restar la pausa
        return CallMethood.actualizar_duracion_pausa(id)
    except Exception as e:
        # Manejo de errores
        print(f"Error al restar la pausa: {e}")
        return jsonify({"mensaje": "Error al restar la pausa"}), 500
    
@app.route('/duracionPausaHis/<id>', methods=['PUT'])
@cross_origin(allow_headers=['Content-Type'])  # Permite el encabezado Content-Type
def actualizar_duracionpausaHis_ruta(id):
    try:
        # Llamamos a la función para restar la pausa
        return CallMethood.actualizar_duracion_pausa_his(id)
    except Exception as e:
        # Manejo de errores
        print(f"Error al agregar la Duracionpausa: {e}")
        return jsonify({"mensaje": "Error al restar la pausa"}), 500
    
@app.route('/pausasHis/<id>', methods=['PUT'])
@cross_origin(allow_headers=['Content-Type'])  # Permite el encabezado Content-Type
def actualizar_pausaHis_ruta(id):
    try:
        # Llamamos a la función para restar la pausa
        return CallMethood.actualizar_pausa_his(id)
    except Exception as e:
        # Manejo de errores
        print(f"Error al agregar la pausa: {e}")
        return jsonify({"mensaje": "Error al restar la pausa"}), 500

    
#app.run(host="0.0.0.0",port=5000,debug=True,threaded=True)
#2