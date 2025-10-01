# python Vanilla

# 1. Suma de precios por producto: Tienes una lista de tuplas con productos y
# precios:
# Calcula la suma total de precios de todos los productos.
# productos = [("manzana", 1200) , ("banana", 800) , ("pera", 1500)]
# suma_precios = sum(precio for _, precio in productos)

# print("La suma total de los precios es:", suma_precios)



# 2. Promedio de notas por estudiante: Tienes un diccionario donde las claves son 
# estudiantes y los valores son sus notas:
# Calcula el promedio de notas de cada estudiante.
notas = {
    "Ana": [4.5, 3.8, 4.0],
    "Luis": [3.0, 3.5, 4.2],
    "Marta": [5.0, 4.8, 4.9]
}





# Numpy

import numpy as np

# 1. Suma de precios por producto: Tienes una lista de tuplas con productos y
# precios:
productos = [("manzana", 1200),("banana", 800), ("pera", 1500)]
precio = np.array([precio for _, precio in productos])
suma_precios = np.sum(precio)

print(suma_precios)


# 2. Promedio de notas por estudiante: Tienes un diccionario donde las claves son 
# estudiantes y los valores son sus notas:
# Calcula el promedio de notas de cada estudiante.
notas = {
    "Ana": [4.5, 3.8, 4.0],
    "Luis": [3.0, 3.5, 4.2],
    "Marta": [5.0, 4.8, 4.9]
}