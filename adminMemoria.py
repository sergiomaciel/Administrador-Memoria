from proceso import Proceso
from particion import Particion
from memoria import Memoria

class AdminMemoria():

   def __init__(self, memoria:Memoria, estrategia, tiempoSeleccion, tiempoCarga, tiempoLiberacion):
      
      self.memoria = memoria
      self.estrategia = estrategia
      self.tiempoSeleccion = tiempoSeleccion
      self.tiempoCarga = tiempoCarga
      self.tiempoLiberacion = tiempoLiberacion

      self.posUtimo = 0
   

   def agregarProceso(self, proceso:Proceso):
      
      # def switch(estrategia ,proceso):
      #    sw = {
      #       'first-fit': self.__estrategia_FirstFit(proceso),
      #       'best-fit': self.__estrategia_BestFit(proceso),
      #       'next-fit': self.__estrategia_NextFit(proceso),
      #       'worst-fit':self.__estrategia_WorstFit(proceso)            
      #    }
      #    return sw.get(estrategia)

      # switch(self.estrategia, proceso)
      # self.__estrategia_FirstFit(proceso)
      # self.__estrategia_BestFit(proceso)
      # self.__estrategia_NextFit(proceso)
      self.__estrategia_WorstFit(proceso)
      pass


   def __estrategia_FirstFit(self, proceso:Proceso):        
      # Busca y selecciona la primer particion que se ajusta al proceso
      print('Estrategia: '+str(self.estrategia))
      allParticiones = self.memoria.particiones
      i=0
      fin = False
      while ((i<=len(allParticiones)-1) and (fin==False)):
         if ((allParticiones[i].libre) and (proceso.tamaño<=allParticiones[i].tamaño)):
            fragmentacion = allParticiones[i].tamaño - proceso.tamaño            
            self.memoria.asignarParticion(i, proceso)
            if (fragmentacion > 0):
               newParticion = Particion(tamaño=fragmentacion,libre=True)
               self.memoria.insertarEntre(newParticion,i+1,i)
            
            fin = True
         
         i+=1
      
      pass   

   def __estrategia_BestFit(self, proceso:Proceso):
      # Selecciona la particion que mejor se ajusta al proceso
      print('Estrategia: '+str(self.estrategia))
      allParticiones = self.memoria.particiones
      i = 0
      posMejor = 0
      cantCandidatos = 0
      maxTamaño = self.memoria.libre
      # Busca
      for particion in allParticiones:
         if ((particion.libre) and (proceso.tamaño<=particion.tamaño)):
            if (particion.tamaño <= maxTamaño):
               posMejor = i
               cantCandidatos += 1
               maxTamaño = particion.tamaño
         
         i+=1
      # BUSCAR LA FORMA DE CARGAR UN DISCCIONARIO O ARRAY CON LAS PARTICIONES QUE 
      # QUE SE ADAPTEN AL PROCESO; ORDENAR DE MENOR A MAYOR 

      # Si encontro una particion y esta libre(vuelve apregunt por si esla Pos 0 = asignado por default)
      if (cantCandidatos > 0):
         fragmentacion = allParticiones[posMejor].tamaño - proceso.tamaño            
         self.memoria.asignarParticion(posMejor, proceso)
         if (fragmentacion > 0):
            newParticion = Particion(tamaño=fragmentacion,libre=True)
            self.memoria.insertarEntre(newParticion,posMejor+1,posMejor)

      pass


   def __estrategia_NextFit(self, proceso:Proceso):
      # Desde la ultima insercion en memoria se comienza
      # a analizar la memoria para incertar el nuevo proceso

      allParticiones = self.memoria.particiones
      # BUSCA DESDE EL EL UTIMO INGRESA HASTA LA ULTIMA PARTICION
      i = self.posUtimo
      fin = False
      while ((i<=len(allParticiones)-1) and (fin==False)):
         if ((allParticiones[i].libre) and (proceso.tamaño<=allParticiones[i].tamaño)):
            fragmentacion = allParticiones[i].tamaño - proceso.tamaño            
            self.memoria.asignarParticion(i, proceso)
            self.posUtimo = i
            if (fragmentacion > 0):
               newParticion = Particion(tamaño=fragmentacion,libre=True)
               self.memoria.insertarEntre(newParticion,i+1,i)
            
            fin = True
         
         i+=1
      # BUSCA DESDE EL PRINCIPIO DE LA PARTICIONES UTIMO EN INGRESA
      if (fin==False):         
         i=0
         while ((i<=len(allParticiones)-1)  and (i<self.posUtimo)):
            if ((allParticiones[i].libre) and (proceso.tamaño<=allParticiones[i].tamaño)):
               fragmentacion = allParticiones[i].tamaño - proceso.tamaño            
               self.memoria.asignarParticion(i, proceso)
               self.posUtimo = i
               if (fragmentacion > 0):
                  newParticion = Particion(tamaño=fragmentacion,libre=True)
                  self.memoria.insertarEntre(newParticion,i+1,i)
               
               fin = True
            
            i+=1
      print('Pos Ultima Insert: '+str(self.posUtimo))     
      pass  


   def __estrategia_WorstFit(self, proceso:Proceso):
      # Selecciona la mayor particion para el proceso
      print('Estrategia: '+str(self.estrategia))
      allParticiones = self.memoria.particiones
      i = 0
      posMejor = 0
      cantCandidatos = 0
      minTamaño = 0
      # Busca
      for particion in allParticiones:
         if ((particion.libre) and (proceso.tamaño<=particion.tamaño)):
            if (particion.tamaño >= minTamaño):
               posMejor = i
               cantCandidatos += 1
               minTamaño = particion.tamaño
         
         i+=1
      # BUSCAR LA FORMA DE CARGAR UN DISCCIONARIO O ARRAY CON LAS PARTICIONES QUE 
      # QUE SE ADAPTEN AL PROCESO; ORDENAR DE MENOR A MAYOR 

      # Si encontro una particion y esta libre(vuelve apregunt por si esla Pos 0 = asignado por default)
      if (cantCandidatos > 0):
         fragmentacion = allParticiones[posMejor].tamaño - proceso.tamaño            
         self.memoria.asignarParticion(posMejor, proceso)
         if (fragmentacion > 0):
            newParticion = Particion(tamaño=fragmentacion,libre=True)
            self.memoria.insertarEntre(newParticion,posMejor+1,posMejor)

      pass


   
   def eliminarProceso(self, pos):
      self.memoria.vaciarParticion(pos)
      
      if (self.posUtimo >= pos):
         self.posUtimo-=1

      if (self.verificarCompactacion(pos)):
         print('COMPACTAR PARTICION '+str(pos))
         self.compactar(pos)
      else:
         print('SIN COMPACTACION')

   def verificarCompactacion(self, pos):
      particiones = self.memoria.particiones
      if ( (pos>0)and(pos<(len(particiones)-1)) ):
         # Verifica si la POS esta libre la POS ANTERIOR O LA POSTERIOR
         if ( (particiones[pos-1].libre) or (particiones[pos+1].libre) ):
            return True
         else:
            return False
      else:
         # Verifica si la  1er POS esta libre y la 2da POS esta libre
         if ( (pos==0)and(particiones[pos+1].libre) ):
            return True
         # Verifica si la ultima POS esta libre y la antes ultima POS esta libre
         if ( (pos==(len(particiones)-1))and(particiones[pos-1].libre) ):
            return True

         return False
      pass
   

   def compactar(self, pos):
      particiones = self.memoria.particiones
      memoriaTotal = particiones[pos].tamaño
      
      posBase = pos
      posTope = pos
      posIzq = pos-1
      posDer = pos+1
      
      # BUSCAR PARTICIONES LIBRES POR IZQ DE LA POS
      if ((posIzq>=0) and (particiones[posIzq].libre)):
         memoriaTotal += particiones[posIzq].tamaño
         posBase = posIzq         
         posIzq -=1

      # BUSCAR PARTICIONES LIBRES POR DER DE LA POS
      if ((posDer<=(len(particiones)-1)) and (particiones[posDer].libre)):
         memoriaTotal += particiones[posDer].tamaño
         posTope = posDer
         posDer +=1

      print('-- Desde: '+str(posBase)+'  Hasta: '+str(posTope))
      # RECALCULAR TAMAÑO DE LA NUEVA PARTICION LIBRE
      newPartUnif = Particion(tamaño=memoriaTotal, libre=True)
      self.memoria.insertarEntre(newPartUnif,posBase,posTope)
      pass

def imprimirMemoria(M:Memoria):
   # IMPRIMIR
   print()
   print('MEMORIA - '+str(M.tamaño)+' MB')
   i=0
   inicio = 0
   for particion in M.particiones:
      print(' POS:'+str(i)+' Dir.Inicio: '+str(inicio)+' |Particion|  '+str(particion)+'   -->   |Proceso|   '+ str(particion.proceso))
      i+=1
      inicio += particion.tamaño

   print('MEMORIA LIBRE: '+str(M.libre)+' MB')
   print('CANT PARTICIONES: '+str(len(M.particiones)))
   print('---------------------------------')

if __name__ == "__main__":
   import random
   M = Memoria(256)
   # AdmMem = AdminMemoria(M,'first-fit',15,2,2)
   AdmMem = AdminMemoria(M,'next-fit',15,2,2)

   for i in range(6):
      P = Proceso(
         nombre='P-'+str(i),
         arribo=random.randrange(60)+1,
         tiempoTotal=random.randrange(50)+1,
         tamaño=random.randrange(10)+35
         )
      AdmMem.agregarProceso(P)
   
   print('NUEVA TANDA')
   imprimirMemoria(AdmMem.memoria)
   # AdmMem.eliminarProceso(0)
   AdmMem.eliminarProceso(1)
   AdmMem.eliminarProceso(3)
   # imprimirMemoria(AdmMem.memoria)
 
   # imprimirMemoria(AdmMem.memoria)
   AdmMem.eliminarProceso(2)
   imprimirMemoria(AdmMem.memoria)
   
   for i in range(1):
      P = Proceso(
         nombre='PR-'+str(random.randrange(200)),
         arribo=random.randrange(60)+1,
         tiempoTotal=random.randrange(50)+1,
         tamaño=random.randrange(10)+10
         )
      AdmMem.agregarProceso(P)

   imprimirMemoria(AdmMem.memoria)

