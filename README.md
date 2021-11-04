# Backend

## Criar a env:
* Após verificar se possui o python3 (ou python) instalado, execute o seguinte comando:
```
python3 -m venv pi2021
```

* O nome da env vai ser pi2021
* Para entrar na env basta executar o comando o comando para Linux ou para Windows respectivamente:
```
source pi2021/bin/activate
```
```
pi2021\Scripts\activate.bat
```
* Para desativar a env, basta digitar o comando:
```
deactivate
```
* Dependências:
```
pip install autopep8
pip install fastapi
pip install uvicorn
pip install dnspython
pip install pymongo
```

* Como executar o flask:
```
uvicorn main:app --reload
```
* Os testes serão realizados dentro do http://127.0.0.1:8000/docs#/ 
* As principais funções/rotas que teremos será:
* Mensagem de boas-vindas
* Conexão com o banco de dados
  * Vai retornar se está funcional ou não
  * Print simples (no terminal)
* Listar o nome de todas as empresas que responderam o questionário
  * No formato JSON
  * Podemos retornar os IDs caso necessário como opcional
* A partir do ID ou NOME da empresa, buscar os formulários de respostas
  * No formato JSON
* Função para mandar por body as respostas do questionário da respectiva empresa
  * No formato JSON

## Usuários do MongoDB
* simpleUser:AovgIGUoYKSbpczO
* admin:cFFEh3yTL4WdwsMm

