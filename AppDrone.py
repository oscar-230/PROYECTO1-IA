import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from Amplitud import busqueda_amplitud
from Profundidad import busqueda_profundidad
from CostoUniforme import busqueda_costo_uniforme
from Avara import busqueda_avara
from A_star import busqueda_A_star
from main import leer_mundo
from PIL import Image


algoritmos = {
    "No Informada": {
        "Amplitud": busqueda_amplitud,
        "Costo Uniforme": busqueda_costo_uniforme,
        "Profundidad evitando ciclos": busqueda_profundidad
    },
    "Informada": {
        "Avara": busqueda_avara,
        "A*": busqueda_A_star
    }
}

def mostrar_reporte(Camino, nodos_expandidos, profundidad, tiempo, costo):
    print("\n--- REPORTE DE LA BÚSQUEDA ---")
    print(f"Nodos expandidos: {nodos_expandidos}")
    print(f"Profundidad del árbol: {profundidad}")
    print(f"Tiempo de cómputo: {tiempo:.4f} segundos")
    print(f"Costo de la solución: {costo}")
    print("-----------------------------\n")

def mostrar_reporte_gui(nodos_expandidos, profundidad, tiempo, costo=None):
    mensaje = f"Nodos expandidos: {nodos_expandidos}\n"
    mensaje += f"Profundidad del árbol: {profundidad}\n"
    mensaje += f"Tiempo de cómputo: {tiempo:.4f} segundos\n"
    if costo is not None:
        mensaje += f"Costo de la solución: {costo}\n"
    messagebox.showinfo("Reporte de la Búsqueda", mensaje)

cesped_img = Image.open("./assets/cesped.png")
drone_img = Image.open("./assets/drone.png")
paquete_img = Image.open("./assets/paquete.png")
muro_img = Image.open("./assets/muro.png")
campo_img = Image.open("./assets/campo.png")

def visualizar_resultado(mundo, camino, posicion_inicial, paquetes_originales, camino_datos):
    cmap = mcolors.ListedColormap(['white', 'black', 'green', 'red', 'blue'])
    bounds = [0, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = Normalize(vmin=min(bounds), vmax=max(bounds)) 

    fig, ax = plt.subplots(figsize=(10, 10))
    posiciones_camino = [posicion_inicial] + [pos for pos, _ in camino]

    def update(frame):
        ax.clear()
        mundo_copia = mundo.copy()
        muros = np.argwhere(mundo_copia == 1)
        paquetes_restantes = set(paquetes_originales)

        for i in range(frame + 1):
            pos = posiciones_camino[i]
            paquetes_restantes.discard(pos)

        for pos in paquetes_restantes:
            mundo_copia[pos] = 4

        for pos in paquetes_restantes:
            img_extent = [pos[1] - 0.5, pos[1] + 0.5, pos[0] + 0.5, pos[0] - 0.5]
            ax.imshow(paquete_img, extent=img_extent, zorder=4)

        for muro_pos in muros:
            img_extent = [muro_pos[1] - 0.5, muro_pos[1] + 0.5, muro_pos[0] + 0.5, muro_pos[0] - 0.5]
            ax.imshow(muro_img, extent=img_extent, zorder=2)

        campos = np.argwhere(mundo == 3)
        for campo_pos in campos:
            img_extent = [campo_pos[1] - 0.5, campo_pos[1] + 0.5, campo_pos[0] + 0.5, campo_pos[0] - 0.5]
            ax.imshow(campo_img, extent=img_extent, zorder=3)
        
        cespedes = np.argwhere(mundo == 0)
        for cesped_pos in cespedes:
            img_extent = [cesped_pos[1] - 0.5, cesped_pos[1] + 0.5, cesped_pos[0] + 0.5, cesped_pos[0] - 0.5]
            ax.imshow(cesped_img, extent=img_extent, zorder=0.5)

        ax.imshow(mundo_copia, cmap=cmap, norm=norm)

        pos_actual = posiciones_camino[frame]
        img_extent = [pos_actual[1] - 0.5, pos_actual[1] + 0.5, pos_actual[0] + 0.5, pos_actual[0] - 0.5]
        ax.imshow(drone_img, extent=img_extent, zorder=5)


        if frame > 0:
            camino_x = [posiciones_camino[i][1] for i in range(frame + 1)]
            camino_y = [posiciones_camino[i][0] for i in range(frame + 1)]
            ax.plot(camino_x, camino_y, 'y-', linewidth=2)
            costo_actual = sum(costo for _, costo in camino[:frame])
            ax.set_title(f'Paso {frame}/{len(posiciones_camino)-1} - Costo acumulado: {costo_actual}')
        else:
            ax.set_title('Posición inicial')

        ax.set_xticks(np.arange(-0.5, 10, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, 10, 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        ax.set_xticks(np.arange(0, 10, 1))
        ax.set_yticks(np.arange(0, 10, 1))

        patches = [
            plt.Rectangle((0, 0), 1, 1, facecolor='darkgreen', edgecolor='gray', label='Libre'),
            plt.Rectangle((0, 0), 1, 1, facecolor='grey', label='Obstáculo'),
            plt.Rectangle((0, 0), 1, 1, facecolor='green', label='Inicio'),
            plt.Rectangle((0, 0), 1, 1, facecolor='red', label='Campo Electromagnético'),
            plt.Rectangle((0, 0), 1, 1, facecolor='blue', label='Paquete'),
            plt.Line2D([0], [0], color='y', lw=2, label='Camino'),
            plt.Line2D([0], [0], marker='o', color='black', markersize=10, label='Dron')
        ]
        ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left')

        if frame == len(posiciones_camino) - 1:
            mostrar_reporte_gui(*camino_datos[1:])

    ani = FuncAnimation(fig, update, frames=len(posiciones_camino), interval=500, repeat=False)
    plt.tight_layout()
    plt.show()
    return ani

def ejecutar_busqueda(tipo, nombre_algo):
    ruta_archivo = './input/Prueba1.txt'
    mundo, posicion_inicial, paquetes = leer_mundo(ruta_archivo)

    if mundo is None:
        messagebox.showerror("Error", "No se pudo leer el archivo.")
        return

    funcion_busqueda = algoritmos[tipo][nombre_algo]
    camino, nodos_expandidos, profundidad, tiempo, costo = funcion_busqueda(mundo, posicion_inicial, paquetes)

    if camino:
        mostrar_reporte(camino, nodos_expandidos, profundidad, tiempo, costo)
        camino_datos = (camino, nodos_expandidos, profundidad, tiempo, costo)
        visualizar_resultado(mundo, camino, posicion_inicial, paquetes, camino_datos)
    else:
        messagebox.showinfo("Resultado", "No se encontró una solución.")

def crear_interfaz():
    root = tk.Tk()
    root.title("Smart Drone - Simulador de Búsqueda")
    root.geometry("600x350")
    root.resizable(False, False)
    root.configure(bg="#1e1e1e")

    estilo = ttk.Style()
    estilo.theme_use('clam')
    estilo.configure("TButton", font=("Helvetica", 12, "bold"), padding=10, background="#007acc", foreground="white")
    estilo.map("TButton", background=[("active", "#005f99")])
    estilo.configure("TLabel", font=("Helvetica", 12), background="#1e1e1e", foreground="white")
    estilo.configure("TCombobox", font=("Helvetica", 12))

    marco = tk.Frame(root, bg="#2b2b2b", bd=2, relief="ridge", padx=20, pady=20)
    marco.place(relx=0.5, rely=0.5, anchor="center")

    titulo = tk.Label(marco, text="Seleccione el tipo de búsqueda y algoritmo", font=("Helvetica", 14, "bold"), bg="#2b2b2b", fg="white")
    titulo.pack(pady=(0, 15))

    label_tipo = ttk.Label(marco, text="Tipo de Búsqueda:")
    label_tipo.pack(anchor="w", pady=5)

    tipo_var = tk.StringVar()
    combo_tipo = ttk.Combobox(marco, textvariable=tipo_var, values=list(algoritmos.keys()), state="readonly")
    combo_tipo.pack(fill="x")

    label_algo = ttk.Label(marco, text="Algoritmo:")
    label_algo.pack(anchor="w", pady=5)

    algo_var = tk.StringVar()
    combo_algo = ttk.Combobox(marco, textvariable=algo_var, state="readonly")
    combo_algo.pack(fill="x")

    def actualizar_algoritmos(event):
        tipo = tipo_var.get()
        if tipo in algoritmos:
            combo_algo['values'] = list(algoritmos[tipo].keys())
            combo_algo.current(0)

    combo_tipo.bind("<<ComboboxSelected>>", actualizar_algoritmos)

    boton = ttk.Button(marco, text="Ejecutar Búsqueda", command=lambda: ejecutar_busqueda(tipo_var.get(), algo_var.get()))
    boton.pack(pady=20, fill="x")

    root.mainloop()


if __name__ == "__main__":
    crear_interfaz()
