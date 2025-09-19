# arbol_avl.py

class NodoAVL:
    def __init__(self, x, y, tipo="default"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.izquierda = None
        self.derecha   = None
        self.altura    = 1

    def coordenada(self):
        return (self.x, self.y)


class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, nodo, x, y, tipo="default"):
        if not nodo:
            return NodoAVL(x, y, tipo)

        if (x, y) == (nodo.x, nodo.y):
            return nodo

        if (x, y) < (nodo.x, nodo.y):
            nodo.izquierda = self.insertar(nodo.izquierda, x, y, tipo)
        else:
            nodo.derecha = self.insertar(nodo.derecha, x, y, tipo)

        nodo.altura = 1 + max(
            self.obtener_altura(nodo.izquierda),
            self.obtener_altura(nodo.derecha)
        )
        balance = self.obtener_balance(nodo)

        # Left Left
        if balance > 1 and (x, y) < (nodo.izquierda.x, nodo.izquierda.y):
            return self.rotar_derecha(nodo)

        # Right Right
        if balance < -1 and (x, y) > (nodo.derecha.x, nodo.derecha.y):
            return self.rotar_izquierda(nodo)

        # Left Right
        if balance > 1 and (x, y) > (nodo.izquierda.x, nodo.izquierda.y):
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)

        # Right Left
        if balance < -1 and (x, y) < (nodo.derecha.x, nodo.derecha.y):
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo

    def obtener_altura(self, nodo):
        return nodo.altura if nodo else 0

    def obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)

    def rotar_izquierda(self, z):
        y  = z.derecha
        T2 = y.izquierda

        y.izquierda = z
        z.derecha    = T2

        z.altura = 1 + max(self.obtener_altura(z.izquierda),
                           self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda),
                           self.obtener_altura(y.derecha))

        return y

    def rotar_derecha(self, z):
        y  = z.izquierda
        T3 = y.derecha

        y.derecha    = z
        z.izquierda = T3

        z.altura = 1 + max(self.obtener_altura(z.izquierda),
                           self.obtener_altura(z.derecha))
        y.altura = 1 + max(self.obtener_altura(y.izquierda),
                           self.obtener_altura(y.derecha))

        return y

    def rango(self, nodo, x_min, x_max, y_min, y_max, resultado=None):
        if resultado is None:
            resultado = []
        if not nodo:
            return resultado

        if nodo.x > x_min:
            self.rango(nodo.izquierda, x_min, x_max, y_min, y_max, resultado)

        if x_min <= nodo.x <= x_max and y_min <= nodo.y <= y_max:
            resultado.append({
                "x": nodo.x,
                "y": nodo.y,
                "tipo": nodo.tipo
            })

        if nodo.x < x_max:
            self.rango(nodo.derecha, x_min, x_max, y_min, y_max, resultado)

        return resultado

    def _min_value_node(self, nodo):
        current = nodo
        while current.izquierda:
            current = current.izquierda
        return current

    def eliminar(self, nodo, x, y):
        if not nodo:
            return None

        if (x, y) < (nodo.x, nodo.y):
            nodo.izquierda = self.eliminar(nodo.izquierda, x, y)
        elif (x, y) > (nodo.x, nodo.y):
            nodo.derecha = self.eliminar(nodo.derecha, x, y)
        else:
            # Caso nodo a borrar
            if not nodo.izquierda:
                return nodo.derecha
            if not nodo.derecha:
                return nodo.izquierda

            temp = self._min_value_node(nodo.derecha)
            nodo.x, nodo.y, nodo.tipo = temp.x, temp.y, temp.tipo
            nodo.derecha = self.eliminar(nodo.derecha, temp.x, temp.y)

        nodo.altura = 1 + max(
            self.obtener_altura(nodo.izquierda),
            self.obtener_altura(nodo.derecha)
        )
        balance = self.obtener_balance(nodo)

        # Reequilibrio
        if balance > 1 and self.obtener_balance(nodo.izquierda) >= 0:
            return self.rotar_derecha(nodo)
        if balance > 1 and self.obtener_balance(nodo.izquierda) < 0:
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)
        if balance < -1 and self.obtener_balance(nodo.derecha) <= 0:
            return self.rotar_izquierda(nodo)
        if balance < -1 and self.obtener_balance(nodo.derecha) > 0:
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo









