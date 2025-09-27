import pygame

def dibujar_arbol_en_pantalla(avl, pantalla, offset_x=800, ancho=400, alto=600):
    font = pygame.font.SysFont(None, 18)
    font_tipo = pygame.font.SysFont(None, 14)

    def _dibujar(nodo, x, y, dx):
        if not nodo:
            return
        
        # Dibujar círculo para el nodo
        pygame.draw.circle(pantalla, (100, 100, 150), (offset_x + x, y), 15)
        pygame.draw.circle(pantalla, (255, 255, 255), (offset_x + x, y), 15, 2)
        
        # Dibujar coordenadas
        text = font.render(f"({nodo.x},{nodo.y})", True, (255,255,255))
        text_rect = text.get_rect(center=(offset_x + x, y - 30))
        pantalla.blit(text, text_rect)
        
        # Dibujar tipo de obstáculo
        tipo_text = font_tipo.render(f"{nodo.tipo}", True, (200, 200, 100))
        tipo_rect = tipo_text.get_rect(center=(offset_x + x, y + 25))
        pantalla.blit(tipo_text, tipo_rect)
        
        # Dibujar conexiones
        if nodo.izquierda:
            x2, y2 = x - dx, y + 70
            pygame.draw.line(pantalla, (150,150,150), (offset_x + x, y + 15), (offset_x + x2, y2 - 15), 2)
            _dibujar(nodo.izquierda, x2, y2, dx//2)
        if nodo.derecha:
            x2, y2 = x + dx, y + 70
            pygame.draw.line(pantalla, (150,150,150), (offset_x + x, y + 15), (offset_x + x2, y2 - 15), 2)
            _dibujar(nodo.derecha, x2, y2, dx//2)

    # Fondo del árbol con título
    pygame.draw.rect(pantalla, (30,30,40), (offset_x, 0, ancho, alto))
    pygame.draw.rect(pantalla, (100,100,120), (offset_x, 0, ancho, alto), 2)
    
    # Título
    titulo_font = pygame.font.SysFont(None, 24)
    titulo = titulo_font.render("AVL Tree Structure", True, (255, 255, 255))
    pantalla.blit(titulo, (offset_x + 10, 10))
    
    if avl.raiz:
        _dibujar(avl.raiz, ancho//2, 50, ancho//4)
    else:
        no_tree_text = font.render("Empty Tree", True, (150, 150, 150))
        pantalla.blit(no_tree_text, (offset_x + ancho//2 - 40, alto//2))