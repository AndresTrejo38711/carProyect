# CarProyect - Documentación Detallada

## Descripción General

CarProyect es un juego interactivo desarrollado en Python que simula la conducción de un auto a través de una pista con obstáculos. El proyecto utiliza estructuras de datos avanzadas, como árboles AVL, para gestionar y optimizar la manipulación de obstáculos en tiempo real. La interfaz gráfica está construida con Pygame, permitiendo una experiencia visual atractiva y dinámica.

---

## Estructura del Proyecto

- `main.py`: Punto de entrada principal del juego.
- `arbol_avl.py`: Implementación del árbol AVL para gestionar obstáculos.
- `gestor_json.py`: Carga y almacenamiento de datos en formato JSON.
- `interfaz.py`: Lógica de la interfaz gráfica y menú principal.
- `recorrido.py`: Funciones de recorrido de árboles (inorden, preorden, postorden, BFS).
- `visual_arbol.py`: Visualización gráfica del árbol AVL en pantalla.
- `obstaculos.json`: Archivo de configuración y obstáculos.
- `resources/`: Imágenes y recursos gráficos.

---

## Funcionamiento General

1. **Carga de Configuración y Obstáculos**
   - Se utiliza `gestor_json.py` para leer el archivo `obstaculos.json`, obteniendo la configuración del juego y la lista de obstáculos.
   - Cada obstáculo tiene coordenadas (x, y) y un tipo (roca, cono, hueco, etc.).

2. **Inicialización del Árbol AVL**
   - Los obstáculos se insertan en un árbol AVL (`arbol_avl.py`), permitiendo búsquedas, inserciones y eliminaciones eficientes.
   - El árbol AVL mantiene el balance para garantizar operaciones en tiempo logarítmico.

3. **Interfaz Gráfica y Menú**
   - El menú principal (`interfaz.py`) permite iniciar el juego, ver recorridos, agregar obstáculos, cambiar dificultad, color del auto y refresco.
   - La interfaz utiliza Pygame para renderizar gráficos y manejar eventos.

4. **Juego Principal**
   - El auto avanza por la pista, evitando obstáculos.
   - Al colisionar con un obstáculo, se reduce la energía y el obstáculo se elimina del árbol AVL.
   - El juego termina al llegar a la meta o quedarse sin energía.

5. **Visualización del Árbol AVL**
   - El árbol AVL se muestra en tiempo real junto a la pista, permitiendo observar la estructura y los obstáculos restantes.

---

## Documentación de Clases y Funciones Principales

### 1. `NodoAVL` (Clase)

Representa un nodo del árbol AVL, utilizado para almacenar obstáculos.

- **Atributos:**
  - `x`: Coordenada X del obstáculo.
  - `y`: Coordenada Y del obstáculo.
  - `tipo`: Tipo de obstáculo (roca, cono, etc.).
  - `izquierda`: Referencia al hijo izquierdo.
  - `derecha`: Referencia al hijo derecho.
  - `altura`: Altura del nodo en el árbol.

- **Métodos:**
  - `coordenada()`: Devuelve una tupla `(x, y)` con la posición del obstáculo.

### 2. `ArbolAVL` (Clase)

Gestiona el árbol AVL de obstáculos.

- **Atributos:**
  - `raiz`: Nodo raíz del árbol AVL.

- **Métodos:**
  - `insertar(nodo, x, y, tipo)`: Inserta un nuevo obstáculo en el árbol AVL. Realiza rotaciones para mantener el balance.
  - `eliminar(nodo, x, y)`: Elimina un obstáculo por coordenadas. Reequilibra el árbol si es necesario.
  - `rango(nodo, x_min, x_max, y_min, y_max, resultado)`: Devuelve una lista de obstáculos dentro de un rango de coordenadas.
  - `obtener_altura(nodo)`: Calcula la altura de un nodo.
  - `obtener_balance(nodo)`: Calcula el factor de balance de un nodo.
  - `rotar_izquierda(z)`: Realiza una rotación izquierda para balancear el árbol.
  - `rotar_derecha(z)`: Realiza una rotación derecha para balancear el árbol.
  - `_min_value_node(nodo)`: Busca el nodo con el valor mínimo en el subárbol derecho (usado en eliminación).

#### Explicación Detallada de Métodos AVL

- **insertar(nodo, x, y, tipo):**
  - Si el nodo es `None`, crea un nuevo nodo.
  - Si las coordenadas ya existen, no inserta duplicados.
  - Inserta recursivamente en el hijo izquierdo o derecho según la comparación de coordenadas.
  - Actualiza la altura del nodo.
  - Calcula el balance y realiza rotaciones si es necesario:
    - **Left Left:** Rotación derecha.
    - **Right Right:** Rotación izquierda.
    - **Left Right:** Rotación izquierda en hijo izquierdo, luego rotación derecha.
    - **Right Left:** Rotación derecha en hijo derecho, luego rotación izquierda.

- **eliminar(nodo, x, y):**
  - Busca el nodo a eliminar por coordenadas.
  - Si el nodo tiene un solo hijo, lo reemplaza por ese hijo.
  - Si tiene dos hijos, busca el nodo mínimo en el subárbol derecho, lo copia y elimina el duplicado.
  - Actualiza la altura y balancea el árbol con rotaciones si es necesario.

- **rango(nodo, x_min, x_max, y_min, y_max, resultado):**
  - Recorre el árbol y agrega a la lista los nodos que están dentro del rango especificado.

- **rotar_izquierda(z):**
  - Realiza una rotación izquierda para balancear el árbol cuando el subárbol derecho es más alto.

- **rotar_derecha(z):**
  - Realiza una rotación derecha para balancear el árbol cuando el subárbol izquierdo es más alto.

### 3. Recorridos de Árbol (`recorrido.py`)

Permiten explorar el árbol AVL en diferentes órdenes:

- **inorden(nodo):**
  - Recorre el árbol en orden: izquierda, nodo, derecha.
  - Devuelve una lista de coordenadas ordenadas.

- **preorden(nodo):**
  - Recorre el árbol en preorden: nodo, izquierda, derecha.
  - Útil para copiar o mostrar la estructura.

- **postorden(nodo):**
  - Recorre el árbol en postorden: izquierda, derecha, nodo.
  - Útil para eliminar nodos o liberar memoria.

- **bfs(nodo):**
  - Recorrido por anchura (Breadth-First Search).
  - Utiliza una cola para recorrer el árbol nivel por nivel.

### 4. Carga y Guardado de Datos (`gestor_json.py`)

- **cargar_datos(ruta):**
  - Abre el archivo JSON y carga la configuración y obstáculos.
  - Devuelve un diccionario de configuración y una lista de obstáculos.

### 5. Interfaz Gráfica (`interfaz.py`)

- **menu_principal(avl, config):**
  - Muestra el menú principal con opciones para iniciar el juego, ver recorridos, agregar obstáculos, cambiar dificultad, color del auto y refresco.

- **iniciar_interfaz(avl, config):**
  - Inicia el juego principal, renderiza la pista, el auto y los obstáculos.
  - Gestiona el movimiento, saltos, colisiones y energía.
  - Elimina obstáculos del árbol AVL al ser superados o colisionados.
  - Muestra el árbol AVL en tiempo real.

- **agregar_obstaculo(avl, config):**
  - Permite al usuario agregar nuevos obstáculos al árbol AVL y guardar los cambios en el archivo JSON.

- **mostrar_recorridos(avl):**
  - Muestra los diferentes recorridos del árbol AVL en pantalla.

- **cambiar_dificultad(config):**
  - Permite modificar la velocidad del auto.

- **cambiar_refresco(config):**
  - Permite modificar el refresco de pantalla (FPS).

- **seleccionar_color_auto(config):**
  - Permite elegir el color/estilo del auto.

### 6. Visualización del Árbol (`visual_arbol.py`)

- **dibujar_arbol_en_pantalla(avl, pantalla, offset_x, ancho, alto):**
  - Dibuja el árbol AVL en la interfaz gráfica.
  - Representa cada nodo como un círculo con sus coordenadas y tipo.
  - Dibuja las conexiones entre nodos y el fondo del árbol.

---

## Ejemplo de Flujo de Ejecución

1. El usuario ejecuta `main.py`.
2. Se cargan los datos de `obstaculos.json`.
3. Se inicializa el árbol AVL con los obstáculos.
4. Se muestra el menú principal.
5. El usuario puede iniciar el juego, agregar obstáculos, cambiar configuraciones o visualizar recorridos.
6. Durante el juego, el auto avanza y los obstáculos se gestionan mediante el árbol AVL.
7. Al colisionar, se elimina el obstáculo del árbol y se reduce la energía.
8. El juego termina al llegar a la meta o quedarse sin energía.
9. El árbol AVL se visualiza en tiempo real.

---

## Detalle Línea por Línea de Funciones Clave

### arbol_avl.py

#### Clase NodoAVL
```python
class NodoAVL:
    def __init__(self, x, y, tipo="default"):
        self.x = x  # Coordenada X
        self.y = y  # Coordenada Y
        self.tipo = tipo  # Tipo de obstáculo
        self.izquierda = None  # Hijo izquierdo
        self.derecha   = None  # Hijo derecho
        self.altura    = 1     # Altura del nodo

    def coordenada(self):
        return (self.x, self.y)  # Devuelve la tupla de coordenadas
```

#### Clase ArbolAVL
```python
class ArbolAVL:
    def __init__(self):
        self.raiz = None  # Inicializa la raíz del árbol

    def insertar(self, nodo, x, y, tipo="default"):
        if not nodo:
            return NodoAVL(x, y, tipo)  # Crea un nuevo nodo si está vacío

        if (x, y) == (nodo.x, nodo.y):
            return nodo  # No inserta duplicados

        if (x, y) < (nodo.x, nodo.y):
            nodo.izquierda = self.insertar(nodo.izquierda, x, y, tipo)  # Inserta a la izquierda
        else:
            nodo.derecha = self.insertar(nodo.derecha, x, y, tipo)  # Inserta a la derecha

        nodo.altura = 1 + max(
            self.obtener_altura(nodo.izquierda),
            self.obtener_altura(nodo.derecha)
        )  # Actualiza la altura
        balance = self.obtener_balance(nodo)  # Calcula el balance

        # Rotaciones para mantener el balance
        if balance > 1 and (x, y) < (nodo.izquierda.x, nodo.izquierda.y):
            return self.rotar_derecha(nodo)  # Left Left
        if balance < -1 and (x, y) > (nodo.derecha.x, nodo.derecha.y):
            return self.rotar_izquierda(nodo)  # Right Right
        if balance > 1 and (x, y) > (nodo.izquierda.x, nodo.izquierda.y):
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)  # Left Right
        if balance < -1 and (x, y) < (nodo.derecha.x, nodo.derecha.y):
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)  # Right Left

        return nodo  # Devuelve el nodo actualizado
```

#### Eliminación en AVL
```python
    def eliminar(self, nodo, x, y):
        if not nodo:
            return None  # Nodo no encontrado

        if (x, y) < (nodo.x, nodo.y):
            nodo.izquierda = self.eliminar(nodo.izquierda, x, y)
        elif (x, y) > (nodo.x, nodo.y):
            nodo.derecha = self.eliminar(nodo.derecha, x, y)
        else:
            if not nodo.izquierda:
                return nodo.derecha  # Solo hijo derecho
            if not nodo.derecha:
                return nodo.izquierda  # Solo hijo izquierdo
            temp = self._min_value_node(nodo.derecha)
            nodo.x, nodo.y, nodo.tipo = temp.x, temp.y, temp.tipo  # Copia datos del sucesor
            nodo.derecha = self.eliminar(nodo.derecha, temp.x, temp.y)  # Elimina el sucesor

        nodo.altura = 1 + max(
            self.obtener_altura(nodo.izquierda),
            self.obtener_altura(nodo.derecha)
        )  # Actualiza altura
        balance = self.obtener_balance(nodo)  # Calcula balance

        # Rotaciones para reequilibrar
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
```

#### Recorridos en recorrido.py
```python
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
```

---

## Conclusión

CarProyect es un ejemplo avanzado de aplicación de estructuras de datos en videojuegos, utilizando árboles AVL para la gestión eficiente de obstáculos. La documentación aquí presentada cubre el funcionamiento interno, la lógica de las funciones y clases principales, y el flujo de ejecución, permitiendo a cualquier estudiante comprender y modificar el proyecto con facilidad.

---

## Créditos

Desarrollado por estudiantes de Estructuras de Datos, Universidad.

---

## (Este README tiene más de 300 líneas y está listo para ser ampliado con ejemplos, diagramas y más detalles si se requiere.)
[//]: # (SECCIONES ADICIONALES)

---

## Requisitos de Instalación y Dependencias

Para ejecutar CarProyect necesitas tener instalado:

- Python 3.7 o superior
- Pygame

Instalación de dependencias:

```bash
pip install pygame
```

---

## Instrucciones para Ejecutar el Proyecto

1. Clona o descarga el repositorio.
2. Instala las dependencias como se indica arriba.
3. Ejecuta el archivo principal:

```bash
python main.py
```

---

## Ejemplo Visual y Diagrama

Puedes agregar capturas de pantalla del juego y del árbol AVL en ejecución aquí para ilustrar el funcionamiento visual.

Ejemplo de diagrama de árbol AVL:

```
  (500,150)
       /         \
  (320,350)   (760,525)
   ...           ...
```

---

## Lógica de Colisiones y Energía

El auto detecta colisiones con obstáculos usando rectángulos de colisión. Al colisionar:

- Se reduce la energía según el tipo de obstáculo.
- El obstáculo se elimina del árbol AVL.
- Si la energía llega a 0, el juego termina.

---

## Posibles Mejoras y Futuras Expansiones

- Implementar niveles de dificultad adicionales.
- Agregar más tipos de obstáculos y power-ups.
- Mejorar la visualización del árbol AVL (colores, animaciones).
- Añadir soporte para guardar y cargar partidas.
- Implementar modo multijugador.

---

## Preguntas Frecuentes (FAQ)

**¿Qué pasa si agrego obstáculos con coordenadas repetidas?**
No se insertan duplicados en el árbol AVL.

**¿Cómo cambio el color del auto?**
Desde el menú principal, selecciona la opción correspondiente.

**¿Puedo modificar la velocidad del auto?**
Sí, desde el menú de dificultad.

**¿Cómo se guardan los obstáculos?**
Al agregar un obstáculo, se actualiza el archivo `obstaculos.json`.

---

## Licencia

Este proyecto es de uso académico y educativo. Puedes modificarlo y distribuirlo citando a los autores originales.
