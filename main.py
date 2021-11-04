# https://www.youtube.com/watch?v=G7hZlOLhhMY

from fastapi import FastAPI
from routes.answerRoute import answerAPI
from routes.firmRoute import firmAPI
from routes.ipAttackRoute import ipAttackAPI
from routes.userRoute import userAPI

# Instaciando a API
app = FastAPI()
app.include_router(userAPI)
app.include_router(answerAPI)
app.include_router(firmAPI)
app.include_router(ipAttackAPI)

# Abrindo conexão com o Banco de Dados MongoDB (Atlas)
# CONNECTION_STRING = "mongodb+srv://simpleUser:AovgIGUoYKSbpczO@cluster0.ynrb3.mongodb.net/maindb?retryWrites=true&w=majority"
# client = pymongo.MongoClient(CONNECTION_STRING)

# Mensagem de Boas-Vindas


@app.get("/")
def read_root():
    return {"Mensagem": "Boas Vindas!!"}

# Rota auxiliar para conexão com banco de dados

# Listar o nome de todas as empresas que responderam o questionário

# A partir do ID ou NOME da empresa, buscar os formulários de respostas

# Função para mandar as respostas do questionário da respectiva empresa
