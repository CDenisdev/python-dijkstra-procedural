# Definimos las constantes del terreno que nos servira para Dijkstra
import heapq
import math

#Sirve para etiquetar cada celda, mayuscula por que son constantes
LIBRE = 0
EDIFICIO = 1    # No transitable
AGUA = 2        # transitable pero mas caro 
BLOQ = 3        # No transitable 

# Emojis para la visual 

EMOJIS = {
    LIBRE: "⬜",     # libre
    EDIFICIO: "🏢", # edificio (obstáculo duro)
    AGUA: "💧",     # agua (más costosa de cruzar)
    BLOQ: "⛔"      # bloqueado (obstáculo duro)
}
EMOJI_INICIO = "🚦"
EMOJI_DESTINO = "🏁"
EMOJI_RUTA = "⭐"

# Funcion para crear el mundo 
def crear_mundo(alto, ancho):
    if alto <= 0 or ancho <= 0:
        print("Tamaño invalido. se usara 10x10 por defecto")
        alto, ancho = 10, 10
    
    matriz = [[LIBRE for _ in range(ancho)] for _ in range(alto)]

    mundo = {
        "alto": alto,
        "ancho": ancho,
        "matriz": matriz,
        "inicio" : None,
        "destino": None
    }
    return mundo

# Funcion que valida los limites 
def dentro_limites(fila, columna, mundo):
    return 0 <= fila < mundo["alto"] and 0 <= columna < mundo ["ancho"] #al colocar directo en el return nos ahorramos lineas de codigo

#Funcion para mostrar el mapa, devuelve un string con el mapa en emojis 
# Inicio y destino tienen prioridad visual sobre la ruta
def mostrar_mapa(mundo, ruta=None):

    ruta_set = set(ruta) if ruta else set()
    alto = mundo["alto"]
    ancho = mundo["ancho"]
    matriz = mundo["matriz"]
    inicio = mundo["inicio"]
    destino = mundo["destino"]

    lineas = []
    for f in range(alto):
        piezas = []
        for c in range(ancho):
            simbolo = EMOJIS[matriz[f][c]]

            # marcar ruta si viene 
            if (f, c) in ruta_set:
                simbolo = EMOJI_RUTA
            
            # Inicio/destino tienen prioridad
            if inicio == (f, c):
                simbolo = EMOJI_INICIO
            if destino == (f, c):
                simbolo = EMOJI_DESTINO

            piezas.append(simbolo)
        lineas.append("".join(piezas))
    return "\n".join(lineas)

# Funciones para editar el mapa 
def definir_inicio(mundo, fila, columna):
    # Coloca el inicio en una celda 
    if not dentro_limites(fila, columna, mundo):
        print("El inicio esta fuera del mapa.")
        return
    if mundo ["matriz"][fila][columna] != LIBRE:
        print("El inicio no puede estar en un obstaculo.")
        return
    mundo["inicio"] = (fila, columna)
    print(f"Inicio definido en ({fila}, {columna})")

# Coloca el destino en una celda valida
def definir_destino(mundo, fila, columna):
    if not dentro_limites(fila, columna, mundo):
        print("El destino esta fuera del mapa.")
        return
    if mundo["matriz"][fila][columna] != LIBRE:
        print ("El destino no puede estar en un obstaculo.")
        return
    mundo["destino"] = (fila, columna)
    print(f"Destino definido en ({fila}, {columna})")

# agrega un obstaculo en la posicion indicada
def agregar_obstaculo(mundo, tipo, fila, columna):

    if tipo not in (EDIFICIO, AGUA, BLOQ):
        print("Tipo de obstaculo invalido (usa 1=Edificio, 2=Agua, 3=Bloqu).")
        return
    if not dentro_limites(fila, columna, mundo):
        print("Coordenadas fuera del mapa.")
        return
    if mundo["inicio"] == (fila, columna) or mundo["destino"] == (fila, columna):
        print("No puedes poner un obstaculo sobre inicio o destino")
        return
    mundo["matriz"][fila][columna] = tipo
    print(f"Obstaculo agregado en ({fila}, {columna})")

# Funcion que sirve para limpiar una celda 
def limpiar_celda(mundo, fila, columna):
    if not dentro_limites(fila, columna, mundo):
        print("Coordenadas fuera del mapa.")

    mundo["matriz"][fila][columna] = LIBRE
    print(f"Celda limpiada en ({fila}, {columna})")
    

COSTO_CELDA = {
        LIBRE: 1,           # ⬜
        AGUA: 3,            # 💧 (más caro)
        EDIFICIO: None,     # 🏢 no transitable
        BLOQ: None          # ⛔ no transitable
    }

# Direcciones posibles (arriba, abajo, izquierda, derecha)
DIRECCIONES = [(-1,0), (1,0), (0,-1), (0,1)]

# Devuelve el costo de una celda o None si no es transitable
def costo_de_valor(valor):
    return COSTO_CELDA.get(valor, None)

#Reconstruye la ruta desde el diccionario Padres 
def reconstruir_ruta(padres, inicio, destino):
    ruta = []
    actual = destino
    while actual != inicio:
        ruta.append(actual)
        actual = padres[actual]
    ruta.append(inicio)
    ruta.reverse()
    return ruta

#Encuentra la ruta mas barata entre inicio y destino usando Dijkstra
def dijkstra(mundo):

    # primero lo que hacemos es verificar si tenemos inicio y destino por que sin eso no se puede encontrar una ruta 
    if mundo["inicio"] is None or mundo["destino"] is None:
        print("Define inicio y destino primero")
        return None, None
    
    si, sj = mundo["inicio"]
    gi, gj = mundo["destino"]

    dist = {}               # Este es un diccionario donde guardamos el costo mas bajo para llegar a cada celda. Comienza con el costo de inicio que es igual a cero
    padres = {}             #Este es un diccionario que guarda el camino hacia atras desde cada celda para poder reconstruir la ruta mas tarde
    dist[(si, sj)] = 0
    heap = [(0, (si, sj))]  # esta es una cola de prioridad que nos ayuda a procesar las celdas por el costo mas bajo primero. Empieza con el punto de inicio, con costo 0

    # Este buque lo que hace es que mientras hayas celdas por procesar en heap elige la celda con el costo mas bajo
    # que se extrae con heapq.heappop()
    #costo_actual es el costo acumulado hasta esta celda, y (i, j) son las coordenadas de la celda actual
    while heap:             
        costo_actual, (i, j) = heapq.heappop(heap)

        # Si ya llegamos al destino
        # Si la celda actual es el destino, se llama a la funcion reconstruir_ruta para reconstruir el camino
        # desde inicio hasta el destino usando los padres(las celdas previas)
        if (i, j) == (gi, gj):
            ruta = reconstruir_ruta(padres, (si, sj), (gi, gj))
            return ruta, costo_actual
        
        #Si este costo es peor que uno ya conocido lo ignoramos
        #Si el costo de la celda actual es mayor que el costo mas bajo ya conocido (guardado en dist[(i,j)]), la ignoramos 
        # por que ya se encontro algo mas barato
        if costo_actual > dist.get((i, j), math.inf):
            continue

        # Explorar vecinos
        # Esto reccore los vecinos de la celda actial (arriba, abajo, izquierda y derecha)
        #si el vecino esta fuera de los limites del mapa, lo ignoramos.
        # si la celda vecina tiene un costo de movimiento valido (no es un obstaculo ni bloqueada), se sigue adelante
        for di, dj in DIRECCIONES:
            ni, nj = i + di, j + dj
            if not dentro_limites(ni, nj, mundo):
                continue

            costo_celda = costo_de_valor(mundo["matriz"][ni][nj])
            if costo_celda is None:    # obstaculos duros
                continue
        # Esto calcula el nuevo costo de llegar al vecino, suma el costo actual con el costo de la celda vecina 
            nuevo_costo = costo_actual + costo_celda
        # Actualizar el costo si encontramos un camino mas barato 
        # Si el nuevo costo hacia el vecino es mas bataro que cualquier costo previo, actualiza
            if nuevo_costo < dist.get((ni, nj), math.inf):
                dist[(ni, nj)] = nuevo_costo    #dist: el costo minimo para llegar a esa celda
                padres[(ni, nj)] = (i, j)       #padres: registra que venimos de la celda actual(i, j)
                heapq.heappush(heap, (nuevo_costo, (ni, nj)))       # Luego agrega el vecino a la cola de prioridad heap con el nuevo costo
    
    # Si no hay ruta encontrada entoces returna None
    return None, None

# Funcion crear el menu
def menu():
    mundo = None 
    
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Crear mapa personalizado")
        print("2. Usar mapa por defecto (10x10)")
        print("3. Definir inicio 🚦")
        print("4. Definir destino 🏁")
        print("5. Agregar obstáculo (🏢, 💧, ⛔)")
        print("6. Limpiar celda ⬜")
        print("7. Mostrar mapa")
        print("8. Calcular ruta ⭐ con Dijkstra")
        print("9. Salir")
        
        opcion = input("Elige una opción: ")

        if opcion == "1":
            alto = int(input("Numero de filas: "))
            ancho = int(input("Numero de columnas: "))
            mundo = crear_mundo(alto, ancho)
            print("Mapa creado.")
        
        elif opcion == "2":
            mundo = crear_mundo(10, 10)
            print("Mapa por defecto creado.")

        elif opcion == "3":
            if mundo is None:
                print("Primero crea un mapa.")
                continue
            f = int(input("Fila de inicio: "))
            c = int(input("Columna de inicio: "))
            definir_inicio(mundo, f, c)

        elif opcion == "4":
            if mundo is None:
                print("Primero crea un mapa.")
                continue
            f = int(input("Fila de destino. "))
            c = int(input("Columna de destino. "))
            definir_destino(mundo, f, c)

        elif opcion == "5":
            if mundo is None:
                print("Primero crea un mapa.")
                continue
            print("Tipos: 1=🏢 Edificio, 2=💧 Agua, 3=⛔ Bloqueado")
            t = int(input("Tipo: "))
            f = int(input("Fila: "))
            c = int(input("Columna: "))
            agregar_obstaculo(mundo, t, f, c)

        elif opcion == "6":
            if mundo is None:
                print("Primero crea un mapa.")
                continue
            f = int(input("Fila: "))
            c = int(input("Columnna: "))
            limpiar_celda(mundo, f, c)

        elif opcion == "7":
            if mundo is None:
                print("Primero crea un mapa.")
                continue
            print("\nMapa actual:")
            print(mostrar_mapa(mundo))
        
        elif opcion == "8":
            if mundo is None:
                print("Primero crea un mapa.")
                continue
            ruta, costo = dijkstra(mundo)
            if ruta is None:
                print("No hay ruta encontrada.")
            else:
                print(f"\n Ruta encontrada con costo total {costo}:")
                print(mostrar_mapa(mundo, ruta))
        
        elif opcion == "9":
            print("Saliendo del programa...")
            break
        
        else:
            print("Opcion invalida, intenta de nuevo.")


# Para iniciar 
if __name__ == "__main__":
    menu()
