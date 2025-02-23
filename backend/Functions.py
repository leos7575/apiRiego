from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId
import backend.GlobalInfo.Keys as keys
import backend.GlobalInfo.ResponseMessages as ResponseMessage

if keys.dbconn==None:
    mongoconect=MongoClient(keys.strConnection)
    keys.dbconn=mongoconect[keys.strDBConnection]
    dbUsers=keys.dbconn['usuarios']
    dbConfig=keys.dbconn['control_riego']
    
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
    
def insertSector(sector_data):
    try:
        # Verificar si se proporciona un ID
        if '_id' in sector_data and sector_data['_id']:
            # Convertir el ID a ObjectId si es necesario
            sector_id = ObjectId(sector_data['_id'])
            sector_data['_id'] = sector_id

            # Actualizar el documento existente
            result = dbConfig.update_one(
                {'_id': sector_id},
                {'$set': sector_data},
                upsert=False
            )
            
            # Verificar si se actualizó algún documento
            if result.matched_count == 0:
                objResponse = ResponseMessage['err500'].copy()
                objResponse['message'] = 'Documento no encontrado para actualizar.'
                return jsonify(objResponse)
        else:
            # Insertar un nuevo documento
            result = dbConfig.insert_one(sector_data)
            sector_id = result.inserted_id

        # Crear una respuesta con el ID del sector
        objResponse = ResponseMessage['succ200'].copy()
        objResponse['Respuesta'] = {"id": str(sector_id)}
        return jsonify(objResponse)
    except Exception as e:
        print("Error en insertSector", e)
        objResponse = ResponseMessage['err500'].copy()
        return jsonify(objResponse)
       