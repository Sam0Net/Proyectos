from tkinter import ttk
from tkinter import *
import customtkinter 
import sqlite3

class Product:
    # Conexión con la base de datos 
    db_name = 'database.db'

    def __init__(self, window):
        # Ventana Principal 
        self.wind = window
        self.wind.title('Libros de mi biblioteca') 

        # Creamos un Contenedor 
        frame = LabelFrame(self.wind, text = 'Registrar Nuevo Libro', font=customtkinter.CTkFont(family='Cascadia code'))
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Nombre Input  
        customtkinter.CTkLabel(frame, text = 'Nombre: ', font=customtkinter.CTkFont(family='Cascadia code')).grid(row = 1, column = 0) 
        self.name = customtkinter.CTkEntry(frame, font=customtkinter.CTkFont(family='Cascadia code'))  
        self.name.focus() 
        self.name.grid(row = 1, column = 1)

        # Precio Input
        customtkinter.CTkLabel(frame, text = 'Precio: ', font=customtkinter.CTkFont(family='Cascadia code')).grid(row = 2, column = 0) 
        self.price = customtkinter.CTkEntry (frame, font=customtkinter.CTkFont(family='Cascadia code')) 
        self.price.grid(row = 2, column = 1) 

        # Button Add Product 
        customtkinter.CTkButton(frame, text = 'Guardar Libro', command = self.add_product, corner_radius=50, font=customtkinter.CTkFont(family='Cascadia code')).grid(row = 3, columnspan = 2, sticky = W + E)

        # Mensajes de salida 
        self.message = Label(text = '', fg = 'blue')   
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E) 

        # Tabla 
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER) 

        # Botones 
        customtkinter.CTkButton(master= window, text = 'ELIMINAR', command = self.delete_product, font=customtkinter.CTkFont(family='Cascadia code'), corner_radius=0).grid(row = 5, column = 0, sticky = W + E)
        customtkinter.CTkButton(master= window,text = 'EDITAR', command = self.edit_product, font=customtkinter.CTkFont(family='Cascadia code'), corner_radius=0).grid(row = 5, column = 1, sticky = W + E)

        # Mostrar libros 
        self.get_products()

    # Función de ejecución de consultas a bases de datos 
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Obtener libros de la base de datos 
    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # obtención de datos 
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    # Validación de entradas de usuario 
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation(): 
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters =  (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Libro: {} agregado correctamente'.format(self.name.get()) 
            self.name.delete(0, END)
            self.price.delete(0, END) 
        else:
            self.message['text'] = 'Nombre y precio obligatorios' 
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor, seleccione Libro' 
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Libro: {} eliminado correctamente'.format(name) 
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor, seleccione Libro' 
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Libro' 
        # Old Name
        customtkinter.CTkLabel(self.edit_wind, text = 'Antiguo Nombre:').grid(row = 0, column = 1)
        customtkinter.CTkEntry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        customtkinter.CTkLabel(self.edit_wind, text = 'Nuevo Precio:').grid(row = 1, column = 1)
        new_name = customtkinter.CTkEntry(self.edit_wind)
        new_name.grid(row = 1, column = 2) 

        # Old Price 
        customtkinter.CTkLabel(self.edit_wind, text = 'Antiguo precio:').grid(row = 2, column = 1)
        customtkinter.CTkEntry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # New Price
        customtkinter.CTkLabel(self.edit_wind, text = 'Nuevo Nombre:').grid(row = 3, column = 1)
        new_price= customtkinter.CTkEntry(self.edit_wind) 
        new_price.grid(row = 3, column = 2)

        customtkinter.CTkButton(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop() 

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price,name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Libro: {} actualizado correctamente'.format(name) 
        self.get_products()

if __name__ == '__main__':
    window = customtkinter.CTk() 
    application = Product(window)
    customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue") 
    window.resizable(0,0)
    window.mainloop() 