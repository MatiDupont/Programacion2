# Crear un programa en Python para mantener una lista de peliculas recomendadas por parte de los usuarios

from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import json

app = Flask(__name__)

with open("Proyecto Final/usuarios.json", encoding = "utf-8") as archivo_usuarios:
    usuarios_data = json.load(archivo_usuarios)

with open("Proyecto Final/peliculas.json", encoding = "utf-8") as archivo_peliculas:
    peliculas_data = json.load(archivo_peliculas)
    
with open("Proyecto Final/directores.json", encoding = "utf-8") as archivo_directores:
    directores_data = json.load(archivo_directores)
    
flag = False

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
            
            #modificar el printeo para que se vea mejor por consola    
            print("Se cargo la pelicula nueva con exito.")
            return jsonify(nueva_pelicula["titulo"]), HTTPStatus.OK
        else:
            print("Error!. Pelicula ya cargada en base da datos.")
            return jsonify("No es posible agregar esa pelicula dado que ya se encuentra registrada en la base de datos del sistema."), HTTPStatus.BAD_REQUEST
           
@app.route("/peliculas/editar/<id>", methods = ["PUT"])
def editar_pelicula(id):
    datos_json = request.get_json()
    
    pelicula_editar = next((pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["id"] == int(id)), None)
    
    if pelicula_editar:
        print("Pelicula encontrada.")
        
        titulo = datos_json["titulo"] or pelicula_editar["titulo"]
        anio = datos_json["anio"] or pelicula_editar["anio"]
        director = datos_json["director"] or pelicula_editar["director"]
        genero = datos_json["genero"] or pelicula_editar["genero"]
        sinopsis = datos_json["sinopsis"] or pelicula_editar["sinopsis"]
        imagen = datos_json["link"] or pelicula_editar["link"]
        comentarios = datos_json["comentarios"] or pelicula_editar["comentarios"]
        
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
        print("Error!. Pelicula no encontrada.")
        return jsonify("No se encontro la pelicula con el ID especificado."), HTTPStatus.NOT_FOUND
        
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
            
        #modificar el printeo para que se vea mejor por consola    
        print("Se cargo el director nueva con exito.")
        return jsonify(nuevo_director["nombre_director"]), HTTPStatus.OK
    else:
        print("Error!. Director ya cargado en base da datos.")
        return jsonify("No es posible agregar ese director dado que ya se encuentra registrado en la base de datos del sistema."), HTTPStatus.BAD_REQUEST

@app.route("/directores/editar/<id>", methods = ["PUT"])
def editar_director(id):
    datos_json = request.get_json()
    
    director_editar = next((dire for dire in directores_data[0]["directores"] if dire["id_director"] == int(id)), None)
    
    if director_editar:
        print("Director encontrado.")
        
        nombre = datos_json["nombre_director"] or director_editar["nombre_director"]
        
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
        
if __name__ == "__main__":
    app.run(debug = True)  

print("-----------------------------------------------")
print("BIENVENIDO AL SISTEMA DE PELICULAS 'FILM QUEST'")
print("-----------------------------------------------")
login = input("¿Ya estas registrado? Inicia sesion para acceder [Si - No]: ").lower()
while (login != "si" and login != "no"):
    login = input("¿Ya estas registrado? Inicia sesion para acceder [Si - No]: ").lower()
if (login == "no"):
    #El programa tendra un modulo publico, es decir, una pantalla que puede ser accedida sin necesidad de tener cuenta ni estar logueado
    #En esa pantalla se mostraran las ultimas 10 peliculas agregadas al sistema independientemente del usuario
    print("Usted solo puede acceder al modulo publico ya que no esta logueado en el sistema.")
    print("A continuacion se mostraran las ultimas 10 peliculas agregadas al sistema:\n")
    mostrar_peliculas(peliculas_data[0]["peliculas"])     
    print("\nGracias por utilizar el sistema, hasta la proxima!")
else:
    username = input("Ingrese nombre de usuario: ")
    password = input ("Ingrese su contraseña: ")
    usuario = next((usuario for usuario in usuarios_data[0]["usuarios"] if usuario["user"] == username and usuario["password"] == password), None)
    
    if usuario:
        id_usuario = str(usuario["id"])
        flag = True
        print("¡Usuario encontrado en la base de datos!")
        
        while(True):          
            print("\n --- Menu de opciones ---")
            print("1. Agregar pelicula")
            print("2. Editar pelicula")
            print("3. Eliminar pelicula")
            print("4. Mostrar ultimas (10) peliculas")
            print("5. Salir\n")
            
            opcion = int(input("Ingrese una opcion: "))
            
            if (opcion == 1):
                with app.test_client() as client:
                    client.post("/peliculas/agregar/nueva")
            elif (opcion == 2):
                with app.test_client() as client:
                    client.put("/peliculas/editar/<id>")
            elif (opcion == 3):
                with app.test_client() as client:
                    client.delete("/peliculas/eliminar/<id>")
            elif (opcion == 4):
                mostrar_peliculas(peliculas_data[0]["peliculas"])
            elif (opcion == 5):
                print("Gracias por utilizar el sistema. Hasta luego!")
                exit(0)
            else:
                print("Opcion invalida. Intente nuevamente.")        
    else:
        print("Error, el usuario no fue encontrado en la base de datos.")        