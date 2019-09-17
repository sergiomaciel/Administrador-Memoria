class Proceso():

   def __init__(self, nombre:str='', arribo:int=0, tiempoTotal:int=0, tamaño:int=0):
      
      self.nombre = nombre
      self.arribo = arribo
      self.tiempoTotal = tiempoTotal
      self.tamaño = tamaño

   def __str__(self):
      return self.nombre+' Arribo:'+str(self.arribo)+'  T.Total:'+str(self.tiempoTotal)+'  Mem:'+str(self.tamaño)+' Mb'