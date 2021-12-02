from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from authentication.oaut2 import get_current_user
from conf.db import client
from bson import ObjectId
import numpy as np

from models.answerModel import Answer
from schemas.answerSchema import answerEntity, answersEntity

answerAPI = APIRouter(tags=['Answer'])

questionsList = ["rec","arm","ent","exp","ins","com","aca","inft","infm","dad",]

@answerAPI.get('/getAllAnswers')
# Get all answer to database
async def getAllAnswers():
    return answersEntity(client.maindb.answer.find())


@answerAPI.get('/getAnswers/{value}')
# Get all answer to database by value (cnpj or date)
async def getAnswers(value):
    if value.isnumeric():
        if not client.maindb.firm.find_one({"cnpj": value}):
            raise HTTPException(status_code=404, detail="Firm not found")
        return answersEntity(client.maindb.answer.find({"firm": str(value)}))
    else:
        resultByDate = answersEntity(client.maindb.answer.find({"date": str(value)}))
        if not resultByDate:
            raise HTTPException(status_code=404, detail="Answers by date not found")
        else:
            return resultByDate


@answerAPI.get('/getScoreFirmByQuestion/{firm}/{quest}')
# Get all answers in especific question
async def getScoreAnswersByQuestion(firm,quest):
    try:
        if not client.maindb.firm.find_one({"cnpj": firm}):
            raise HTTPException(status_code=404, detail="Firm not found")
    except:
        raise HTTPException(status_code=404, detail="Invalid CNPJ")

    n=client.maindb.answer.find({"firm": str(firm)}).count()

    if quest not in questionsList:
        raise HTTPException(status_code=404, detail="Quest not found")
    if quest == "rec" or quest == "ent":
        sumResult = list(np.zeros(5))
    elif quest == "inft":
        sumResult = list(np.zeros(4))
    else:
        sumResult = list(np.zeros(3))
    for doc in client.maindb.answer.find({"firm": str(firm)},{quest:1}):
        sumResult = [ (a + b) for a, b in zip(sumResult, doc[quest]['answers']) ]

    sumResult = list(map(lambda x: x/n, sumResult))

    return sumResult


@answerAPI.get('/getScoreFirmTotal/{firm}')
# pergar todas as respostas, somar o valor e partir da quantidade
# que possui (relacionados a firma) dividir e obter a média
# da pontuação
async def getScoreTotal(firm):
    try:
        if not client.maindb.firm.find_one({"cnpj": firm}):
            raise HTTPException(status_code=404, detail="Firm not found")
    except:
        raise HTTPException(status_code=404, detail="Invalid CNPJ")

    answers = answersEntity(client.maindb.answer.find({"firm": str(firm)}))

    if not answers:
        raise HTTPException(status_code=404, detail="Doesn't has answers")

    n = client.maindb.answer.find({"firm": str(firm)}).count()
    
    dictAux = {
        "firm": str(firm),
        "rec":{
            "title": "Reconhecimento",
            "answers":[0,0,0,0,0],
            "sumAnswers":0
        },
        "arm":{
            "title": "Armamento",
            "answers":[0,0,0],
            "sumAnswers":0
        },
        "ent":{
            "title": "Entrega",
            "answers":[0,0,0,0,0],
            "sumAnswers":0
        },
        "exp":{
            "title": "Exploracao",
            "answers":[0,0,0],
            "sumAnswers":0
        },
        "ins":{
            "title": "Instalacao",
            "answers":[0,0,0],
            "sumAnswers":0
        },
        "com":{
            "title": "ComandoControle",
            "answers":[0,0,0],
            "sumAnswers":0
        },
        "aca":{
            "title": "AcaoObjetivo",
            "answers":[0,0,0],
            "sumAnswers":0
        },
        "inft":{
            "title": "Infraestrutura",
            "answers":[0,0,0,0],
            "sumAnswers":0
        },
        "infm":{
            "title": "informacao",
            "answers":[0,0,0],
            "sumAnswers":0
        },
        "dad":{
            "title": "Dados",
            "answers":[0,0,0]   ,
            "sumAnswers":0
        }
    }
    
    for doc in answers:
        for item in doc:
            if item == "id" or item == "firm" or item == "date":
                pass
            else:
                dictAux[item]['answers'] = [ (a + b) for a, b in zip(dictAux[item]['answers'], doc[item]['answers']) ]
            
    for item in dictAux:
        if item != "firm":
            dictAux[item]['answers'] = list(map(lambda x: x/n, dictAux[item]['answers']))
            dictAux[item]['sumAnswers']  = sum(dictAux[item]['answers'])

    return dictAux


@answerAPI.get('/getScoreByQuestionSum/{firm}')
# pergar a questão específica de todas as respostas
# para somar e dividir pela quantidade dela (média)
async def getScoreByQuestionSum(firm):
    dictAux = {
    "firm": firm,
    "score_total": 0
    }

    try:
        if not client.maindb.firm.find_one({"cnpj": firm}):
            raise HTTPException(status_code=404, detail="Firm not found")
    except:
        raise HTTPException(status_code=404, detail="Invalid CNPJ")
    
    answers = answersEntity(client.maindb.answer.find({"firm": str(firm)}))

    if not answers:
        raise HTTPException(status_code=200, detail="Doesn't has answers")
    
    n = client.maindb.answer.find({"firm": str(firm)}).count()
    
    for doc in answers:
        for item in doc:
            if item == "id" or item == "firm" or item == "date":
                pass
            else:
                dictAux["score_total"] += sum(doc[item]['answers'])

    dictAux["score_total"] = float(dictAux["score_total"]/n)
    return dictAux


@answerAPI.get('/getComments/{firm}')
# Get all comments
async def getComments(firm):
    try:
        if not client.maindb.firm.find_one({"cnpj": firm}):
            raise HTTPException(status_code=404, detail="Firm not found")
    except:
        raise HTTPException(status_code=404, detail="Invalid CNPJ")

    answers = answersEntity(client.maindb.answer.find({"firm": str(firm)}))

    if not answers:
        raise HTTPException(status_code=404, detail="Doesn't has answers")

    n = client.maindb.answer.find({"firm": str(firm)}).count()

    dictAuxFinal ={
        "firm": firm,
        "comments":[]
    }
    
    listComments = []

    dictAux = {
        "firm": str(firm),
        "rec":{
            "title": "Reconhecimento",
            "answers":[0,0,0,0,0]
        },
        "arm":{
            "title": "Armamento",
            "answers":[0,0,0]
        },
        "ent":{
            "title": "Entrega",
            "answers":[0,0,0,0,0]
        },
        "exp":{
            "title": "Exploracao",
            "answers":[0,0,0]
        },
        "ins":{
            "title": "Instalacao",
            "answers":[0,0,0]
        },
        "com":{
            "title": "ComandoControle",
            "answers":[0,0,0]
        },
        "aca":{
            "title": "AcaoObjetivo",
            "answers":[0,0,0]
        },
        "inft":{
            "title": "Infraestrutura",
            "answers":[0,0,0,0]
        },
        "infm":{
            "title": "informacao",
            "answers":[0,0,0]
        },
        "dad":{
            "title": "Dados",
            "answers":[0,0,0]   
        }
    }
    
    for doc in answers:
        for item in doc:
            if item == "id" or item == "firm" or item == "date":
                pass
            else:
                dictAux[item]['answers'] = [ (a + b) for a, b in zip(dictAux[item]['answers'], doc[item]['answers']) ]
            
    listComments.append({"id":"1","code":"rec3","utterance":"Seu e-mail de trabalho é o mesmo pessoal?","idealAnswer":"Não","comment":"É ideal utilizar o email corporativos e não pessoais pois podem estar contaminados com spams e e-mails mal intencionados deixando a rede interna da empresa suscetível a ataques. Por isso, criar um email corporativo é a melhor forma de evitar estes problemas."}) if ((dictAux["rec"]['answers'][2]/n) < (3*70/100)) else None
    listComments.append({"id":"1","code":"rec4","utterance":"Você utiliza as senhas pessoais para softwares do local de trabalho?","idealAnswer":"Não","comment":"O ideal é que se tenha senha diferentes para cada tipo de acesso para aumentar a segurança de aplicativos e inclusive evitar invasões dos próprios dados pessoais e dos dados das empresas.Aconselha-se que notifique os funcionários para que mudem as senhas para deixar a segurança maior."}) if ((dictAux["rec"]['answers'][3]/n) < (3*70/100)) else None
    listComments.append({"id":"2","code":"arm1","utterance":"O laboratório possui uma equipe de TI?","idealAnswer":"Não","comment":"Deve-se atentar neste ponto pois a equipe de TI deve existir e estar disponível para auxílio das outras áreas da empresa.Aconselha-se que identifique a razão da equipe de TI seja pouco vista ou caso não exista uma equipe contratá-la."}) if ((dictAux["arm"]['answers'][0]/n) < (7*70/100)) else None
    listComments.append({"id":"3","code":"ent1","utterance":"Durante a entrega de exames é comum permitir que clientes usem seus pendrives para entregar informações no laboratório?","idealAnswer":"Não","comment":"Permitir que pendrives não autorizados sejam conectados a computadores na rede da empresa cria um risco a empresa por serem uma forma de transmissão direta de malwares.Aconselha-se que as informações de exames sejam entregues fisicamente ou caso não seja possível, enviadas por e-mail do paciente ou da empresa que prestou o exame."}) if ((dictAux["ent"]['answers'][0]/n) < (7*70/100)) else None
    listComments.append({"id":"3","code":"ent2","utterance":"Você utiliza seus pendrives particulares para enviar arquivos para computadores ligados à rede da empresa?","idealAnswer":"Não","comment":"A utilização de pendrives particulares não deve ser utilizada pois como é de uso comum do funcionário ele pode estar infectado podendo ser perigoso para o sistema da empresa."}) if ((dictAux["ent"]['answers'][1]/n) < (7*70/100)) else None
    listComments.append({"id":"3","code":"ent3","utterance":"Existe uma limitação dos sites que podem ser acessados dentro do laboratório?","idealAnswer":"Sim","comment":"É importante uma limitação dos sites a fim de evitar que funcionários entrem indevidamente em sites que podem conter malwares em links perigosos.Aconselha-se que restrinja o acesso para apenas links seguros e/ou importante para o uso dos funcionários."}) if ((dictAux["ent"]['answers'][2]/n) < (7*70/100)) else None
    listComments.append({"id":"3","code":"ent4","utterance":"Você abre e-mails suspeitos dentro da rede do laboratório?","idealAnswer":"Não","comment":"E-Mails onde não possui um identificação conhecida e/ou confiável não é indicado abrir, principalmente se estiver com links para outros sites podem conter ameaças ao sistema.Aconselha-se que apenas abra emails que tem identificação e que os assuntos são apenas sobre a empresa."}) if ((dictAux["ent"]['answers'][3]/n) < (7*70/100)) else None
    listComments.append({"id":"4","code":"exp2","utterance":"Existe um mapeamento dos arquivos dentro do sistema?","idealAnswer":"Sim, semanalmente.","comment":"É importante a existência de um mapeamento pois alguns tipos de malwares ficam escondidos em pastas de arquivos antigos para se camuflar. Aconselha-se que sempre faça uma varredura nos arquivos do sistema para evitar que estes malwares persistam no sistema."}) if ((dictAux["exp"]['answers'][1]/n) < (5*70/100)) else None
    listComments.append({"id":"5","code":"ins1","utterance":"Quando identificado uma possível ameaça os serviços afetados continuam disponíveis?","idealAnswer":"Sim e imediatamente é tratado o erro","comment":"Por mais que alguns serviços estejam em produção, torna-se prioridade a eliminação do risco iminente, em vista que o mesmo pode infectar e causar danos muito maiores com relação a pausa do serviço em execução."}) if ((dictAux["ins"]['answers'][0]/n) < (15*70/100)) else None
    listComments.append({"id":"5","code":"ins3","utterance":"Mesmo com a ameaça eliminada é feito uma varredura no sistema para possíveis arquivos ainda infectados?","idealAnswer":"Sim","comment":"Por mais que o sistema não acuse risco ou que haja algum malware, o malware pode estar dentro da arquitetura e causará danos assim que for “ativado”."}) if ((dictAux["ins"]['answers'][2]/n) < (15*70/100)) else None
    listComments.append({"id":"6","code":"com1","utterance":"Existe algum software de análise e controle de malwares?","idealAnswer":"Sim","comment":"Extremamente importante para a prevenção de problemas futuros, mas não garante que não terá invasões/ataques."}) if ((dictAux["com"]['answers'][0]/n) < (15*70/100)) else None
    listComments.append({"id":"6","code":"com3","utterance":"É solicitado proxy para os tráfegos de dados entre as redes externas e internas?","idealAnswer":"Sim","comment":"Faz com que o IP do seu computador não seja reconhecido, viabilizando uma navegação mais segura, evitando que dados estratégicos sejam compartilhados erroneamente."}) if ((dictAux["com"]['answers'][2]/n) < (15*70/100)) else None
    listComments.append({"id":"7","code":"aca1","utterance":"Quando identificado um agente estranho na rede do laboratório a rede é desligada?","idealAnswer":"É desligado e feito a varredura imediatamente","comment":"Identificando um agente externo incomum, não importando o nível de risco, tem que se possuir o maior cuidado possível para que o sistema não seja totalmente infectado."}) if ((dictAux["aca"]['answers'][0]/n) < (7*70/100)) else None
    listComments.append({"id":"8","code":"inft1","utterance":"Qual a frequência que é feito backup dos dados?","idealAnswer":"Diariamente/Semanalmente","comment":"As empresas nunca esperam um ataque, e o que garante com que elas consigam restaurar um sistema ou continuar com ele,  é o controle de malware e backups periódicos. Garantindo que até mesmo os arquivos e informações mais sensíveis estejam protegidos."}) if ((dictAux["inft"]['answers'][0]/n) < (2*70/100)) else None
    listComments.append({"id":"8","code":"inft2","utterance":"Existe um backup físico e um na nuvem?","idealAnswer":"Físico e em nuvem","comment":"Backup é um conceito extremamente importante, garantindo que caso aconteça algo de negativo com dados, possui uma segunda fonte utilizada para repor, não sendo vítimas de criptográficas com recompensa como o ransomware."}) if ((dictAux["inft"]['answers'][1]/n) < (2*70/100)) else None
    listComments.append({"id":"8","code":"inft4","utterance":"Existe algum sistema de LOG/Registro no servidor?","idealAnswer":"Sim","comment":"Ferramentas como essa, garante um registro de todas as ações realizadas no sistema, login, consulta no Banco de Dados, alteração em senha, acesso arquivos, etc… Servindo de grande ajuda em situações de risco e no controle do sistema"}) if ((dictAux["inft"]['answers'][3]/n) < (4*70/100)) else None
    listComments.append({"id":"9","code":"infm2","utterance":"As informações de pacientes estão disponíveis para qualquer funcionário acessar?","idealAnswer":"Sim","comment":"O ideal é que essas informações sejam sigilosas conforme a Lei Geral de Proteção de Dados Pessoais, Lei nº 13.709/2018."}) if ((dictAux["infm"]['answers'][1]/n) < (15*70/100)) else None
    listComments.append({"id":"9","code":"infm3","utterance":"Os dados são submetidos a algum sistema de encriptação da informação?","idealAnswer":"Sim","comment":"Dados sensíveis tem um grande peso, havendo um cuidado maior tanto na segurança como também na garantia da privacidade, sendo responsabilidade total da empresa. Caso seja exposto dados como esse, haverá um impacto negativo na empresa como um todo."}) if ((dictAux["infm"]['answers'][2]/n) < (8*70/100)) else None
    listComments.append({"id":"10","code":"dad3","utterance":"Em caso de possível invasão, o que a parte do sistema responsável pelos dados faz?","idealAnswer":"O sistema é derrubado mesmo não sendo o foco do ataque.","comment":"Pois, a depender do impacto, precisa-se garantir a segurança e flexibilidade dos dados, então, a reação negativa que o sistema poderá possuir depois de uma invasão pode ocasionar em perda ou até mesmo falência da instituição."}) if ((dictAux["dad"]['answers'][2]/n) < (8*70/100)) else None

    dictAuxFinal['comments'] = listComments

    return dictAuxFinal


@answerAPI.post('/postAnswer')
# Post answer to database
async def postAnswer(answer: Answer):
    _id = client.maindb.answer.insert_one(dict(answer))
    print(_id.inserted_id)
    return answerEntity(client.maindb.answer.find_one({"_id": ObjectId(str(_id.inserted_id))}))


@answerAPI.put('/updateAnswer/{id}')
# Upate a answer by ID
async def updateAnswer(id, answer: Answer):
    try:
        client.maindb.answer.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": dict(answer)})
        return answerEntity(client.maindb.answer.find_one({"_id": ObjectId(id)}))
    except:
        return dict([])


@answerAPI.delete('/delAnswer/{id}')
# Delete a answer by ID
async def deleteAnswer(id):
    try:
        return answerEntity(client.maindb.answer.find_one_and_delete({"_id": ObjectId(id)}))
    except:
        raise HTTPException(status_code=404, detail="Doesn't has answer")
