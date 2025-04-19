import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from Amplitud import busqueda_amplitud
from main import leer_mundo
from Profundidad import busqueda_profundidad #from Profundidad import busqueda_profundidad_evitando_ciclos    
from CostoUniforme import busqueda_costo_uniforme
from Avara import busqueda_avara
from A_star import busqueda_A_star


def visualizar_resultado(mundo, camino, posicion_inicial, paquetes_originales):
    # Configurar colores para la visualización
    cmap = mcolors.ListedColormap(['white', 'black', 'green', 'red', 'blue'])
    bounds = [0, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = Normalize(vmin=min(bounds), vmax=max(bounds)) 
    
    # Crear figura 
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Posiciones visitadas en el camino
    posiciones_camino = [posicion_inicial] + [pos for pos, _ in camino]
    
    # Función para actualizar la animación
    def update(frame):
        ax.clear()
        
        mundo_copia = mundo.copy()
        
        # Marcar paquetes restantes
        paquetes_restantes = set(paquetes_originales)
        for i in range(frame + 1):
            pos = posiciones_camino[i]
            if pos in paquetes_restantes:
                paquetes_restantes.remove(pos)
        
        for pos in paquetes_restantes:
            mundo_copia[pos] = 4
        
        ax.imshow(mundo_copia, cmap=cmap, norm=norm)
        
        # Mostrar posición actual del dron
        pos_actual = posiciones_camino[frame]
        ax.plot(pos_actual[1], pos_actual[0], 'ko', markersize=10)
        
        # Dibujar camino recorrido
        if frame > 0:
            camino_x = [posiciones_camino[i][1] for i in range(frame + 1)]
            camino_y = [posiciones_camino[i][0] for i in range(frame + 1)]
            ax.plot(camino_x, camino_y, 'y-', linewidth=2)
        
        if frame > 0:
            costo_actual = sum(costo for _, costo in camino[:frame])
            ax.set_title(f'Paso {frame}/{len(posiciones_camino)-1} - Costo acumulado: {costo_actual}')
        else:
            ax.set_title('Posición inicial')
        
        # Configurar ejes
        ax.set_xticks(np.arange(-0.5, 10, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, 10, 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        ax.set_xticks(np.arange(0, 10, 1))
        ax.set_yticks(np.arange(0, 10, 1))
        
        # Leyenda
        patches = [
            plt.Rectangle((0, 0), 1, 1, facecolor='white', edgecolor='gray', label='Libre'),
            plt.Rectangle((0, 0), 1, 1, facecolor='black', label='Obstáculo'),
            plt.Rectangle((0, 0), 1, 1, facecolor='green', label='Inicio'),
            plt.Rectangle((0, 0), 1, 1, facecolor='red', label='Campo Electromagnético'),
            plt.Rectangle((0, 0), 1, 1, facecolor='blue', label='Paquete'),
            plt.Line2D([0], [0], color='y', lw=2, label='Camino'),
            plt.Line2D([0], [0], marker='o', color='black', markersize=10, label='Dron')
        ]
        ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left')
    
    ani = FuncAnimation(fig, update, frames=len(posiciones_camino), interval=500, repeat=False)
    
    plt.tight_layout()
    plt.show()
    
    return ani

def mostrar_reporte(Camino, nodos_expandidos, profundidad, tiempo, costo):
    print("\n--- REPORTE DE LA BÚSQUEDA ---")
    print(f"Nodos expandidos: {nodos_expandidos}")
    print(f"Profundidad del árbol: {profundidad}")
    print(f"Tiempo de cómputo: {tiempo:.4f} segundos")
    print(f"Costo de la solución: {costo}")
    print("-----------------------------\n")

def main():
    """
    Función principal que ejecuta el programa.
    """
    # Solicitar la ruta del archivo
    ruta_archivo = './input/Prueba1.txt'
    
    # Leer el mundo
    mundo, posicion_inicial, paquetes = leer_mundo(ruta_archivo)
    
    if mundo is None:
        print("No se pudo leer el archivo correctamente.")
        return
    
    # Mostrar opciones de algoritmos
    print("\nSeleccione el algoritmo de búsqueda:")
    print("1. Búsqueda No Informada - Amplitud")
    print("2. Búsqueda No Informada - Costo Uniforme")
    print("3. Búsqueda No Informada - Profundidad evitando ciclos")
    print("4. Búsqueda Informada - Avara")
    print("5. Búsqueda Informada - A*")
    
    opcion = input("Ingrese su opción (1-5): ")
    
    # Aplicar el algoritmo seleccionado
    if opcion == "1":
        print("\nAplicando Búsqueda por Amplitud...")
        camino, nodos_expandidos, profundidad, tiempo, costo = busqueda_amplitud(mundo, posicion_inicial, paquetes)
        if camino:
            print("¡Solución encontrada!")
            mostrar_reporte(camino, nodos_expandidos, profundidad, tiempo, costo)
            visualizar_resultado(mundo, camino, posicion_inicial, paquetes)
        else:
            print("No se encontró solución.")
    
    elif opcion == "2":
        print("\nAplicando Búsqueda por Costo Uniforme...")
        camino, nodos_expandidos, profundidad, tiempo, costo = busqueda_costo_uniforme(mundo, posicion_inicial, paquetes)
        if camino:
            print("¡Solución encontrada!")
            mostrar_reporte(camino, nodos_expandidos, profundidad, tiempo, costo)
            visualizar_resultado(mundo, camino, posicion_inicial, paquetes)
        else:
            print("No se encontró solución.")
    elif opcion == "3":
        print("\nAplicando Búsqueda por Profundidad evitando Ciclos...")
        camino, nodos_expandidos, profundidad, tiempo, costo = busqueda_profundidad(mundo, posicion_inicial, paquetes)
        if camino:
             print("¡Solución encontrada!")
             mostrar_reporte(camino, nodos_expandidos, profundidad, tiempo, costo)
             visualizar_resultado(mundo, camino, posicion_inicial, paquetes)
        else:
             print("No se encontró solución.")
    elif opcion == "4":
        print("\nAplicando Búsqueda Avara...")
        camino, nodos_expandidos, profundidad, tiempo, costo = busqueda_avara(mundo, posicion_inicial, paquetes)
        if camino:
            print("¡Solución encontrada!")
            mostrar_reporte(camino, nodos_expandidos, profundidad, tiempo, costo)
            visualizar_resultado(mundo, camino, posicion_inicial, paquetes)
        else:
            print("No se encontró solución.")
    elif opcion == "5":
        print("\nAplicando Búsqueda A*...")
        camino, nodos_expandidos, profundidad, tiempo, costo = busqueda_A_star(mundo, posicion_inicial, paquetes)
        if camino:
            print("¡Solución encontrada!")
            mostrar_reporte(camino, nodos_expandidos, profundidad, tiempo, costo)
            visualizar_resultado(mundo, camino, posicion_inicial, paquetes)
        else:
            print("No se encontró solución.")

if __name__ == "__main__":
    main()