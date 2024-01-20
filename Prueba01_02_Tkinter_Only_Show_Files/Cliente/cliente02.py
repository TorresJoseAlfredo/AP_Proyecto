import asyncio
import websockets
import tkinter as tk
from tkinter import Listbox, SINGLE, messagebox

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

    # Obtener la lista de archivos en la conexión
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_file_list(server_uri, file_listbox))

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Cliente WebSocket")

# Crear el Listbox
file_listbox = Listbox(root, selectmode=SINGLE)
file_listbox.pack(pady=10)

# Botón para obtener la lista de archivos disponibles
get_list_button = tk.Button(root, text="Obtener Lista de Archivos", command=lambda: connect_to_server(file_listbox))
get_list_button.pack(pady=5)

# Iniciar el bucle de eventos de Tkinter
root.mainloop()
