import pygame

def dibujar_arbol_en_pantalla(avl, pantalla, offset_x=800, ancho=400, alto=600):
    font = pygame.font.SysFont(None, 20)

    def _dibujar(nodo, x, y, dx):
        if not nodo:
            return
        text = font.render(f"{nodo.x},{nodo.y}", True, (255,255,255))
        pantalla.blit(text, (offset_x + x-10, y-10))
        if nodo.izquierda:
            x2, y2 = x - dx, y + 60
            pygame.draw.line(pantalla, (200,200,200), (offset_x + x, y), (offset_x + x2, y2))
            _dibujar(nodo.izquierda, x2, y2, dx//2)
        if nodo.derecha:
            x2, y2 = x + dx, y + 60
            pygame.draw.line(pantalla, (200,200,200), (offset_x + x, y), (offset_x + x2, y2))
            _dibujar(nodo.derecha, x2, y2, dx//2)

    # Fondo del árbol
    pygame.draw.rect(pantalla, (30,30,30), (offset_x, 0, ancho, alto))
    _dibujar(avl.raiz, ancho//2, 20, ancho//4)
