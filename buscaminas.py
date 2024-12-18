#-------------------------------------- IMPORTACIONES Y BIBLIOTECAS -------------------------------
from bibiloteca import *

#-------------------------------------- PANTALLAS ---------------------------------------------------
def pantalla_menu(estado:dict)->None:
    pantalla.fill(COLOR_FONDO)
    titulo = pygame.font.Font(None, 36).render("Buscaminas", True, NEGRO)
    imagen_mina = pygame.image.load('C:/Users/user/Documents/buscaminas_python/mina.png')
    x = estado["ancho"] // 2 - imagen_mina.get_width() // 2 
    y = 5  
    pantalla.blit(imagen_mina, (x, y))
    pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ANCHO // 6)))
    return  crear_boton("Jugar", ANCHO // 2 - 50, ANCHO // 2 - 120, 100, 40), \
            crear_boton("Niveles", ANCHO // 2 - 50, ANCHO // 2 - 60, 100, 40), \
            crear_boton("Puntaje", ANCHO // 2 - 50, ANCHO // 2, 100, 40), \
            crear_boton("Salir", ANCHO // 2 - 50, ANCHO // 2 + 60, 100, 40), \
            crear_boton("Mute", ANCHO // 2 - 250, ANCHO // 2 + 250, 100, 30)


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

def pantalla_puntaje(estado:dict)->None:
    pantalla.fill((GRIS))
    imagen_mina = pygame.image.load('C:/Users/user/Documents/buscaminas_python/mina.png')
    x = estado["ancho"] // 2 - imagen_mina.get_width() // 2 
    y = 5  
    pantalla.blit(imagen_mina, (x, y))
    escribir_texto(f"PUNTAJE TOTAL : {guardar_puntaje_tiempo(estado)}", ANCHO // 2 - 250, ANCHO // 2 - 250)
    return crear_boton("Atras", ANCHO // 2 - 250, ANCHO // 2 + 250, 100, 30)

def pedir_nick(estado):
    input_box = pygame.Rect(ANCHO // 4, ANCHO // 3, 400, 50)  # Rectángulo para el cuadro de texto
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('gray15')
    color = color_inactive
    active = False
    nick = estado.get("nick", "")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Activar/desactivar cuadro de texto
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    nick = nick[:-1]
                else:
                    nick += event.unicode
                    return
 
        # Dibujar pantalla
        pantalla.fill((200, 200, 200))  # Fondo gris claro

        # Renderizar título
        titulo = fuente.render("Ingrese su Nick:", True, (0, 0, 0))
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ANCHO // 4)))

        # Renderizar cuadro de texto
        pygame.draw.rect(pantalla, color, input_box, 2)
        txt_surface = fuente.render(nick, True, (0, 0, 0))
        pantalla.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(400, txt_surface.get_width() + 10)

        boton_rect = pygame.Rect(ANCHO // 2 - 50, ANCHO // 2 + 60, 100, 40)
        pygame.draw.rect(pantalla, (0, 150, 0), boton_rect)
        boton_texto = fuente.render("Enter", True, (255, 255, 255))
        pantalla.blit(boton_texto, boton_texto.get_rect(center=boton_rect.center))

        # Detectar clic en el botón
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):
                    estado["nick"] = nick
                    inicializar_juego(estado, estado["dificultad"])  


        pygame.display.flip()
        clock.tick(60)

#-------------------------------------- EJECUCCION --------------------------------------------------
def ejecutar():
    estado = inicializar_estado()
    corriendo = True
    mute = False
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if estado["estado"] == "menu":
                    botones = pantalla_menu(estado)
                    if botones[0].collidepoint(evento.pos):
                        inicializar_juego(estado, "medio")
                        mostrar_matriz(estado, estado["tablero"])
                        estado["estado"] = "juego"
                    elif botones[1].collidepoint(evento.pos):
                        estado["estado"] = "niveles"
                    elif botones[2].collidepoint(evento.pos):
                        estado["estado"] = "puntaje"
                    elif botones[3].collidepoint(evento.pos):
                        corriendo = False
                    elif botones[4].collidepoint(evento.pos):
                            if mute:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()
                            mute = not mute
                elif estado["estado"] == "puntaje":
                    botones = pantalla_puntaje(estado)
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
            pantalla_puntaje(estado)
        elif estado["estado"] == "niveles":
            pantalla_niveles(estado)
        elif estado["estado"] == "juego":
            pantalla.fill(COLOR_FONDO)
            dibujar_tablero(estado)
            dibujar_puntaje(estado)
            if estado["perdido"]:
                for evento in pygame.event.get():
                    if evento.type == pygame.MOUSEBUTTONDOWN:  
                        verificar_reinicio(estado, evento.pos)
                guardar_puntaje_tiempo(estado)
                texto = pygame.font.Font(None, 36).render("¡Perdiste!", True, COLOR_MINA)
                pantalla.blit(texto, texto.get_rect(center=(estado["ancho"] // 2, estado["alto"] // 2)))
                estado["puntaje"] = 0 
                estado["temporizador"] = pygame.time.get_ticks()
        pygame.display.flip()
    guardar_puntaje_tiempo(estado)
    pygame.quit()

ejecutar()
