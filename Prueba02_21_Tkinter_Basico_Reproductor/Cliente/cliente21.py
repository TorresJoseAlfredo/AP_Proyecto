import asyncio
import websockets
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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

def get_file_list(uri, file_listbox):
    async def get_list():
        async with websockets.connect(uri, max_size=None) as websocket:
            files_available = await websocket.recv()
            file_listbox.delete(0, tk.END)
            file_listbox.insert(tk.END, *files_available.split(', '))

    asyncio.run(get_list())

def connect_to_server(file_listbox, file_entry):
    server_uri = "ws://localhost:5555"
    file_request = file_entry.get()

    if not file_request:
        messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de archivo.")
        return

    asyncio.run(download_file(server_uri, file_request, file_listbox))

def on_listbox_select(event, file_listbox, file_entry):
    selected_index = file_listbox.curselection()

    if selected_index:
        selected_option = file_listbox.get(selected_index[0])
        file_entry.delete(0, tk.END)
        file_entry.insert(0, selected_option)

def drop(event, dummy_label):
    file_paths = event.data
    for file_path in file_paths:
        print(f"File dropped: {file_path}")
        # Implement the logic for playing the dropped file
        # For now, let's just print the dropped file path

def browse_file():
    file_paths = filedialog.askopenfilenames(filetypes=[("Audio/Video Files", "*.mp3;*.mp4;*.avi;*.mkv")])
    if file_paths:
        for file_path in file_paths:
            print(f"Archivo seleccionado: {file_path}")
            # Implement the logic for playing the selected file
            # For now, let's just print the selected file path

# Create the GUI
root = tk.Tk()
root.title("Cliente WebSocket")

style = ttk.Style()
style.configure("TButton", padding=5, relief="flat", background="#000000", foreground="BLACK")
style.configure("TLabel", padding=5, background="#f0f0f0")
style.configure("TEntry", padding=5, relief="flat")

get_list_button = ttk.Button(root, text="Obtener Lista de Archivos", command=lambda: get_file_list("ws://localhost:5555", file_listbox))
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

# Reproductor de audio y video
player_frame = ttk.Frame(root, padding=10)
player_frame.pack(side=tk.RIGHT, padx=10, pady=10)

play_button = ttk.Button(player_frame, text="Reproducir", command=browse_file)
play_button.pack(pady=5)

# Create a dummy label for drag-and-drop
dummy_label = ttk.Label(player_frame, text="Arrastra y suelta aquí", background="lightgray", padx=10, pady=10)
dummy_label.pack(pady=20)

# Bind the drop event to the dummy label
dummy_label.bind("<Button-1>", lambda event: drop(event, dummy_label))
dummy_label.drop_target_register(tk.DND_FILES)
dummy_label.dnd_bind('<<Drop>>', lambda event: drop(event, dummy_label))

root.mainloop()
