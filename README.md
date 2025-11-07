# 🗺️ Calculadora de Rutas con Algoritmo de Dijkstra (Script)

Este proyecto es una aplicación de consola en Python que calcula la ruta de costo mínimo en un mapa de grilla con terrenos variables. Esta fue la **primera implementación** (procedural) del reto, enfocada puramente en la lógica del algoritmo.

El objetivo era construir una herramienta interactiva que pudiera encontrar el camino más corto en un mapa donde moverse por "Agua" (💧) tiene un costo mayor que moverse por "Libre" (⬜).

---

## 🛠️ Conceptos Técnicos Implementados

El núcleo de este proyecto es la implementación del **Algoritmo de Dijkstra** para resolver un problema de búsqueda del camino más corto en un grafo ponderado (el mapa).

* **Algoritmo de Dijkstra:** Implementado desde cero para manejar los diferentes "pesos" o "costos" de cada celda (ej. Agua = 3, Libre = 1).
* **Cola de Prioridad (`heapq`):** Se utilizó la librería `heapq` de Python para gestionar la cola de prioridad. Esto es crucial para asegurar que el algoritmo funcione de manera eficiente ($O((E+V) \log V)$), ya que siempre procesa el nodo con el menor costo acumulado primero.
* **Gestión de Estado:** El estado del mapa (obstáculos, inicio, fin) se gestiona mediante un diccionario de Python (`mundo`) que se pasa entre las diferentes funciones.
* **Reconstrucción de Ruta:** Se utiliza un diccionario `padres` para rastrear el camino desde el destino hasta el inicio, permitiendo reconstruir la ruta óptoima una vez encontrada.

---

## ✨ Funcionalidades

* Creación de mapas de tamaño dinámico o por defecto.
* Menú interactivo para:
    * Definir inicio (🚦) y destino (🏁).
    * Agregar obstáculos (🏢 Edificio, 💧 Agua, ⛔ Bloqueado).
    * Limpiar celdas.
* Visualización en consola de la ruta óptima (⭐) y el costo total.

---

