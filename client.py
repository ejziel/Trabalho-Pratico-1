import websockets
import sys
import asyncio
import pickle
import time

# este programa exemplifica o envio via TCP de dois numeros x, y para o servidor
# o servidor retorna x*y 


# vamos obter os parametros: endereco, porta, x, y
#address = sys.argv[1]
#port = int(sys.argv[2])
#x = sys.argv[3]
#y = sys.argv[4]

async def hello():
    address = sys.argv[1]
    port = int(sys.argv[2])
    x = sys.argv[3]
    y = sys.argv[4]
    uri = "ws://"+address+":"+str(port)
    async with websockets.connect(uri) as websocket:
        # vamos serializar os dados a enviar
        msg = pickle.dumps((x,y))

        # vamos enviar os dados
        await websocket.send(msg)
        #print(f"> {msg}")

        # vamos receber dados
        # buffer possui tamanho de 1024 bytes
        data = await websocket.recv()
        
        # vamos desserializar os dados
        z = pickle.loads(data)

        # vamos imprimir o resultado
        print('%s*%s = %d'%(x,y,z))

asyncio.get_event_loop().run_until_complete(hello())


