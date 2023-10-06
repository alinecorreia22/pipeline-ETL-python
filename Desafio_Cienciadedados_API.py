<div class="markdown-google-sans">

## <strong>Onde está a API?</strong>
</div>

A API se encontra no Swagger UI no link mencionado abaixo :

```
# Isto está formatado como código

# Utilize sua própria URL se quiser ;)
# Repositório da API: https://github.com/digitalinnovationone/santander-dev-week-2023-api
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'


Aqui nesta etapa extai a lista de IDs de usuario a parti do arquivo CSV. 
Para cada ID, foi feito uma requisição GET e assim conseguimos obter os dados
do usuario correspondente

import pandas as pd
df = pd.read_csv('boot_ciencia.csv')
user_ids = df ['UserID'].tolist()
print(user_ids)

import requests
import json

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

<div class="markdown-google-sans">

## Transformação do Dado
</div>

Utilizei a API do OpenAl GPT-4 para gerar uma mensagem de marketing personalizada para cada usuário.

!pip install openai

openai_api_key = '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'

import openai

openai.api_key = openai_api_key

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
          {
              "role": "system",
              "content": "Você é um especialista em markting bancário." 
          },

          {
              "role": "user",
              "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
          }
      ]
  )  
  return completion.choices[0].message.content.strip('\"')

  for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news                 
    })


    <div class="markdown-google-sans">

## Etapa de Carregamento
Atualizar os dados na API com os dados enriquecidos

</div>

def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/user/{user['id']}",json=user)
  return True if response.status_code == 200 else False

  for user in users:
    sucess = update_user(user)
    print(f"User {user ['name']} update? {success}")