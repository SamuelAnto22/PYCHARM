# import  math
# nombre= input("Ingrese su nombre: ")
# print("hola", nombre, "un gusto")
# print(f"El nombre es {nombre}")
# if nombre=="samuel":
#     print("CORRECTO")
# else:
#     print("INCORRECTO")
#
# def hola():
#     print("hola")
# hola()
class Persona:

    def __init__(self,nombre,apellido,edad):
        self.nombre = nombre
        self.apellido = apellido
        self.edad= edad
    def introduccion(self):
        print(f"""
        El nombre es {self.nombre}
        el apellido es {self.apellido}
        la edad es {self.edad}
""")


if __name__=="__main__":

    person1=Persona("samuel","cordova","21")
    person1.introduccion()

# print(math.pi)
