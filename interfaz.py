import pygame
from visual_arbol import dibujar_arbol_en_pantalla

# ---------------------------------------------------
# Constantes de pantalla y objetos
# ---------------------------------------------------
ANCHO_JUEGO, ANCHO_ARBOL = 700, 400
ANCHO, ALTO = ANCHO_JUEGO + ANCHO_ARBOL, 600

CAR_WIDTH, CAR_HEIGHT = 80, 60
CAR_POS_X = 100

OBS_WIDTH, OBS_HEIGHT = 60, 60

#Barra de energia style  (esto deberia ir en otra clase al igual que las rutas de las imagenes de los obstaculos y carrito)
def dibujar_barra_energia(pantalla, x, y, ancho, alto, energia, energia_max):
    # Dibuja el fondo de la barra (gris)
    pygame.draw.rect(pantalla, (50, 50, 50), (x, y, ancho, alto))
    # Dibuja el degradado de energía
    barra_ancho = int(ancho * energia / energia_max)
    for i in range(barra_ancho):
        r = int(0 + (50 * (i / ancho)))
        g = int(255 - (80 * (i / ancho)))
        b = int(0 + (50 * (i / ancho)))
        color = (r, g, b)
        pygame.draw.rect(pantalla, color, (x + i, y, 1, alto))
    # Dibuja el borde de la barra
    pygame.draw.rect(pantalla, (0, 0, 0), (x, y, ancho, alto), 2)

# Carga de imagenes
car_img = pygame.image.load("C:\\Users\\Camil\\Documents\\Andres U\\Sistemas 5\\estructura de datos\\proyecto\\CarProyect\\resources\\carrito.png")
car_img = pygame.transform.scale(car_img, (CAR_WIDTH, CAR_HEIGHT))
img_obstaculos = {
    "roca":   pygame.transform.scale(pygame.image.load("C:\\Users\\Camil\\Documents\\Andres U\\Sistemas 5\\estructura de datos\\proyecto\\CarProyect\\resources\\rocas.png"),   (OBS_WIDTH, OBS_HEIGHT)),
    "cono":   pygame.transform.scale(pygame.image.load("C:\\Users\\Camil\\Documents\\Andres U\\Sistemas 5\\estructura de datos\\proyecto\\CarProyect\\resources\\conos.png"),   (OBS_WIDTH, OBS_HEIGHT)),
    "hueco":  pygame.transform.scale(pygame.image.load("C:\\Users\\Camil\\Documents\\Andres U\\Sistemas 5\\estructura de datos\\proyecto\\CarProyect\\resources\\bache.png"),  (OBS_WIDTH, OBS_HEIGHT)),
    "aceite": pygame.transform.scale(pygame.image.load("C:\\Users\\Camil\\Documents\\Andres U\\Sistemas 5\\estructura de datos\\proyecto\\CarProyect\\resources\\aceite.png"), (OBS_WIDTH, OBS_HEIGHT)),
    "arbol":  pygame.transform.scale(pygame.image.load("C:\\Users\\Camil\\Documents\\Andres U\\Sistemas 5\\estructura de datos\\proyecto\\CarProyect\\resources\\arbol.png"),  (OBS_WIDTH, OBS_HEIGHT)),
    "arbusto":pygame.transform.scale(pygame.image.load("C:\\Users\\Camil\\Documents\\Andres U\\Sistemas 5\\estructura de datos\\proyecto\\CarProyect\\resources\\arbusto.png"), (OBS_WIDTH, OBS_HEIGHT)),
    "perrito":pygame.transform.scale(pygame.image.load("C:\\Users\\Camil\\Documents\\Andres U\\Sistemas 5\\estructura de datos\\proyecto\\CarProyect\\resources\\perrito.png"), (OBS_WIDTH, OBS_HEIGHT)),
    "default":pygame.transform.scale(pygame.image.load("C:\\Users\\Camil\\Documents\\Andres U\\Sistemas 5\\estructura de datos\\proyecto\\CarProyect\\resources\\carrito.png"),   (OBS_WIDTH, OBS_HEIGHT))
}


COLOR_FONDO      = (50, 50, 50)
COLOR_CARRITO    = (0, 255, 0)
COLOR_OBSTACULO  = (255, 0, 0)
COLOR_ENERGIA_BG = (0,   0,   0)
COLOR_ENERGIA    = (0, 120, 255)

DAÑO_POR_TIPO = {
    "roca":   110,
    "cono":   110,
    "hueco":  125,
    "aceite":  115,
    "default":10
}

def menu_principal(avl, config):
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Menú Principal")
    font = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()

    fondo = pygame.image.load("C://Users//Camil//Documents//Andres U//Sistemas 5//estructura de datos//proyecto//CarProyect//resources//fondo.png")
    fondo = pygame.transform.scale(fondo, (1200, 900))  

    seleccionado = 0  # índice de la opción seleccionada
    opciones = ["Iniciar Juego", "Salir"]

    while True:
        #pantalla.fill((0, 100, 200))  # fondo azul
        pantalla.blit(fondo, (0, 0))  # dibuja el fondo

        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == seleccionado else (255, 255, 255)
            texto = font.render(opcion, True, color)
            pantalla.blit(texto, (ANCHO//2 - 150, ALTO//2 + i*80))

        pygame.display.flip()

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seleccionado = (seleccionado - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    seleccionado = (seleccionado + 1) % len(opciones)
                elif event.key == pygame.K_RETURN:  # Enter
                    if opciones[seleccionado] == "Iniciar Juego":
                        iniciar_interfaz(avl, config)
                        return
                    elif opciones[seleccionado] == "Salir":
                        pygame.quit()
                        sys.exit()
        clock.tick(30)

def iniciar_interfaz(avl, config):
    # Extraer configuración
    velocidad     = config.get("velocidad", 2)
    salto_altura  = config.get("salto_altura", 15)
    refresco_ms   = config.get("refresco_ms", 200)
    fps           = max(1, 1000 // refresco_ms)

    # Inicializar pygame
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Carrito con Obstáculos AVL")
    reloj = pygame.time.Clock()

    # Estado inicial
    carrito_y = ALTO // 2
    mundo_x   = 0
    saltando  = False
    vel_salto = 0
    energia   = 300

    mostrar_arbol = True  # Mostrar el árbol al lado del juego
    pausado = False  # Estado de pausa


    # Bucle principal
    while True:
        # 1) Procesar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not saltando:
                    vel_salto = salto_altura
                    saltando  = True

                elif evento.key == pygame.K_t:
                    mostrar_arbol = not mostrar_arbol  # Alternar visibilidad del árbol

                elif evento.key == pygame.K_p:
                    pausado = not pausado  # Alternar pausa
        if pausado:
            # Mostrar letrero de pausa
            pantalla.fill(COLOR_FONDO)
            font = pygame.font.SysFont(None, 80)
            texto = font.render("PAUSA", True, (255, 255, 0))
            pantalla.blit(texto, (ANCHO // 2 - 120, ALTO // 2 - 40))
            pygame.display.flip()
            reloj.tick(fps)
            continue

        # 2) Movimiento vertical
        teclas = pygame.key.get_pressed()
        if not saltando:
            if teclas[pygame.K_UP]:
                carrito_y = max(0, carrito_y - velocidad)
            if teclas[pygame.K_DOWN]:
                carrito_y = min(ALTO - CAR_HEIGHT, carrito_y + velocidad)

        # 3) Lógica de salto
        if saltando:
            carrito_y -= vel_salto
            vel_salto  -= 1
            if carrito_y >= ALTO // 2:
                carrito_y = ALTO // 2
                saltando  = False

        # 4) Avance en X del "mundo" y cálculo de cámara
        mundo_x += velocidad
        cam_x    = mundo_x - CAR_POS_X

        # 5) Consulta de obstáculos visibles
        visibles = avl.rango(
                avl.raiz,
                float('-inf'), float('inf'),  # Todos los valores de x
                float('-inf'), float('inf')   # Todos los valores de y
        )

        # 5.1) Eliminar obstáculos que ya pasaste (quedaron atrás de la cámara)
        pasados = avl.rango(avl.raiz, float('-inf'), cam_x - 1, 0, ALTO)
        for obs in pasados:
            avl.raiz = avl.eliminar(avl.raiz, obs["x"], obs["y"])

        # 6) Detección de colisiones y eliminación de nodo AVL
        car_rect = pygame.Rect(CAR_POS_X, carrito_y, CAR_WIDTH, CAR_HEIGHT)
        for obs in visibles:
            x_p    = obs["x"] - cam_x
            obs_rc = pygame.Rect(x_p, obs["y"], OBS_WIDTH, OBS_HEIGHT)
            if car_rect.colliderect(obs_rc):
                daño     = DAÑO_POR_TIPO.get(obs["tipo"], DAÑO_POR_TIPO["default"])
                energia -= daño
                avl.raiz = avl.eliminar(avl.raiz, obs["x"], obs["y"])
                break

        if energia <= 0:
            pantalla.fill(COLOR_FONDO)
            font = pygame.font.SysFont(None, 80)
            texto = font.render("GAME OVER", True, (255, 0, 0))
            pantalla.blit(texto, (ANCHO // 2 - 200, ALTO // 2 - 40))
            font2 = pygame.font.SysFont(None, 40)
            texto2 = font2.render("¡Sin energía!", True, (255, 255, 255))
            pantalla.blit(texto2, (ANCHO // 2 - 120, ALTO // 2 + 50))
            pygame.display.flip()
            pygame.time.wait(3000)  # Espera 3 segundos
            pygame.quit()
            return

        # 7) Dibujado de elementos

        # Fondo verde (césped)
        pantalla.fill((34, 139, 34))  # Verde césped

        # Carretera (rectángulo gris)
        carretera_y = 100
        carretera_alto = 400
        pygame.draw.rect(pantalla, (60, 60, 60), (0, carretera_y, ANCHO_JUEGO, carretera_alto))
        
        # Líneas blancas de los bordes
        pygame.draw.line(pantalla, (255, 255, 255), (0, carretera_y), (ANCHO_JUEGO, carretera_y), 4)
        pygame.draw.line(pantalla, (255, 255, 255), (0, carretera_y + carretera_alto), (ANCHO_JUEGO, carretera_y + carretera_alto), 4)

        # Línea central amarilla (continua)
        pygame.draw.line(
            pantalla, (255, 215, 0),
            (0, carretera_y + carretera_alto // 2),
            (ANCHO_JUEGO, carretera_y + carretera_alto // 2), 4
        )

        # Líneas blancas de carriles (continuas)
        for offset in [carretera_alto // 3, 2 * carretera_alto // 3]:
            pygame.draw.line(
                pantalla, (255, 255, 255),
                (0, carretera_y + offset),
                (ANCHO_JUEGO, carretera_y + offset), 2
            )

        # Dibuja el área del juego
        #pygame.draw.rect(pantalla, (40, 40, 40), (0, 0, ANCHO_JUEGO, ALTO))
        pantalla.blit(car_img, (CAR_POS_X, carrito_y))

        for obs in visibles:
            x_p = obs["x"] - cam_x
            tipo = obs.get("tipo", "default")
            img = img_obstaculos.get(tipo, img_obstaculos["default"])
            pantalla.blit(img, (x_p, obs["y"]))

        # Barra de energía
        dibujar_barra_energia(pantalla, 10, 10, 100, 20, energia, 300)

        # Dibuja el árbol al lado derecho si está activado
        if mostrar_arbol:
            dibujar_arbol_en_pantalla(avl, pantalla, offset_x=ANCHO_JUEGO, ancho=ANCHO_ARBOL, alto=ALTO)

        if avl.raiz is None:
            pantalla.fill(COLOR_FONDO)
            font = pygame.font.SysFont(None, 80)
            texto = font.render("GANASTE!!", True, (255, 255, 255))
            pantalla.blit(texto, (ANCHO // 2 - 200, ALTO // 2 - 40))
            pygame.display.flip()
            pygame.time.wait(3000)  # Espera 3 segundos
            pygame.quit()
            return

        pygame.display.flip()
        reloj.tick(fps)






