from arbol_avl    import ArbolAVL
from gestor_json  import cargar_datos
from interfaz     import iniciar_interfaz, menu_principal

def main():

    config, obstaculos = cargar_datos("obstaculos.json")

    avl = ArbolAVL()
    for o in obstaculos:
        avl.raiz = avl.insertar(avl.raiz, o["x"], o["y"], o["tipo"])

    #iniciar_interfaz(avl, config)
    menu_principal(avl, config)

    

if __name__ == "__main__":
    main()


