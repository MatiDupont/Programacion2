# Crear un programa en Python para mantener una lista de peliculas recomendadas por parte de los usuarios

from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import json
import subprocess

app = Flask(__name__)

with open("Proyecto Final/usuarios.json", encoding = "utf-8") as archivo_usuarios:
    usuarios_data = json.load(archivo_usuarios)

with open("Proyecto Final/peliculas.json", encoding = "utf-8") as archivo_peliculas:
    peliculas_data = json.load(archivo_peliculas)
    
with open("Proyecto Final/directores.json", encoding = "utf-8") as archivo_directores:
    directores_data = json.load(archivo_directores)
    
with open("Proyecto Final/usuarios.json", encoding = "utf-8") as archivo_usuarios:
    usuarios_data = json.load(archivo_usuarios) 

def mostrar_peliculas(peliculas):
    for pelicula in peliculas[-10:]:
        print("Titulo: " + pelicula["titulo"])
        print("Año: " + pelicula["anio"])
        print("Director: " + pelicula["director"])
        print("Genero: " + pelicula["genero"])
        print("Sinopsis:" + pelicula["sinopsis"])
        print("Imagen:" + pelicula["link"])
        print("Comentarios:" + pelicula["comentarios"])
        print("Alta:" + str(pelicula["alta"]))
        print("---------------------------------")
            
def existe_pelicula(titulo):
    titulo_pelicula = next((pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["titulo"].lower() == titulo.lower()),None)
    if titulo_pelicula:
        return True
    else:
        return False   

def existe_director(nombre):
    nombre_director = next((director for director in directores_data[0]["directores"] if director["nombre_director"].lower() == nombre.lower()), None)
    if nombre_director:
        return True
    else:
        return False
    
def existe_genero(genero):
    pelicula_genero = next((gen for gen in peliculas_data[1]["generos"] if gen["nombre_genero"].lower() == genero.lower()), None)
    if pelicula_genero:
        return True
    else:
        return False
    
def existe_usuario(nombre):
    nombre_usuario = next((usuario for usuario in usuarios_data[0]["usuarios"] if usuario["user"] == nombre), None)
    if nombre_usuario:
        return True
    else:
        return False
        
def buscar_peliculas(dato):
    resultados = []
    for pelicula in peliculas_data[0]["peliculas"]:
        if ((pelicula["titulo"].lower()).startswith(dato)):
            resultados.append(pelicula)
    return resultados

def buscar_directores(dato):
    resultados = []
    for director in directores_data[0]["directores"]:
        if ((director["nombre_director"].lower()).startswith(dato)):
            resultados.append(director)
    return resultados
    
#Ademas, el sistema debera proveer servicios web a traves de endpoints para ser consultados por otros sistemas y devolver un documento de formato JSON.
#Los servicios que se necesitan son:
# Ruta de inicio
@app.route("/", methods = ["GET"])
def home():
    return "Bienvenido al sistema de peliculas 'Film Quest"

# 1. Devolver la lista de directores presentes en la plataforma
@app.route("/peliculas/directores", methods = ["GET"])
def devolver_directores():   
    directores = [director["nombre_director"] for director in directores_data[0]["directores"]]
    return jsonify(directores), HTTPStatus.OK

# 2. Devolver la lista de generos presentes en la plataforma
@app.route("/peliculas/generos/todos", methods = ["GET"])
def devolver_todos_generos():
    total_generos = [genero["nombre_genero"] for genero in peliculas_data[1]["generos"]]
    return jsonify(total_generos),  HTTPStatus.OK

@app.route("/peliculas/generos/presentes", methods = ["GET"])
def devolver_generos():
    generos = list(set([pelicula["genero"] for pelicula in peliculas_data[0]["peliculas"]]))
    return jsonify(generos), HTTPStatus.OK

# 3. Devolver la lista de peliculas dirigidas por un director en particular
@app.route("/peliculas/directores/<director>", methods = ["GET"])
def devolver_peliculas_por_director(director):
    encontrar_director = next((dire for dire in directores_data[0]["directores"] if dire["nombre_director"] == director), None)
    if encontrar_director:
        peliculas = [pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["director"] == director]
        return jsonify(peliculas), HTTPStatus.OK
    else:
        return jsonify("Director no encontrado."), HTTPStatus.NOT_FOUND

# 4. Devolver las peliculas que tienen imagen de portada agregada
@app.route("/peliculas/imagen", methods = ["GET"])
def devolver_peliculas_con_imagen():
    peliculas_imagen = [pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula.get("link") != ""]
    return jsonify(peliculas_imagen), HTTPStatus.OK

# 5. ABM de cada pelicula
# ALTA (A) DE PELICULAS
@app.route("/peliculas/agregar/nueva", methods = ["POST"])
def agregar_pelicula():
    datos_json = request.get_json()
    print(datos_json)
    
    print(len(datos_json))
    
    if(len(datos_json) < 7):
        print("Error!, faltan campos en el pedido.")
        exit(0)
    elif(len(datos_json) > 7):
        print("Error!, exceso de campos en el pedido.")
        exit(0)
    else: 
        if (existe_pelicula(datos_json["titulo"]) == False):
            id_pelicula = len(peliculas_data[0]["peliculas"]) + 1
            nueva_pelicula = {
            "id":id_pelicula,
            "titulo":datos_json["titulo"],
            "anio":datos_json["anio"],
            "director":datos_json["director"],
            "genero":datos_json["genero"],
            "sinopsis":datos_json["sinopsis"],
            "link":datos_json["link"],
            "comentarios":datos_json["comentarios"],
            #la key de la value alta, la tengo que traer de donde llamo a la funcion
            "alta": 1
            }
        
            peliculas_data[0]["peliculas"].append(nueva_pelicula)
        
            with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                json.dump(peliculas_data, archivo_peliculas, indent = 4)
              
            print("Se cargo la pelicula nueva con exito.")
            return jsonify(nueva_pelicula["titulo"]), HTTPStatus.OK
        else:
            print("Error!. Pelicula ya cargada en base de datos.")
            return jsonify("No es posible agregar esa pelicula dado que ya se encuentra registrada en la base de datos del sistema."), HTTPStatus.BAD_REQUEST

# MODIFICACION (M) DE PELICULAS 
# Un usuario puede editar la informacion de una pelicula ya cargada, pero no puede borrar ni editar comentarios de otros usuarios          
@app.route("/peliculas/editar/<id>", methods = ["PUT"])
def editar_pelicula(id):
    datos_json = request.get_json()
    
    pelicula_editar = next((pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["id"] == int(id)), None)
    
    if pelicula_editar:
        print("Pelicula encontrada.")
        
        if (existe_pelicula(datos_json["titulo"]) == False):
            titulo = datos_json["titulo"] 
            anio = datos_json["anio"] 
            director = datos_json["director"] 
            genero = datos_json["genero"] 
            sinopsis = datos_json["sinopsis"] 
            imagen = datos_json["link"] 
            comentarios = datos_json["comentarios"] 
            
            pelicula_editar["id"] = id
            pelicula_editar["titulo"] = titulo
            pelicula_editar["anio"] = anio
            pelicula_editar["director"] = director
            pelicula_editar["genero"] = genero
            pelicula_editar["sinopsis"] = sinopsis
            pelicula_editar["link"] = imagen
            pelicula_editar["comentarios"] = comentarios
            
            with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                json.dump(peliculas_data, archivo_peliculas, indent = 4)
            
            print("La pelicula ha sido editada correctamente.")
            return jsonify(pelicula_editar["titulo"]), HTTPStatus.OK
        else:
            print("Error al guardar los cambios!. Nombre de pelicula ya registrado.")
            return jsonify("No es posible modificar el nombre de la pelicula dado que ya se encuentra en la base de datos del sistema."), HTTPStatus.BAD_REQUEST
    else:
        print("Error!. Pelicula no encontrada.")
        return jsonify("No se encontro la pelicula con el ID especificado."), HTTPStatus.NOT_FOUND

# BAJA (B) DE PELICULAS   
# Un usuario puede eliminar una pelicula solo si esta no tiene comentarios de otros usuarios   
@app.route("/peliculas/eliminar/<id>", methods = ["DELETE"])
def eliminar_pelicula(id):
    peliculas_eliminar = next((pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["id"] == int(id)), None)
    
    if peliculas_eliminar:
        if (peliculas_eliminar["comentarios"] != ""):
            peliculas_data[0]["peliculas"].remove(peliculas_eliminar)
            
            with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                json.dump(peliculas_data, archivo_peliculas, indent = 4)
                
            print("La pelicula ha sido eliminada correctamente.")
            return jsonify(peliculas_eliminar["titulo"]), HTTPStatus.OK
        else:
            print("Error!. Pelicula con comentarios.")
            return jsonify("No se puede eliminar la pelicula porque tiene comentarios de otros usuarios."), HTTPStatus.BAD_REQUEST
    else:
        print("Error!. Pelicula no encontrada.")
        return jsonify("No se encontro la pelicula con el ID especificado."), HTTPStatus.NOT_FOUND

# Buscador de peliculas y directores
# BUSCADOR DE PELICULAS
@app.route("/buscador/peliculas", methods = ["POST"])
def buscador_peliculas():
    datos_json = request.get_json()
    
    for key, value in datos_json.items():
        print(value)
        
    resultados_peliculas = buscar_peliculas(value)
    
    resultado = {
        "peliculas": resultados_peliculas
    }
    
    return jsonify(resultado), HTTPStatus.OK

# BUSCADOR DE DIRECTORES
@app.route("/buscador/directores", methods = ["POST"])
def buscador_directores():
    datos_json = request.get_json()
    
    for key, value in datos_json.items():
        print(value)
        
    resultados_directores = buscar_directores(value)
    
    resultado = {
        "directores": resultados_directores
    }
    
    return jsonify(resultado), HTTPStatus.OK

# Implementar ABM de directores y generos
# ALTA (A) DE DIRECTORES
@app.route("/directores/agregar/nuevo", methods = ["POST"])
def agregar_director():
    datos_json = request.get_json()
    
    if (existe_director(datos_json["nombre_director"]) == False):
        id_director = len(directores_data[0]["directores"]) + 1
        nuevo_director = {
            "id_director":id_director,
            "nombre_director":datos_json["nombre_director"]
        }
        
        directores_data[0]["directores"].append(nuevo_director)
        
        with open("Proyecto Final/directores.json", "w", encoding = "utf-8") as archivo_directores:
                json.dump(directores_data, archivo_directores, indent = 4)
               
        print("Se cargo el director nueva con exito.")
        return jsonify(nuevo_director["nombre_director"]), HTTPStatus.OK
    else:
        print("Error!. Director ya cargado en base de datos.")
        return jsonify("No es posible agregar ese director dado que ya se encuentra registrado en la base de datos del sistema."), HTTPStatus.BAD_REQUEST

# MODIFICACION (M) DE DIRECTORES
@app.route("/directores/editar/<id>", methods = ["PUT"])
def editar_director(id):
    datos_json = request.get_json()
    
    director_editar = next((dire for dire in directores_data[0]["directores"] if dire["id_director"] == int(id)), None)
    
    if director_editar:
        print("Director encontrado.")
        
        nombre = datos_json["nombre_director"]
        
        for pelicula in peliculas_data[0]["peliculas"]:
            if (pelicula["director"] == director_editar["nombre_director"]): 
                pelicula["director"] =  nombre
                print("modificado aca tambien!!!")
        
        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
            json.dump(peliculas_data, archivo_peliculas, indent = 4)

        director_editar["nombre_director"] = nombre
                
        with open("Proyecto Final/directores.json", "w", encoding = "utf-8") as archivo_directores:
            json.dump(directores_data, archivo_directores, indent = 4)
        
        print("El director ha sido editado correctamente.")
        return jsonify(director_editar["nombre_director"]), HTTPStatus.OK
    else:
        print("Error!. Director no encontrado.")
        return jsonify("No se encontro el director con el ID especificado."), HTTPStatus.NOT_FOUND

# BAJA (B) DE DIRECTORES
@app.route("/directores/eliminar/<id>", methods = ["DELETE"])
def eliminar_director(id):
    director_eliminar = next((dire for dire in directores_data[0]["directores"] if dire["id_director"] == int(id)), None)
    
    if director_eliminar:
        print("Director encontrado.")
        
        for pelicula in peliculas_data[0]["peliculas"]:
            if (pelicula["director"] == director_eliminar["nombre_director"]):
                pelicula["director"] = "Desconocido"
                print("Eliminado aca tambien!!!")
        
        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
            json.dump(peliculas_data, archivo_peliculas, indent = 4)
            
        directores_data[0]["directores"].remove(director_eliminar)
        
        with open("Proyecto Final/directores.json", "w", encoding = "utf-8") as archivo_directores:
            json.dump(directores_data, archivo_directores, indent = 4)
        
        print("El director ha sido eliminado correctamente.")
        return jsonify(director_eliminar["nombre_director"]), HTTPStatus.OK
    else:
        print("Error!. Director no encontrado.")
        return jsonify("No se encontro el director con el ID especificado."), HTTPStatus.NOT_FOUND

# ALTA (A) DE GENEROS    
@app.route("/peliculas/generos/agregar/nuevo", methods = ["POST"])
def agregar_genero():
    datos_json = request.get_json()
    
    if (existe_genero(datos_json["nombre_genero"]) == False):      
        id_genero = len(peliculas_data[1]["generos"]) + 1
        nuevo_genero = {
            "nombre_genero":datos_json["nombre_genero"],
            "id_genero":id_genero
        }
        
        peliculas_data[1]["generos"].append(nuevo_genero)
        
        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                json.dump(peliculas_data, archivo_peliculas, indent = 4)
               
        print("Se cargo el genero nuevo con exito.")
        return jsonify(nuevo_genero["nombre_genero"]), HTTPStatus.OK
    else:
        print("Error!. Genero ya cargado en base de datos.")
        return jsonify("No es posible agregar ese genero dado que ya se encuentra registrado en la base de datos del sistema."), HTTPStatus.BAD_REQUEST

# MODIFICACION (M) DE GENEROS        
@app.route("/peliculas/generos/editar/<id>", methods = ["PUT"])
def editar_genero(id):
    datos_json = request.get_json()
    
    genero_editar = next((genero for genero in peliculas_data[1]["generos"] if genero["id_genero"] == int(id)), None)
    
    if genero_editar:
        print("Genero encontrado.")
        
        nombre = datos_json["nombre_genero"]
        
        for pelicula in peliculas_data[0]["peliculas"]:
            if (pelicula["genero"] == genero_editar["nombre_genero"]): 
                pelicula["genero"] =  nombre
                print("modificado aca tambien!!!")

        genero_editar["nombre_genero"] = nombre
                
        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
            json.dump(peliculas_data, archivo_peliculas, indent = 4)
        
        print("El genero ha sido editado correctamente.")
        return jsonify(genero_editar["nombre_genero"]), HTTPStatus.OK
    else:
        print("Error!. Genero no encontrado.")
        return jsonify("No se encontro el genero con el ID especificado."), HTTPStatus.NOT_FOUND
    
# BAJA (B) DE GENEROS
@app.route("/peliculas/generos/eliminar/<id>", methods = ["DELETE"])
def eliminar_genero(id):
    genero_eliminar = next((genero for genero in peliculas_data[1]["generos"] if genero["id_genero"] == int(id)), None)
    
    if genero_eliminar:
        print("Genero encontrado.")
        
        for pelicula in peliculas_data[0]["peliculas"]:
            if (pelicula["genero"] == genero_eliminar["nombre_genero"]):
                pelicula["genero"] = "Desconocido"
                print("Eliminado aca tambien!!!")
            
        peliculas_data[1]["generos"].remove(genero_eliminar)
        
        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
            json.dump(peliculas_data, archivo_peliculas, indent = 4)
        
        print("El genero ha sido eliminado correctamente.")
        return jsonify(genero_eliminar["nombre_genero"]), HTTPStatus.OK
    else:
        print("Error!. Genero no encontrado.")
        return jsonify("No se encontro el genero con el ID especificado."), HTTPStatus.NOT_FOUND

# ALTA (A) DE USUARIOS
@app.route("/usuarios/agregar/nuevo", methods = ["POST"])
def agregar_usuario():
    datos_json = request.get_json()
    
    if (existe_usuario(datos_json["user"]) == False):
        id_usuario = len(usuarios_data[0]["usuarios"]) + 1
        nuevo_usuario = {
            "id":id_usuario,
            "user":datos_json["user"],
            "password":datos_json["password"],
            "permiso":datos_json["permiso"]
        }
        
        usuarios_data[0]["usuarios"].append(nuevo_usuario)
        
        with open("Proyecto Final/usuarios.json", "w", encoding = "utf-8") as archivo_usuarios:
            json.dump(usuarios_data, archivo_usuarios, indent = 4)
        
        print("Se cargo el usuario nuevo con exito.")
        return jsonify(nuevo_usuario["user"]), HTTPStatus.OK
    else:
        print("Error!. Usuario ya cargado en base de datos.")
        return jsonify("No es posible agregar ese usuario dado que ya se encuentra registrado en la base de datos del sistema."), HTTPStatus.BAD_REQUEST
    
# MODIFICACION (M) DE USUARIOS
@app.route("/usuarios/editar/<id>", methods = ["PUT"])
def editar_usuario(id):
    datos_json = request.get_json()
    
    usuario_editar = next((usuario for usuario in usuarios_data[0]["usuarios"] if usuario["id"] == int(id)), None)

    if usuario_editar:
        print("Usuario encontrado.")
        
        if (existe_usuario(datos_json[datos_json["user"]]) == False):
            usuario = datos_json["user"]
            contrasenia = datos_json["password"]
            permiso = datos_json["permiso"]
            
            usuario_editar["id"] = id
            usuario_editar["user"] = usuario
            usuario_editar["password"] = contrasenia
            usuario_editar["permiso"] = permiso
            
            with open("Proyecto Final/usuarios.json", "w", encoding = "utf-8") as archivo_usuarios:
                json.dump(usuarios_data, archivo_usuarios, indent = 4)
        
            print("El usuario ha sido editado correctamente.")
            return jsonify(usuario_editar["user"]), HTTPStatus.OK
        else:
            print("Error al guardar los cambios!. Nombre de usuario ya registrado.")
            return jsonify("No es posible modificar el nombre de usuario dado que ya se encuentra en la base de datos del sistema."), HTTPStatus.BAD_REQUEST
    else:
        print("Error!. Usuario no encontrado.")
        return jsonify("No se encontro el usuario con el ID especificado."), HTTPStatus.NOT_FOUND
    
# BAJA (B) DE USUARIOS
@app.route("/usuarios/eliminar/<id>", methods = ["DELETE"])
def eliminar_usuario(id):
    usuario_eliminar = next((usuario for usuario in usuarios_data[0]["usuarios"] if usuario["id"] == int(id)), None)

    if usuario_eliminar:
        print("Usuario encontrado.")
        
        if (usuario_eliminar["permiso"] == "public"):
            usuarios_data[0]["usuarios"].remove(usuario_eliminar)
            
            with open("Proyecto Final/usuarios.json", "w", encoding = "utf-8") as archivo_usuarios:
                json.dump(usuarios_data, archivo_usuarios, indent = 4)
        
            print("El usuario ha sido eliminado correctamente.")
            return jsonify(usuario_eliminar["user"]), HTTPStatus.OK
        else:
            print("Error de solicitud!. No es posible eliminar a un usuario con permiso admin")
            return jsonify("No es posible eliminar a un usuario con permiso admin."), HTTPStatus.BAD_REQUEST
    else:
        print("Error!. Usuario no encontrado.")
        return jsonify("No se encontro el usuario con el ID especificado."), HTTPStatus.NOT_FOUND
    
# ASIGNAR PERMISOS DE ADMINISTRADOR O USUARIO PUBLICO
@app.route("/usuarios/permisos/<id>", methods = ["PUT"])
def asignar_permisos(id):
    datos_json = request.get_json()
    
    usuario = next((user for user in usuarios_data[0]["usuarios"] if user["id"] == int(id)), None)
    
    if usuario:
        print("Usuario encontrado.")
        
        if (datos_json["permiso"] == "admin"):
            usuario["permiso"] = "admin"
        else:
            usuario["permiso"] = "public"
        
        with open("Proyecto Final/usuarios.json", "w", encoding = "utf-8") as archivo_usuarios:
            json.dump(usuarios_data, archivo_usuarios, indent = 4)
        
        print("El permiso de usuario ha sido modificado correctamente.")
        return jsonify(usuario["permiso"]), HTTPStatus.OK
    else:
        print("Error!. Usuario no encontrado.")
        return jsonify("No se encontro el usuario con el ID especificado."), HTTPStatus.NOT_FOUND

def mostrar_menu():
    print("\n --- MENU DE OPCIONES ---")
    print("1. AGREGAR PELICULA")
    print("2. EDITAR PELICULA")
    print("3. ELIMINAR PELICULA")
    print("4. SALIR\n")
    
    opcion = int(input("Ingrese una opcion: "))
    
    return opcion

def main():
    print("-----------------------------------------------")
    print("BIENVENIDO AL SISTEMA DE PELICULAS 'FILM QUEST'")
    print("-----------------------------------------------")

    # El programa debe permitir a un usuario ingresar usuario y contraseña para ingresar al mismo
    username = input("INGRESE NOMBRE DE USUARIO: ")
    password = input ("INGRESE SU CONTRASEÑA: ")
    print()
    usuario = next((usuario for usuario in usuarios_data[0]["usuarios"] if usuario["user"] == username and usuario["password"] == password), None)
    
    if usuario:
        id_usuario = str(usuario["id"])
        print("¡Usuario encontrado en la base de datos!")
        
        if (usuario["permiso"] == "admin"):
            while(True):          
                opcion = mostrar_menu()
                
                if (opcion == 1):
                    postman_path = "C:/Users/Usuario/Documents/Matias/PROGRA2 2023/Postman/Postman-win64-Setup.exe"
                    collection_uid = "<bf934137-5e4f-4804-83e7-2b007cefcfa6>"
                    action = "openRequest"
                    request_uid = "<24275799-deb8045e-8cdc-402a-a023-f78167e96ae7>"
    
                    url = f"postman://run/{collection_uid}?action={action}&uid={request_uid}"
                    subprocess.run([postman_path, url])
                    app.run(debug = True)
                elif (opcion == 2):
                    postman_path = "C:/Users/Usuario/Documents/Matias/PROGRA2 2023/Postman/Postman-win64-Setup.exe"
                    collection_uid = "<bf934137-5e4f-4804-83e7-2b007cefcfa6>"
                    action = "openRequest"
                    request_uid = "<24275799-2e49f5d7-e2d8-4ad5-8093-27e3931f81bf>"
                    
                    url = f"postman://run/{collection_uid}?action={action}&uid={request_uid}"
                    subprocess.run([postman_path, url])
                    app.run(debug = True)
                elif (opcion == 3):
                    postman_path = "C:/Users/Usuario/Documents/Matias/PROGRA2 2023/Postman/Postman-win64-Setup.exe"
                    collection_uid = "bf934137-5e4f-4804-83e7-2b007cefcfa6"
                    action = "openRequest"
                    request_uid = "24275799-65583ea6-092e-4905-9729-fc1dacfd037b"
                    
                    url = f"postman://run/{collection_uid}?action={action}&uid={request_uid}"
                    subprocess.run([postman_path, url])
                    app.run(debug = True)
                elif (opcion == 4):
                    print("Gracias por utilizar el sistema. Hasta luego!")
                    exit(0)
                else:
                    print("Opcion invalida. Intente nuevamente.") 
        else:
            #El programa tendra un modulo publico, es decir, una pantalla que puede ser accedida sin necesidad de tener cuenta ni estar logueado
            #En esa pantalla se mostraran las ultimas 10 peliculas agregadas al sistema independientemente del usuario
            print("Usted solo puede acceder al modulo publico ya que no esta logueado en el sistema o no tiene los permisos necesarios para acceder al modulo privado.")
            print("A continuacion se mostraran las ultimas 10 peliculas agregadas al sistema:\n")
            mostrar_peliculas(peliculas_data[0]["peliculas"])     
            print("\nGracias por utilizar el sistema, hasta la proxima!")       
    else:
        print("Error, el usuario no fue encontrado en la base de datos.")      
    
if __name__ == "__main__":
    main()  