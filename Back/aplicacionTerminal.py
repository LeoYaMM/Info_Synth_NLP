from LlamaAPIResumen import resumen_Llama
from LlamaAPITrivia import *
from sqlConnector import *

def main():
    print("Bienvenido a Thot!")
    print("Por favor, ingresa tu nombre: ")
    id_visitante = 1
    nombre = input()
    agregar_nombre_visitante(1, nombre)
    print("Por favor, ingresa tu edad: ")
    edad = input()
    agregar_edad_visitante(id_visitante,edad)
    while True:
        # Limpia la pantalla
        print("\033c")
        # Menú de opciones
        print("¿Qué deseas hacer?")
        print("1. Escanear objeto")
        print("2. Finalizar recorrido")
        print("3. Salir de Thot")
        opcion = input()
        
        if opcion == "1":
            print("Por favor, ingresa el id del objeto")
            id_objeto = input()
            print("\033c")
            resumen_Llama(id_objeto, id_visitante)
        elif opcion == "2":
            print("\033c")
            trivia_Llama(id_visitante)
            print("\033c")
            califica_trivia_Llama(id_visitante)
            break
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

    print("Gracias por usar Thot!")

if __name__ == "__main__":
    main()
