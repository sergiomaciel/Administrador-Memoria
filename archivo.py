import os

class CargarArchivo():

   def __init__(self, nombre):
      self.__archivo = open(nombre+".txt", "r")

   def procesar(self):
      trabajos = []

      for tanda in self.__archivo.readlines():
         data = tanda.split(";")
         trabajo = {
            'nombre': data[0],
            'arribo': data[1],
            'tiempo-total': data[2],
            'cantidad-memoria': data[3]
         }
         trabajos.append(trabajo)
            
      self.__archivo.close()
      return trabajos

if __name__ == "__main__":
   A = CargarArchivo('archivo1')
   print(A.procesar())
