# ==============================================================================
# SISTEMA DE GESTIÓN DE INVENTARIOS
# Equipo 12: Joalin Jonathan Pineda Del valle & Ariel Hernández Flores
# Programación Estructurada - Nivel Principiante
# ==============================================================================

# Diccionario principal que almacena el inventario global
inventario = {}


def registrar_producto():
    """
    Función para dar de alta un producto nuevo en el inventario.
    Pide los datos al usuario, valida que no existan duplicados ni valores negativos,
    y guarda la información en el diccionario principal.
    """
    print("\n--- REGISTRAR NUEVO PRODUCTO ---")
    codigo = input("Ingrese el código del producto: ").strip().upper()

    # Validar que el código no esté vacío
    if codigo == "":
        print(" Error: El código no puede estar vacío.")
        return

    # Validar si el producto ya existe
    if codigo in inventario:
        print(f" Error: El código '{codigo}' ya existe en el inventario.")
        return

    nombre = input("Ingrese el nombre del producto: ").strip()
    descripcion = input("Ingrese la descripción: ").strip()
    categoria = input("Ingrese la categoría: ").strip()

    # Validar que los valores numéricos sean válidos
    try:
        precio = float(input("Ingrese el precio (mayor a 0): "))
        if precio <= 0:
            print(" Error: El precio debe ser mayor a 0.")
            return

        cantidad = int(input("Ingrese la cantidad inicial (0 o más): "))
        if cantidad < 0:
            print(" Error: La cantidad no puede ser negativa.")
            return

        stock_minimo = int(input("Ingrese el stock mínimo (0 o más): "))
        if stock_minimo < 0:
            print(" Error: El stock mínimo no puede ser negativo.")
            return
    except ValueError:
        print(" Error: Debe ingresar un valor numérico válido.")
        return

    # Guardar los datos en la base de datos (diccionario)
    inventario[codigo] = {
        'nombre': nombre,
        'descripcion': descripcion,
        'categoria': categoria,
        'precio': precio,
        'cantidad': cantidad,
        'stock_minimo': stock_minimo
    }

    print(f" ¡Éxito! Producto '{nombre}' (Código: {codigo}) registrado.")


def buscar_producto():
    """
    Función para buscar un producto en el inventario.
    Permite buscar por el código exacto o por una palabra contenida en el nombre.
    """
    print("\n--- BUSCAR PRODUCTO ---")
    if len(inventario) == 0:
        print(" El inventario está vacío.")
        return

    busqueda = input("Ingrese el código exacto o parte del nombre a buscar: ").strip().upper()
    encontrados = 0

    print("\nResultados de la búsqueda:")
    print("-" * 50)

    # Recorremos el diccionario para buscar coincidencias
    for codigo, datos in inventario.items():
        # Comprobar coincidencia en código o en el nombre
        if busqueda == codigo or busqueda in datos['nombre'].upper():
            print(f"Código: {codigo}")
            print(f"  Nombre:       {datos['nombre']}")
            print(f"  Categoría:    {datos['categoria']}")
            print(f"  Precio:       ${datos['precio']:.2f}")
            print(f"  Stock actual: {datos['cantidad']} unidades")
            print(f"  Stock mínimo: {datos['stock_minimo']} unidades")
            print("-" * 50)
            encontrados += 1

    if encontrados == 0:
        print(" No se encontraron productos que coincidan con la búsqueda.")


def eliminar_producto():
    """
    Función para borrar un producto existente.
    Solicita el código del producto y una confirmación explícita antes de eliminarlo.
    """
    print("\n--- ELIMINAR PRODUCTO ---")
    codigo = input("Ingrese el código del producto a eliminar: ").strip().upper()

    if codigo not in inventario:
        print(f" Error: No se encontró ningún producto con el código '{codigo}'.")
        return

    nombre = inventario[codigo]['nombre']
    confirmacion = input(f"¿Está seguro de eliminar '{nombre}'? (Escriba 'S' para confirmar): ").strip().upper()

    if confirmacion == 'S':
        del inventario[codigo]
        print(f" ¡Éxito! El producto '{nombre}' ha sido eliminado.")
        
    else:
        print(" Operación cancelada. El producto no fue eliminado.")


def registrar_entrada():
    """
    Función para aumentar el inventario cuando se recibe nueva mercancía.
    """
    print("\n--- REGISTRAR ENTRADA DE MERCANCÍA ---")
    codigo = input("Ingrese el código del producto: ").strip().upper()

    if codigo not in inventario:
        print(f" Error: El producto con código '{codigo}' no existe.")
        return

    try:
        cantidad = int(input("Ingrese la cantidad que ingresa al almacén: "))
        if cantidad <= 0:
            print(" Error: La cantidad a ingresar debe ser mayor a 0.")
            return
    except ValueError:
        print(" Error: Ingrese un número entero válido.")
        return

    # Sumar la cantidad ingresada al stock actual
    inventario[codigo]['cantidad'] += cantidad
    nuevo_stock = inventario[codigo]['cantidad']
    print(f" ¡Éxito! Se sumaron {cantidad} unidades. Nuevo stock de '{codigo}': {nuevo_stock}")


def registrar_salida():
    """
    Función para reducir el inventario por ventas o salidas.
    Verifica que existan suficientes unidades disponibles antes de restar.
    """
    print("\n--- REGISTRAR SALIDA DE MERCANCÍA ---")
    codigo = input("Ingrese el código del producto: ").strip().upper()

    if codigo not in inventario:
        print(f" Error: El producto con código '{codigo}' no existe.")
        return

    stock_actual = inventario[codigo]['cantidad']

    try:
        cantidad = int(input(f"Cantidad a retirar (Stock disponible: {stock_actual}): "))
        if cantidad <= 0:
            print(" Error: La cantidad a retirar debe ser mayor a 0.")
            return
    except ValueError:
        print(" Error: Ingrese un número entero válido.")
        return

    # Validar que haya suficiente stock
    if cantidad > stock_actual:
        print(f" Error: Stock insuficiente. Disponible: {stock_actual}, Solicitado: {cantidad}.")
        return

    # Restar la cantidad del stock actual
    inventario[codigo]['cantidad'] -= cantidad
    nuevo_stock = inventario[codigo]['cantidad']
    print(f" ¡Éxito! Se retiraron {cantidad} unidades. Nuevo stock de '{codigo}': {nuevo_stock}")


def consultar_poco_stock():
    """
    Función para mostrar reportes de productos con stock bajo
    (aquellos cuya cantidad actual sea menor o igual al stock mínimo configurado).
    """
    print("\n--- ALERTA DE STOCK BAJO ---")
    alertas = 0

    for codigo, datos in inventario.items():
        if datos['cantidad'] <= datos['stock_minimo']:
            print(f"⚠️  [ALERTA] Código: {codigo} | Nombre: {datos['nombre']}")
            print(f"    Stock Actual: {datos['cantidad']} | Stock Mínimo Permitido: {datos['stock_minimo']}")
            print("-" * 50)
            alertas += 1

    if alertas == 0:
        print(" Todos los productos tienen suficiente stock.")


def mostrar_inventario_completo():
    """
    Función auxiliar para mostrar la lista completa de productos registrados.
    """
    print("\n--- LISTA COMPLETA DE INVENTARIO ---")
    if len(inventario) == 0:
        print(" El inventario está vacío.")
        return

    for codigo, datos in inventario.items():
        print(f"[{codigo}] {datos['nombre']} - Cantidad: {datos['cantidad']} | Precio: ${datos['precio']:.2f}")


def ejecutar_menu():
    """
    Función principal que despliega el menú de opciones en pantalla y controla 
    el flujo del programa según la opción elegida por el usuario.
    """
    mantenimiento = True

    while mantenimiento:
        print("\n==============================================")
        print("      SISTEMA DE GESTIÓN DE INVENTARIO        ")
        print("==============================================")
        print("1. Registrar nuevo producto")
        print("2. Buscar producto")
        print("3. Eliminar producto")
        print("4. Registrar entrada de mercancía")
        print("5. Registrar salida de mercancía")
        print("6. Consultar productos con stock bajo")
        print("7. Ver todo el inventario")
        print("8. Salir del sistema")
        print("==============================================")

        opcion = input("Seleccione una opción (1-8): ").strip()

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            buscar_producto()
        elif opcion == "3":
            eliminar_producto()
        elif opcion == "4":
            registrar_entrada()
        elif opcion == "5":
            registrar_salida()
        elif opcion == "6":
            consultar_poco_stock()
        elif opcion == "7":
            mostrar_inventario_completo()
        elif opcion == "8":
            print("\n¡Gracias por utilizar el sistema! Hasta luego.")
            mantenimiento = False
        else:
            print("\n Opción no válida. Por favor, ingrese un número del 1 al 8.")


# Punto de entrada para ejecutar el programa
ejecutar_menu()