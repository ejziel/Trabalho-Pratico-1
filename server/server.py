import websockets
import sys
import asyncio
import pickle
import time
import tqdm


# vamos os parametros passados pela linha de comando: porta
port = int(sys.argv[1])

async def echo(websocket, path):
    print("recebendo o arquivo...")
    arq = open('File_ouputt.pdf','wb')

    while True:

        # vamos esperar o recebimento de dados
        data = await websocket.recv()

        #print('log: processando...')

        if not data:
            break
        arq.write(data)

    #msg = 1

    #await websocket.send(msg)

    print("Done")
    arq.close()

start_server = websockets.serve(echo, "localhost", port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

print("Esperando..")
