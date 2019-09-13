from proceso import Proceso
from particion import Particion

class Memoria():

   def __init__(self, tamaño, estrategia, tiempoSeleccion, tiempoCarga, tiempoLiberacion):
      
      self.tamaño = tamaño
      self.estrategia = estrategia
      self.tiempoSeleccion = tiempoSeleccion
      self.tiempoCarga = tiempoCarga
      self.tiempoLiberacion = tiempoLiberacion

      self.particiones = []
      self.libre = tamaño
   

   def agregarProceso(self, proceso:Proceso):
      # SEGUN SEA LA ESTRATEGIA DE ASIGNACION
      # ASIGNA PARTICION(
      # Para no perder el orden preguntar si no es la ultima 
      # particion agregar la particion entre las particiones
      # exixtentes y en el caso de exixtir memoria libre restante de
      # la particion agregar la memoria restante despues de la nueva particion
      # )
      # RESTAR TAMAÑO DE MEMORIA - TAMAÑO DE PROCESO

      # VERIFICAQUE TENGA MEMORIA LIBRE SUFICIENTE EL NUEVO PROCESO
      if (self.libre >= proceso.memoria):
         self.libre -=proceso.memoria
         particion = Particion(
            proceso.nombre,
            proceso.memoria,
            proceso.tiempoTotal
            )
         self.particiones.append(particion)
      
      
      
      pass


   def liberarParticion(self, pos):
      # VERIFICAR PORCESO DE IZQ Y DER
      # SI ESTA LIBRE __unificarParticion()
      self.libre += self.particiones[pos].memoria
      self.particiones[pos].liberar()

      if (self.__verificarUnificacion(pos)):
         print('UNIFICACION Particion '+str(pos))
         self.unificarParticion(pos)
      else:
         print('SIN UNIFICAR')


   def __verificarUnificacion(self, pos):
      if ( (pos>0)and(pos<(len(self.particiones)-1)) ):
         # Verifica si la POS esta libre la POS ANTERIOR O LA POSTERIOR
         if ( (self.particiones[pos-1].vacio) or (self.particiones[pos+1].vacio) ):
            return True
         else:
            return False
      else:
         # Verifica si la  1er POS esta libre y la 2da POS esta libre
         if ( (pos==0)and(self.particiones[pos+1].vacio) ):
            return True
         # Verifica si la ultima POS esta libre y la antes ultima POS esta libre
         if ( (pos==(len(self.particiones)-1))and(self.particiones[pos-1].vacio) ):
            return True

         return False
   

   def unificarParticion(self, pos):
      memoriaTotal = self.particiones[pos].memoria
      
      posBase = pos
      posTope = pos
      posIzq = pos-1
      posDer = pos+1
      
      # BUSCAR PARTICIONES LIBRES POR IZQ DE LA POS
      while ((posIzq>=0) and (self.particiones[posIzq].vacio)):
         memoriaTotal += self.particiones[posIzq].memoria
         posBase = posIzq         
         posIzq -=1

      # BUSCAR PARTICIONES LIBRES POR DER DE LA POS
      while ((posDer<=(len(self.particiones)-1)) and (self.particiones[posDer].vacio)):
         memoriaTotal += self.particiones[posDer].memoria
         posTope = posDer
         posDer +=1

      print('-- Desde: '+str(posBase)+'  Hasta: '+str(posTope))
      # RECALCULAR TAMAÑO DE LA NUEVA PARTICION LIBRE
      newPartUnif = Particion(nombre='---',memoria=memoriaTotal,tiempo=0,vacio=True)
      # DIVIDIR LA MEMORIA Y AGREGAR NUEVA PARTICION ENTRE LAS PARTES
      parte1 = self.particiones[:posBase]
      parte2 = self.particiones[posTope+1:]
      self.particiones = parte1
      self.particiones.append(newPartUnif)
      self.particiones += parte2
   pass


def imprimirMemoria(M:Memoria):
   # IMPRIMIR
   print()
   print('MEMORIA - '+str(M.tamaño)+' MB')
   i=0
   for particion in M.particiones:
      print('|Particion| ID:'+str(particion.id)+' Vacia:'+ str(particion.vacio)+' POS:'+str(i)+' Mem:'+str(particion.memoria)+' MB '+' -->  |Proceso| '+ particion.nombre)
      i+=1

   print('MEMORIA LIBRE: '+str(M.libre)+' MB')
   print('CANT PARTICIONES: '+str(len(M.particiones)))
   print('---------------------------------')

if __name__ == "__main__":
   import random
   M = Memoria(256,'DDR4',15,2,2)

   for i in range(5):
      P = Proceso('P-'+str(random.randrange(200)),0,33,random.randrange(10)+5)
      M.agregarProceso(P)
   
   print('NUEVA TANDA')
   imprimirMemoria(M)
   M.liberarParticion(0)
   imprimirMemoria(M)
   M.liberarParticion(4)
   imprimirMemoria(M)
   M.liberarParticion(0)
   imprimirMemoria(M)
   M.liberarParticion(3)
   imprimirMemoria(M)
   M.liberarParticion(2)
   imprimirMemoria(M)
   M.liberarParticion(1)
   imprimirMemoria(M)
