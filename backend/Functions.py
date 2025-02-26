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
        # Insertar el sector en la base de datos
        result = dbConfig.insert_one(sector_data)
        
        # Crear una respuesta con el ID del nuevo sector
        objResponse = ResponseMessage.succ200.copy()
        objResponse['Respuesta'] = {"id": str(result.inserted_id)}
        return jsonify(objResponse)
    except Exception as e:
        print("Error en insertUser", e)
        objResponse = ResponseMessage.err500.copy()
        return jsonify(objResponse)
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
                }
                arrFinalRiego.append(objFormateado)
        objResponse=ResponseMessage.succ200.copy()
        objResponse['Respuesta']=arrFinalRiego
        return jsonify(objResponse)
    except Exception as e:
        print("Error en fnMensaje",e)
        objResponse=ResponseMessage.err500.copy()
        return jsonify(objResponse)