from particion import Particion
from proceso import Proceso

class Memoria():

   def __init__(self, tamaño):
      
      self.tamaño = tamaño
      self.particiones = []
      self.libre = tamaño
      self.particiones.append(Particion(tamaño=tamaño, libre=True))
      # self.asignarParticion()
      

   def asignarParticion(self, pos, proceso:Proceso):
      self.libre -= proceso.tamaño
      self.particiones[pos].asignarProceso(proceso)

   def vaciarParticion(self, pos):
      self.libre += self.particiones[pos].tamaño
      self.particiones[pos].eliminarProceso()

   # def insertarInicio(self, particion:Particion):
   #    # AGREGAR AL PRINCIPIO      
   #    parte1 = []
   #    parte2 = self.particiones
   #    parte1.append(particion)
   #    self.particiones = parte1 + parte2


   def insertarEntre(self, particion:Particion, pos1, pos2):
      # DIVIDIR LA MEMORIA Y AGREGAR LA PARTICION ENTRE LAS PARTES
      # self.libre -= particion.tamaño 
      parte1 = self.particiones[:pos1]
      parte2 = self.particiones[pos2+1:]
      self.particiones = parte1
      self.particiones.append(particion)
      self.particiones += parte2

   # def insertarFinal(self, particion:Particion):
   #    # AGREGAR AL FINAL
   #    self.libre -= particion.tamaño       
   #    self.particiones.append(particion)
