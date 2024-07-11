import pygame
import sys
import time

from buscaminas import Buscaminas, BuscaminasIA

# Definir dimensiones del tablero y cantidad de minas
ALTO = 8
ANCHO = 8
MINAS = 10

# Colores
NEGRO = (0, 0, 0)
GRIS = (180, 180, 180)
BLANCO = (255, 255, 255)
ROSADO = (255, 192, 203)
ROJO = (255, 0, 0)

# Inicializar Pygame
pygame.init()
size = ancho, alto = 600, 400
screen = pygame.display.set_mode(size)

# Fuentes
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
fuente_pequeña = pygame.font.Font(OPEN_SANS, 20)
fuente_mediana = pygame.font.Font(OPEN_SANS, 28)
fuente_grande = pygame.font.Font(OPEN_SANS, 40)

# Calcular tamaño del tablero
MARGEN_TABLERO = 20
ancho_tablero = ((2 / 3) * ancho) - (MARGEN_TABLERO * 2)
alto_tablero = alto - (MARGEN_TABLERO * 2)
tamaño_celda = int(min(ancho_tablero / ANCHO, alto_tablero / ALTO))
origen_tablero = (MARGEN_TABLERO, MARGEN_TABLERO)

# Cargar imágenes
bandera = pygame.image.load("assets/images/flag.png")
bandera = pygame.transform.scale(bandera, (tamaño_celda, tamaño_celda))
mina = pygame.image.load("assets/images/mine.png")
mina = pygame.transform.scale(mina, (tamaño_celda, tamaño_celda))
mina_roja = pygame.image.load("assets/images/mine-red.png")
mina_roja = pygame.transform.scale(mina_roja, (tamaño_celda, tamaño_celda))

# Mina detonada
mina_detonada = None

# Crear juego y agente IA
juego = Buscaminas(alto=ALTO, ancho=ANCHO, minas=MINAS)
ia = BuscaminasIA(alto=ALTO, ancho=ANCHO)

# Llevar registro de celdas reveladas, celdas marcadas y si se ha tocado una mina
reveladas = set()
banderas = set()
perdido = False

# Mostrar instrucciones inicialmente
instrucciones = True

# Autoplay del juego
autoplay = False
velocidad_autoplay = 0.3
realizar_movimiento_ia = False

# Mostrar celdas seguras y minas
mostrar_inferencia = False

while True:

    # Comprobar si se ha cerrado la ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(NEGRO)

    # Mostrar instrucciones del juego
    if instrucciones:

        # Título
        titulo = fuente_grande.render("Jugar Buscaminas", True, BLANCO)
        rect_titulo = titulo.get_rect()
        rect_titulo.center = ((ancho / 2), 50)
        screen.blit(titulo, rect_titulo)

        # Reglas
        reglas = [
            "Haz clic en una celda para revelarla.",
            "Haz clic derecho en una celda para marcarla como mina.",
            "Marca todas las minas correctamente para ganar."
        ]
        for i, regla in enumerate(reglas):
            linea = fuente_pequeña.render(regla, True, BLANCO)
            rect_linea = linea.get_rect()
            rect_linea.center = ((ancho / 2), 150 + 30 * i)
            screen.blit(linea, rect_linea)

        # Botón para jugar
        rect_boton = pygame.Rect((ancho / 4), (3 / 4) * alto, ancho / 2, 50)
        texto_boton = fuente_mediana.render("Jugar", True, NEGRO)
        rect_texto_boton = texto_boton.get_rect()
        rect_texto_boton.center = rect_boton.center
        pygame.draw.rect(screen, BLANCO, rect_boton)
        screen.blit(texto_boton, rect_texto_boton)

        # Comprobar si se ha clickeado el botón
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            raton = pygame.mouse.get_pos()
            if rect_boton.collidepoint(raton):
                instrucciones = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Dibujar tablero
    celdas = []
    for i in range(ALTO):
        fila = []
        for j in range(ANCHO):

            # Dibujar rectángulo para la celda
            rect = pygame.Rect(
                origen_tablero[0] + j * tamaño_celda,
                origen_tablero[1] + i * tamaño_celda,
                tamaño_celda, tamaño_celda
            )
            pygame.draw.rect(screen, GRIS, rect)
            pygame.draw.rect(screen, BLANCO, rect, 3)

            # Agregar una mina, bandera o número si es necesario
            if juego.es_mina((i, j)) and perdido:
                if (i,j) == mina_detonada:
                    screen.blit(mina_roja, rect)
                else:
                    screen.blit(mina, rect)
            elif (i, j) in banderas:
                screen.blit(bandera, rect)
            elif (i, j) in reveladas:
                vecinos = fuente_pequeña.render(
                    str(juego.minas_cercanas((i, j))),
                    True, NEGRO
                )
                rect_vecinos = vecinos.get_rect()
                rect_vecinos.center = rect.center
                screen.blit(vecinos, rect_vecinos)
            elif (i, j) in ia.seguras and mostrar_inferencia:
                pygame.draw.rect(screen, ROSADO, rect)
                pygame.draw.rect(screen, BLANCO, rect, 3)
            elif (i, j) in ia.minas and mostrar_inferencia:
                pygame.draw.rect(screen, ROJO, rect)
                pygame.draw.rect(screen, BLANCO, rect, 3)
            fila.append(rect)
        celdas.append(fila)

    # Botón de Autoplay
    rect_autoplay = pygame.Rect(
        (2 / 3) * ancho + MARGEN_TABLERO, MARGEN_TABLERO,
        (ancho / 3) - MARGEN_TABLERO * 2, 50
    )
    texto_boton = "Autoplay" if not autoplay else "Detener"
    texto_boton = fuente_mediana.render(texto_boton, True, NEGRO)
    rect_texto_boton = texto_boton.get_rect()
    rect_texto_boton.center = rect_autoplay.center
    pygame.draw.rect(screen, BLANCO, rect_autoplay)
    screen.blit(texto_boton, rect_texto_boton)

    # Botón de movimiento de IA
    rect_boton_ia = pygame.Rect(
        (2 / 3) * ancho + MARGEN_TABLERO, MARGEN_TABLERO + 70,
        (ancho / 3) - MARGEN_TABLERO * 2, 50
    )

    tamaño_fuente_nueva = 30  # Tamaño de la nueva fuente
    nueva_fuente = pygame.font.Font(None, tamaño_fuente_nueva)
    texto_boton = nueva_fuente.render("Movimiento IA", True, NEGRO)
    rect_texto_boton = texto_boton.get_rect()
    rect_texto_boton.center = rect_boton_ia.center
    if not autoplay:
        pygame.draw.rect(screen, BLANCO, rect_boton_ia)
        screen.blit(texto_boton, rect_texto_boton)

    # Botón de reinicio
    rect_boton_reinicio = pygame.Rect(
        (2 / 3) * ancho + MARGEN_TABLERO, MARGEN_TABLERO + 140,
        (ancho / 3) - MARGEN_TABLERO * 2, 50
    )
    texto_boton = fuente_mediana.render("Reiniciar", True, NEGRO)
    rect_texto_boton = texto_boton.get_rect()
    rect_texto_boton.center = rect_boton_reinicio.center
    if not autoplay:
        pygame.draw.rect(screen, BLANCO, rect_boton_reinicio)
        screen.blit(texto_boton, rect_texto_boton)

    # Mostrar texto
    texto = "Perdiste" if perdido else "Ganaste" if juego.minas == banderas else ""
    texto = fuente_mediana.render(texto, True, BLANCO)
    rect_texto = texto.get_rect()
    rect_texto.center = ((5 / 6) * ancho, MARGEN_TABLERO + 232)
    screen.blit(texto, rect_texto)

    # Botón de mostrar celdas seguras y minas
    rect_boton_inferencia = pygame.Rect(
        (2 / 3) * ancho + MARGEN_TABLERO, MARGEN_TABLERO + 280,
        (ancho / 3) - MARGEN_TABLERO * 2, 50
    )

    tamaño_fuente_nueva = 25  # Tamaño de la nueva fuente
    nueva_fuente = pygame.font.Font(None, tamaño_fuente_nueva)
    texto_boton = "Mostrar Inferencia" if not mostrar_inferencia else "Ocultar Inferencia"
    texto_boton = nueva_fuente.render(texto_boton, True, NEGRO)
    rect_texto_boton = texto_boton.get_rect()
    rect_texto_boton.center = rect_boton_inferencia.center
    if not autoplay:
        pygame.draw.rect(screen, BLANCO, rect_boton_inferencia)
        screen.blit(texto_boton, rect_texto_boton)

    movimiento = None

    izquierda, _, derecha = pygame.mouse.get_pressed()

    # Comprobar clic derecho para marcar/desmarcar mina
    if derecha == 1 and not perdido and not autoplay:
        raton = pygame.mouse.get_pos()
        for i in range(ALTO):
            for j in range(ANCHO):
                if celdas[i][j].collidepoint(raton) and (i, j) not in reveladas:
                    if (i, j) in banderas:
                        banderas.remove((i, j))
                    else:
                        banderas.add((i, j))
                    time.sleep(0.2)

    elif izquierda == 1:
        raton = pygame.mouse.get_pos()

        # Si se hace clic en el botón de Autoplay, activar/desactivar autoplay
        if rect_autoplay.collidepoint(raton):
            if not perdido:
                autoplay = not autoplay
            else:
                autoplay = False
            time.sleep(0.2)
            continue

        # Si se hace clic en el botón de IA, hacer un movimiento de IA
        elif rect_boton_ia.collidepoint(raton) and not perdido:
            realizar_movimiento_ia = True
            time.sleep(0.2)

        # Reiniciar estado del juego
        elif rect_boton_reinicio.collidepoint(raton):
            juego = Buscaminas(alto=ALTO, ancho=ANCHO, minas=MINAS)
            ia = BuscaminasIA(alto=ALTO, ancho=ANCHO)
            reveladas = set()
            banderas = set()
            perdido = False
            mina_detonada = None
            continue

        # Si se hace clic en el botón de Inferencia, activar/desactivar mostrar_inferencia
        elif rect_boton_inferencia.collidepoint(raton):
            mostrar_inferencia = not mostrar_inferencia
            time.sleep(0.2)

        # Movimiento hecho por el usuario
        elif not perdido:
            for i in range(ALTO):
                for j in range(ANCHO):
                    if (celdas[i][j].collidepoint(raton)
                            and (i, j) not in banderas
                            and (i, j) not in reveladas):
                        movimiento = (i, j)

    # Si autoplay, hacer movimiento con IA
    if autoplay or realizar_movimiento_ia:
        if realizar_movimiento_ia:
            realizar_movimiento_ia = False
        movimiento = ia.hacer_movimiento(3)
        if movimiento is None:
            movimiento = ia.hacer_movimiento_aleatorio()
            if movimiento is None:
                banderas = ia.minas.copy()
                print("No quedan movimientos por hacer.")
                autoplay = False
            else:
                print("No hay movimientos seguros conocidos, IA haciendo movimiento aleatorio.")
        else:
            print("IA haciendo movimiento seguro.")

        # Añadir retraso para autoplay
        if autoplay:
            time.sleep(velocidad_autoplay)

    # Hacer movimiento y actualizar conocimiento de la IA
    if movimiento:
        if juego.es_mina(movimiento):
            perdido = True
            mina_detonada = movimiento
            autoplay = False
        else:
            cercanas = juego.minas_cercanas(movimiento)
            reveladas.add(movimiento)
            ia.agregar_conocimiento(movimiento, cercanas)

    pygame.display.flip()
