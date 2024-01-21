
import asyncio
import websockets
import os
import json
import logging

async def handle_client(websocket, path):
    try:
        # Inicializar la lista de archivos
        file_list = get_file_list()

        while True:
            request = await websocket.recv()
            if not request:
                break  # Salir si el cliente cierra la conexión

            # Decodificar el mensaje JSON enviado por el cliente
            try:
                request_data = json.loads(request)
                action = request_data.get("action")
            except json.JSONDecodeError:
                await websocket.send("Error: Mensaje no válido.")
                continue

            if action == "get_file_list":
                # Enviar la lista de archivos al cliente
                await websocket.send(json.dumps({"files": file_list}))
            elif action == "download_file":
                # Descargar el archivo solicitado por el cliente
                file_request = request_data.get("file_request")

                # Volver a obtener la lista de archivos antes de verificar la solicitud
                file_list = get_file_list()

                if file_request and file_request in file_list:
                    file_path = os.path.join("archivos", file_request)

                    # Enviar el archivo en bloques de 64 KB
                    with open(file_path, 'rb') as file:
                        chunk_size = 64 * 1024  # 64 KB
                        while True:
                            data_chunk = file.read(chunk_size)
                            if not data_chunk:
                                break
                            await websocket.send(data_chunk)
                else:
                    await websocket.send("Archivo no encontrado.")
            elif action == "exit":
                break  # Salir si el cliente envía 'exit'
            else:
                await websocket.send(f"Error: Acción desconocida '{action}'.")

    except websockets.exceptions.ConnectionClosedOK:
        pass  # La conexión se cerró de manera ordenada

    print(f"Conexión cerrada con {websocket.remote_address}.")

def get_file_list():
    folder_path = "archivos"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    files = [f for f in os.listdir(folder_path)]
    return files

if __name__ == "__main__":
    start_server = websockets.serve(handle_client, "localhost", 5555, max_size=None)

    print("Servidor esperando conexiones...")

    logging.basicConfig(level=logging.DEBUG)  # Agrega esta línea para logs
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
