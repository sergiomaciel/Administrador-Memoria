##############################################################################################
#                    ADMINISTRACION DE MEMORIA:                #           ALUMNO:           #
#     ALOCACION CONTIGUA DE MEMORIA – PARTICIONES DINAMICAS    #     SERGIO DARIO MACIEL     #
##############################################################################################

from archivo import Archivo
from proceso import Proceso
from memoria import Memoria
from adminMemoria import AdminMemoria

# ARCHIVO
tanda = Archivo().leer('archivo1')

# MEMORIA 
tamañoMemoria = 512

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
   estrategia[3],
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
# Contador
T = 0
print('T: '+str(T)+' --> Inicializar Memoria')
imprimirMemoria(admin.memoria)
T+=1 
while (simular):

   if (len(procesos)!=0):      
            
      # LIBERACION (Mientras existan procesos a liberar)
      estado = admin.liberacion()
      while (estado['exito']):         
         Tliberacion = T
         for i in range(tiempoLiberacion):
            print('T: '+str(Tliberacion)+':   --> Trabajando... ')
            Tliberacion +=1
            admin.tiempo()
         
         T+=tiempoLiberacion
         print('--- LIBERACION COMPLETADA ---')
         estado = admin.liberacion()
         imprimirMemoria(admin.memoria)
      
       # SELECCION
      proceso = procesos[0]     
      if (proceso.arribo <= T):
         Tseleccion = T
         for i in range(tiempoSelecion):
            print('T: '+str(Tseleccion)+':   --> SELECCIONANDO PARTICION AL PROCESO: '+str(proceso))
            Tseleccion += 1
            admin.tiempo()

         T+=tiempoSelecion
         
         # ASIGNACION
         if (admin.arriboProceso(proceso)):
            Tasignacion = T
            for i in range(tiempoCarga):
               print('T: '+str(Tasignacion)+':   --> CARGANDO PROCESO: '+str(proceso))
               Tasignacion += 1
               admin.tiempo()
            
            T+=tiempoCarga
            
            imprimirMemoria(admin.memoria)    
            procesos.pop(0)
            
      else:
         print('T: '+str(T)+':   --> Sin Arribos')
         # TIEMPO           
         admin.tiempo()
         T+=1

   else:
      simular = False
   

# print('PARTICIONES A LIBERAR')
# for particiones in admin.particionesLiberar:
#    print(particiones)

