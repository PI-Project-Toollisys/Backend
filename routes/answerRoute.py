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
# que possui (relacionados a firma) dividir e obter a m??dia
# da pontua????o
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
# pergar a quest??o espec??fica de todas as respostas
# para somar e dividir pela quantidade dela (m??dia)
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
            
    listComments.append({"id":"1","code":"rec3","utterance":"Seu e-mail de trabalho ?? o mesmo pessoal?","idealAnswer":"N??o","comment":"?? ideal utilizar o email corporativos e n??o pessoais pois podem estar contaminados com spams e e-mails mal intencionados deixando a rede interna da empresa suscet??vel a ataques. Por isso, criar um email corporativo ?? a melhor forma de evitar estes problemas."}) if ((dictAux["rec"]['answers'][2]/n) < (3*70/100)) else None
    listComments.append({"id":"1","code":"rec4","utterance":"Voc?? utiliza as senhas pessoais para softwares do local de trabalho?","idealAnswer":"N??o","comment":"O ideal ?? que se tenha senha diferentes para cada tipo de acesso para aumentar a seguran??a de aplicativos e inclusive evitar invas??es dos pr??prios dados pessoais e dos dados das empresas.Aconselha-se que notifique os funcion??rios para que mudem as senhas para deixar a seguran??a maior."}) if ((dictAux["rec"]['answers'][3]/n) < (3*70/100)) else None
    listComments.append({"id":"2","code":"arm1","utterance":"O laborat??rio possui uma equipe de TI?","idealAnswer":"N??o","comment":"Deve-se atentar neste ponto pois a equipe de TI deve existir e estar dispon??vel para aux??lio das outras ??reas da empresa.Aconselha-se que identifique a raz??o da equipe de TI seja pouco vista ou caso n??o exista uma equipe contrat??-la."}) if ((dictAux["arm"]['answers'][0]/n) < (7*70/100)) else None
    listComments.append({"id":"3","code":"ent1","utterance":"Durante a entrega de exames ?? comum permitir que clientes usem seus pendrives para entregar informa????es no laborat??rio?","idealAnswer":"N??o","comment":"Permitir que pendrives n??o autorizados sejam conectados a computadores na rede da empresa cria um risco a empresa por serem uma forma de transmiss??o direta de malwares.Aconselha-se que as informa????es de exames sejam entregues fisicamente ou caso n??o seja poss??vel, enviadas por e-mail do paciente ou da empresa que prestou o exame."}) if ((dictAux["ent"]['answers'][0]/n) < (7*70/100)) else None
    listComments.append({"id":"3","code":"ent2","utterance":"Voc?? utiliza seus pendrives particulares para enviar arquivos para computadores ligados ?? rede da empresa?","idealAnswer":"N??o","comment":"A utiliza????o de pendrives particulares n??o deve ser utilizada pois como ?? de uso comum do funcion??rio ele pode estar infectado podendo ser perigoso para o sistema da empresa."}) if ((dictAux["ent"]['answers'][1]/n) < (7*70/100)) else None
    listComments.append({"id":"3","code":"ent3","utterance":"Existe uma limita????o dos sites que podem ser acessados dentro do laborat??rio?","idealAnswer":"Sim","comment":"?? importante uma limita????o dos sites a fim de evitar que funcion??rios entrem indevidamente em sites que podem conter malwares em links perigosos.Aconselha-se que restrinja o acesso para apenas links seguros e/ou importante para o uso dos funcion??rios."}) if ((dictAux["ent"]['answers'][2]/n) < (7*70/100)) else None
    listComments.append({"id":"3","code":"ent4","utterance":"Voc?? abre e-mails suspeitos dentro da rede do laborat??rio?","idealAnswer":"N??o","comment":"E-Mails onde n??o possui um identifica????o conhecida e/ou confi??vel n??o ?? indicado abrir, principalmente se estiver com links para outros sites podem conter amea??as ao sistema.Aconselha-se que apenas abra emails que tem identifica????o e que os assuntos s??o apenas sobre a empresa."}) if ((dictAux["ent"]['answers'][3]/n) < (7*70/100)) else None
    listComments.append({"id":"4","code":"exp2","utterance":"Existe um mapeamento dos arquivos dentro do sistema?","idealAnswer":"Sim, semanalmente.","comment":"?? importante a exist??ncia de um mapeamento pois alguns tipos de malwares ficam escondidos em pastas de arquivos antigos para se camuflar. Aconselha-se que sempre fa??a uma varredura nos arquivos do sistema para evitar que estes malwares persistam no sistema."}) if ((dictAux["exp"]['answers'][1]/n) < (5*70/100)) else None
    listComments.append({"id":"5","code":"ins1","utterance":"Quando identificado uma poss??vel amea??a os servi??os afetados continuam dispon??veis?","idealAnswer":"Sim e imediatamente ?? tratado o erro","comment":"Por mais que alguns servi??os estejam em produ????o, torna-se prioridade a elimina????o do risco iminente, em vista que o mesmo pode infectar e causar danos muito maiores com rela????o a pausa do servi??o em execu????o."}) if ((dictAux["ins"]['answers'][0]/n) < (15*70/100)) else None
    listComments.append({"id":"5","code":"ins3","utterance":"Mesmo com a amea??a eliminada ?? feito uma varredura no sistema para poss??veis arquivos ainda infectados?","idealAnswer":"Sim","comment":"Por mais que o sistema n??o acuse risco ou que haja algum malware, o malware pode estar dentro da arquitetura e causar?? danos assim que for ???ativado???."}) if ((dictAux["ins"]['answers'][2]/n) < (15*70/100)) else None
    listComments.append({"id":"6","code":"com1","utterance":"Existe algum software de an??lise e controle de malwares?","idealAnswer":"Sim","comment":"Extremamente importante para a preven????o de problemas futuros, mas n??o garante que n??o ter?? invas??es/ataques."}) if ((dictAux["com"]['answers'][0]/n) < (15*70/100)) else None
    listComments.append({"id":"6","code":"com3","utterance":"?? solicitado proxy para os tr??fegos de dados entre as redes externas e internas?","idealAnswer":"Sim","comment":"Faz com que o IP do seu computador n??o seja reconhecido, viabilizando uma navega????o mais segura, evitando que dados estrat??gicos sejam compartilhados erroneamente."}) if ((dictAux["com"]['answers'][2]/n) < (15*70/100)) else None
    listComments.append({"id":"7","code":"aca1","utterance":"Quando identificado um agente estranho na rede do laborat??rio a rede ?? desligada?","idealAnswer":"?? desligado e feito a varredura imediatamente","comment":"Identificando um agente externo incomum, n??o importando o n??vel de risco, tem que se possuir o maior cuidado poss??vel para que o sistema n??o seja totalmente infectado."}) if ((dictAux["aca"]['answers'][0]/n) < (7*70/100)) else None
    listComments.append({"id":"8","code":"inft1","utterance":"Qual a frequ??ncia que ?? feito backup dos dados?","idealAnswer":"Diariamente/Semanalmente","comment":"As empresas nunca esperam um ataque, e o que garante com que elas consigam restaurar um sistema ou continuar com ele,  ?? o controle de malware e backups peri??dicos. Garantindo que at?? mesmo os arquivos e informa????es mais sens??veis estejam protegidos."}) if ((dictAux["inft"]['answers'][0]/n) < (2*70/100)) else None
    listComments.append({"id":"8","code":"inft2","utterance":"Existe um backup f??sico e um na nuvem?","idealAnswer":"F??sico e em nuvem","comment":"Backup ?? um conceito extremamente importante, garantindo que caso aconte??a algo de negativo com dados, possui uma segunda fonte utilizada para repor, n??o sendo v??timas de criptogr??ficas com recompensa como o ransomware."}) if ((dictAux["inft"]['answers'][1]/n) < (2*70/100)) else None
    listComments.append({"id":"8","code":"inft4","utterance":"Existe algum sistema de LOG/Registro no servidor?","idealAnswer":"Sim","comment":"Ferramentas como essa, garante um registro de todas as a????es realizadas no sistema, login, consulta no Banco de Dados, altera????o em senha, acesso arquivos, etc??? Servindo de grande ajuda em situa????es de risco e no controle do sistema"}) if ((dictAux["inft"]['answers'][3]/n) < (4*70/100)) else None
    listComments.append({"id":"9","code":"infm2","utterance":"As informa????es de pacientes est??o dispon??veis para qualquer funcion??rio acessar?","idealAnswer":"Sim","comment":"O ideal ?? que essas informa????es sejam sigilosas conforme a Lei Geral de Prote????o de Dados Pessoais, Lei n?? 13.709/2018."}) if ((dictAux["infm"]['answers'][1]/n) < (15*70/100)) else None
    listComments.append({"id":"9","code":"infm3","utterance":"Os dados s??o submetidos a algum sistema de encripta????o da informa????o?","idealAnswer":"Sim","comment":"Dados sens??veis tem um grande peso, havendo um cuidado maior tanto na seguran??a como tamb??m na garantia da privacidade, sendo responsabilidade total da empresa. Caso seja exposto dados como esse, haver?? um impacto negativo na empresa como um todo."}) if ((dictAux["infm"]['answers'][2]/n) < (8*70/100)) else None
    listComments.append({"id":"10","code":"dad3","utterance":"Em caso de poss??vel invas??o, o que a parte do sistema respons??vel pelos dados faz?","idealAnswer":"O sistema ?? derrubado mesmo n??o sendo o foco do ataque.","comment":"Pois, a depender do impacto, precisa-se garantir a seguran??a e flexibilidade dos dados, ent??o, a rea????o negativa que o sistema poder?? possuir depois de uma invas??o pode ocasionar em perda ou at?? mesmo fal??ncia da institui????o."}) if ((dictAux["dad"]['answers'][2]/n) < (8*70/100)) else None

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
