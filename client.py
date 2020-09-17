import websockets
import sys
import asyncio
import pickle
import time
import os

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
    #x = sys.argv[3]
    #y = sys.argv[4]
    uri = "ws://"+address+":"+str(port)

    async with websockets.connect(uri) as websocket:
        # vamos serializar os dados a enviar
        
        print ("abrindo arquivo...")
        print(os.path.getsize('projeto_pratico1.pdf'))
        arq = open('projeto_pratico1.pdf','rb')
        
        print ("enviado  arquivo")
        for i in arq:

            # vamos enviar os dados
            await websocket.send(i)
            #tam = i
        #print(f"> {msg}")
        #print(tam)

        # vamos receber dados
        # buffer possui tamanho de 1024 bytes
        #data = await websocket.recv()
        
        # vamos imprimir o resultado
        #print(data)

asyncio.get_event_loop().run_until_complete(hello())


