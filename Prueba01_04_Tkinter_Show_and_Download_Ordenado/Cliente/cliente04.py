import asyncio
import websockets
import tkinter as tk
from tkinter import Listbox, messagebox
import os
import threading

async def client(uri, file_request, file_listbox):
    async with websockets.connect(uri, max_size=None) as websocket:
        files_available = await websocket.recv()
        print(files_available)

        # Mostrar la lista de archivos en el Listbox
        file_listbox.delete(0, tk.END)
        files_list = files_available.split(', ')
        for file in files_list:
            file_listbox.insert(tk.END, file)

        await websocket.send(file_request)

        response = await websocket.recv()
        if response == "Archivo no encontrado.":
            print(response)
            messagebox.showinfo("Error", response)
        else:
            downloads_folder = "descargas"
            os.makedirs(downloads_folder, exist_ok=True)

            file_path = os.path.join(downloads_folder, file_request)
            with open(file_path, 'wb') as file:
                file.write(response)
                print(f"Archivo {file_request} recibido y guardado en {downloads_folder}.")
                messagebox.showinfo("Éxito", f"Archivo {file_request} recibido y guardado en {downloads_folder}.")

async def get_file_list(uri, file_listbox):
    async with websockets.connect(uri, max_size=None) as websocket:
        # Recibir la lista de archivos del servidor
        files_available = await websocket.recv()

        # Mostrar la lista de archivos en el Listbox
        file_listbox.delete(0, tk.END)
        files_list = files_available.split(', ')
        for file in files_list:
            file_listbox.insert(tk.END, file)

def connect_to_server(file_listbox):
    server_uri = "ws://localhost:5555"
    file_request = file_entry.get()

    if not file_request:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de archivo.")
        return

    asyncio.run(client(server_uri, file_request, file_listbox))

def connect_to_server2(file_listbox):
    server_uri1 = "ws://localhost:5555"

    # Obtener la lista de archivos en la conexión
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_file_list(server_uri1, file_listbox))

# Función para ejecutar el bucle de eventos de asyncio en un hilo
def asyncio_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Cliente WebSocket")

get_list_button = tk.Button(root, text="Obtener Lista de Archivos", command=lambda: connect_to_server2(file_listbox))
get_list_button.pack(pady=5)

# Crear el Listbox
file_listbox = Listbox(root, selectmode=tk.SINGLE)
file_listbox.pack(pady=10)

label = tk.Label(root, text="Ingrese el nombre del archivo:")
label.pack(pady=10)

file_entry = tk.Entry(root, width=30)
file_entry.pack(pady=10)

connect_button = tk.Button(root, text="Descargar", command=lambda: connect_to_server(file_listbox))
connect_button.pack(pady=10)



# Iniciar el bucle de eventos de asyncio en un hilo separado
asyncio_thread = threading.Thread(target=asyncio_thread, daemon=True)
asyncio_thread.start()

# Botón para obtener la lista de archivos disponibles


# Iniciar el bucle de eventos de Tkinter
root.mainloop()
