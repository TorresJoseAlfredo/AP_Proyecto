import asyncio
import websockets
import os

async def handle_client(websocket, path):
    try:
        file_list = get_file_list()
        await websocket.send(f"Archivos disponibles: {', '.join(file_list)}")

        request = await websocket.recv()
        if request in file_list:
            file_path = os.path.join("archivos", request)
            with open(file_path, 'rb') as file:
                data = file.read()
                await websocket.send(data)
        else:
            await websocket.send("Archivo no encontrado.")
    except websockets.exceptions.ConnectionClosedOK:
        pass  # La conexión se cerró de manera ordenada

    print(f"Conexión cerrada con {websocket.remote_address}.")

async def server(websocket, path):
    print(f"Conexión establecida desde: {websocket.remote_address}")
    await handle_client(websocket, path)

def get_file_list():
    folder_path = "archivos"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    files = [f for f in os.listdir(folder_path)]
    return files

if __name__ == "__main__":
    start_server = websockets.serve(server, "localhost", 5555, max_size=None)

    print("Servidor esperando conexiones...")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
