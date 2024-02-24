import requests
import json


def fetch_osu_user_data(api_key, username, beatmap_id, mode):
    # URL base da API do osu!
    url = "https://osu.ppy.sh/api/get_user_recent"


    # Parâmetros da API
    params = {
        'k': api_key,
        'u': username,
        'b': beatmap_id,
        'm': mode,
        'type': 'string'
    }


    # Realizar a solicitação GET à API
    response = requests.get(url, params=params)


    # Verificar se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Carregar os dados JSON da resposta
        user_data = json.loads(response.text)


        # Verificar se os dados do usuário estão presentes
        if user_data:
            return user_data
        else:
            return "Usuário não encontrado."
    else:
        return f"Erro ao conectar à API: {response.status_code}"


# Substitua YOUR_API_KEY e YOUR_USERNAME pelos seus respectivos valores
api_key = "07e5bae41ba15ecfb3dea2020f6c726930be3b97"
username = " " # Inserir nome
mode = '3'
beatmap_id = '0'


# Buscar e imprimir dados do usuário
user_data = fetch_osu_user_data(api_key, username, beatmap_id, mode)
print(user_data)
# countgeki = marvelous, #count300 = perfect, #countkatu = great, #count100 = good, #count50 = bad, #countmiss = miss
