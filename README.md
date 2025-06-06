# Solucionador del 8-Puzzle usando A*

Este proyecto implementa un solucionador para el clásico problema del **8-Puzzle** empleando el algoritmo de búsqueda A*.

## Características

- Interfaz gráfica con **Tkinter** (`main.py`).
- Clase abstracta `Solucionador` genérica (`solucionador.py`).
- Algoritmo **A*** en (`aestrella.py`).
- Representación del tablero, generación de sucesores y heurística de Manhattan (`tablero.py`).
- Visualización del árbol de búsqueda con **NetworkX** y **Matplotlib**.

## Requisitos

- Python 3.7 o superior
- numpy
- psutil
- networkx
- matplotlib
- pygraphviz
- tkinter (incluido en la mayoría de distribuciones de Python)

Instala las dependencias con:

```powershell
pip install numpy psutil networkx matplotlib pygraphviz
```

## Estructura del proyecto

```
├── aestrella.py         # Implementación de A* (AEstrella)
├── solucionador.py     # Clase abstracta Solucionador
├── tablero.py          # Clase Tablero y heurística de Manhattan
├── main.py             # Interfaz gráfica y funciones de entrada/salida
└── __pycache__/        # Archivos compilados
```

## Uso

1. Clona o descarga este repositorio.
2. Asegúrate de tener instaladas las dependencias.
3. Ejecuta la interfaz gráfica:
   ```powershell
   python main.py
   ```
4. En la ventana:
   - Introduce un estado inicial en la cuadrícula 3×3 (usa 0 para el espacio vacío).
   - Pulsa **Generar Aleatorio** para obtener un puzzle válido al azar.
   - Pulsa **Resolver** para ejecutar A* y visualizar el camino, estadísticas y el árbol de búsqueda.

## Contribuciones

Las contribuciones son bienvenidas. Abre un _issue_ o envía un _pull request_ con mejoras o correcciones.

