##############################################################################################
#                    ADMINISTRACION DE MEMORIA:                #           ALUMNO:           #
#     ALOCACION CONTIGUA DE MEMORIA – PARTICIONES DINAMICAS    #     SERGIO DARIO MACIEL     #
##############################################################################################
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *

from archivo import Archivo
from proceso import Proceso
from memoria import Memoria
from adminMemoria import AdminMemoria


def imprimirMemoria(M:Memoria):
   # IMPRIMIR
   log = ''
   log += '------ ESTADO MEMORIA ------ \n'
   i=0
   inicio = 0
   for particion in M.particiones:
      log += ' POS:'+str(i)+' Dir.Inicio: '+str(inicio)+' |Particion|  '+str(particion)+'   -->   |Proceso|   '+ str(particion.proceso)+'\n'
      i+=1
      inicio += particion.tamaño

   log += 'MEMORIA LIBRE: '+str(M.libre)+' MB \n'
   log += 'CANT PARTICIONES: '+str(len(M.particiones))+'\n'
   log += '---------------------------------\n'
   return log
###   Fin Imprimir   ###

def simular(tanda, tamañoMemoria:int, estrategia, tiempoSelecion:int, tiempoCarga:int, tiempoLiberacion:int):
   # SIMULAR
   simular = True
   memoria = Memoria(tamañoMemoria)

   admin = AdminMemoria(
      memoria,
      estrategia,
      tiempoSelecion,
      tiempoCarga,
      tiempoLiberacion
      )

   # Estadistica
   logs = []
   tandaOriginal = []
   indiceFragmantacion = 0
   countFragamntacion = True
   tiemposRetorno = []
   tiempoMedioRetorno = 0
   # Contador
   T = 0
   # Ordenar tanda por tiempo de Arribo
   procesos = sorted(tanda, key=lambda proceso: proceso.arribo)
   print('######################################################')
   print('#################   SIMULADOR  #######################')
   print('#########   ADMINISTRADOR DE MEMORIA  ################')
   print('######################################################')
   print()
   print('TANDA DE TRABAJO')
   for proceso in procesos:
      print(proceso)
      tandaOriginal.append(proceso)

   txt = 'INICIAR SIMULACION\nT: 0 --> Inicializar Memoria\n'
   logs.append(txt)
   print(txt)   
   
   txt = imprimirMemoria(admin.memoria)
   logs.append(txt)
   print(txt)

   T+=1
   admin.tiempo() 
   while (simular):

      if ((len(procesos)!=0)or(len(admin.memoria.particiones) > 1 )):      
               
         # LIBERACION (Mientras existan procesos a liberar)
         estado = admin.liberacion()
         while (estado['exito']):         
            Tliberacion = T
            for i in range(tiempoLiberacion):            
               txt=('T: '+str(Tliberacion)+':   --> Trabajando... '+' MemLib.: '+str(admin.memoria.libre)+'\n')
               logs.append(txt)
               print(txt)
               Tliberacion +=1
               admin.tiempo()               
               if (countFragamntacion):
                  indiceFragmantacion += admin.memoria.libre
            
            # Resta al indice la memoria contada como libre
            # en el ultimo ciclo.
            if (countFragamntacion):
               indiceFragmantacion -= estado['proceso'].tamaño
         
            T+=tiempoLiberacion
            txt = ('--- LIBERACION COMPLETADA ---\n')
            logs.append(txt)
            print(txt)
            tiemposRetorno.append({
               'proceso':estado['proceso'].nombre,
               'arribo':estado['proceso'].arribo,
               'tiempoRetorno':T - 1
            })
            admin.arribos = True #Permite nuevos arrivos
            estado = admin.liberacion()
            txt = (imprimirMemoria(admin.memoria))
            logs.append(txt)
            print(txt)
         
         # SELECCION
         if (len(procesos)!=0):
            proceso = procesos[0]
            # Verifica que esten permitidos los arribos y sea el turno del proceso
            if ((admin.arribos)and(proceso.arribo <= T)):
               Tseleccion = T
               for i in range(tiempoSelecion):
                  txt = ('T: '+str(Tseleccion)+':   --> SELECCIONANDO PARTICION AL PROCESO: '+str(proceso)+' MemLib: '+str(admin.memoria.libre)+'\n')
                  logs.append(txt)
                  print(txt)
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
                     txt = ('T: '+str(Tasignacion)+':   --> CARGANDO PROCESO: '+str(proceso.nombre)+' MemLib: '+str(memoriaLibreAsignacion)+'\n')
                     logs.append(txt)
                     print(txt)
                     Tasignacion += 1
                     admin.tiempo()
                     # Verifica | Si no es el ultimo proceso en arribar cuanta IndFrag / Detiene la cuenta.
                     indiceFragmantacion += memoriaLibreAsignacion
                  
                  T+=tiempoCarga
                  
                  txt = imprimirMemoria(admin.memoria)
                  logs.append(txt)
                  print(txt)
                  procesos.pop(0)
                  if (len(procesos)==0):
                     countFragamntacion = False
               else:
                  if (proceso.tamaño > admin.memoria.tamaño):
                     txt = ('T: '+str(T)+':   --> EL PROCESO: '+str(proceso.nombre)+' EXEDE EL TAMAÑO DE LA MEMORIA'+'\n')
                     logs.append(txt)
                     print(txt)
                  
            else:
               txt = ('T: '+str(T)+':   --> Sin Arribos\n')
               logs.append(txt)
               print(txt)
               # TIEMPO  
               T+=1         
               admin.tiempo()
               if (countFragamntacion):
                  indiceFragmantacion += admin.memoria.libre
         else:
            txt = ('T: '+str(T)+':   --> Sin Arribos - Tanda Completada'+'\n')
            logs.append(txt)
            print(txt)
            # TIEMPO  
            T+=1         
            admin.tiempo()
            tetx = imprimirMemoria(admin.memoria)
            logs.append(txt)
            print(txt)

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

   return logs

###   Fin Simula  ####

###   Geafica  ###
window = Tk() 
# mainFrame = Frame(master=window)
window.title("ADMINISTRADOR DE MEMORIA")
window.geometry('550x110')
window.filename =  filedialog.askopenfilename(initialdir = "/",title = "SELECCIONAR TANDA",filetypes = (("Txt files","*.txt"),("all files","*.*")))

window.after(1, lambda: window.focus_force())
frameCrl = Frame(window)
frameCrl.pack( side = TOP )

lblTiempos = Label(frameCrl, text=" MEMORIA", justify=LEFT)
lblTiempos.grid(column=0, row=0) 

lblMemoria = Label(frameCrl, text=" Tamaño:") 
lblMemoria.grid(column=0, row=1) 
txtMemoria = Entry(frameCrl, width=10)
txtMemoria.grid(column=1, row=1)
# Separador
Label(frameCrl, text="", justify=CENTER, width=5).grid(column=3, row=0) 

lblTiempos = Label(frameCrl, text="TIEMPOS", justify=LEFT)
lblTiempos.grid(column=4, row=0) 

lblTseleccion = Label(frameCrl, text="Seleccion:",width=10)
lblTseleccion.grid(column=4, row=1) 
txtTseleccion = Entry(frameCrl, width=5) 
txtTseleccion.grid(column=5, row=1)

lblTcarga = Label(frameCrl, text="Carga:",width=10)
lblTcarga.grid(column=4, row=2) 
txtTcarga = Entry(frameCrl, width=5) 
txtTcarga.grid(column=5, row=2)

lblTliberacion = Label(frameCrl, text="Liberación:",width=10)
lblTliberacion.grid(column=4, row=3) 
txtTliberacion = Entry(frameCrl, width=5) 
txtTliberacion.grid(column=5, row=3)

# Separador
lblTiempos = Label(frameCrl, text="", justify=CENTER, width=5)
lblTiempos.grid(column=7, row=0) 

lblTliberacion = Label(frameCrl, text="ESTRATEGIA:", justify=LEFT)
lblTliberacion.grid(column=8, row=0) 

selected = StringVar()
selected.set('first-fit')
rad1 = Radiobutton(frameCrl,text='First Fit', value='first-fit', variable=selected, width=10) 
rad1.grid(column=8, row=1)
rad2 = Radiobutton(frameCrl,text='Best Fit', value='best-fit', variable=selected, width=10) 
rad2.grid(column=8, row=2)
rad3 = Radiobutton(frameCrl,text='Next Fit', value='next-fit', variable=selected, width=10)
rad3.grid(column=8, row=3)
rad4 = Radiobutton(frameCrl,text='Worst Fit', value='worst-fit', variable=selected, width=10)
rad4.grid(column=8, row=4)
 
def clicked(): 
   # ARCHIVO
   tanda = Archivo().leer(window.filename)
   # MEMORIA 
   tamañoMemoria = txtMemoria.get()
   #ESTRATEGIA
   estrategia = selected.get()
   # TIEMPO DE SELECCION
   tiempoSelecion = txtTseleccion.get()
   # TIEMPO DE CARGA
   tiempoCarga = txtTcarga.get()
   # TIEMPO DE LIBERACION
   tiempoLiberacion = txtTliberacion.get()
   # Simular CPU
   logs = simular(
      tanda,
      int(tamañoMemoria),
      estrategia,
      int(tiempoSelecion),
      int(tiempoCarga),
      int(tiempoLiberacion)
      )


# Separador
Label(frameCrl, text="", justify=CENTER, width=10).grid(column=11, row=0)   
   
btn = Button(frameCrl, text="Simular", command=clicked)
btn.grid(column=12, row=2)



window.mainloop()
###   Fin Grafica    ###
