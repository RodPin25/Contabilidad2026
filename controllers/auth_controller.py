from flask import request, jsonify
from Services.auth_service import login_user, sign_up_user

def login_controller():
    # Recibimos el JSON del frontend
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Llamamos al servicio
    token = login_user(username, password)
    
    if token:
        return jsonify({"access_token": token}), 200
    return jsonify({"msg": "Credenciales inválidas"}), 401

def signup_controller():
    data = request.get_json()
    # Asegúrate de enviar idEmpresa e idRol según tu BD
    success = sign_up_user(
        data['username'], 
        data['password'], 
        data.get('idEmpresa', 1), 
        data.get('idRol', 2)
    )
    
    if success:
        return jsonify({"msg": "Usuario registrado exitosamente"}), 201
    return jsonify({"msg": "Error al registrar usuario"}), 400