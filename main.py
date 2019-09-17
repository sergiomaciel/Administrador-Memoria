##############################################################################################
#                    ADMINISTRACION DE MEMORIA:                #           ALUMNO:           #
#     ALOCACION CONTIGUA DE MEMORIA – PARTICIONES DINAMICAS    #     SERGIO DARIO MACIEL     #
##############################################################################################

from .archivo import CargarArchivo

# TAMAÑO MEMORIA 
memoria = 256

# ESTRAGIA
estrategia = {
   'first-fit': 1,
   'best-fit': 2,
   'next-fit': 3,
   'worst-fit': 4
   }

# TIEMPO DE SELECCION
tiempoSelecion = 0

# TIEMPO DE CARGA
tiempoCarga = 0

# TIEMPO DE LIBERACION
tiempoLiberacion = 0