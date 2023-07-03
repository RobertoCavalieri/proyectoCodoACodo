import sqlite3
from flask import Flask, jsonify


# Verificar la versión de SQLite
print(sqlite3.sqlite_version)
DATABASE = 'inventario.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            codigo INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def create_database():
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()


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
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def agregar_producto(self, codigo, descripcion, cantidad, precio):
        producto_existente = self.consultar_producto(codigo)
        if producto_existente:
            return jsonify({'message': 'Ya existe un producto con ese código.'}), 400
        nuevo_producto = Producto(codigo, descripcion, cantidad, precio)
        sql = 'INSERT INTO productos VALUES (?, ?, ?, ?)'
        self.cursor.execute(sql, (codigo, descripcion, cantidad, precio))
        self.conexion.commit()
        return jsonify({'message': 'Producto agregado correctamente.'}), 200

    def consultar_producto(self, codigo):
        sql = 'SELECT * FROM productos WHERE codigo = ?'
        self.cursor.execute(sql, (codigo,))
        row = self.cursor.fetchone()
        if row:
            return Producto(row['codigo'], row['descripcion'], row['cantidad'], row['precio'])
        return None

    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        producto = self.consultar_producto(codigo)
        if producto:
            producto.modificar(nueva_descripcion, nueva_cantidad, nuevo_precio)
            sql = 'UPDATE productos SET descripcion = ?, cantidad = ?, precio = ? WHERE codigo = ?'
            self.cursor.execute(sql, (nueva_descripcion, nueva_cantidad, nuevo_precio, codigo))
            self.conexion.commit()
            return True
        return False

    def eliminar_producto(self, codigo):
        sql = 'DELETE FROM productos WHERE codigo = ?'
        self.cursor.execute(sql, (codigo,))
        self.conexion.commit()

    def listar_productos(self):
        sql = 'SELECT * FROM productos'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for row in rows:
            producto = Producto(row['codigo'], row['descripcion'], row['cantidad'], row['precio'])
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


app = Flask(__name__)
carrito = Carrito()
inventario = Inventario()


@app.route('/productos/<int:codigo>', methods=['GET'])
def obtener_producto(codigo):
    producto = inventario.consultar_producto(codigo)
    if producto:
        return jsonify({
            'codigo': producto.codigo,
            'descripcion': producto.descripcion,
            'cantidad': producto.cantidad,
            'precio': producto.precio
        }), 200
    return jsonify({'message': 'Producto no encontrado.'}), 404


@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    return carrito.mostrar()


if __name__ == '__main__':
    create_database()
    app.run()
