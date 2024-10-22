from menu import Menu, Option, MenuCallable

inventario = {}


def agregar_item(nombre: str, item: str):
    if nombre in inventario:
        raise ValueError("El item ya existe")
    inventario[nombre] = item


def eliminar_item(nombre: str):
    inventario.pop(nombre)


def modificar_item(nombre: str, nuevo_item: str):
    if nombre not in inventario:
        raise ValueError("El item no existe")
    inventario[nombre] = nuevo_item


def obtener_item(nombre: str):
    return inventario[nombre]


show_menu = Menu(
    main_text=["Bienvenido al inventario", "¿Que se le ofrece el dia de hoy?"],
    expects_input=True,
    options=[
        Option(
            option_message="1) Agregar item",
            menu_callable=MenuCallable(
                input_options=["1"],
                func_call=agregar_item,
                request_input={"nombre": "Ingrese el nombre del item", "item": "Ingrese el item"}
            )
        ),
        Option(
            option_message="2) Eliminar item",
            menu_callable=MenuCallable(
                input_options=["2"],
                func_call=eliminar_item,
                request_input={"nombre": "Ingrese el nombre del item"}
            )
        ),
        Option(
            option_message="3) Modificar item",
            menu_callable=MenuCallable(
                input_options=["3"],
                func_call=modificar_item,
                request_input={"nombre": "Ingrese el nombre del item"}
            )
        ),
        Option(
            option_message="4) Obtener item",
            menu_callable=MenuCallable(
                input_options=["4"],
                func_call=obtener_item,
                request_input={"nombre": "Ingrese el nombre del item"},
                print_result=True
            )
        )
    ],
    exit_option=Option(option_message="5) Salir", menu_callable=MenuCallable(input_options=["5"])),
    loop_menu=True
)

show_menu()
