import os
import re
from proceso import Proceso

class Archivo():

   def leer(self, path):
      tanda = []
      archivo = open(path, "r")
      for trabajo in archivo.readlines():
         data = trabajo.split(";")
         proceso = Proceso(
            nombre=data[0],
            arribo=int(re.sub("\s+","", data[1])),
            tiempoTotal=int(re.sub("\s+","", data[2])),
            tamaño=int(re.sub("\s+","", data[3]))
         )
         tanda.append(proceso)
            
      archivo.close()
      return tanda

   def escribir(self, nombre):

      archivo = open(nombre+".txt", "w")
      archivo.write('Hola \n')
      # for linea in registro:
      #    archivo.write(linea+'\n')
      
      archivo.close()
      pass

if __name__ == "__main__":
   A = Archivo()
   print(A.leer('archivo1'))
   
