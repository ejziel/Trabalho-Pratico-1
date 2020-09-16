import websockets
import sys
import asyncio
import pickle
import time

# vamos os parametros passados pela linha de comando: porta
port = int(sys.argv[1])

async def echo(websocket, path):
   # async for message in websocket:

    # vamos esperar o recebimento de dados
    # o buffer possui tamanho 1024 dados
    data = await websocket.recv()

    # vamos desserializar
    x,y = pickle.loads(data)
    
    # vamos esperar 10s antes de enviar o resultado
    print('log: processando...')
    time.sleep(10)

    # vamos calcular o produto
    z = int(x)*int(y)

    print('log: %s x %s = %d'%(x,y,z))

    # vamos serializar o resultado
    msg = pickle.dumps(z)

    await websocket.send(msg)

start_server = websockets.serve(echo, "localhost", port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

print("Esperando..")
