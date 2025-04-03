import numpy as np


class EstadoDron:
    def __init__(self, posicion, paquetes_restantes, camino=None, costo_total=0):
        self.posicion = posicion
        self.paquetes_restantes = frozenset(paquetes_restantes)  # Usamos frozenset para que sea hashable
        self.camino = camino if camino is not None else []
        self.costo_total = costo_total
    
    def __lt__(self, other):
        return self.costo_total < other.costo_total
    
    def __eq__(self, other):
        return (self.posicion == other.posicion and self.paquetes_restantes == other.paquetes_restantes)
    
    def __hash__(self):
        return hash((self.posicion, self.paquetes_restantes))

def leer_mundo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as archivo:
            lineas = archivo.readlines()
        
        mundo = []
        for linea in lineas:
            fila = [int(valor) for valor in linea.strip().split()]
            mundo.append(fila)
            
        posicion_inicial = None
        paquetes = []
        
        for i in range(len(mundo)):
            for j in range(len(mundo[i])):
                if mundo[i][j] == 2:
                    posicion_inicial = (i, j)
                elif mundo[i][j] == 4:
                    paquetes.append((i, j))
                                        
        return np.array(mundo), posicion_inicial, paquetes
        
    except Exception as e:
        print(f"Error al leer el mundo: {e}")
        return None, None, None
    
def obtener_acciones_posibles():
    return [(-1, 0), (1, 0), (0, -1), (0, 1)]

def es_movimiento_valido(mundo, posicion):
    x, y = posicion
    filas, columnas = mundo.shape
    
    if x < 0 or x >= filas or y < 0 or y >= columnas:
        return False
    
    if mundo[x][y] == 1:
        return False
    
    return True

def costo_movimento(mundo, posicion):
    x, y = posicion
    if mundo[x][y] == 3:
        return 8
    else:
        return 1
    
def aplicar_accion(estado, accion, mundo):
    dx, dy = accion 
    nueva_posicion = (estado.posicion[0] + dx, estado.posicion[1] + dy)
    
    if not es_movimiento_valido(mundo, nueva_posicion):
        return None
    
    nuevos_paquetes_restantes = set(estado.paquetes_restantes)
    
    if nueva_posicion in nuevos_paquetes_restantes:
        nuevos_paquetes_restantes.remove(nueva_posicion)
    
    costo = costo_movimento(mundo, nueva_posicion)
    
    nuevo_camino = estado.camino + [(nueva_posicion, costo)]
    
    return EstadoDron(nueva_posicion, nuevos_paquetes_restantes, nuevo_camino, estado.costo_total + costo)