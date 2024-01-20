import asyncio
import websockets
import tkinter as tk
from tkinter import messagebox
import os
import threading

async def client(uri, file_request):
    async with websockets.connect(uri, max_size=None) as websocket:
        files_available = await websocket.recv()
        print(files_available)

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

def connect_to_server():
    server_uri = "ws://localhost:5555"
    file_request = file_entry.get()

    if not file_request:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de archivo.")
        return

    asyncio.run(client(server_uri, file_request))

# Función para ejecutar el bucle de eventos de asyncio en un hilo
def asyncio_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Cliente WebSocket")

label = tk.Label(root, text="Ingrese el nombre del archivo:")
label.pack(pady=10)

file_entry = tk.Entry(root, width=30)
file_entry.pack(pady=10)

connect_button = tk.Button(root, text="Conectar al servidor", command=connect_to_server)
connect_button.pack(pady=10)

# Iniciar el bucle de eventos de asyncio en un hilo separado
asyncio_thread = threading.Thread(target=asyncio_thread, daemon=True)
asyncio_thread.start()

# Iniciar el bucle de eventos de Tkinter
root.mainloop()