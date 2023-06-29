# Crear un programa en Python para mantener una lista de peliculas recomendadas por parte de los usuarios

from flask import Flask, jsonify
import json

app = Flask(__name__)

with open("Proyecto Final/usuarios.json", encoding = "utf-8") as archivo_usuarios:
    usuarios = json.load(archivo_usuarios)

with open("Proyecto Final/peliculas.json", encoding = "utf-8") as archivo_peliculas:
    peliculas = json.load(archivo_peliculas)
    
with open("Proyecto Final/directores.json", encoding = "utf-8") as archivo_directores:
    directores = json.load(archivo_directores)

print("-----------------------------------------------")
print("BIENVENIDO AL SISTEMA DE PELICULAS 'FILM QUEST'")
print("-----------------------------------------------")

login = input("¿Ya estas registrado? Inicia sesion para acceder [Si - No]: ")
lower_input = login.lower()

while (lower_input != "si" and lower_input != "no"):
    login = input("¿Ya estas registrado? Inicia sesion para acceder [Si - No]: ")
    lower_input = login.lower()

if (lower_input == "no"):
    #El programa tendra un modulo publico, es decir, una pantalla que puede ser accedida sin necesidad de tener cuenta ni estar logueado
    #En esa pantalla se mostraran las ultimas 10 peliculas agregadas al sistema independientemente del usuario
    print("Usted solo puede acceder al modulo publico ya que no esta logueado en el sistema.")
    print("A continuacion se mostraran las ultimas 10 peliculas agregadas al sistema:\n")
    
    for pelicula in peliculas[-10:]:
        print(pelicula["titulo"], end = "\n")
        
    print("\nGracias por utilizar el sistema, hasta la proxima!")
else:
    username = input("Ingrese nombre de usuario: ")
    password = input ("Ingrese su contraseña: ")

    flag = False
    for user in usuarios:
        if (user["user"] == username) and (user["password"] == password):
            print("Usuario encontrado en la base de datos!")
            flag = True
            break
    if (flag == False):
        print("Error el usuario no fue encontrado en la base de datos")   
    
#Ademas, el sistema debera proveer servicios web a traves de endpoints para ser consultados por otros sistemas y devolver un documento de formato JSON.
#Los servicios que se necesitan son:
#@app.route("/")
def home():
    return ""
# 1. Devolver la lista de directores presentes en la plataforma
@app.route("/directores", methods = ["GET"])
def devolver_directores():
    return jsonify(directores["director"])
# 2. Devolver la lista de generos presentes en la plataforma
@app.route("/peliculas/generos", methods = ["GET"])
def devolver_generos():
    return jsonify(peliculas["genero"])
# 3. Devolver la lista de peliculas dirigidas por un director en particular
# 4. Devolver las peliculas que tienen imagen de portada agregada
# 5. ABM de cada pelicula

if __name__ == "__main__":
    app.run(debug = True)