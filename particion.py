class Particion():

   id = 1

   def __init__(self, nombre:str, memoria:int, tiempo:int, vacio:bool=False):
      self.id = Particion.id
      self.nombre = nombre
      self.memoria = memoria
      self.tiempo = tiempo
      self.vacio = vacio
      Particion.id +=1
      

   def liberar(self):
      self.nombre = '---'
      self.tiempo = 0
      self.vacio = True

