# Crear un programa en Python para mantener una lista de peliculas recomendadas por parte de los usuarios

from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import json
import time

app = Flask(__name__)

with open("Proyecto Final/usuarios.json", encoding = "utf-8") as archivo_usuarios:
    usuarios_data = json.load(archivo_usuarios)

with open("Proyecto Final/peliculas.json", encoding = "utf-8") as archivo_peliculas:
    peliculas_data = json.load(archivo_peliculas)
    
with open("Proyecto Final/directores.json", encoding = "utf-8") as archivo_directores:
    directores_data = json.load(archivo_directores)
    
def mostrar_peliculas(peliculas):
    for pelicula in peliculas[-10:]:
        print("Id: " + str(pelicula["id"]))
        print("Titulo: " + pelicula["titulo"])
        print("Año: " + pelicula["anio"])
        print("Director: " + pelicula["director"])
        print("Genero: " + pelicula["genero"])
        print("Sinopsis: " + pelicula["sinopsis"])
        print("Imagen: " + pelicula["link"])
        print("Comentarios: ")
        for comentario in pelicula["comentarios"]:
            print("User " + str(comentario["usuario_id"]) + ", comentó: " + comentario["comentario"])
        if len(pelicula["comentarios"]) == 0:
            print("Por el momento no hay comentarios sobre esta pelicula. Deje el suyo!")
        print("Alta: " + str(pelicula["alta"]))
        print("Puntuaciones: ")
        for puntuacion in pelicula["puntuaciones"]:
            print("User " + str(puntuacion["usuario_id"]) + ", puntuó: " + puntuacion["puntuacion"])
        if len(pelicula["puntuaciones"]) == 0:
            print("Por el momento no hay puntuaciones sobre esta pelicula. Deje la suya!")
        print("Contador: " + str(pelicula["contador"]))
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
        if ((pelicula["titulo"].lower()).startswith(dato.lower())):
            resultados.append(pelicula)
    return resultados

def buscar_directores(dato):
    resultados = []
    for director in directores_data[0]["directores"]:
        if ((director["nombre_director"].lower()).startswith(dato.lower())):
            resultados.append(director)
    return resultados
    
#Ademas, el sistema debera proveer servicios web a traves de endpoints para ser consultados por otros sistemas y devolver un documento de formato JSON.
#Los servicios que se necesitan son:
# Ruta de inicio
@app.route("/", methods = ["GET"])
def home():
    return "BIENVENIDO AL SISTEMA DE PELICULAS 'FILM QUEST"

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

#@app.route("/peliculas/generos/presentes", methods = ["GET"])
#def devolver_generos():
#    generos = list(set([pelicula["genero"] for pelicula in peliculas_data[0]["peliculas"]]))
#    return jsonify(generos), HTTPStatus.OK

# 3. Devolver la lista de peliculas dirigidas por un director en particular
@app.route("/peliculas/directores/<director>", methods = ["GET"])
def devolver_peliculas_por_director(director):
    encontrar_director = next((dire for dire in directores_data[0]["directores"] if dire["nombre_director"].lower() == director.lower()), None)
    flag = 0
    peliculas = []
    if encontrar_director:
        for pelicula in peliculas_data[0]["peliculas"]:
            if pelicula["director"].lower() == director.lower():
                flag = 1
                peliculas.append(pelicula)

        if flag == 0:
            return jsonify("POR EL MOMENTO NO HAY PELICULAS CARGADAS EN EL SISTEMA DE ESE DIRECTOR."), HTTPStatus.NOT_FOUND
        
        return jsonify(peliculas), HTTPStatus.OK
    else:
        return jsonify("DIRECTOR NO ENCONTRADO."), HTTPStatus.NOT_FOUND

# 4. Devolver las peliculas que tienen imagen de portada agregada
@app.route("/peliculas/imagen", methods = ["GET"])
def devolver_peliculas_con_imagen():
    peliculas_portada = []
    for pelicula in peliculas_data[0]["peliculas"]:
        if pelicula.get("link") != "":
            peliculas_portada.append(pelicula["titulo"])
    return jsonify(peliculas_portada), HTTPStatus.OK

# 5. ABM de cada pelicula
# ALTA (A) DE PELICULAS
@app.route("/peliculas/agregar/nueva", methods = ["POST"])
def agregar_pelicula():
    datos_json = request.get_json()
    
    print(len(datos_json))
    
    if(len(datos_json) < 9):
        print("ERROR!, FALTAN CAMPOS EN EL PEDIDO.")
        exit(0)
    elif(len(datos_json) > 9):
        print("ERROR!, EXCESO DE CAMPOS EN EL PEDIDO.")
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
            "comentarios":[
                {
                    "usuario_id": datos_json["usuario_id"],
                    "comentario": datos_json["comentarios"]
                }
            ],
            "alta": datos_json["usuario_id"],
            "puntuaciones": [
                {
                    "usuario_id": datos_json["usuario_id"],
                    "puntuacion": datos_json["puntuaciones"]
                }
            ],
            "contador": 0
            }
        
            peliculas_data[0]["peliculas"].append(nueva_pelicula)
        
            with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                json.dump(peliculas_data, archivo_peliculas, indent = 4)
              
            print("SE CARGO LA PELICULA NUEVA CON EXITO DESDE POSTMAN.")
            return jsonify(nueva_pelicula["titulo"]), HTTPStatus.OK
        else:
            print("ERROR!. PELICULA YA CARGADA EN BASE DE DATOS.")
            return jsonify("NO ES POSIBLE AGREGAR ESA PELICULA DADO QUE YA SE ENCUENTRA REGISTRADA EN LA BASE DE DATOS DEL SISTEMA."), HTTPStatus.BAD_REQUEST

# MODIFICACION (M) DE PELICULAS 
# Un usuario puede editar la informacion de una pelicula ya cargada, pero no puede borrar ni editar comentarios de otros usuarios          
@app.route("/peliculas/editar/<titulo>", methods = ["PUT"])
def editar_pelicula(titulo):
    datos_json = request.get_json()
    
    pelicula_editar = next((pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["titulo"].lower() == titulo.lower()), None)
    
    if pelicula_editar:
        print("PELICULA ENCONTRADA.")
        
        if (existe_pelicula(datos_json["titulo"]) == False):
            titulo = datos_json["titulo"] 
            anio = datos_json["anio"] 
            director = datos_json["director"] 
            genero = datos_json["genero"] 
            sinopsis = datos_json["sinopsis"] 
            imagen = datos_json["link"] 
            if pelicula_editar["comentarios"]["usuario_id"] == datos_json["usuario_id"]:
                comentarios = datos_json["comentarios"] 

            pelicula_editar["titulo"] = titulo
            pelicula_editar["anio"] = anio
            pelicula_editar["director"] = director
            pelicula_editar["genero"] = genero
            pelicula_editar["sinopsis"] = sinopsis
            pelicula_editar["link"] = imagen
            pelicula_editar["comentarios"]["comentario"] = comentarios
            
            with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                json.dump(peliculas_data, archivo_peliculas, indent = 4)
            
            print("LA PELICULA HA SIDO EDITADA CORRECTAMENTE.")
            return jsonify(pelicula_editar["titulo"]), HTTPStatus.OK
        else:
            print("ERROR!. NOMBRE DE LA PELICULA YA REGISTRADO.")
            return jsonify("NO ES POSIBLE MODIFICAR EL NOMBRE DE LA PELICULA DADO QUE EL MISMO YA SE ENCUENTRA UTILIZADO EN LA BASE DE DATOS DEL SISTEMA."), HTTPStatus.BAD_REQUEST
    else:
        print("ERROR!. PELICULA NO ENCONTRADA.")
        return jsonify("NO SE ENCONTRO UNA PELICULA CON ESE TITULO."), HTTPStatus.NOT_FOUND

# BAJA (B) DE PELICULAS   
# Un usuario puede eliminar una pelicula solo si esta no tiene comentarios de otros usuarios   
@app.route("/peliculas/eliminar/<titulo>", methods = ["DELETE"])
def eliminar_pelicula(titulo):
    datos_json = request.get_json()
    
    pelicula_eliminar = next((pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["titulo"].lower() == titulo.lower()), None)

    if pelicula_eliminar:
        comentarios = pelicula_eliminar["comentarios"]
        print(comentarios)
        for comentario in comentarios:
            comentario_usuario_id = comentario["usuario_id"]
            if comentario_usuario_id != datos_json["usuario_id"]:  
                print("ERROR!. PELICULA CON COMENTARIOS.")
                return jsonify("ERROR!. NO ES POSIBLE ELIMINAR LA PELICULA PORQUE TIENE COMENTARIOS HECHOS POR OTROS USUARIOS."), HTTPStatus.BAD_REQUEST
        
        peliculas_data[0]["peliculas"].remove(pelicula_eliminar)
            
        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
            json.dump(peliculas_data, archivo_peliculas, indent = 4)
                    
        print("LA PELICULA HA SIDO ELIMINADA CORRECTAMENTE.")
        return jsonify(pelicula_eliminar["titulo"]), HTTPStatus.OK
    else:
        print("ERROR!. PELICULA NO ENCONTRADA.")
        return jsonify("NO SE ENCONTRO UNA PELICULA CON ESE TITULO."), HTTPStatus.NOT_FOUND
    
# PAGINADO
# Implementar paginado. Si la cantidad de elementos a mostrar por una pantalla es demasiada, mostrar un subconjunto y brindar la posibilidad de moverse a otra pantalla.
@app.route("/peliculas/<pagina>", methods = ["GET"])
def obtener_peliculas_paginadas(pagina):
    elementos_por_pagina = 3
    
    inicio = (int(pagina) - 1) * elementos_por_pagina
    fin = inicio + elementos_por_pagina
    
    peliculas_paginadas = peliculas_data[0]["peliculas"][inicio:fin]
    
    return jsonify(peliculas_paginadas), HTTPStatus.OK

#if __name__ == "__main__":
#    app.run(debug=True)
        
def mostrar_menu():
    print("\n --- MENU DE OPCIONES ---")
    print("1. AGREGAR PELICULA") #HECHO
    print("2. EDITAR PELICULA") #HECHO
    print("3. ELIMINAR PELICULA") #HECHO
    print("4. BUSCAR DIRECTOR") #HECHO
    print("5. BUSCAR PELICULA") #HECHO
    print("6. AÑADIR USUARIO") #HECHO
    print("7. MODIFICAR USUARIO") #HECHO
    print("8. ELIMINAR USUARIO") #HECHO
    print("9. ASIGNAR PERMISOS A UN USUARIO") #HECHO
    print("10. AÑADIR DIRECTOR") #HECHO
    print("11. MODIFICAR DIRECTOR") #HECHO
    print("12. ELIMINAR DIRECTOR") #HECHO
    print("13. AÑADIR GENERO") #HECHO
    print("14. MODIFICAR GENERO") #HECHO
    print("15. ELIMINAR GENERO") #HECHO
    print("16. AÑADIR PUNTUACION") #HECHO
    print("17. MODIFICAR PUNTUACION") #HECHO
    print("18. ELIMINAR PUNTUACION") #HECHO
    print("19. DIRECTORES CARGADOS") #HECHO
    print("20. GENEROS CARGADOS") #HECHO
    print("21. BUSCAR PELICULAS POR DIRECTOR") #HECHO
    print("22. VER PELICULAS CON PORTADA") #HECHO
    print("23. SALIR\n") #HECHO
    
    opcion = int(input("Ingrese una opcion: "))
    print()
    
    return opcion

print("-----------------------------------------------")
print("BIENVENIDO AL SISTEMA DE PELICULAS 'FILM QUEST'")
print("-----------------------------------------------")

# El programa debe permitir a un usuario ingresar usuario y contraseña para ingresar al mismo
username = input("INGRESE NOMBRE DE USUARIO: ")
password = input ("INGRESE SU CONTRASEÑA: ")
print()
usuario = next((usuario for usuario in usuarios_data[0]["usuarios"] if usuario["user"] == username and usuario["password"] == password), None)
    
global id_usuario
if usuario:
    id_usuario = usuario["id"]
    print(id_usuario)
    print("¡USUARIO ENCONTRADO EN LA BASE DE DATOS!")
    print("DISFRUTE DEL SISTEMA.")
    print()
        
    if (usuario["permiso"] == "admin"):
        while(True):          
            opcion = mostrar_menu()
                
            if (opcion == 1):
                print("++++++++++++++++++++++++++")
                print("SECCION 'AGREGAR PELICULA'")
                print("++++++++++++++++++++++++++")
                print()
                usuario_id = id_usuario

                print("LISTA DE DIRECTORES DISPONIBLES EN EL SISTEMA: ")
                for direc in directores_data[0]["directores"]:
                    print(direc["nombre_director"], end = ", ")
                print()
                director = input("NOMBRE DEL DIRECTOR (SELECCIONAR): ")
                while not existe_director(director):
                    print("DIRECTOR NO ENCONTRADO.")
                    director = input("NOMBRE DEL DIRECTOR (SELECCIONAR): ")
                titulo = input("NOMBRE DE LA PELICULA: ")
                anio = input("AÑO DE ESTRENO: ")
                print("LISTA DE GENEROS DISPONIBLES EN EL SISTEMA: ")
                for genre in peliculas_data[1]["generos"]:
                    print(genre["nombre_genero"], end = ", ")
                print()
                genero = input("GENERO (SELECCIONAR): ")
                while not existe_genero(genero):
                    print("GENERO NO ENCONTRADO.")
                    genero = input("GENERO (SELECCIONAR): ")
                sinopsis = input("SINOPSIS: ")
                link_imagen = input("IMAGEN DE PORTADA: ")
                comentario = input("COMENTARIOS: ")
                puntuacion = int(input("PUNTUA LA PELICULA [1-10]: "))
                
                if (existe_pelicula(titulo) == False):
                    id_pelicula = len(peliculas_data[0]["peliculas"]) + 1
                    nueva_pelicula = {
                        "id":id_pelicula,
                        "titulo":titulo,
                        "anio":anio,
                        "director":director,
                        "genero":genero,
                        "sinopsis":sinopsis,
                        "link":link_imagen,
                        "comentarios": [
                            {
                                "usuario_id": usuario_id,
                                "comentario": comentario
                            }
                        ],
                        "alta": usuario_id,
                        "puntuaciones": [
                            {
                                "usuario_id": usuario_id,
                                "puntuacion": puntuacion
                            }
                        ],
                        "contador": 0
                    }
                        
                    peliculas_data[0]["peliculas"].append(nueva_pelicula)
                    
                    with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                        json.dump(peliculas_data, archivo_peliculas, indent = 4)
                            
                        print("SE CARGO LA PELICULA NUEVA CON EXITO.")
                else:
                    print("ERROR!. LA PELICULA YA SE ENCUENTRA CARGADA EN LA BASE DE DATOS.")
                    break
            elif (opcion == 2):
                print("+++++++++++++++++++++++++")
                print("SECCION 'EDITAR PELICULA'")
                print("+++++++++++++++++++++++++")
                print()
                usuario_id = id_usuario
                
                titulo_pelicula = input("NOMBRE DE LA PELICULA: ")
                pelicula_editar = next((pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["titulo"].lower() == titulo_pelicula.lower()), None)
 
                if pelicula_editar:
                    print("PELICULA ENCONTRADA.")
                    
                    item = input("DESEA MODIFICAR EL DIRECTOR? [SI - NO]:")
                    if item.upper() == "SI":
                        print("LISTA DE DIRECTORES DISPONIBLES EN EL SISTEMA: ")
                        for direc in directores_data[0]["directores"]:
                            print(direc["nombre_director"], end = ", ")
                        print()
                        director = input("NOMBRE DEL DIRECTOR (SELECCIONAR): ")
                        while not existe_director(director):
                            print("DIRECTOR NO ENCONTRADO.")
                            director = input("NOMBRE DEL DIRECTOR (SELECCIONAR): ")
                        pelicula_editar["director"] = director
                    item = input("DESEA MODIFICAR EL TITULO? [SI - NO]: ")
                    if item.upper() == "SI":
                        titulo = input("NOMBRE DE LA PELICULA: ")
                        while existe_pelicula(titulo):
                            print("NO ES POSIBLE MODIFICAR EL NOMBRE DE LA PELICULA DADO QUE EL MISMO YA SE ENCUENTRA UTILIZADO EN LA BASE DE DATOS DEL SISTEMA. INTENTE NUEVAMENTE.")
                            titulo = input("NOMBRE DE LA PELICULA: ")
                        else:
                            pelicula_editar["titulo"] = titulo
                    item = input("DESEA MODIFICAR EL AÑO? [SI - NO]: ")
                    if item.upper() == "SI":
                        anio = input("AÑO DE ESTRENO: ")
                        pelicula_editar["anio"] = anio
                    item = input("DESEA MODIFICAR EL GENERO? [SI - NO]: ")
                    if item.upper() == "SI":
                        print("LISTA DE GENEROS DISPONIBLES EN EL SISTEMA: ")
                        for genre in peliculas_data[1]["generos"]:
                            print(genre["nombre_genero"], end = ", ")
                        print()
                        genero = input("GENERO (SELECCIONAR): ")
                        while not existe_genero(genero):
                            print("GENERO NO ENCONTRADO.")
                            genero = input("GENERO (SELECCIONAR): ")
                        pelicula_editar["genero"] = genero
                    item = input("DESEA MODIFICAR LA SINOPSIS? [SI - NO]: ")
                    if item.upper() == "SI":
                        sinopsis = input("SINOPSIS: ")
                        pelicula_editar["sinopsis"] = sinopsis
                    item = input("DESEA MODIFICAR LA IMAGEN DE PORTADA? [SI - NO]: ")
                    if item.upper() == "SI":
                        link_imagen = input("IMAGEN DE PORTADA: ")
                        pelicula_editar["link"] = link_imagen
                    item = input("DESEA MODIFICAR EL COMENTARIO? [SI - NO]: ")
                    if item.upper() == "SI":
                        comentario = next((coment for coment in pelicula_editar["comentarios"] if coment["usuario_id"] == usuario_id), None)
                        if comentario:
                            comentarios = input("COMENTARIO: ")
                            comentario["comentario"] = comentarios
                        else:
                            print("USTED NO PUEDE EDITAR COMENTARIOS PORQUE NO HIZO NINGUNO.")
   
                    with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                        json.dump(peliculas_data, archivo_peliculas, indent = 4)
                        
                    print("LA PELICULA HA SIDO EDITADA CORRECTAMENTE.")
                else:
                    print("ERROR!. PELICULA NO ENCONTRADA.")
            elif (opcion == 3):
                print("+++++++++++++++++++++++++++")
                print("SECCION 'ELIMINAR PELICULA'")
                print("+++++++++++++++++++++++++++")
                print()
                usuario_id = id_usuario
                titulo_pelicula = input("NOMBRE DE LA PELICULA: ")
                
                pelicula_eliminar = next((pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["titulo"].lower() == titulo_pelicula.lower()), None)
                
                if pelicula_eliminar:
                    comentarios = next((comentario for comentario in pelicula_eliminar["comentarios"] if comentario["usuario_id"] != usuario_id), None)
                    if comentarios:
                        print("ERROR!. PELICULA CON COMENTARIOS.")
                    else:
                        peliculas_data[0]["peliculas"].remove(pelicula_eliminar)
                        
                        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                            json.dump(peliculas_data, archivo_peliculas, indent = 4)
                            
                        print("LA PELICULA HA SIDO ELIMINADA CORRECTAMENTE.")
                else:
                    print("ERROR!. PELICULA NO ENCONTRADA.")
            elif (opcion == 4):
                print("+++++++++++++++++++++++++")
                print("SECCION 'BUSCAR DIRECTOR'")
                print("+++++++++++++++++++++++++")
                print()
                
                director = input("NOMBRE DEL DIRECTOR A BUSCAR: ")
                    
                resultados_directores = buscar_directores(director)
                
                if resultados_directores == []:
                    print("NO HAY RESULTADOS DE SU BUSQUEDA.")
                else:
                    print("RESULTADOS DE SU BUSQUEDA: ")
                    for resultado in resultados_directores:
                        print(resultado["nombre_director"])                                              
            elif (opcion == 5):
                print("+++++++++++++++++++++++++")
                print("SECCION 'BUSCAR PELICULA'")
                print("+++++++++++++++++++++++++")
                print()
            
                pelicula = input("NOMBRE DE LA PELICULA A BUSCAR: ")
                
                resultados_peliculas = buscar_peliculas(pelicula)

                if resultados_peliculas == []:
                    print("NO HAY RESULTADOS DE SU BUSQUEDA.")
                else:
                    print("RESULTADOS DE SU BUSQUEDA: ")
                    for resultado in resultados_peliculas:
                        print(resultado["titulo"])
                        resultado["contador"] += 1
                        
                with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                    json.dump(peliculas_data, archivo_peliculas, indent = 4)
            elif (opcion == 6):
                print("++++++++++++++++++++++++")
                print("SECCION 'AÑADIR USUARIO'")
                print("++++++++++++++++++++++++")
                print()
                
                nombre_usuario = input("NOMBRE DE USUARIO: ")
                contrasenia = input("CONTRASEÑA DE USUARIO: ")
                permiso = input("PERMISO DE USUARIO: ")
                
                if (existe_usuario(nombre_usuario) == False):
                    id = len(usuarios_data[0]["usuarios"]) + 1
                    nuevo_usuario = {
                        "id":id,
                        "user":nombre_usuario,
                        "password":contrasenia,
                        "permiso":permiso
                    }
                    
                    usuarios_data[0]["usuarios"].append(nuevo_usuario)
                    
                    with open("Proyecto Final/usuarios.json", "w", encoding = "utf-8") as archivo_usuarios:
                        json.dump(usuarios_data, archivo_usuarios, indent = 4)
                    
                    print("SE CARGO EL USUARIO NUEVO EN LA BASE DE DATOS CON EXITO.")
                else:
                    print("ERROR!. NO ES POSIBLE AGREGAR ESE USUARIO DADO QUE YA SE ENCUENTRA REGISTRADO EN LA BASE DE DATOS DEL SISTEMA.")
            elif (opcion == 7):
                print("+++++++++++++++++++++++++++")
                print("SECCION 'MODIFICAR USUARIO'")
                print("+++++++++++++++++++++++++++")
                print()

                usuario = input("NOMBRE DEL USUARIO A MODIFICAR: ")
                
                usuario_editar = next((user for user in usuarios_data[0]["usuarios"] if user["user"].lower() == usuario.lower()), None)

                if usuario_editar:
                    print("USUARIO ENCONTRADO.")
                    
                    if (existe_usuario(usuario) == True):
                        item = input("DESEA MODIFICAR EL NOMBRE DE USUARIO? [SI - NO]:")
                        if item.upper() == "SI":
                            nombre_usuario = input("NOMBRE DE USUARIO: ")
                            usuario_editar["user"] = nombre_usuario
                        item = input("DESEA MODIFICAR LA CONTRASEÑA DE USUARIO? [SI - NO]:")
                        if item.upper() == "SI":
                            contrasenia = input("CONTRASEÑA DE USUARIO: ")
                            usuario_editar["password"] = contrasenia
                        item = input("DESEA MODIFICAR EL PERMISO DE USUARIO? [SI - NO]:")
                        if item.upper() == "SI":
                            permiso = input("PERMISO DE USUARIO: ")
                            usuario_editar["permiso"] = permiso
                        
                        with open("Proyecto Final/usuarios.json", "w", encoding = "utf-8") as archivo_usuarios:
                            json.dump(usuarios_data, archivo_usuarios, indent = 4)
                    
                        print("EL USUARIO HA SIDO EDITADO CORRECTAMENTE.")
                    else:
                        print("ERROR!. NOMBRE DE USUARIO YA REGISTRADO EN EL SISTEMA.")
                else:
                    print("ERROR!. USUARIO NO ENCONTRADO.")
            elif (opcion == 8):
                print("++++++++++++++++++++++++++")
                print("SECCION 'ELIMINAR USUARIO'")
                print("++++++++++++++++++++++++++")
                print()
                                
                usuario = input("NOMBRE DEL USUARIO A ELIMINAR: ")    

                usuario_eliminar = next((user for user in usuarios_data[0]["usuarios"] if user["user"].lower() == usuario.lower()), None)

                if usuario_eliminar:
                    print("USUARIO ENCONTRADO.")
                    
                    if (usuario_eliminar["permiso"] == "public"):
                        usuarios_data[0]["usuarios"].remove(usuario_eliminar)
                        
                        with open("Proyecto Final/usuarios.json", "w", encoding = "utf-8") as archivo_usuarios:
                            json.dump(usuarios_data, archivo_usuarios, indent = 4)
                    
                        print("EL USUARIO HA SIDO ELIMINADO CORRECTAMENTE.")
                    else:
                        print("ERROR!. NO ES POSIBLE ELIMINAR A UN USUARIO CON PERMISO 'ADMIN'.")
                else:
                    print("ERROR!. USUARIO NO ENCONTRADO.")
            elif (opcion == 9):
                print("+++++++++++++++++++++++++++++++++++++++")
                print("SECCION 'ASIGNAR PERMISOS A UN USUARIO'")
                print("+++++++++++++++++++++++++++++++++++++++")
                print()
                
                usuario_modificar_permiso = input("NOMBRE DEL USUARIO PARA MODIFICAR PERMISOS: ")
                
                usuario = next((user for user in usuarios_data[0]["usuarios"] if user["user"] == usuario_modificar_permiso), None)
                
                if usuario:
                    print("USUARIO ENCONTRADO.")
                    
                    permiso = input("PERMISO A ASIGNAR [ADMIN-PUBLIC]: ")
                    
                    if (permiso == "admin"):
                        usuario["permiso"] = "admin"
                    else:
                        usuario["permiso"] = "public"
                    
                    with open("Proyecto Final/usuarios.json", "w", encoding = "utf-8") as archivo_usuarios:
                        json.dump(usuarios_data, archivo_usuarios, indent = 4)
                    
                    print("EL PERMISO DE USUARIO HA SIDO MODIFICADO CORRECTAMENTE.")
                else:
                    print("ERROR!. USUARIO NO ENCONTRADO.")
            elif (opcion == 10):
                print("+++++++++++++++++++++++++")
                print("SECCION 'AÑADIR DIRECTOR'")
                print("+++++++++++++++++++++++++")
                print()
                
                nombre_director = input("NOMBRE DE DIRECTOR: ")
                
                if (existe_director(nombre_director) == False):
                    id = len(directores_data[0]["directores"]) + 1
                    nuevo_director = {
                        "id_director":id,
                        "nombre_director":nombre_director
                    }
                    
                    directores_data[0]["directores"].append(nuevo_director)
                    
                    with open("Proyecto Final/directores.json", "w", encoding = "utf-8") as archivo_directores:
                            json.dump(directores_data, archivo_directores, indent = 4)
                        
                    print("SE CARGO EL DIRECTOR NUEVO CON EXITO.")
                else:
                    print("ERROR!. NO ES POSIBLE AGREGAR ESE DIRECTOR DADO QUE YA SE ENCUENTRA REGISTRADO EN LA BASE DE DATOS DEL SISTEMA.")
            elif (opcion == 11):
                print("++++++++++++++++++++++++++++")
                print("SECCION 'MODIFICAR DIRECTOR'")
                print("++++++++++++++++++++++++++++")
                print()
                
                director = input("NOMBRE DEL DIRECTOR A MODIFICAR: ")
                
                director_editar = next((dire for dire in directores_data[0]["directores"] if dire["nombre_director"].lower() == director.lower()), None)
                
                if director_editar:
                    print("DIRECTOR ENCONTRADO.")
                    
                    nombre_director = input("NOMBRE DE DIRECTOR: ")
                    
                    if existe_director(nombre_director):
                        print("ERROR!. NOMBRE DE DIRECTOR YA REGISTRADO EN EL SISTEMA.")
                    else:
                        for pelicula in peliculas_data[0]["peliculas"]:
                            if (pelicula["director"] == director_editar["nombre_director"]): 
                                pelicula["director"] =  nombre_director
                        
                        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                            json.dump(peliculas_data, archivo_peliculas, indent = 4)

                        director_editar["nombre_director"] = nombre_director
                                
                        with open("Proyecto Final/directores.json", "w", encoding = "utf-8") as archivo_directores:
                            json.dump(directores_data, archivo_directores, indent = 4)
                        
                        print("EL DIRECTOR HA SIDO EDITADO CORRECTAMENTE.")
                else:
                    print("ERROR!. DIRECTOR NO ENCONTRADO.")
            elif (opcion == 12):
                print("+++++++++++++++++++++++++++")
                print("SECCION 'ELIMINAR DIRECTOR'")
                print("+++++++++++++++++++++++++++")
                print()
                
                director = input("NOMBRE DEL DIRECTOR A ELIMINAR: ")
                
                director_eliminar = next((dire for dire in directores_data[0]["directores"] if dire["nombre_director"].lower() == director.lower()), None)
                
                if director_eliminar:
                    print("DIRECTOR ENCONTRADO.")
                    
                    for pelicula in peliculas_data[0]["peliculas"]:
                        if (pelicula["director"] == director_eliminar["nombre_director"]):
                            pelicula["director"] = "Desconocido"
                    
                    with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                        json.dump(peliculas_data, archivo_peliculas, indent = 4)
                        
                    directores_data[0]["directores"].remove(director_eliminar)
                    
                    with open("Proyecto Final/directores.json", "w", encoding = "utf-8") as archivo_directores:
                        json.dump(directores_data, archivo_directores, indent = 4)
                    
                    print("EL DIRECTOR HA SIDO ELIMINADO CORRECTAMENTE.")
                else:
                    print("ERROR!. DIRECTOR NO ENCONTRADO.")
            elif (opcion == 13):
                print("+++++++++++++++++++++++")
                print("SECCION 'AÑADIR GENERO'")
                print("+++++++++++++++++++++++")
                print()
                
                nombre_genero = input("NOMBRE DE GENERO: ")
                
                if (existe_genero(nombre_genero) == False):      
                    id = len(peliculas_data[1]["generos"]) + 1
                    nuevo_genero = {
                        "nombre_genero":nombre_genero,
                        "id_genero":id
                    }
                    
                    peliculas_data[1]["generos"].append(nuevo_genero)
                    
                    with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                            json.dump(peliculas_data, archivo_peliculas, indent = 4)
                        
                    print("SE CARGO EL GENERO NUEVO CON EXITO.")
                else:
                    print("ERROR!. NO ES POSIBLE AGREGAR ESE GENERO DADO QUE YA SE ENCUENTRA REGISTRADO EN LA BASE DE DATOS DEL SISTEMA.")
            elif (opcion == 14):
                print("++++++++++++++++++++++++++")
                print("SECCION 'MODIFICAR GENERO'")
                print("++++++++++++++++++++++++++")
                print()
                
                genre = input("NOMBRE DEL GENERO A MODIFICAR: ")
                
                genero_editar = next((genero for genero in peliculas_data[1]["generos"] if genero["nombre_genero"].lower() == genre.lower()), None)
                
                if genero_editar:
                    print("GENERO ENCONTRADO.")
                    
                    nombre_genero = input("NOMBRE DE GENERO: ")
                    
                    if existe_genero(nombre_genero):
                        print("ERROR!. NOMBRE DE DIRECTOR YA REGISTRADO EN EL SISTEMA.")
                    else:
                        for pelicula in peliculas_data[0]["peliculas"]:
                            if (pelicula["genero"] == genero_editar["nombre_genero"]): 
                                pelicula["genero"] =  nombre_genero

                        genero_editar["nombre_genero"] = nombre_genero
                                
                        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                            json.dump(peliculas_data, archivo_peliculas, indent = 4)
                        
                        print("EL GENERO HA SIDO EDITADO CORRECTAMENTE.")
                else:
                    print("ERROR!. GENERO NO ENCONTRADO.")
            elif (opcion == 15):
                print("+++++++++++++++++++++++++")
                print("SECCION 'ELIMINAR GENERO'")
                print("+++++++++++++++++++++++++")
                print()
                
                genre = input("NOMBRE DEL GENERO A ELIMINAR: ")
                
                genero_eliminar = next((genero for genero in peliculas_data[1]["generos"] if genero["nombre_genero"].lower() == genre.lower()), None)
                
                if genero_eliminar:
                    print("GENERO ENCONTRADO.")
                    
                    for pelicula in peliculas_data[0]["peliculas"]:
                        if (pelicula["genero"] == genero_eliminar["nombre_genero"]):
                            pelicula["genero"] = "Desconocido"
                        
                    peliculas_data[1]["generos"].remove(genero_eliminar)
                    
                    with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                        json.dump(peliculas_data, archivo_peliculas, indent = 4)
                    
                    print("EL GENERO HA SIDO ELIMINADO CORRECTAMENTE.")
                else:
                    print("ERROR!. GENERO NO ENCONTRADO.")
            elif (opcion == 16):
                print("+++++++++++++++++++++++++++")
                print("SECCION 'AÑADIR PUNTUACION'")
                print("+++++++++++++++++++++++++++")
                print()
                
                usuario_id = id_usuario
                
                titulo = input("PELICULA QUE DESEA PUNTUAR: ")    
                
                pelicula = next((peli for peli in peliculas_data[0]["peliculas"] if peli["titulo"].lower() == titulo.lower()), None)
                    
                if pelicula:
                    usuario_puntuacion_existente = next((puntuacion for puntuacion in pelicula["puntuaciones"] if puntuacion["usuario_id"] == usuario_id), None)
                    
                    if usuario_puntuacion_existente:
                        print("ERROR!. USTED YA HA AGREGADO UNA PUNTUACION ANTERIORMENTE A ESTA PELICULA.")
                        print("EN CASO DE QUERER MODIFICAR SU PUNTUACION INGRESE A LA OPCION ADECUADA.")
                    else:
                        puntuacion = int(input("PUNTUACION [1-10]: "))
                        pelicula["puntuaciones"].append({
                            "usuario_id": usuario_id,
                            "puntuacion": puntuacion
                            })
                            
                        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                            json.dump(peliculas_data, archivo_peliculas, indent = 4)
                            
                        print("LA PUNTUACION SE REALIZO CON EXITO.")
                else:
                    print("NO SE ENCONTRO UNA PELICULA CON ESE NOMBRE EN LA BASE DE DATOS DEL SISTEMA.")
            elif (opcion == 17):
                print("++++++++++++++++++++++++++++++")
                print("SECCION 'MODIFICAR PUNTUACION'")
                print("++++++++++++++++++++++++++++++")
                print()
                
                usuario_id = id_usuario
                
                titulo = input("PELICULA QUE DESEA PUNTUAR: ")  
                  
                pelicula = next((peli for peli in peliculas_data[0]["peliculas"] if peli["titulo"].lower() == titulo.lower()), None)
                    
                if pelicula:
                    puntuacion_editar = next((puntuacion for puntuacion in pelicula["puntuaciones"] if puntuacion["usuario_id"] == usuario_id), None)
                        
                    if puntuacion_editar:
                        puntuacion = int(input("PUNTUACION [1-10]: "))
                        
                        puntuacion_editar["puntuacion"] = puntuacion
                            
                        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                            json.dump(peliculas_data, archivo_peliculas, indent = 4)  
                            
                        print("PUNTUACION MODIFICADA CON EXITO.")
                    else:
                        print("ERROR!. NO SE ENCONTRO UNA PUNTUACION DEL USUARIO A MODIFICAR PARA ESTA PELICULA.")
                else:
                    print("PELICULA NO ENCONTRADA.")
            elif (opcion == 18):
                print("+++++++++++++++++++++++++++++")
                print("SECCION 'ELIMINAR PUNTUACION'")
                print("+++++++++++++++++++++++++++++")
                print()
                
                usuario_id = id_usuario
                    
                titulo = input("PELICULA QUE DESEA PUNTUAR: ")
                
                pelicula = next((peli for peli in peliculas_data[0]["peliculas"] if peli["titulo"].lower() == titulo.lower()), None)
                    
                if pelicula: 
                    puntuacion_eliminar = next((puntuacion for puntuacion in pelicula["puntuaciones"] if puntuacion["usuario_id"] == usuario_id), None)
                        
                    if puntuacion_eliminar:
                        pelicula["puntuaciones"].remove(puntuacion_eliminar)
                            
                        with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                            json.dump(peliculas_data, archivo_peliculas, indent = 4)

                        print("PUNTUACION ELIMINADA CON EXITO.")
                    else:
                        print("ERROR!. NO SE ENCONTRO UNA PUNTUACION DEL USUARIO A ELIMINAR PARA ESTA PELICULA.")
                else:
                    print("PELICULA NO ENCONTRADA.")
            elif (opcion == 19):
                print("+++++++++++++++++++++++++++++")
                print("SECCION 'DIRECTORES CARGADOS'")
                print("+++++++++++++++++++++++++++++")
                print()
                
                for director in directores_data[0]["directores"]:
                    print(director["nombre_director"])
            elif (opcion == 20):
                print("++++++++++++++++++++++++++")
                print("SECCION 'GENEROS CARGADOS'")
                print("++++++++++++++++++++++++++")
                print()
                
                for genero in peliculas_data[1]["generos"]:
                    print(genero["nombre_genero"]) 
            elif (opcion == 21):
                print("++++++++++++++++++++++++++++++++++++++")
                print("SECCION 'BUSCAR PELICULA POR DIRECTOR'")
                print("++++++++++++++++++++++++++++++++++++++")
                print()
                
                director = input("NOMBRE DEL DIRECTOR A BUSCAR: ")
                
                encontrar_director = next((dire for dire in directores_data[0]["directores"] if dire["nombre_director"].lower() == director.lower()), None)
                flag = 0
                if encontrar_director:
                    for pelicula in peliculas_data[0]["peliculas"]:
                        if pelicula["director"].lower() == director.lower():
                            print(pelicula["titulo"])
                            flag = 1
                    
                    if flag == 0:
                        print("POR EL MOMENTO NO HAY PELICULAS CARGADAS EN EL SISTEMA DE ESE DIRECTOR.")   
                else:
                    print("DIRECTOR NO ENCONTRADO.")
            elif (opcion == 22):
                print("+++++++++++++++++++++++++++++++++++")
                print("SECCION 'VER PELICULAS CON PORTADA'")
                print("+++++++++++++++++++++++++++++++++++")
                print()
                
                for pelicula in peliculas_data[0]["peliculas"]:
                    if pelicula.get("link") != "":
                        print(pelicula["titulo"])
            elif (opcion == 23):
                print("AGUARDE UNOS SEGUNDOS...")
                time.sleep(5)
                print("GRACIAS POR UTILIZAR EL SISTEMA. HASTA LUEGO!")
                exit(0)
            else:
                print("OPCION INVALIDA. INTENTE NUEVAMENTE.")
    else:
        #El programa tendra un modulo publico, es decir, una pantalla que puede ser accedida sin necesidad de tener cuenta ni estar logueado
        #En esa pantalla se mostraran las ultimas 10 peliculas agregadas al sistema independientemente del usuario
        print("USTED SOLO PUEDE ACCEDER AL MODULO PUBLICO YA QUE NO ESTA LOGUEADO EN EL SISTEMA O NO TIENE LOS PERMISOS NECESARIOS PARA ACCEDER AL MODULO PRIVADO.")
        print("A CONTINUACION SE MOSTRARAN LAS ULTIMAS 10 PELICULAS AGREGADAS AL SISTEMA:\n")
        mostrar_peliculas(peliculas_data[0]["peliculas"])     
        print("\nGRACIAS POR UTLIZAR EL SISTEMA, HASTA LA PROXIMA!")      
else:
    print("ERROR, EL USUARIO NO FUE ENCONTRADO EN LA BASE DE DATOS.")  