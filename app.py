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
            print("---------------------------------")
            
def existe_pelicula(titulo):
    titulo_pelicula = next((pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["titulo"].lower() == titulo.lower()),None)
    if titulo_pelicula:
        return True
    else:
        return False   
    
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
    
    campos = {"titulo", "anio", "director", "genero", "sinopsis", "link", "comentarios"}
    
    claves = list(next(iter(datos_json)) for clave in range(7))
    
    for clave in claves:
        if (clave == "null"):
            print("Error!, faltan campos en el pedido.")
            exit(1)
            
    i = 0
    salida = 0
    for campo in campos:
        if (claves[i] == campo):
            i = i + 1
            continue
        else:
            print("Los campos deben estar en el orden correcto. --> titulo, anio, director, genero, sinopsis, link, comentarios")
            salida = 1
            exit(1)
     
    if (salida == 0):   
        if (existe_pelicula(datos_json["titulo"]) == False):
            id_pelicula = len(peliculas_data[0]["peliculas"]) + 1
            nueva_pelicula = {
            "id":id_pelicula,
            "titulo":datos_json["titulo"],
            "anio":datos_json["anio"],
            "director":datos_json["director"],
            "genero":datos_json["genero"],
            "sinopsis":datos_json["sinopsis"],
            "link":datos_json["imagen"],
            "comentarios":datos_json["comentarios"]
            }
        
            peliculas_data[0]["peliculas"].append(nueva_pelicula)
        
            with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                json.dump(peliculas_data, archivo_peliculas, indent = 8)
                
            print("Se cargo la pelicula nueva con exito.")
            return Response(jsonify(nueva_pelicula["titulo"]), status = HTTPStatus.OK)
        else:
            print("Error!. Pelicula ya cargada en base da datos.")
            Response(jsonify("No es posible agregar esa pelicula dado que ya se encuentra registrada en la base de datos del sistema."), status = HTTPStatus.BAD_REQUEST) 
           
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
            json.dump(peliculas_data, archivo_peliculas, indent = 8)
        
        print("La pelicula ha sido editada correctamente.")
        return Response(jsonify(pelicula_editar["titulo"]), status = HTTPStatus.OK)
    else:
        print("Error!. Pelicula no encontrada.")
        Response(jsonify("No se encontro la pelicula con el ID especificado."), status = HTTPStatus.NOT_FOUND)
        
@app.route("/peliculas/eliminar/<id>", methods = ["DELETE"])
def eliminar_pelicula(id):
    peliculas_eliminar = next((pelicula for pelicula in peliculas_data[0]["peliculas"] if pelicula["id"] == int(id)), None)
    
    if peliculas_eliminar:
        if (peliculas_eliminar["comentarios"] != ""):
            peliculas_data[0]["peliculas"].remove(peliculas_eliminar)
            
            with open("Proyecto Final/peliculas.json", "w", encoding = "utf-8") as archivo_peliculas:
                json.dump(peliculas_data, archivo_peliculas, indent = 8)
                
            print("La pelicula ha sido eliminada correctamente.")
            return Response(jsonify(peliculas_eliminar["titulo"]), status = HTTPStatus.OK)
        else:
            print("Error!. Pelicula con comentarios.")
            return Response(jsonify("No se puede eliminar la pelicula porque tiene comentarios de otros usuarios."), status = HTTPStatus.BAD_REQUEST)
    else:
        print("Error!. Pelicula no encontrada.")
        return Response(jsonify("No se encontro la pelicula con el ID especificado."), status = HTTPStatus.NOT_FOUND)
    


if __name__ == "__main__":
   app.run(debug = True)