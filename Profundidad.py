import time
from main import EstadoDron, obtener_acciones_posibles, aplicar_accion

def busqueda_profundidad(mundo, posicion_inicial, paquetes):
    tiempo_inicial = time.time()
    estado_inicial = EstadoDron(posicion_inicial, paquetes)
    pila = [estado_inicial]
    visitados = set()
    visitados.add((estado_inicial.posicion, estado_inicial.paquetes_restantes))
    nodos_expandidos = 0

    while pila:
        estado_actual = pila.pop()
        nodos_expandidos += 1
        
        if not estado_actual.paquetes_restantes:
            tiempo_fin = time.time()
            return estado_actual.camino, nodos_expandidos, len(estado_actual.camino), tiempo_fin - tiempo_inicial, estado_actual.costo_total
        
        for accion in obtener_acciones_posibles():
            nuevo_estado = aplicar_accion(estado_actual, accion, mundo)

            if nuevo_estado and (nuevo_estado.posicion, nuevo_estado.paquetes_restantes) not in visitados:
                pila.append(nuevo_estado)
                visitados.add((nuevo_estado.posicion, nuevo_estado.paquetes_restantes))

    tiempo_fin = time.time()
    return None, nodos_expandidos, 0, tiempo_fin - tiempo_inicial, 0 
 