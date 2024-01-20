import asyncio
import websockets

async def client(uri):
    async with websockets.connect(uri, max_size=None) as websocket:
        files_available = await websocket.recv()
        print(files_available)

        file_request = input("Ingrese el nombre del archivo que desea ver: ")
        await websocket.send(file_request)

        response = await websocket.recv()
        if response == "Archivo no encontrado.":
            print(response)
        else:
            with open(file_request, 'wb') as file:
                file.write(response)
                print(f"Archivo {file_request} recibido.")

if __name__ == "__main__":
    server_uri = "ws://localhost:5555"

    asyncio.get_event_loop().run_until_complete(client(server_uri))
