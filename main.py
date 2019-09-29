##############################################################################################
#                    ADMINISTRACION DE MEMORIA:                #           ALUMNO:           #
#     ALOCACION CONTIGUA DE MEMORIA – PARTICIONES DINAMICAS    #     SERGIO DARIO MACIEL     #
##############################################################################################

from archivo import Archivo
from proceso import Proceso
from memoria import Memoria
from adminMemoria import AdminMemoria

# ARCHIVO
tanda = Archivo().leer('archivo2')

# MEMORIA 
tamañoMemoria = 150

# ESTRAGIA
estrategia = [
   'first-fit',
   'best-fit',
   'next-fit',
   'worst-fit'
   ]

# TIEMPO DE SELECCION
tiempoSelecion = 1

# TIEMPO DE CARGA
tiempoCarga = 1

# TIEMPO DE LIBERACION
tiempoLiberacion = 1

# -----SIMULAR-------
memoria = Memoria(tamañoMemoria)

admin = AdminMemoria(
   memoria,
   estrategia[0],
   tiempoSelecion,
   tiempoCarga,
   tiempoLiberacion
   )



# Ordenar tanda por tiempo de Arribo
procesos = sorted(tanda, key=lambda proceso: proceso.arribo)
print()
print('TANDA DE TRABAJO')
for proceso in procesos:
   print(proceso)

print()
print('INICIAR SIMULACION')
print()

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

# Simular CPU
simular = True
# Estadistica
indiceFragmantacion = 0
countFragamntacion = True
tiemposRetorno = []
tiempoMedioRetorno = 0
# Contador
T = 0
print('T: '+str(T)+' --> Inicializar Memoria')
imprimirMemoria(admin.memoria)
T+=1
# indiceFragmantacion += admin.memoria.libre
while (simular):

   if ((len(procesos)!=0)or(len(admin.memoria.particiones) > 1 )):      
            
      # LIBERACION (Mientras existan procesos a liberar)
      estado = admin.liberacion()
      while (estado['exito']):         
         Tliberacion = T
         for i in range(tiempoLiberacion):
            print('T: '+str(Tliberacion)+':   --> Trabajando... '+' MemLib.: '+str(admin.memoria.libre))
            Tliberacion +=1
            if (countFragamntacion):
               indiceFragmantacion += admin.memoria.libre

            admin.tiempo()
                     
         T+=tiempoLiberacion
         print('--- LIBERACION COMPLETADA ---')
         tiemposRetorno.append({
            'proceso':estado['proceso'].nombre,
            'arribo':estado['proceso'].arribo,
            'tiempoRetorno':T - 1
         })
         admin.arribos = True #Permite nuevos arrivos
         estado = admin.liberacion()
         imprimirMemoria(admin.memoria)
      
       # SELECCION
      if (len(procesos)!=0):
         proceso = procesos[0]
         # Verifica que esten permitidos los arribos y sea el turno del proceso
         if ((admin.arribos)and(proceso.arribo <= T)):
            Tseleccion = T
            for i in range(tiempoSelecion):
               print('T: '+str(Tseleccion)+':   --> SELECCIONANDO PARTICION AL PROCESO: '+str(proceso)+' MemLib: '+str(admin.memoria.libre))
               Tseleccion += 1
               admin.tiempo()
               if (countFragamntacion):
                  indiceFragmantacion += admin.memoria.libre

            T+=tiempoSelecion
            
            # ASIGNACION
            procesoAsig = Proceso(
               proceso.nombre,
               proceso.arribo,
               proceso.tiempoTotal + tiempoCarga,
               proceso.tamaño
               )
            memoriaLibreAsignacion = admin.memoria.libre
            if (admin.arriboProceso(procesoAsig)):
               Tasignacion = T
               for i in range(tiempoCarga):
                  print('T: '+str(Tasignacion)+':   --> CARGANDO PROCESO: '+str(proceso.nombre)+' MemLib: '+str(memoriaLibreAsignacion))
                  Tasignacion += 1
                  admin.tiempo()
                  # Verifica | Si no es el ultimo proceso en arribar cuanta IndFrag / Detiene la cuenta.
                  indiceFragmantacion += memoriaLibreAsignacion
               
               T+=tiempoCarga
               
               imprimirMemoria(admin.memoria)
               procesos.pop(0)
               if (len(procesos)==0):
                  countFragamntacion = False
            else:
               if (proceso.tamaño > admin.memoria.tamaño):
                  print('T: '+str(T)+':   --> EL PROCESO: '+str(proceso.nombre)+' EXEDE EL TAMAÑO DE LA MEMORIA')
               
         else:
            print('T: '+str(T)+':   --> Sin Arribos'+' MemLib: '+str(indiceFragmantacion))
            # TIEMPO  
            T+=1         
            admin.tiempo()
            if (countFragamntacion):
               indiceFragmantacion += admin.memoria.libre
      else:
         print('T: '+str(T)+':   --> Sin Arribos - Tanda Completada')
         # TIEMPO  
         T+=1         
         admin.tiempo()
         imprimirMemoria(admin.memoria)

   else:
      simular = False
   
print('ESTRATEGIA: '+admin.estrategia)
print('FRAGMENTACION EXTERNA: '+str(indiceFragmantacion))
print('TIEMPO DE RETORNO | PROCESOS | ')
for dato in tiemposRetorno:
   tiempoRetorno = dato['tiempoRetorno'] - dato['arribo']
   print(
      '| '+str(dato['proceso'])+' |'+
      ' Arribo: '+str(dato['arribo'])+
      ' Retorno: '+str(dato['tiempoRetorno'])+
      ' Tiempo Retorno: '+str(tiempoRetorno)
   )
   tiempoMedioRetorno += tiempoRetorno

# len(tiemposRetorno) retorn la cantidad de procesos
print('TIEMPO MEDIO DE RETORNO: '+ str(tiempoMedioRetorno / len(tiemposRetorno)))
print('TIEMPO DE RETORNO DE LA TANDA: '+str(tiemposRetorno.pop()['tiempoRetorno']))