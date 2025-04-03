import heapq
import time
from main import EstadoDron, obtener_acciones_posibles, aplicar_accion

def heuristica_Astar(posicion, paquetes_restantes):
    if not paquetes_restantes:
        return 0
    #Distancia Manhattan
    return min(abs(posicion[0] - px) + abs(posicion[1] - py) for px, py in paquetes_restantes)

def busqueda_A_star(mundo, posicion_inicial, paquetes):
    inicio_tiempo = time.time()
    
    estado_inicial = EstadoDron(posicion_inicial, paquetes)
    frontera = [(heuristica_Astar(posicion_inicial, paquetes), estado_inicial)]
    explorados = set()
    nodos_expandidos = 0
    
    while frontera:
        _, estado_actual = heapq.heappop(frontera)
        
        if estado_actual in explorados:
            continue
        
        explorados.add(estado_actual)
        nodos_expandidos += 1

        if not estado_actual.paquetes_restantes:
            tiempo_total = time.time() - inicio_tiempo
            return estado_actual.camino, nodos_expandidos, len(estado_actual.camino), tiempo_total, estado_actual.costo_total

        for accion in obtener_acciones_posibles():
            nuevo_estado = aplicar_accion(estado_actual, accion, mundo)
            if nuevo_estado and nuevo_estado not in explorados:
                heapq.heappush(frontera, (nuevo_estado.costo_total + heuristica_Astar(nuevo_estado.posicion, nuevo_estado.paquetes_restantes), nuevo_estado))

    return None, nodos_expandidos, 0, time.time() - inicio_tiempo, float('inf')
