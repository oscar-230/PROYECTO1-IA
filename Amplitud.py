#Oscar David Cuaical López - 2270657
#Javier Andres Lasso Rojas - 2061149
#Juan Esteban Guerrero - 2040798

import time
from collections import deque
from main import EstadoDron, obtener_acciones_posibles, aplicar_accion

  
def busqueda_amplitud(mundo, posicion_inicial, paquetes):
    tiempo_inicial = time.time()
    estado_inicial = EstadoDron(posicion_inicial, paquetes)
    cola = deque([estado_inicial])
    visitados = set()
    visitados.add((estado_inicial.posicion, estado_inicial.paquetes_restantes))
    nodos_expandidos = 0
    
    while cola:
        estado_actual = cola.popleft()

        nodos_expandidos += 1
        
        if not estado_actual.paquetes_restantes:
            tiempo_fin = time.time()
            
            return estado_actual.camino, nodos_expandidos, len(estado_actual.camino), tiempo_fin - tiempo_inicial, estado_actual.costo_total
            
        for accion in obtener_acciones_posibles():
            nuevo_estado = aplicar_accion(estado_actual, accion, mundo)
            
            if nuevo_estado and (nuevo_estado.posicion, nuevo_estado.paquetes_restantes) not in visitados:
                cola.append(nuevo_estado)
                visitados.add((nuevo_estado.posicion, nuevo_estado.paquetes_restantes))


    tiempo_fin = time.time()
    return None, nodos_expandidos, 0, tiempo_fin - tiempo_inicial, 0