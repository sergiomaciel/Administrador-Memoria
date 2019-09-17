from proceso import Proceso

class Particion():

   id = 0

   def __init__(self, tamaño:int=0, libre:bool=True):
      Particion.id +=1
      self.id = Particion.id
      self.tamaño = tamaño
      self.libre = libre
      self.proceso = None
      
   
   def asignarProceso(self, proceso:Proceso):
      self.proceso = proceso
      self.libre = False
      self.tamaño = proceso.tamaño


   def eliminarProceso(self):
      self.proceso = None
      self.libre = True


   def __str__(self):
      return 'ID:'+str(self.id)+'  Tamaño:'+str(self.tamaño)+' Mb  Estado:'+str(self.libre)
