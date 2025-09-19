import pygame
from visual_arbol import dibujar_arbol_en_pantalla

# ---------------------------------------------------
# Constantes de pantalla y objetos
# ---------------------------------------------------
ANCHO_JUEGO, ANCHO_ARBOL = 700, 400
ANCHO, ALTO = ANCHO_JUEGO + ANCHO_ARBOL, 600

CAR_WIDTH, CAR_HEIGHT = 50, 30
CAR_POS_X = 100

OBS_WIDTH, OBS_HEIGHT = 40, 40

COLOR_FONDO      = (50, 50, 50)
COLOR_CARRITO    = (0, 255, 0)
COLOR_OBSTACULO  = (255, 0, 0)
COLOR_ENERGIA_BG = (0,   0,   0)
COLOR_ENERGIA    = (0, 255,   0)

DAÑO_POR_TIPO = {
    "roca":   20,
    "cono":   10,
    "hueco":  15,
    "aceite":  5,
    "default":10
}

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
    energia   = 100

    mostrar_arbol = True  # Mostrar el árbol al lado del juego

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
            cam_x, cam_x + ANCHO_JUEGO,
            0,         ALTO
        )

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
            print("¡Juego terminado! Sin energía.")
            pygame.quit()
            return

        # 7) Dibujado de elementos
        pantalla.fill(COLOR_FONDO)
        # Dibuja el área del juego
        pygame.draw.rect(pantalla, (40, 40, 40), (0, 0, ANCHO_JUEGO, ALTO))
        pygame.draw.rect(pantalla, COLOR_CARRITO,
                         (CAR_POS_X, carrito_y, CAR_WIDTH, CAR_HEIGHT))

        for obs in visibles:
            x_p = obs["x"] - cam_x
            pygame.draw.rect(pantalla, COLOR_OBSTACULO,
                             (x_p, obs["y"], OBS_WIDTH, OBS_HEIGHT))

        # Barra de energía
        pygame.draw.rect(pantalla, COLOR_ENERGIA_BG, (10, 10, 100, 20))
        pygame.draw.rect(pantalla, COLOR_ENERGIA,    (10, 10, energia, 20))

        # Dibuja el árbol al lado derecho si está activado
        if mostrar_arbol:
            dibujar_arbol_en_pantalla(avl, pantalla, offset_x=ANCHO_JUEGO, ancho=ANCHO_ARBOL, alto=ALTO)

        pygame.display.flip()
        reloj.tick(fps)






