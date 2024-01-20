import asyncio
import websockets
import tkinter as tk
from tkinter import ttk, messagebox
import os

async def download_file(uri, file_request, file_listbox):
    async with websockets.connect(uri, max_size=None) as websocket:
        files_available = await websocket.recv()

        file_listbox.delete(0, tk.END)
        files_list = files_available.split(', ')
        file_listbox.insert(tk.END, *files_list)

        if file_request not in files_list:
            messagebox.showinfo("Error", "Archivo no encontrado.")
            return

        await websocket.send(file_request)
        response = await websocket.recv()

        downloads_folder = "descargas"
        os.makedirs(downloads_folder, exist_ok=True)
        file_path = os.path.join(downloads_folder, file_request)

        with open(file_path, 'wb') as file:
            file.write(response)

        print(f"Archivo {file_request} recibido y guardado en {downloads_folder}.")
        messagebox.showinfo("Éxito", f"Archivo {file_request} recibido y guardado en {downloads_folder}.")

async def get_file_list(uri, file_listbox):
    async with websockets.connect(uri, max_size=None) as websocket:
        files_available = await websocket.recv()
        file_listbox.delete(0, tk.END)
        file_listbox.insert(tk.END, *files_available.split(', '))

def connect_to_server(file_listbox, file_entry):
    server_uri = "ws://localhost:5555"
    file_request = file_entry.get()

    if not file_request:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de archivo.")
        return

    asyncio.run(download_file(server_uri, file_request, file_listbox))

def connect_to_server2(file_listbox):
    server_uri = "ws://localhost:5555"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_file_list(server_uri, file_listbox))

def on_listbox_select(event, file_listbox, file_entry):
    selected_index = file_listbox.curselection()

    if selected_index:
        selected_option = file_listbox.get(selected_index[0])
        file_entry.delete(0, tk.END)
        file_entry.insert(0, selected_option)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Cliente WebSocket")

style = ttk.Style()
style.configure("TButton", padding=5, relief="flat", background="#000000", foreground="BLACK")
style.configure("TLabel", padding=5, background="#f0f0f0")
style.configure("TEntry", padding=5, relief="flat")

get_list_button = ttk.Button(root, text="Obtener Lista de Archivos", command=lambda: connect_to_server2(file_listbox))
get_list_button.pack(pady=5)

file_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=5, width=40)
file_listbox.pack(pady=10)
file_listbox.bind("<<ListboxSelect>>", lambda event: on_listbox_select(event, file_listbox, file_entry))

label = ttk.Label(root, text="Ingrese el nombre del archivo:")
label.pack(pady=10)

file_entry = ttk.Entry(root, width=30)
file_entry.pack(pady=10)

connect_button = ttk.Button(root, text="Descargar", command=lambda: connect_to_server(file_listbox, file_entry))
connect_button.pack(pady=10)

root.mainloop()
