from collections import deque

def inorden(nodo):
    resultado = []
    def recorrer(n):
        if n:
            recorrer(n.izquierda)
            resultado.append(n.coordenada())
            recorrer(n.derecha)
    recorrer(nodo)
    return resultado

def preorden(nodo):
    resultado = []
    def recorrer(n):
        if n:
            resultado.append(n.coordenada())
            recorrer(n.izquierda)
            recorrer(n.derecha)
    recorrer(nodo)
    return resultado

def postorden(nodo):
    resultado = []
    def recorrer(n):
        if n:
            recorrer(n.izquierda)
            recorrer(n.derecha)
            resultado.append(n.coordenada())
    recorrer(nodo)
    return resultado

def bfs(nodo):
    resultado = []
    if not nodo:
        return resultado
    cola = deque()
    cola.append(nodo)
    while cola:
        actual = cola.popleft()
        resultado.append(actual.coordenada())
        if actual.izquierda:
            cola.append(actual.izquierda)
        if actual.derecha:
            cola.append(actual.derecha)
    return resultado
