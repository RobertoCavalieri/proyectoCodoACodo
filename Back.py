import sqlite3

from flask import Flask

DATABASE = 'DATABASE'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Crear la tabla 'productos' si no existe
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            codigo INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        ) ''')


app = Flask(__name__)
# Arreglo para almacenar los productos
productos = []

# Arreglo para almacenar los productos en el carrito de compras
carrito = []


class Producto:
    def __init__(self, codigo, descripcion, cantidad, precio):
        self.codigo = codigo
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio = precio

    def modificar(self, nueva_descripcion, nueva_cantidad, nuevo_precio):
        self.descripcion = nueva_descripcion
        self.cantidad = nueva_cantidad
        self.precio = nuevo_precio


class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, codigo, descripcion, cantidad, precio):
        producto = Producto(codigo, descripcion, cantidad, precio)
        self.productos.append(producto)

    def consultar_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        return None

    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        producto = self.consultar_producto(codigo)
        if producto:
            producto.modificar(nueva_descripcion, nueva_cantidad, nuevo_precio)
            return True
        return False

    def eliminar_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo:
                self.productos.remove(producto)
                print(f"Producto con código {codigo} eliminado.")
                return
        print(f"No se encontró ningún producto con el código {codigo}.")

    def listar_productos(self):
        for producto in self.productos:
            print(
                f"Código: {producto.codigo}, Descripción: {producto.descripcion}, Cantidad: {producto.cantidad}, Precio: {producto.precio}")


class Carrito:
    def __init__(self):
        self.items = []

    def agregar(self, codigo, cantidad, inventario):
        producto = inventario.consultar_producto(codigo)

        if producto is None:
            print(f"El producto con código {codigo} no existe en el inventario.")
            return

        if cantidad > producto.cantidad:
            print(f"No hay suficiente stock del producto con código {codigo}.")
            return

        for item in self.items:
            if item['producto'].codigo == codigo:
                item['cantidad'] += cantidad
                print(f"Se agregaron {cantidad} unidades del producto con código {codigo} al carrito.")
                return

        self.items.append({'producto': producto, 'cantidad': cantidad})
        print(f"Se agregaron {cantidad} unidades del producto con código {codigo} al carrito.")

    def quitar(self, codigo, cantidad):
        for item in self.items:
            if item['producto'].codigo == codigo:
                if cantidad > item['cantidad']:
                    print(
                        f"No se puede quitar una cantidad mayor a la que hay en el carrito para el producto con código {codigo}.")
                    return

                item['cantidad'] -= cantidad

                if item['cantidad'] == 0:
                    self.items.remove(item)
                    print(f"El producto con código {codigo} fue completamente removido del carrito.")
                else:
                    print(f"Se quitaron {cantidad} unidades del producto con código {codigo} del carrito.")

                return

        print(f"No se encontró el producto con código {codigo} en el carrito.")

    def mostrar(self):
        if len(self.items) == 0:
            print("El carrito está vacío.")
        else:
            print("Contenido del carrito:")
            for item in self.items:
                producto = item['producto']
                print(
                    f"Código: {producto.codigo}, Descripción: {producto.descripcion}, Cantidad: {item['cantidad']}, Precio: {producto.precio}")


# Ejemplo de uso
inventario = Inventario()
inventario.agregar_producto(1, "Premium Service", 10, 9.99)
inventario.agregar_producto(2, "Deluxe Service", 5, 19.99)
inventario.listar_productos()


producto = inventario.consultar_producto(1)
if producto:
    producto.modificar("Super premium", 15, 12.99)
    inventario.eliminar_producto(2)

inventario.listar_productos()

if __name__ == '__main__':
    app.run()
