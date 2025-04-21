#Oscar David Cuaical López - 2270657
#Javier Andres Lasso Rojas - 2061149
#Juan Esteban Guerrero - 2040798

import heapq 
import time
from main import EstadoDron, obtener_acciones_posibles, aplicar_accion


def busqueda_costo_uniforme(mundo, posicion_inicial, paquetes):
    tiempo_inicial = time.time()

    estado_inicial = EstadoDron(posicion_inicial, paquetes)

    # Usamos un heap (cola de prioridad) para almacenar los estados
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (estado_inicial.costo_total, estado_inicial))  # (costo_total, estado)

    visitados = set()
    visitados.add((estado_inicial.posicion, estado_inicial.paquetes_restantes))

    nodos_expandidos = 0
    
    while cola_prioridad:
        # Extraemos el estado con el menor costo total
        costo_actual, estado_actual = heapq.heappop(cola_prioridad)

        nodos_expandidos += 1
        
        # Verificamos si se han recogido todos los paquetes
        if not estado_actual.paquetes_restantes:
            tiempo_fin = time.time()

            return estado_actual.camino, nodos_expandidos, len(estado_actual.camino), tiempo_fin - tiempo_inicial, estado_actual.costo_total
            
        # Exploramos las acciones posibles
        for accion in obtener_acciones_posibles():
            nuevo_estado = aplicar_accion(estado_actual, accion, mundo)
            
            if nuevo_estado:
                # Verificamos si el nuevo estado no ha sido visitado o tiene un costo menor
                if (nuevo_estado.posicion, nuevo_estado.paquetes_restantes) not in visitados:
                    heapq.heappush(cola_prioridad, (nuevo_estado.costo_total, nuevo_estado))
                    visitados.add((nuevo_estado.posicion, nuevo_estado.paquetes_restantes))

    tiempo_fin = time.time()
    return None, nodos_expandidos, 0, tiempo_fin - tiempo_inicial, 0