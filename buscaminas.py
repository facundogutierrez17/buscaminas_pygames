#-------------------------------------- IMPORTACIONES Y BIBLIOTECAS -------------------------------
import pygame
import random

#-------------------------------------- INCIALIZADORES --------------------------------------------
pygame.init()  # Inicializa todos los módulos de Pygame, incluyendo fuentes
pygame.font.init()  # Asegura que el módulo de fuentes esté inicializado correctamente

#-------------------------------------- COLORES ---------------------------------------------------

BLANCO = (255, 255, 255)
GRIS = (192, 192, 192)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)  
AZUL = (0, 0, 255)  
AMARILLO = (255, 255, 0)  
VIOLETA =  (128, 0, 128)
NARANJA = (255, 165, 0)
COLOR_BOTON = (100, 150, 255)
COLOR_FONDO = (200, 200, 200)
COLOR_BOTON = (100, 150, 255)
COLOR_TEXTO = NEGRO
COLOR_CELDA = GRIS
COLOR_REVELADO = (240, 240, 240)
COLOR_MINA = ROJO
COLOR_BANDERA = (0, 0, 255)

#-------------------------------------- CONFIGURACION -----------------------------------------------
ANCHO = 600
CELDA = 35
pantalla = pygame.display.set_mode((ANCHO,ANCHO + 40 ))
fuente = pygame.font.Font(None, 36)
pygame.display.set_caption("Buscaminas")

COLORES_NUMEROS = {   
    1: AZUL,
    2: VERDE,
    3: ROJO,
    4: AMARILLO,
    5: NARANJA,
    6: VIOLETA,
    7: NEGRO,
    8: GRIS
}

DIFICULTADES = {
    "facil": (8, 8, 10),
    "medio": (16, 16, 40),
    "dificil": (24, 24, 99)
}

def inicializar_estado()->dict:
    """
    funcion que contiene el diccionario principal que nos servira mas adelante para desarrollar el juego
    - No recibe parametros solo retorna el diccionario principal 
    """
    return {
        "pantalla": pygame.display.set_mode((ANCHO, ANCHO + 40)),  # Aumentamos el alto de la pantalla
        "estado": "menu",
        "dificultad": None,
        "tablero": [],
        "revelado": [],
        "perdido": False,
        "jugando": True,
        "filas": 0,
        "columnas": 0,
        "minas": 0,
        "ancho": ANCHO,
        "alto": ANCHO + 40,
        "puntaje": 0,  # Iniciamos el puntaje en 0
        "banderas_colocadas": 0  # Bandera inicialmente colocadas en 0  diccionario principal que nos servira mas adelante para desarrollar el juego
    }

def inicializar_juego(estado:dict, dificultad:dict)-> None:
    """
    funcion que accede a los valores del diccionario principal asi como al de dificultad, asignandoles la logica que nos servira mas adelante para desarrollar el juego
    - recibe como parametros estado y dificultad para poder acceder a los valores de los diccionarios 
    - ubica de manera aleatoria las minas dentro del tablero, NO DIBUJA LAS BANDERAS.
    """
    estado["dificultad"] = dificultad
    estado["filas"], estado["columnas"], estado["minas"] = DIFICULTADES[dificultad]
    estado["ancho"] = estado["columnas"] * CELDA
    estado["alto"] = estado["filas"] * CELDA  + 40 # Ajustamos el alto para el margen superior
    estado["pantalla"] = pygame.display.set_mode((estado["ancho"] + 2, estado["alto"] + 2))
    estado["banderas"] = [[False for _ in range(estado["columnas"])] for _ in range(estado["filas"])]  # Inicializamos el estado de banderas
    estado["tablero"] = [[0 for _ in range(estado["columnas"])] for _ in range(estado["filas"])]
    estado["revelado"] = [[False for _ in range(estado["columnas"])] for _ in range(estado["filas"])]
    estado["perdido"] = False
    estado["puntaje"] = 0

    minas_colocadas = 0
    while minas_colocadas < estado["minas"]:
        x, y = random.randint(0, estado["columnas"] - 1), random.randint(0, estado["filas"] - 1)
        if estado["tablero"][y][x] == 0:
            estado["tablero"][y][x] = -1
            minas_colocadas += 1
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nx, ny = x + i, y + j
                    if 0 <= nx < estado["columnas"] and 0 <= ny < estado["filas"] and estado["tablero"][ny][nx] != -1:
                        estado["tablero"][ny][nx] += 1

    estado["puntaje"] = 0

#-------------------------------------- FUNCIONES ---------------------------------------------------
def mostrar_matriz(estado:dict, matriz:list)->list:
    """
    funcion que muestra por pantalla la matriz recibida como parametro
    - recibe como parametro la matriz que indiquemos
    - muestra por pantalla dicha matriz ubicando de la forma correcta sus filas y sus columnas
    """
    for i in range(estado["filas"]):
        for j in range(estado["columnas"]):
            print(matriz[i][j],end=" ")
        print(" ")
        
def dibujar_tablero(estado:dict)->None:
    """
    funcion que genera la matriz del tablero y dibuja el tablero del buscamina
    - recibe como parametro estado para poder acceder a los valores del diccionario
    - muestra por pantalla el tablero del juego
    """
    for y in range(estado["filas"]):
        for x in range(estado["columnas"]):  #celda + 40 -> genera espacio arriba para colocar puntaje, tiempo y reinicio
            rect = pygame.Rect(x * CELDA, y * CELDA + 40, CELDA, CELDA)
            if estado["revelado"][y][x]:
                # Celda revelada
                pygame.draw.rect(pantalla, COLOR_REVELADO, rect)
                if estado["tablero"][y][x] == -1:                    
                    # Dibujar mina
                    pygame.draw.circle(pantalla, COLOR_MINA, rect.center, CELDA // 4)
                elif estado["tablero"][y][x] > 0:
                    # Dibujar número
                    color_texto = COLORES_NUMEROS.get(estado["tablero"][y][x], COLOR_TEXTO)
                    texto = fuente.render(str(estado["tablero"][y][x]), True, color_texto)
                    pantalla.blit(texto, texto.get_rect(center=rect.center))
            else:
                # Celda no revelada con relieve
                pygame.draw.rect(pantalla, COLOR_CELDA, rect)

                # Bordes resaltados y sombreados
                pygame.draw.line(pantalla, (255, 255, 255), rect.topleft, rect.bottomleft, 8)  # Izquierdo
                pygame.draw.line(pantalla, (255, 255, 255), rect.topleft, rect.topright, 8)    # Superior
                pygame.draw.line(pantalla, (0, 0, 0), rect.bottomleft, rect.bottomright, 8)    # Inferior
                pygame.draw.line(pantalla, (0, 0, 0), rect.topright, rect.bottomright, 8)      # Derecho

            # Dibujar contorno de celda
            pygame.draw.rect(pantalla, (0, 0, 0), rect, 1)
             # Dibujar banderas
            if estado["banderas"][y][x]:
                bandera_rect = pygame.Rect(x * CELDA + CELDA // 4, y * CELDA + 40 + CELDA // 4, CELDA // 2, CELDA // 2)
                pygame.draw.line(pantalla, COLOR_BANDERA, bandera_rect.topleft, bandera_rect.bottomright, 3)  # Bandera cruzada
                pygame.draw.line(pantalla, COLOR_BANDERA, bandera_rect.bottomleft, bandera_rect.topright, 3)
    
    # Dibujar botón de reinicio
    crear_boton_reinicio(estado)       

def revelar_celdas(estado:dict, x:int, y:int)->None:
    """
    funcion que recorre las filas y las columnas de la matriz del tablero asi como tambien establece el limite del mismo para prevenir errores
    - recibe como parametro estado para poder acceder a los valores del diccionario asi como tambien x,y que son coordenadas
    - esta funcion no tiene retorno, es una funcion recursiva ya que se llama asi misma dentro de su propio algoritmo
    """
    if not (0 <= x < estado["columnas"] and 0 <= y < estado["filas"]) or estado["revelado"][y][x]:
        return
    estado["revelado"][y][x] = True
    if estado["tablero"][y][x] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                revelar_celdas(estado, x + i, y + j)

def escribir_texto(texto:str, x:int, y:int)->None:
    """
    funcion para escribir en patalla 
    - recibe como parametro el texto que se va a mostrar en pantalla, asi como tambien sus coordenadas para ubicarlo donde queramos(x,Y)
    - no tiene retorno solo renderiza el texto que recibe por parametro, lo ubica y muestra en pantalla
    """
    texto_renderizado = fuente.render(texto, True, NEGRO)
    pantalla.blit(texto_renderizado, (x, y))

def crear_boton(texto:str, x:int, y:int, ancho:int, alto:int)->None:
    """
    funcion para crear botones, solo crea el boton visualmente en pantalla sin funcionalidad
    - recibe como parametro el texto que se va a mostrar en el boton, asi como tambien sus coordenadas para ubicarlo donde queramos(x,Y)
    - retorna la variable que contiene  la clase Rect de pygame, se utiliza para ubicar y dar forma a areas rectangulares
    """
    # Dibujar fondo del botón
    rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, COLOR_BOTON, rect)

    # Borde resaltado (superior e izquierdo)
    pygame.draw.line(pantalla, (255, 255, 255), rect.topleft, rect.bottomleft, 4)  # Izquierdo
    pygame.draw.line(pantalla, (255, 255, 255), rect.topleft, rect.topright, 4)    # Superior

    # Borde intermedio (color entre el resaltado y el fondo del botón)
    pygame.draw.line(pantalla, (200, 200, 255), rect.inflate(-4, -4).topleft, rect.inflate(-4, -4).bottomleft, 2)  # Izquierdo intermedio
    pygame.draw.line(pantalla, (200, 200, 255), rect.inflate(-4, -4).topleft, rect.inflate(-4, -4).topright, 2)    # Superior intermedio

    # Borde sombreado (inferior y derecho)
    pygame.draw.line(pantalla, (0, 0, 0), rect.bottomleft, rect.bottomright, 4)    # Inferior
    pygame.draw.line(pantalla, (0, 0, 0), rect.topright, rect.bottomright, 4)      # Derecho

    # Dibujar texto del botón
    texto_superficie = pygame.font.Font(None, 36).render(texto, True, COLOR_TEXTO)
    texto_rect = texto_superficie.get_rect(center=rect.center)
    pantalla.blit(texto_superficie, texto_rect)

    return rect

def dibujar_puntaje(estado:dict)->None:
    """
    funcion que muestra por pantalla el puntaje
    - recibe como parametro estado para poder acceder a los valores del diccionario
    - muestra por pantalla el puntaje obtenido y guardado en el archivos csv asi como la dificultad de juego y el tiempo transcurrido
    """
    fuente = pygame.font.Font(None, 36)
    if estado["dificultad"] == "facil":
        fuente = pygame.font.Font(None, 24)  # Reducir tamaño de fuente en dificultad fácil
    puntaje_texto = fuente.render(f"Puntaje: {estado['puntaje']}", True, COLOR_TEXTO)
    pantalla.blit(puntaje_texto, (estado["ancho"] - 10 - puntaje_texto.get_width(), 10))  # Puntaje a la derecha

def guardar_puntaje(estado:dict, tiempo_transcurrido:int)->None:
    """
    esta funcion importa las bibliotecas csv y os para poder almacenar en un archivo de texto los valores obtenidos (puntaje, dificultad, tiempo)
    - recibe como parametro estado para poder acceder a los valores del diccionario como tambien el tiempo transcurrido
    - retorna la variable que guarda los datos obtenidos
    """
    import csv
    import os
    if not os.path.exists("puntajes.csv"):
        with open('puntajes.csv', 'w', newline='') as file:
            crear_archivo = csv.writer(file)
            crear_archivo.writerow(["Dificultad", "Puntaje", "Tiempo"])
    with open('puntajes.csv', 'a', newline='') as file:
        crear_archivo = csv.writer(file)
        crear_archivo = crear_archivo.writerow([estado["dificultad"], estado["puntaje"], tiempo_transcurrido])
    
    return crear_archivo

def colocar_bandera(estado:dict, x:int, y:int)->None:
    """
    funcion para poder colocar las banderas dentro del tablero del juego
    - recibe como parametro estado para poder acceder a los valores del diccionario asi como tambien las coordenadas de la casilla a marcar
    - funcion contiene solo la logica de como colocar la bandera, NO DIBUJA LA BANDERA A COLOCAR
    """
    if estado["revelado"][y][x] == False and estado["banderas"][y][x] == False:
        estado["banderas"][y][x] = True
    if estado["revelado"][y][x] == True and estado["banderas"][y][x] == False:
        estado["banderas"][y][x] = False

def quitar_bandera(estado:dict, x:int, y:int)->None:
    """
    funcion para poder sacar las banderas ya colocadas dentro del tablero del juego
    - recibe como parametro estado para poder acceder a los valores del diccionario asi como tambien las coordenadas de la casilla a desmarcar
    - funcion contiene solo la logica de cuando quitar la bandera, NO DIBUJA LA BANDERA A QUITAR
    """
    if estado["banderas"][y][x]:
        estado["banderas"][y][x] = False

def crear_boton_reinicio(estado:dict)->None:
    """
    funcion que dibuja el boton de reincio y le asigna una imagen al mismo
    - recibe como parametro estado para poder acceder a los valores del diccionario 
    - retorna el boton de reinicio creado con la imagen y mostrandola en la parte centro superior del tablero del juego
    """
    # Cargar la imagen del botón de reinicio
    imagen_boton = pygame.image.load('C:/Users/user/Documents/buscaminas_python/buscaminas.jpg')
    imagen_boton = pygame.transform.scale(imagen_boton, (60, 30))  # Ajustar el tamaño de la imagen
    # Definir la posición del botón entre el puntaje y el temporizador
    x = estado["ancho"] // 2 - imagen_boton.get_width() // 2
    y = 5  # Un poco debajo del margen superior, cerca del temporizador
    boton_rect = pygame.Rect(x, y, imagen_boton.get_width(), imagen_boton.get_height())

    # Dibujar el botón de imagen en la pantalla
    pantalla.blit(imagen_boton, (x, y))
    return boton_rect

def verificar_reinicio(estado:dict, pos)->None:
    """
    funcion que contiene la logica del boton de reinicio
    - recibe como parametro estado para poder acceder a los valores del diccionario 
    - se asegura que una vez pulsado el boton de reinicio el juego empiece de nuevo en la misma dificulta 
    """
    boton_reinicio = crear_boton_reinicio(estado)
    if boton_reinicio.collidepoint(pos):
        inicializar_juego(estado, estado["dificultad"])  # Reiniciar el juego con la misma dificultad
                
def dibujar_temporizador(estado:dict, tiempo_transcurrido:int)->None:
    """
    funcion que dibuja el contador dentro del tablero de juego
    - recibe como parametro estado para poder acceder a los valores del diccionario asi como el tiempo transcurrido en la partidad
    - ubica el temporizador en la parte superior izquierda , tambien reduce el tamaño de la fuente si se achica la pantalla (como en la dificultad facil)
    """
    fuente = pygame.font.Font(None, 36)
    if estado["dificultad"] == "facil":
        fuente = pygame.font.Font(None, 24)  # Reducir tamaño de fuente en dificultad fácil
    tiempo_texto = fuente.render(f"Tiempo: {tiempo_transcurrido}s", True, COLOR_TEXTO)
    pantalla.blit(tiempo_texto, (10, 10))  # Temporizador a la izquierda

#-------------------------------------- PANTALLAS ---------------------------------------------------
def pantalla_menu(estado:dict)->None:
    pantalla.fill(COLOR_FONDO)
    titulo = pygame.font.Font(None, 36).render("Buscaminas", True, NEGRO)
    imagen_mina = pygame.image.load('C:/Users/user/Documents/buscaminas_python/mina.png')
    x = estado["ancho"] // 2 - imagen_mina.get_width() // 2 
    y = 5  
    pantalla.blit(imagen_mina, (x, y))
    pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ANCHO // 4)))
    return  crear_boton("Jugar", ANCHO // 2 - 50, ANCHO // 2 - 60, 100, 40), \
            crear_boton("Puntaje", ANCHO // 2 - 50, ANCHO // 2, 100, 40), \
            crear_boton("Salir", ANCHO // 2 - 50, ANCHO // 2 + 60, 100, 40)

def pantalla_niveles(estado:dict)->None:
    pantalla.fill(COLOR_FONDO)
    titulo = pygame.font.Font(None, 36).render("Seleccionar Nivel", True, COLOR_TEXTO)
    imagen_mina = pygame.image.load('C:/Users/user/Documents/buscaminas_python/mina.png')
    x = estado["ancho"] // 2 - imagen_mina.get_width() // 2 
    y = 5  
    pantalla.blit(imagen_mina, (x, y))
    pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ANCHO // 4)))
    return crear_boton("Fácil", ANCHO // 2 - 50, ANCHO // 2 - 60, 100, 40), \
           crear_boton("Medio", ANCHO // 2 - 50, ANCHO // 2, 100, 40), \
           crear_boton("Difícil", ANCHO // 2 - 50, ANCHO // 2 + 60, 100, 40), \
            crear_boton("Atras", ANCHO // 2 - 250, ANCHO // 2 + 250, 100, 30)

def pantalla_puntaje(estado:dict, tiempo_transcurrido:int)->None:
    pantalla.fill((GRIS))
    imagen_mina = pygame.image.load('C:/Users/user/Documents/buscaminas_python/mina.png')
    x = estado["ancho"] // 2 - imagen_mina.get_width() // 2 
    y = 5  
    pantalla.blit(imagen_mina, (x, y))
    escribir_texto(f"PUNTAJE TOTAL : {guardar_puntaje(estado, tiempo_transcurrido)}", ANCHO // 2 - 250, ANCHO // 2 - 250)
    return crear_boton("Atras", ANCHO // 2 - 250, ANCHO // 2 + 250, 100, 30)

#-------------------------------------- EJECUCCION --------------------------------------------------
def ejecutar():
    estado = inicializar_estado()
    pygame.init()  # Inicializa todos los módulos de Pygame, incluyendo fuentes
    pygame.font.init()  # Asegura que el módulo de fuentes esté inicializado correctamente
    corriendo = True
    tiempo_inicio = pygame.time.get_ticks()

    while corriendo:
        tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicio) // 1000
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if estado["estado"] == "menu":
                    botones = pantalla_menu(estado)
                    if botones[0].collidepoint(evento.pos):
                        estado["estado"] = "niveles"
                    elif botones[1].collidepoint(evento.pos):
                        estado["estado"] = "puntaje"
                    elif botones[2].collidepoint(evento.pos):
                        corriendo = False
                elif estado["estado"] == "puntaje":
                    botones = pantalla_puntaje(estado, tiempo_transcurrido)
                    if botones.collidepoint(evento.pos):
                        estado["estado"] = "menu"            
                elif estado["estado"] == "niveles":
                    botones = pantalla_niveles(estado)
                    if botones[0].collidepoint(evento.pos):
                        inicializar_juego(estado, "facil")
                        mostrar_matriz(estado, estado["tablero"])
                        estado["estado"] = "juego"
                    elif botones[1].collidepoint(evento.pos):
                        inicializar_juego(estado, "medio")
                        mostrar_matriz(estado, estado["tablero"])
                        estado["estado"] = "juego"
                    elif botones[2].collidepoint(evento.pos):
                        inicializar_juego(estado, "dificil")
                        mostrar_matriz(estado, estado["tablero"])
                        estado["estado"] = "juego"
                    elif botones[3].collidepoint(evento.pos):
                        estado["estado"] = "menu"
                elif estado["estado"] == "juego" and not estado["perdido"]:
                    x, y = evento.pos
                    cx, cy = x // CELDA, y // CELDA
                    if evento.button == 1:  # Click izquierdo (revelar)
                        if estado["dificultad"] == "facil":
                            estado["puntaje"] += 1
                        if estado["dificultad"] == "medio":
                            estado["puntaje"] += 2
                        if estado["dificultad"] == "dificil":
                            estado["puntaje"] += 4
                        if estado["tablero"][cy][cx] == -1:
                            estado["perdido"] = True
                        else:
                            revelar_celdas(estado, cx, cy)
                    elif evento.button == 3:  # Click derecho (colocar bandera)
                        if estado["banderas"][cy][cx]:
                            quitar_bandera(estado, cx, cy)

                        else:
                            colocar_bandera(estado, cx, cy)

                    # Verificar si se hace clic en el botón de reinicio
                    verificar_reinicio(estado, evento.pos)

                
        if estado["estado"] == "menu":
            pantalla_menu(estado)
        elif estado["estado"] == "puntaje":
            pantalla_puntaje(estado, tiempo_transcurrido)
        elif estado["estado"] == "niveles":
            pantalla_niveles(estado)
        elif estado["estado"] == "juego":
            pantalla.fill(COLOR_FONDO)
            dibujar_tablero(estado)
            dibujar_puntaje(estado)
            dibujar_temporizador(estado, tiempo_transcurrido)
 
            if estado["perdido"]:
                texto = pygame.font.Font(None, 36).render("¡Perdiste!", True, COLOR_MINA)
                pantalla.blit(texto, texto.get_rect(center=(estado["ancho"] // 2, estado["alto"] // 2)))
                estado["puntaje"] = 0 
        pygame.display.flip()

    pygame.quit()

ejecutar()
