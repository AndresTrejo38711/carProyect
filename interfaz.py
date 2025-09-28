import pygame
from visual_arbol import dibujar_arbol_en_pantalla
import recorrido 
import sys
import json


# Constantes de pantalla y objetos
ANCHO_JUEGO, ANCHO_ARBOL = 800, 400
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
car_img_salto = pygame.image.load("resources/carroRojo.png")  # Imagen con color diferente
car_img_salto = pygame.transform.scale(car_img_salto, (CAR_WIDTH, CAR_HEIGHT))
car_img = pygame.image.load("resources/carrito.png")
car_img = pygame.transform.scale(car_img, (CAR_WIDTH, CAR_HEIGHT))
img_obstaculos = {
    "roca":   pygame.transform.scale(pygame.image.load("resources/rocas.png"),   (OBS_WIDTH, OBS_HEIGHT)),
    "cono":   pygame.transform.scale(pygame.image.load("resources/conos.png"),   (OBS_WIDTH, OBS_HEIGHT)),
    "hueco":  pygame.transform.scale(pygame.image.load("resources/bache.png"),  (OBS_WIDTH, OBS_HEIGHT)),
    "aceite": pygame.transform.scale(pygame.image.load("resources/aceite.png"), (OBS_WIDTH, OBS_HEIGHT)),
    "arbol":  pygame.transform.scale(pygame.image.load("resources/arbol.png"),  (OBS_WIDTH, OBS_HEIGHT)),
    "arbusto":pygame.transform.scale(pygame.image.load("resources/arbusto.png"), (OBS_WIDTH, OBS_HEIGHT)),
    "perrito":pygame.transform.scale(pygame.image.load("resources/perrito.png"), (OBS_WIDTH, OBS_HEIGHT)),
    "default":pygame.transform.scale(pygame.image.load("resources/carrito.png"),   (OBS_WIDTH, OBS_HEIGHT))
}


COLOR_FONDO      = (50, 50, 50)
COLOR_CARRITO    = (0, 255, 0)
COLOR_OBSTACULO  = (255, 0, 0)
COLOR_ENERGIA_BG = (0,   0,   0)
COLOR_ENERGIA    = (0, 120, 255)

DAÑO_POR_TIPO = {
    "roca":    25,  # 25% de energía
    "cono":    10,  # 10% de energía
    "hueco":   15,  # 15% de energía
    "aceite":  20,  # 20% de energía
    "arbol":   30,  # 30% de energía
    "arbusto": 15,  # 15% de energía
    "perrito": 5,   # 5% de energía (menos daño)
    "default": 10   # 10% por defecto
}


def menu_principal(avl, config):
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Menú Principal")
    font = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()

    fondo = pygame.image.load("resources/fondo.png")
    fondo = pygame.transform.scale(fondo, (1200, 700))  

    seleccionado = 0  # índice de la opción seleccionada
    opciones = ["Iniciar Juego", "Recorridos", "Agregar Obstáculo", "Dificultad", "Color del Auto", "Salir"]

    while True:
        #pantalla.fill((0, 100, 200))  # fondo azul
        pantalla.blit(fondo, (0, 0))  # dibuja el fondo

        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == seleccionado else (255, 255, 255)
            texto = font.render(opcion, True, color)
            pantalla.blit(texto, (30, 120 + i * 60)) 

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
                    elif opciones[seleccionado] == "Recorridos":
                        mostrar_recorridos(avl)
                    elif opciones[seleccionado] == "Agregar Obstáculo":
                        agregar_obstaculo(avl, config)
                    elif opciones[seleccionado] == "Dificultad":
                        cambiar_dificultad(config)
                    elif opciones[seleccionado] == "Color del Auto":
                        seleccionar_color_auto(config)
                    elif opciones[seleccionado] == "Salir":
                        pygame.quit()
                        sys.exit()
# Opción para seleccionar el color/estilo del auto
def seleccionar_color_auto(config):
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Seleccionar Color del Auto")
    font = pygame.font.SysFont(None, 60)
    font2 = pygame.font.SysFont(None, 30)
    clock = pygame.time.Clock()

    estilos = [
        ("Azul", "resources/cars/lr_modern_blue.png"),
        ("Verde", "resources/cars/lr_modern_green.png"),
        ("Rosa", "resources/cars/lr_modern_pink.png"),
        ("Rojo", "resources/cars/lr_modern_red.png"),
        ("Fantasma", "resources/cars/lr_modern_ghost.png")
    ]
    seleccionado = 0

    while True:
        pantalla.fill((30, 30, 60))
        texto = font.render("Selecciona el color del auto", True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO//2 - 320, 60))

        for i, (nombre, ruta) in enumerate(estilos):
            color = (255, 255, 0) if i == seleccionado else (255, 255, 255)
            texto_op = font2.render(nombre, True, color)
            pantalla.blit(texto_op, (ANCHO//2 - 100, 180 + i * 50))
            # Mostrar preview del auto
            img = pygame.image.load(ruta)
            img = pygame.transform.scale(img, (120, 60))
            pantalla.blit(img, (ANCHO//2 + 80, 180 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seleccionado = (seleccionado - 1) % len(estilos)
                elif event.key == pygame.K_DOWN:
                    seleccionado = (seleccionado + 1) % len(estilos)
                elif event.key == pygame.K_RETURN:
                    # Guardar selección en config
                    config["car_img"] = estilos[seleccionado][1]
                    return
        clock.tick(30)
        clock.tick(30)

def cambiar_dificultad(config):
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Cambiar Dificultad")
    font = pygame.font.SysFont(None, 60)
    font2 = pygame.font.SysFont(None, 40)
    clock = pygame.time.Clock()

    velocidades = [5, 10, 20, 25, 35]
    seleccionado = velocidades.index(config.get("velocidad", 2))

    while True:
        pantalla.fill((30, 30, 60))
        texto = font.render("Selecciona la velocidad", True, (255, 255, 255))
        pantalla.blit(texto, (30, 30))

        for i, v in enumerate(velocidades):
            color = (255, 255, 0) if i == seleccionado else (255, 255, 255)
            txt = font2.render(f"{v}", True, color)
            pantalla.blit(txt, (30, 120 + i * 60))

        pantalla.blit(font2.render("Arriba/Abajo para elegir, Enter para confirmar, ESC para salir", True, (200,200,200)), (30, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seleccionado = (seleccionado - 1) % len(velocidades)
                elif event.key == pygame.K_DOWN:
                    seleccionado = (seleccionado + 1) % len(velocidades)
                elif event.key == pygame.K_RETURN:
                    config["velocidad"] = velocidades[seleccionado]
                    return

        pygame.display.flip()
        clock.tick(30)
        
# Opcion de agregar obstaculo
def agregar_obstaculo(avl, config):
    distancia_total = config.get("distancia_total", 5000)

    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Agregar Obstáculo")
    font = pygame.font.SysFont(None, 40)
    font2 = pygame.font.SysFont(None, 30)
    clock = pygame.time.Clock()

    tipos = ["roca", "cono", "hueco", "aceite", "arbol", "arbusto", "perrito"]
    seleccionado = 0
    x_text = ""
    y_text = ""
    input_activo = "x"  # "x" o "y"

    mensaje = ""

    import json

    def guardar_obstaculos_json(config, avl, ruta="obstaculos.json"):
        # Recorrer el árbol y obtener todos los obstáculos
        def recolectar(nodo, lista):
            if nodo:
                recolectar(nodo.izquierda, lista)
                lista.append({"x": nodo.x, "y": nodo.y, "tipo": nodo.tipo})
                recolectar(nodo.derecha, lista)
        lista = []
        recolectar(avl.raiz, lista)
        datos = {"config": config, "obstaculos": lista}
        with open(ruta, "w") as f:
            json.dump(datos, f, indent=2)

    while True:
        pantalla.fill((30, 30, 60))
        texto = font.render("Agregar Obstáculo", True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO//2 - 200, 60))

        # Campos de texto para coordenadas
        color_x = (255, 255, 0) if input_activo == "x" else (255, 255, 255)
        color_y = (255, 255, 0) if input_activo == "y" else (255, 255, 255)
        pantalla.blit(font2.render(f"X: {x_text}", True, color_x), (ANCHO//2 - 100, 150))
        pantalla.blit(font2.render(f"Y: {y_text}", True, color_y), (ANCHO//2 + 50, 150))
        pantalla.blit(font2.render(f"Tipo: {tipos[seleccionado]}", True, (255,255,0)), (ANCHO//2 - 100, 200))

        pantalla.blit(font2.render("Tab para cambiar campo, flechas para tipo, Enter para agregar, ESC para salir", True, (200,200,200)), (ANCHO//2 - 300, 300))
        pantalla.blit(font2.render(mensaje, True, (255,100,100)), (ANCHO//2 - 100, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    input_activo = "y" if input_activo == "x" else "x"
                elif event.key == pygame.K_UP:
                    seleccionado = (seleccionado - 1) % len(tipos)
                elif event.key == pygame.K_DOWN:
                    seleccionado = (seleccionado + 1) % len(tipos)
                elif event.key == pygame.K_RETURN:
                    try:
                        x = int(x_text)
                        y = int(y_text)
                        if 0 <= x <= distancia_total and 0 <= y <= ALTO:
                            avl.raiz = avl.insertar(avl.raiz, x, y, tipos[seleccionado])
                            guardar_obstaculos_json(config, avl)  
                            mensaje = "¡Obstáculo agregado!"
                            x_text, y_text = "", ""
                        else:
                            mensaje = "Coordenadas fuera de rango"
                    except ValueError:
                        mensaje = "Coordenadas inválidas"
                elif event.key == pygame.K_BACKSPACE:
                    if input_activo == "x":
                        x_text = x_text[:-1]
                    else:
                        y_text = y_text[:-1]
                else:
                    if event.unicode.isdigit():
                        if input_activo == "x":
                            x_text += event.unicode
                        else:
                            y_text += event.unicode

        pygame.display.flip()
        clock.tick(30)

# Opcion mostrar recorridos
def mostrar_recorridos(avl):

    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Recorridos AVL")
    font = pygame.font.SysFont(None, 18)
    clock = pygame.time.Clock()

    # Obtén los recorridos
    inorden   = recorrido.inorden(avl.raiz)
    preorden  = recorrido.preorden(avl.raiz)
    postorden = recorrido.postorden(avl.raiz)
    bfs       = recorrido.bfs(avl.raiz)

    recorridos = [
        ("Inorden", inorden),
        ("Preorden", preorden),
        ("Postorden", postorden),
        ("Anchura", bfs)
    ]

    def render_lista(nombre, lista, x, y, font, pantalla, max_width):
        # Título con color diferente
        titulo_color = (255, 215, 0)  # Amarillo dorado
        lista_color = (255, 255, 255) # Blanco

        texto = f"{nombre}: "
        rendered = font.render(texto, True, titulo_color)
        pantalla.blit(rendered, (x, y))
        offset = rendered.get_width()
        linea = ""
        for item in lista:
            item_str = str(item)
            if font.size(linea + item_str)[0] + x + offset > max_width:
                rendered = font.render(linea, True, lista_color)
                pantalla.blit(rendered, (x + offset, y))
                y += 30
                linea = ""
                offset = 0
            linea += item_str + ", "
        if linea:
            rendered = font.render(linea, True, lista_color)
            pantalla.blit(rendered, (x + offset, y))
        return y + 40

    running = True
    while running:
        pantalla.fill((30, 30, 60))
        y = 40
        for nombre, lista in recorridos:
            y = render_lista(nombre, lista, 30, y, font, pantalla, ANCHO - 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        pygame.display.flip()
        clock.tick(30)


def iniciar_interfaz(avl, config):
    # Extraer configuración
    distancia_total = config.get("distancia_total", 5000)
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
    pausado = False  # Estado de pausa

    # Cargar imagen del auto según selección
    car_img_path = config.get("car_img", "resources/carrito.png")
    car_img = pygame.image.load(car_img_path)
    car_img = pygame.transform.scale(car_img, (CAR_WIDTH, CAR_HEIGHT))
    car_img_salto = pygame.image.load("resources/carroRojo.png")
    car_img_salto = pygame.transform.scale(car_img_salto, (CAR_WIDTH, CAR_HEIGHT))

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
            carroPausa = pygame.image.load("resources/carroPausa.png")
            carroPausa = pygame.transform.scale(carroPausa, (ANCHO, ALTO))
            pantalla.blit(carroPausa, (0, 0))  # Dibuja la imagen de fondo de pausa
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

        # Dibuja la meta si está en pantalla
        distancia_total = config.get("distancia_total", 5000)
        meta_x = distancia_total - cam_x
        if 0 <= meta_x <= ANCHO_JUEGO:
            meta_rect = pygame.Rect(meta_x, carretera_y, 20, carretera_alto)
            pygame.draw.rect(pantalla, (255, 0, 255), meta_rect)  # Meta color fucsia
            font_meta = pygame.font.SysFont(None, 40)
            pantalla.blit(font_meta.render("META", True, (255,255,255)), (meta_x - 10, carretera_y - 40))

        if mundo_x >= distancia_total:
            carroMeta = pygame.image.load("resources/carroMeta.png")
            carroMeta = pygame.transform.scale(carroMeta, (ANCHO, ALTO))
            pantalla.blit(carroMeta, (0, 0))  # Dibuja la imagen de fondo de meta
            font = pygame.font.SysFont(None, 80)
            texto = font.render("¡Llegaste a la meta!", True, (255, 0, 0))
            pantalla.blit(texto, (ANCHO // 2 - 250, ALTO // 2 - 40))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            return

         # 5) Consulta de obstáculos visibles (solo los que están en pantalla)
        visibles = avl.rango(
                avl.raiz,
                cam_x, cam_x + ANCHO_JUEGO,  # Solo X visible en pantalla
                0, ALTO                       # Solo Y visible en pantalla
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
            # Solo colisiona si NO está saltando
            if car_rect.colliderect(obs_rc) and not saltando:
                daño     = DAÑO_POR_TIPO.get(obs["tipo"], DAÑO_POR_TIPO["default"])
                energia -= daño
                avl.raiz = avl.eliminar(avl.raiz, obs["x"], obs["y"])
                break

        if energia <= 0:
            img_sin_energia = pygame.image.load("resources/carroEstrellado.png")
            img_sin_energia = pygame.transform.scale(img_sin_energia, (ANCHO, ALTO))    
            pantalla.blit(img_sin_energia, (0, 0))  # Dibuja la imagen de fondo
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
        if saltando:
            # Si el auto seleccionado es fantasma, no cambia color
            if car_img_path.endswith("ghost.png"):
                pantalla.blit(car_img, (CAR_POS_X, carrito_y))
            else:
                # Cambia a rojo durante el salto
                pantalla.blit(car_img_salto, (CAR_POS_X, carrito_y))
        else:
            pantalla.blit(car_img, (CAR_POS_X, carrito_y))

        for obs in visibles:
            x_p = obs["x"] - cam_x
            tipo = obs.get("tipo", "default")
            img = img_obstaculos.get(tipo, img_obstaculos["default"])
            pantalla.blit(img, (x_p, obs["y"]))

        # Barra de energía
        dibujar_barra_energia(pantalla, 10, 10, 100, 20, energia, 100)

        # Dibuja el árbol al lado derecho si está activado
        if mostrar_arbol:
            dibujar_arbol_en_pantalla(avl, pantalla, offset_x=ANCHO_JUEGO, ancho=ANCHO_ARBOL, alto=ALTO)

        if avl.raiz is None and mundo_x >= distancia_total:
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






