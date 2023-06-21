import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date


# Conectar a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost", port="3306", database="articulos", user="root", password=""
)
cursor = conexion.cursor()


# Función para validar la existencia de un SKU en la base de datos
def validar_existencia_sku(sku):
    consulta = "SELECT COUNT(*) FROM tabla_datos WHERE sku = %s"
    cursor.execute(consulta, (sku,))
    count = cursor.fetchone()[0]
    return count > 0


# Función para obtener los datos de un SKU existente
def obtener_datos_sku(sku):
    consulta = "SELECT articulo, marca, modelo, departamento, clase, familia, fecha_alta, stock, cantidad, descontinuado, fecha_baja FROM tabla_datos WHERE sku = %s"
    cursor.execute(consulta, (sku,))
    datos = cursor.fetchone()
    return datos


# Función para insertar datos en la tabla_datos
def insertar_datos(
    sku, articulo, marca, modelo, departamento, clase, familia, stock, cantidad, descontinuado
):
    fecha_actual = date.today()
    descontinuado = 0
    fecha_baja = date(1900, 1, 1)
    consulta = "INSERT INTO tabla_datos (sku, articulo, marca, modelo, departamento, clase, familia, fecha_alta, stock, cantidad, descontinuado, fecha_baja) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    datos = (
        sku,
        articulo,
        marca,
        modelo,
        departamento,
        clase,
        familia,
        fecha_actual,
        stock,
        cantidad,
        descontinuado,
        fecha_baja,
    )
    cursor.execute(consulta, datos)
    conexion.commit()
    messagebox.showinfo("Guardado", "Los datos han sido guardados exitosamente.")


# Función para eliminar un SKU de la tabla_datos
def eliminar_sku(sku):
    confirmacion = messagebox.askyesno(
        "Confirmación", "¿Estás seguro de que deseas eliminar este SKU?"
    )
    if confirmacion:
        consulta = "DELETE FROM tabla_datos WHERE sku = %s"
        cursor.execute(consulta, (sku,))
        conexion.commit()
        messagebox.showinfo("Eliminado", "El SKU ha sido eliminado exitosamente.")


# Función para actualizar datos en la tabla_datos
def actualizar_datos(
    sku,
    articulo,
    marca,
    modelo,
    departamento,
    clase,
    familia,
    cantidad,
    stock,
    descontinuado,
):
    consulta = "UPDATE tabla_datos SET articulo = %s, marca = %s, modelo = %s, departamento = %s, clase = %s, familia = %s, cantidad = %s, stock = %s, descontinuado = %s WHERE sku = %s"
    datos = (
        articulo,
        marca,
        modelo,
        departamento,
        clase,
        familia,
        cantidad,
        stock,
        descontinuado,
        sku,
    )
    cursor.execute(consulta, datos)
    conexion.commit()
    messagebox.showinfo("Actualizado", "Los datos han sido actualizados exitosamente.")


# Función para obtener las clases de un departamento
def obtener_clases(departamento):
    consulta = "SELECT clase FROM tabla_clases WHERE departamento = %s"
    cursor.execute(consulta, (departamento,))
    clases = cursor.fetchall()
    clases = [c[0] for c in clases]
    return clases


# Función para obtener las familias de un departamento y clase
def obtener_familias(departamento, clase):
    consulta = (
        "SELECT familia FROM tabla_familias WHERE departamento = %s AND clase = %s"
    )
    cursor.execute(consulta, (departamento, clase))
    familias = cursor.fetchall()
    familias = [f[0] for f in familias]
    return familias


# Función para manejar el evento del botón Guardar
# ...

def guardar_datos():
    sku = sku_entry.get()

    # Validar si el SKU es un número de 6 dígitos
    if not sku.isdigit() or len(sku) != 6:
        messagebox.showerror("Error", "El SKU debe ser un número de 6 dígitos.")
        return

    if validar_existencia_sku(sku):
        messagebox.showerror("Error", "El SKU ya existe en la base de datos.")
        return

    articulo = articulo_entry.get()

    # Validar la longitud del artículo
    if len(articulo) > 15:
        messagebox.showerror("Error", "El artículo debe tener máximo 15 caracteres.")
        return

    marca = marca_entry.get()

    # Validar la longitud de la marca
    if len(marca) > 15:
        messagebox.showerror("Error", "La marca debe tener máximo 15 caracteres.")
        return
    

    modelo = modelo_entry.get()

    # Validar la longitud del modelo
    if len(modelo) > 20:
        messagebox.showerror("Error", "El modelo debe tener máximo 20 caracteres.")
        return

    departamento = departamento_entry.get()

    # Validar si el departamento es un número de 1 dígito
    if not departamento.isdigit() or len(departamento) != 1:
        messagebox.showerror("Error", "El departamento debe ser un número de 1 dígito.")
        return
    


    clase = clase_entry.get()

    # Validar si la clase es un número de 2 dígitos
    if not clase.isdigit() or len(clase) != 2:
        messagebox.showerror("Error", "La clase debe ser un número de 2 dígitos.")
        return

    familia = familia_entry.get()

    # Validar si la familia es un número de 3 dígitos
    if not familia.isdigit() or len(familia) != 3:
        messagebox.showerror("Error", "La familia debe ser un número de 3 dígitos.")
        return

    stock = stock_entry.get()

    # Validar si el stock es un número y no excede la longitud máxima
    if not stock.isdigit():
        messagebox.showerror("Error", "El valor del stock debe ser un número.")
        return

    if len(stock) > 9:
        messagebox.showerror("Error", "La longitud máxima del stock es de 9 dígitos.")
        return

    cantidad = cantidad_entry.get()

    # Validar si la cantidad es un número de hasta 5 dígitos
    if not cantidad.isdigit() or len(cantidad) > 5:
        messagebox.showerror("Error", "La cantidad debe ser un número de hasta 5 dígitos.")
        return

    descontinuado = descontinuado_entry.get()

    # Validar si el campo descontinuado es una opción válida
    if descontinuado not in ["S", "N"]:
        messagebox.showerror("Error", "El campo descontinuado debe ser 'S' o 'N'.")
        return

    # Guardar los datos en la base de datos
    insertar_datos(sku, articulo, marca, modelo, departamento, clase, familia, stock, cantidad, descontinuado)
    messagebox.showinfo("Éxito", "Los datos se han guardado correctamente.")



# Función para manejar el evento del botón Eliminar
def eliminar_datos():
    sku = sku_entry.get()
    if not validar_existencia_sku(sku):
        messagebox.showerror("Error", "El SKU no existe en la base de datos.")
        return

    eliminar_sku(sku)


# Función para manejar el evento del botón Actualizar
def actualizar_datos_sku():
    sku = sku_entry.get()
    if not validar_existencia_sku(sku):
        messagebox.showerror("Error", "El SKU no existe en la base de datos.")
        return

    descontinuado = descontinuado_entry.get()

    # Validar si el campo descontinuado es un número de 1 dígito
    if not descontinuado.isdigit() or len(descontinuado) != 1:
        messagebox.showerror("Error", "El valor de Descontinuado debe ser un número de 1 dígito.")
        return

    articulo = articulo_entry.get()
    marca = marca_entry.get()
    modelo = modelo_entry.get()
    departamento = departamento_entry.get()
    clase = clase_entry.get()
    familia = familia_entry.get()
    cantidad = cantidad_entry.get()
    stock = stock_entry.get()
    descontinuado = descontinuado_entry.get()

    actualizar_datos(
        sku,
        articulo,
        marca,
        modelo,
        departamento,
        clase,
        familia,
        cantidad,
        stock,
        descontinuado,
    )



  

# Función para manejar el evento del botón Consultar
def consultar_datos():
    sku = sku_entry.get()
    if not validar_existencia_sku(sku):
        messagebox.showerror("Error", "El SKU no existe en la base de datos.")
        return

    datos = obtener_datos_sku(sku)
    articulo_entry.delete(0, tk.END)
    marca_entry.delete(0, tk.END)
    modelo_entry.delete(0, tk.END)
    departamento_entry.delete(0, tk.END)
    clase_entry.delete(0, tk.END)
    familia_entry.delete(0, tk.END)
    fecha_alta_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)
    cantidad_entry.delete(0, tk.END)
    descontinuado_entry.delete(0, tk.END)
    fecha_baja_entry.delete(0, tk.END)

    articulo_entry.insert(tk.END, datos[0])
    marca_entry.insert(tk.END, datos[1])
    modelo_entry.insert(tk.END, datos[2])
    departamento_entry.insert(tk.END, datos[3])
    clase_entry.insert(tk.END, datos[4])
    familia_entry.insert(tk.END, datos[5])
    fecha_alta_entry.insert(tk.END, datos[6])
    stock_entry.insert(tk.END, datos[7])
    cantidad_entry.insert(tk.END, datos[8])
    descontinuado_entry.insert(tk.END, datos[9])
    fecha_baja_entry.insert(tk.END, datos[10])

#limpiar formularios
def limpiar_datos():
    
    sku_entry.delete(0,tk.END)
    articulo_entry.delete(0, tk.END)
    marca_entry.delete(0, tk.END)
    modelo_entry.delete(0, tk.END)
    departamento_entry.delete(0, tk.END)
    clase_entry.delete(0, tk.END)
    familia_entry.delete(0, tk.END)
    fecha_alta_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)
    cantidad_entry.delete(0, tk.END)
    descontinuado_entry.delete(0, tk.END)
    fecha_baja_entry.delete(0, tk.END)



# Crear la ventana de la interfaz
ventana = tk.Tk()
ventana.title("Interfaz de Artículos")

# Crear los elementos de la interfaz
sku_label = tk.Label(ventana, text="SKU:")
sku_entry = tk.Entry(ventana)

articulo_label = tk.Label(ventana, text="Artículo:")
articulo_entry = tk.Entry(ventana)

marca_label = tk.Label(ventana, text="Marca:")
marca_entry = tk.Entry(ventana)

modelo_label = tk.Label(ventana, text="Modelo:")
modelo_entry = tk.Entry(ventana)

departamento_label = tk.Label(ventana, text="Departamento:")
departamento_entry = tk.Entry(ventana)

clase_label = tk.Label(ventana, text="Clase:")
clase_entry = tk.Entry(ventana)

familia_label = tk.Label(ventana, text="Familia:")
familia_entry = tk.Entry(ventana)

fecha_alta_label = tk.Label(ventana, text="Fecha de Alta:")
fecha_alta_entry = tk.Entry(ventana)
fecha_alta_entry.insert(tk.END, date.today())

stock_label = tk.Label(ventana, text="Stock:")
stock_entry = tk.Entry(ventana)

cantidad_label = tk.Label(ventana, text="Cantidad:")
cantidad_entry = tk.Entry(ventana)

descontinuado_label = tk.Label(ventana, text="Descontinuado:")
descontinuado_entry = tk.Entry(ventana)
descontinuado_entry.insert(tk.END, 0)

fecha_baja_label = tk.Label(ventana, text="Fecha de Baja:")
fecha_baja_entry = tk.Entry(ventana)
fecha_baja_entry.insert(tk.END, date(1900, 1, 1))

guardar_button = tk.Button(ventana, text="Guardar", command=guardar_datos)
eliminar_button = tk.Button(ventana, text="Eliminar", command=eliminar_datos)
actualizar_button = tk.Button(ventana, text="Actualizar", command=actualizar_datos_sku)
consultar_button = tk.Button(ventana, text="Consultar", command=consultar_datos)
limpiar_datos = tk.Button(ventana, text="Limpiar", command=limpiar_datos)

# Posicionar los elementos en la interfaz
sku_label.grid(row=0, column=0)
sku_entry.grid(row=0, column=1)

articulo_label.grid(row=1, column=0)
articulo_entry.grid(row=1, column=1)

marca_label.grid(row=2, column=0)
marca_entry.grid(row=2, column=1)

modelo_label.grid(row=3, column=0)
modelo_entry.grid(row=3, column=1)

departamento_label.grid(row=4, column=0)
departamento_entry.grid(row=4, column=1)

clase_label.grid(row=5, column=0)
clase_entry.grid(row=5, column=1)

familia_label.grid(row=6, column=0)
familia_entry.grid(row=6, column=1)

fecha_alta_label.grid(row=7, column=0)
fecha_alta_entry.grid(row=7, column=1)

stock_label.grid(row=8, column=0)
stock_entry.grid(row=8, column=1)

cantidad_label.grid(row=9, column=0)
cantidad_entry.grid(row=9, column=1)

descontinuado_label.grid(row=10, column=0)
descontinuado_entry.grid(row=10, column=1)

fecha_baja_label.grid(row=11, column=0)
fecha_baja_entry.grid(row=11, column=1)

guardar_button.grid(row=12, column=0)
eliminar_button.grid(row=12, column=1)
actualizar_button.grid(row=12, column=2)
consultar_button.grid(row=12, column=3)
limpiar_datos.grid(row=12, column=4)
# Iniciar el bucle de eventos de la interfaz
ventana.mainloop()
