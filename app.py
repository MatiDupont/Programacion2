# Crear un programa en Python para mantener una lista de peliculas recomendadas por parte de los usuarios

from flask import Flask, jsonify
import json

#app = Flask(__name__)

with open("Proyecto Final/usuarios.json", encoding = "utf-8") as archivo_usuarios:
    usuarios_data = json.load(archivo_usuarios)

with open("Proyecto Final/peliculas.json", encoding = "utf-8") as archivo_peliculas:
    peliculas_data = json.load(archivo_peliculas)
    
with open("Proyecto Final/directores.json", encoding = "utf-8") as archivo_directores:
    directores_data = json.load(archivo_directores)
    
def mostrar_peliculas(peliculas):
        for pelicula in peliculas[-10:]:
            print("Titulo: " + pelicula["titulo"])
            print("Año: " + pelicula["anio"])
            print("Director: " + pelicula["director"])
            print("Genero: " + pelicula["genero"])
            print("Sinopsis:" + pelicula["sinopsis"])
            print("---------------------------------")

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
        print("¡Usuario encontrado en la base de datos!")
        
        while (True):
            print("\n --- Menu de opciones ---")
            print("1. Agregar pelicula")
            print("2. Editar pelicula")
            print("3. Eliminar pelicula")
            print("4. Mostrar ultimas (10) peliculas")
            print("5. Salir\n")
            
            opcion = int(input("Ingrese una opcion: "))
            
            if (opcion == 1):
                agregar_pelicula()
            elif (opcion == 2):
                editar_pelicula()
            elif (opcion == 3):
                eliminar_pelicula()
            elif (opcion == 4):
                mostrar_peliculas(peliculas_data[0]["peliculas"])
            elif (opcion == 5):
                print("Gracias por utilizar el sistema. Hasta luego!")
                exit(0)
            else:
                print("Opcion invalida. Intente nuevamente.")
    else:
        print("Error, el usuario no fue encontrado en la base de datos.")
 
    
#Ademas, el sistema debera proveer servicios web a traves de endpoints para ser consultados por otros sistemas y devolver un documento de formato JSON.
#Los servicios que se necesitan son:
#@app.route("/", methods = ["GET"])
#def home():
#    return "Bienvenido al sistema de peliculas 'Film Quest"
# 1. Devolver la lista de directores presentes en la plataforma
#@app.route("/directores", methods = ["GET"])
#def devolver_directores():
#    directores = directores_data[0]["directores"]["nombre_director"]
#    return jsonify(directores)
# 2. Devolver la lista de generos presentes en la plataforma
#@app.route("/peliculas/generos", methods = ["GET"])
#def devolver_generos():
#    return jsonify(peliculas_data["genero"])
# 3. Devolver la lista de peliculas dirigidas por un director en particular
# 4. Devolver las peliculas que tienen imagen de portada agregada
# 5. ABM de cada pelicula

#if __name__ == "__main__":
 #   app.run(debug = True)