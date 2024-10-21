import time
import os
import psutil
import numpy as np
from tkinter import Tk, Entry, Button, messagebox, Label, Toplevel, Text, END, Frame
import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pygraphviz  

from aestrella import AEstrella
from tablero import Tablero

def main():
    raiz = Tk()
    raiz.title("8-Puzzle")

    entradas = []
 
    for i in range(3):
        fila_entradas = []
        for j in range(3):
            entrada = Entry(raiz, width=2, font=('Arial', 24), justify='center')
            entrada.grid(row=i, column=j, padx=5, pady=5)
            fila_entradas.append(entrada) 
        entradas.append(fila_entradas)

    def es_resoluble(puzzle):
        conteo_inversiones = 0
        lista_puzzle = puzzle.copy()
        lista_puzzle = lista_puzzle[lista_puzzle != 0]  # Excluir el cero
        for i in range(len(lista_puzzle)):
            for j in range(i + 1, len(lista_puzzle)):
                if lista_puzzle[i] > lista_puzzle[j]:
                    conteo_inversiones += 1
        return conteo_inversiones % 2 == 0

    def generar_puzzle_aleatorio():
        while True:
            puzzle = np.random.permutation(9)
            if es_resoluble(puzzle):
                break
        # Rellenar la matriz de entrada con los números generados
        indice = 0
        for i in range(3):
            for j in range(3):
                entradas[i][j].delete(0, END)
                entradas[i][j].insert(END, str(puzzle[indice]))
                indice += 1

    def resolver_puzzle():
        # Recopilar números de las entradas
        numeros = []
        for fila in entradas:
            for entrada in fila:
                valor = entrada.get()
                if valor == '':
                    messagebox.showerror("Error de entrada", "Por favor, completa todas las casillas con números del 0 al 8.")
                    return
                try:
                    numero = int(valor)
                except ValueError:
                    messagebox.showerror("Error de entrada", "Por favor, ingresa solo números enteros del 0 al 8.")
                    return
                if numero < 0 or numero > 8:
                    messagebox.showerror("Error de entrada", "Los números deben estar entre 0 y 8.")
                    return
                numeros.append(numero)
        # Validar que los números sean del 0 al 8 sin duplicados
        if sorted(numeros) != list(range(9)):
            messagebox.showerror("Error de entrada", "Los números deben ser del 0 al 8 sin duplicados.")
            return

        # Convertir numeros a un arreglo numpy 1D
        arreglo_puzzle = np.array(numeros)

        # Verificar si el puzzle es resoluble
        if not es_resoluble(arreglo_puzzle):
            messagebox.showerror("Puzzle no resoluble", "El puzzle ingresado no es resoluble. Por favor, ingresa una configuración válida.")
            return

        # Iniciar la solución del puzzle
        tiempo_inicio = time.perf_counter()

        p = Tablero(arreglo_puzzle)
        s = AEstrella(p)

        s.resolver()

        tiempo_ejecucion = time.perf_counter() - tiempo_inicio
        proceso = psutil.Process(os.getpid())

        # Preparar los resultados para mostrar
        texto_resultado = ''
        texto_resultado += 'ruta_al_objetivo: ' + str(s.camino) + '\n'
        texto_resultado += 'costo_del_camino: ' + str(len(s.camino)) + '\n'
        texto_resultado += 'nodos_expandidos: ' + str(s.nodos_expandidos) + '\n'
        texto_resultado += 'nodos_explorados: ' + str(len(s.nodos_explorados)) + '\n'
        texto_resultado += 'profundidad_de_búsqueda: ' + str(s.solucion.profundidad) + '\n'
        texto_resultado += 'máxima_profundidad_de_búsqueda: ' + str(s.max_profundidad) + '\n'
        texto_resultado += 'tiempo_de_ejecución: ' + str(tiempo_ejecucion) + '\n'

        # Obtener la secuencia de estados para mostrar paso a paso
        cadena_estados = s.cadena_estados()

        # Mostrar los resultados en una nueva ventana
        ventana_resultado = Toplevel(raiz)
        ventana_resultado.title("Resultados")

        # Mostrar la matriz resuelta
        etiqueta_resuelto = Label(ventana_resultado, text="Puzzle Resuelto:", font=('Arial', 14))
        etiqueta_resuelto.pack(pady=5)

        marco_resuelto = Frame(ventana_resultado)
        marco_resuelto.pack()

        # Crear una matriz de entradas para mostrar el puzzle
        celdas = []
        for i in range(3):
            fila_celdas = []
            for j in range(3):
                celda = Entry(marco_resuelto, width=2, font=('Arial', 24), justify='center')
                celda.grid(row=i, column=j, padx=5, pady=5)
                celda.config(state='disabled')
                fila_celdas.append(celda)
            celdas.append(fila_celdas)

        #Llenar el grid con el estado solucion
        estado_solucion = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0]).reshape(3, 3)
        for i in range(3):
            for j in range(3):
                valor = estado_solucion[i][j]
                celdas[i][j].config(state='normal')
                celdas[i][j].delete(0, END)
                celdas[i][j].insert(END, str(valor))
                celdas[i][j].config(state='disabled')

        # Funcion para mostrar los estados paso a paso
        def mostrar_paso_a_paso(estados, indice=0):
            if indice == 0:
                # Al iniciar el paso a paso, mostrar el estado inicial
                estado_actual = estados[0].reshape(3, 3)
            else:
                estado_actual = estados[indice].reshape(3, 3)
            for i in range(3):
                for j in range(3):
                    valor = estado_actual[i][j]
                    celdas[i][j].config(state='normal')
                    celdas[i][j].delete(0, END)
                    celdas[i][j].insert(END, str(valor))
                    celdas[i][j].config(state='disabled')
            if indice + 1 < len(estados):
                ventana_resultado.after(1000, mostrar_paso_a_paso, estados, indice + 1) #El 500 es la velocidad 

        # Boton para iniciar el paso a paso
        boton_paso_a_paso = Button(ventana_resultado, text="Mostrar Paso a Paso", command=lambda: mostrar_paso_a_paso(cadena_estados, indice=0))
        boton_paso_a_paso.pack(pady=5)

        # Mostrar los resultados estadisticos
        etiqueta_resultados = Label(ventana_resultado, text="Resultados:", font=('Arial', 14))
        etiqueta_resultados.pack(pady=5)
        textbox_resultados = Text(ventana_resultado, width=50, height=15, font=('Arial', 12))
        textbox_resultados.pack()
        textbox_resultados.insert(END, texto_resultado)
        textbox_resultados.config(state='disabled')

        # Mostrar el arbol de busqueda en una nueva ventana
        mostrar_arbol(s.arbol, s)

    def mostrar_arbol(arbol_relaciones, solucionador, profundidad_maxima=5):
        # Crear el grafo
        G = nx.DiGraph()
        labels = {}

        # Obtener los nodos en el camino de la solución
        camino_nodos = [tuple(nodo.estado) for nodo in solucionador.cadena_ancestral()]
        nodos_solucion = set(camino_nodos)

        # Agregar nodos y aristas, incluyendo siempre los del camino de la solucion
        for padre, hijo in arbol_relaciones:
            incluir_nodo = False
            if hijo.profundidad <= profundidad_maxima:
                incluir_nodo = True
            if tuple(hijo.estado) in nodos_solucion or tuple(padre.estado) in nodos_solucion:
                incluir_nodo = True
            if incluir_nodo:
                estado_padre = tuple(padre.estado)
                estado_hijo = tuple(hijo.estado)
                G.add_node(estado_padre)
                G.add_node(estado_hijo)
                G.add_edge(estado_padre, estado_hijo)
                labels[estado_padre] = '\n'.join(map(str, padre.estado.reshape(3, 3)))
                labels[estado_hijo] = '\n'.join(map(str, hijo.estado.reshape(3, 3)))

        ventana_arbol = Toplevel(raiz)
        ventana_arbol.title("Árbol de Búsqueda")

        # lienzo
        fig, ax = plt.subplots(figsize=(12, 8))

        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')

        nx.draw(G, pos, with_labels=False, node_size=500, arrowsize=20, ax=ax)
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=6, ax=ax)

        # Resaltar el camino de la solucion
        edges_in_solution = list(zip(camino_nodos[:-1], camino_nodos[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_solution, edge_color='r', width=2, ax=ax)

        # Mostrar el grafico en el lienzo
        canvas = FigureCanvasTkAgg(fig, master=ventana_arbol)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Agregar controles de navegacion
        toolbar = NavigationToolbar2Tk(canvas, ventana_arbol)
        toolbar.update()
        canvas.get_tk_widget().pack()

        # Funciones para zoom con la rueda del raton
        def zoom(event):
            base_scale = 1.1
            if event.step > 0:  # Rueda hacia arriba
                scale_factor = 1 / base_scale
            elif event.step < 0:  # Rueda hacia abajo
                scale_factor = base_scale
            else:
                return

            current_xlim = ax.get_xlim()
            current_ylim = ax.get_ylim()
            xdata = event.xdata
            ydata = event.ydata
            if xdata is None or ydata is None:
                return

            new_xlim = [xdata - (xdata - current_xlim[0]) * scale_factor,
                        xdata + (current_xlim[1] - xdata) * scale_factor]
            new_ylim = [ydata - (ydata - current_ylim[0]) * scale_factor,
                        ydata + (current_ylim[1] - ydata) * scale_factor]

            ax.set_xlim(new_xlim)
            ax.set_ylim(new_ylim)
            canvas.draw()

        # Variables para almacenar la posición anterior del ratón
        pan_start = {'x': None, 'y': None}

        def on_press(event):
            if event.button == 1:
                pan_start['x'] = event.x
                pan_start['y'] = event.y

        def on_motion(event):
            if pan_start['x'] is None or pan_start['y'] is None:
                return
            dx = event.x - pan_start['x']
            dy = event.y - pan_start['y']
            current_xlim = ax.get_xlim()
            current_ylim = ax.get_ylim()
            width = canvas.get_tk_widget().winfo_width()
            height = canvas.get_tk_widget().winfo_height()
            if width == 0 or height == 0:
                return  # Evitar división por cero
            scale_x = (current_xlim[1] - current_xlim[0]) / width
            scale_y = (current_ylim[1] - current_ylim[0]) / height
            ax.set_xlim(current_xlim - dx * scale_x)
            ax.set_ylim(current_ylim + dy * scale_y)
            pan_start['x'] = event.x
            pan_start['y'] = event.y
            canvas.draw()

        def on_release(event):
            if event.button == 1:
                pan_start['x'] = None
                pan_start['y'] = None

        # Enlazar los eventos de ratón
        canvas.mpl_connect('scroll_event', zoom)
        canvas.mpl_connect('button_press_event', on_press)
        canvas.mpl_connect('motion_notify_event', on_motion)
        canvas.mpl_connect('button_release_event', on_release)

    # Botón para generar un puzzle aleatorio
    boton_aleatorio = Button(raiz, text="Generar Aleatorio", command=generar_puzzle_aleatorio)
    boton_aleatorio.grid(row=3, column=0, columnspan=3, pady=5)

    # Boton para resolver el puzzle
    boton_resolver = Button(raiz, text="Resolver", command=resolver_puzzle)
    boton_resolver.grid(row=4, column=0, columnspan=3, pady=5)

    raiz.mainloop()

if __name__ == "__main__":
    main()