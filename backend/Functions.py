from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId
import backend.GlobalInfo.Keys as keys
import backend.GlobalInfo.ResponseMessages as ResponseMessage
import datetime

if keys.dbconn==None:
    mongoconect=MongoClient(keys.strConnection)
    keys.dbconn=mongoconect[keys.strDBConnection]
    dbUsers=keys.dbconn['usuarios']
    dbConfig=keys.dbconn['control_riego']
    dbHistorial=keys.dbconn['historial_riego']
    
def fnMensaje():
    try:
        arrFinal=[]
        consulta=dbUsers.find({})
        listUsuarios=list(consulta)
        if len(listUsuarios)!=0:
            for objUser in listUsuarios:
                objFormateado={
                    "id":str(objUser.get("_id")),
                    "user":objUser.get("user"),
                    "email":objUser.get("email"),
                    "password":objUser.get("password"),
                }
                arrFinal.append(objFormateado)
        objResponse=ResponseMessage.succ200.copy()
        objResponse['Respuesta']=arrFinal
        return jsonify(objResponse)
    except Exception as e:
        print("Error en fnMensaje",e)
        objResponse=ResponseMessage.err500.copy()
        return jsonify(objResponse)

def fnMensajeId(id):
    try:
        arrFinal=[]
        consulta=dbUsers.find({"_id":ObjectId(id)})
        listUsuarios=list(consulta)
        if len(listUsuarios)!=0:
            for objUser in listUsuarios:
                objFormateado={
                    "id":str(objUser.get("_id")),
                    "user":objUser.get("user"),
                    "email":objUser.get("email"),
                    "password":objUser.get("password"),
                }
                arrFinal.append(objFormateado)
        objResponse=ResponseMessage.succ200.copy()
        objResponse['Respuesta']=arrFinal
        return jsonify(objResponse)
    except Exception as e:
        print("Error en fnMensaje",e)
        objResponse=ResponseMessage.err500.copy()
        return jsonify(objResponse)
    
def insertUser(user_data):
    try:
        # Insertar el usuario en la base de datos
        result = dbUsers.insert_one(user_data)
        
        # Crear una respuesta con el ID del nuevo usuario
        objResponse = ResponseMessage.succ200.copy()
        objResponse['Respuesta'] = {"id": str(result.inserted_id)}
        return jsonify(objResponse)
    except Exception as e:
        print("Error en insertUser", e)
        objResponse = ResponseMessage.err500.copy()
        return jsonify(objResponse)
    
def actualizar_sector(id, sector_data):
    try:
        # Convertir el id a ObjectId si es MongoDB
        if not ObjectId.is_valid(id):
            raise ValueError("El id no es válido.")
        
        # Lógica para actualizar el sector con el id recibido en la colección de sectores
        result = dbConfig.update_one({"_id": ObjectId(id)}, {"$set": sector_data})
        
        if result.modified_count > 0:
            # Si la actualización en la colección de sectores fue exitosa, también actualizamos la colección secundaria
            # En este ejemplo, estamos insertando el historial de actualizaciones con la misma información
            sector_data["sector_id"] = id  # Añadimos el id del sector actualizado
            sector_data["accion"] = "Actualización del sector"
            sector_data["fecha_actualizacion"] = datetime.datetime.utcnow()
            
            # Insertamos el historial en la colección "historial"
            dbHistorial.insert_one(sector_data)

            return jsonify({"mensaje": "Sector actualizado correctamente y registrado en el historial."}), 200
        else:
            return jsonify({"mensaje": "No se encontró el sector con ese id o no se hizo ninguna modificación."}), 404
    
    except Exception as e:
        print(f"Error al actualizar el sector: {e}")
        return jsonify({"mensaje": f"Error: {e}"}), 500
# def actualizar_sector2(id, sector_data2):
#     try:
#         # Convertir el id a ObjectId si es MongoDB
#         if not ObjectId.is_valid(id):
#             raise ValueError("El id no es válido.")
        
#         # Lógica para actualizar el sector con el id recibido
#         result = dbConfig.update_one({"_id": ObjectId(id)}, {"$set": sector_data2})
        
#         if result.modified_count > 0:
#             return jsonify({"mensaje": "Sector actualizado correctamente"}), 200
#         else:
#             return jsonify({"mensaje": "No se encontró el sector con ese id o no se hizo ninguna modificación."}), 404
    
#     except Exception as e:
#         print(f"Error al actualizar el sector: {e}")
#         raise

def configSec1(id):
    try:
        arrFinal=[]
        consulta=dbUsers.find({"_id":ObjectId(id)})
        listsector=list(consulta)
        if len(listsector)!=0:
            for objUser in listsector:
                objFormateado={
                    "id":str(objUser.get("_id")),
                    "user":objUser.get("user"),
                    "email":objUser.get("email"),
                    "password":objUser.get("password"),
                }
                arrFinal.append(objFormateado)
        objResponse=ResponseMessage.succ200.copy()
        objResponse['Respuesta']=arrFinal
        return jsonify(objResponse)
    except Exception as e:
        print("Error en fnMensaje",e)
        objResponse=ResponseMessage.err500.copy()
        return jsonify(objResponse)
def configSec2(_id):
    try:
        consulta=dbConfig.find_one({_id: ObjectId("65dbe7f4e86a5b9e34a3c8a3")})
        objResponse=ResponseMessage.succ200.copy()
        objResponse['Respuesta']=consulta
        return jsonify(objResponse)
    except Exception as e:
        print("Error en configSec2",e)
        objResponse=ResponseMessage.err500.copy()
        return jsonify(objResponse)    

def configRiego (id):
    try:
        arrFinalRiego=[]
        query = dbConfig.find({"_id":ObjectId(id)})
        arrayRiego = list(query)
        if len(arrayRiego)!=0:
            for objRiego in arrayRiego:
                objFormateado={
                    "id":str(objRiego.get("_id")),
                    "fechaInicio":objRiego.get("fechaInicio"),
                    "fechaFin":objRiego.get("fechaFin"),
                    "duracion":objRiego.get("duracion"),
                    "dias":objRiego.get("dias"),
                    "horaInicio":objRiego.get("horaInicio"),
                    "pausas":objRiego.get("pausas"),
                    "duracionPausa":objRiego.get("duracionPausa"),
                    "estado":objRiego.get("estado")
                }
                arrFinalRiego.append(objFormateado)
        objResponse=ResponseMessage.succ200.copy()
        objResponse['Respuesta']=arrFinalRiego
        return jsonify(objResponse)
    except Exception as e:
        print("Error en fnMensaje",e)
        objResponse=ResponseMessage.err500.copy()
        return jsonify(objResponse)
    
def obtener_estado_riego(id):
    try:
        estado = dbConfig.find_one({"_id": ObjectId(id)})['estado']
        objResponse = ResponseMessage.succ200.copy()
        objResponse['Respuesta'] = {"estado": estado}
        return jsonify(objResponse)
    except Exception as e:
        print("Error al obtener el estado de riego", e)
        objResponse = ResponseMessage.err500.copy()
        return jsonify(objResponse)
def obtener_estado_valvula(id):
    try:
        estado = dbConfig.find_one({"_id": ObjectId(id)})['estadoValvula']
        objResponse = ResponseMessage.succ200.copy()
        objResponse['Respuesta'] = {"estadoValvula": estado}
        return jsonify(objResponse)
    except Exception as e:
        print("Error al obtener el estado de valvula", e)
        objResponse = ResponseMessage.err500.copy()
        return jsonify(objResponse)
    
def actualizar_estado_riego(id):
    try:
        # Cambiar el estado de riego en la base de datos
        result = dbConfig.update_one(
            {"_id": ObjectId(id)},  # Asegúrate de usar ObjectId para búsquedas correctas
            {"$set": {"estado": True}}  # O cambia el estado como lo desees
        )
        
        # Si la actualización fue exitosas
        if result.modified_count > 0:
            objResponse = ResponseMessage.succ200.copy()
            objResponse['Respuesta'] = {"mensaje": "Estado actualizado correctamente"}
        else:
            objResponse = ResponseMessage.err500.copy()
            objResponse['Respuesta'] = {"mensaje": "No se encontró el recurso para actualizar"}
        
        return jsonify(objResponse)
    
    except Exception as e:
        print("Error al actualizar el estado de riego", e)
        objResponse = ResponseMessage.err500.copy()
        return jsonify(objResponse)
def actualizar_estado_valvula(id):
    try:
        # Cambiar el estado de riego en la base de datos
        result = dbConfig.update_one(
            {"_id": ObjectId(id)},  # Asegúrate de usar ObjectId para búsquedas correctas
            {"$set": {"estadoValvula": True}}  # O cambia el estado como lo desees
        )
        
        # Si la actualización fue exitosas
        if result.modified_count > 0:
            objResponse = ResponseMessage.succ200.copy()
            objResponse['Respuesta'] = {"mensaje": "Estado actualizado correctamente"}
        else:
            objResponse = ResponseMessage.err500.copy()
            objResponse['Respuesta'] = {"mensaje": "No se encontró el recurso para actualizar"}
        
        return jsonify(objResponse)
    
    except Exception as e:
        print("Error al actualizar el estado de riego", e)
        objResponse = ResponseMessage.err500.copy()
        return jsonify(objResponse)
def actualizar_estado_riego_false(id):
    try:
        # Cambiar el estado de riego en la base de datos
        result = dbConfig.update_one(
            {"_id": ObjectId(id)},  # Asegúrate de usar ObjectId para búsquedas correctas
            {"$set": {"estado": False}}  # O cambia el estado como lo desees
        )
        
        # Si la actualización fue exitosas
        if result.modified_count > 0:
            objResponse = ResponseMessage.succ200.copy()
            objResponse['Respuesta'] = {"mensaje": "Estado actualizado correctamente"}
        else:
            objResponse = ResponseMessage.err500.copy()
            objResponse['Respuesta'] = {"mensaje": "No se encontró el recurso para actualizar"}
        
        return jsonify(objResponse)
    
    except Exception as e:
        print("Error al actualizar el estado de riego", e)
        objResponse = ResponseMessage.err500.copy()
        return jsonify(objResponse)
    
#Restar pausa
def restar_pausa(id):
    try:
        # Solo restar 1 a la columna 'pausas' en la base de datos
        result = dbConfig.update_one(
            {"_id": ObjectId(id)},  # Asegúrate de usar ObjectId para búsquedas correctas
            {
                "$inc": {"pausas": -1}  # Resta 1 a la columna 'pausas'
            }
        )
        
        # Verificar si la actualización fue exitosa
        if result.modified_count > 0:
            objResponse = ResponseMessage.succ200.copy()
            objResponse['Respuesta'] = {"mensaje": "Pausa restada correctamente"}
        else:
            objResponse = ResponseMessage.err500.copy()
            objResponse['Respuesta'] = {"mensaje": "No se encontró el recurso para restar la pausa"}
        
        return jsonify(objResponse)
    
    except Exception as e:
        print("Error al restar la pausa", e)
        objResponse = ResponseMessage.err500.copy()
        return jsonify(objResponse)
    
# Actualizar duracionPausa a 0
def actualizar_duracion_pausa(id):
    try:
        # Actualizar la columna 'duracionPausa' a 0 en la base de datos
        result = dbConfig.update_one(
            {"_id": ObjectId(id)},  # Asegúrate de usar ObjectId para búsquedas correctas
            {
                "$set": {"duracionPausa": 0}  # Establecer 'duracionPausa' a 0
            }
        )
        
        # Verificar si la actualización fue exitosa
        if result.modified_count > 0:
            objResponse = ResponseMessage.succ200.copy()
            objResponse['Respuesta'] = {"mensaje": "Duración de la pausa actualizada a 0 correctamente"}
        else:
            objResponse = ResponseMessage.err500.copy()
            objResponse['Respuesta'] = {"mensaje": "No se encontró el recurso para actualizar la duración de la pausa"}
        
        return jsonify(objResponse)
    
    except Exception as e:
        print("Error al actualizar la duración de la pausa", e)
        objResponse = ResponseMessage.err500.copy()
        return jsonify(objResponse)
def obtener_historial_riego():
    try:
        # Realizar la consulta a la colección 'historial_riego'
        historial = dbHistorial.find({})  # Busca todos los documentos en la colección

        # Convertir los resultados a una lista
        historial_list = list(historial)

        # Si la lista no está vacía, formateamos los datos
        if len(historial_list) != 0:
            arrFinal = []
            for registro in historial_list:
                # Formatear cada registro para devolverlo con un formato adecuado
                objFormateado = {
                    "id": str(registro.get("_id")),
                    "sector_id": registro.get("sector_id"),
                    "accion": registro.get("accion"),
                    "fecha_actualizacion": registro.get("fecha_actualizacion").strftime("%Y-%m-%d %H:%M:%S"),  # Formato de fecha
                    "fechaInicio": registro.get("fechaInicio"),
                    "fechaFin": registro.get("fechaFin"),
                    "duracion": registro.get("duracion"),
                    "dias": registro.get("dias"),
                    "horaInicio": registro.get("horaInicio"),
                    "pausas": registro.get("pausas"),
                    "duracionPausa": registro.get("duracionPausa"),
                    "estado": registro.get("estado"),
                }
                arrFinal.append(objFormateado)

            # Preparar la respuesta
            objResponse = ResponseMessage.succ200.copy()
            objResponse['Respuesta'] = arrFinal
            return jsonify(objResponse)

        else:
            # Si no se encontraron registros, respondemos con un mensaje adecuado
            objResponse = ResponseMessage.succ200.copy()
            objResponse['Respuesta'] = "No se encontraron registros en el historial."
            return jsonify(objResponse)

    except Exception as e:
        print("Error al obtener el historial de riego:", e)
        objResponse = ResponseMessage.err500.copy()
        return jsonify(objResponse)
    
def actualizar_duracion_pausa_his(id):
    try:
        # Obtener el valor actual de pausasHis
        documento = dbConfig.find_one({"_id": ObjectId(id)}, {"duracionPausaHis": 1})

        if documento and "duracionPausaHis" in documento:
            nuevo_valor = documento["duracionPausaHis"]  # Tomamos el valor de pausasHis
        else:
            nuevo_valor = 0  # Si no existe pausasHis, ponemos 0

        # Reemplazar el valor de pausas con pausasHis
        result = dbConfig.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"duracionPausas": nuevo_valor}}  # Reemplaza pausas con pausasHis
        )

        # Verificar si la actualización fue exitosa
        if result.modified_count > 0:
            objResponse = ResponseMessage.succ200.copy()
            objResponse['Respuesta'] = {"mensaje": "pausa actualizada correctamente"}
        else:
            objResponse = ResponseMessage.err500.copy()
            objResponse['Respuesta'] = {"mensaje": "No se encontró el recurso para actualizar la pausa"}

        return jsonify(objResponse)

    except Exception as e:
        print("Error al actualizar la pausa:", e)
        objResponse = ResponseMessage.err500.copy()
        objResponse['Respuesta'] = {"mensaje": "Error interno al actualizar la pausa"}
        return jsonify(objResponse)

def actualizar_pausa_his(id):
    try:
        # Obtener el valor actual de pausasHis
        documento = dbConfig.find_one({"_id": ObjectId(id)}, {"pausasHis": 1})

        if documento and "pausasHis" in documento:
            nuevo_valor = documento["pausasHis"]  # Tomamos el valor de pausasHis
        else:
            nuevo_valor = 0  # Si no existe pausasHis, ponemos 0

        # Reemplazar el valor de pausas con pausasHis
        result = dbConfig.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"pausas": nuevo_valor}}  # Reemplaza pausas con pausasHis
        )

        # Verificar si la actualización fue exitosa
        if result.modified_count > 0:
            objResponse = ResponseMessage.succ200.copy()
            objResponse['Respuesta'] = {"mensaje": "pausa actualizada correctamente"}
        else:
            objResponse = ResponseMessage.err500.copy()
            objResponse['Respuesta'] = {"mensaje": "No se encontró el recurso para actualizar la pausa"}

        return jsonify(objResponse)

    except Exception as e:
        print("Error al actualizar la pausa:", e)
        objResponse = ResponseMessage.err500.copy()
        objResponse['Respuesta'] = {"mensaje": "Error interno al actualizar la pausa"}
        return jsonify(objResponse)