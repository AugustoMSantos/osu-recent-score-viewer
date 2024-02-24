from flask import Flask, render_template, request
import requests
import json
import math
import webbrowser
app = Flask(__name__)



def fetch_osu_user_data(api_key, username, beatmap_id, mode, limit):
    url = "https://osu.ppy.sh/api/get_user_recent"
    params = {
        'k': api_key,
        'u': username,
        'b': beatmap_id,
        'm': mode,
        'limit': limit,
        'type': 'string'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        user_data = json.loads(response.text)
        if user_data:
            for data in user_data:
                data['prec'] = calcular_prec(data)
                data['date'] = exibir_date(data)
                beatmap_info = get_beatmap_info(data, api_key, limit)
                data['beatmap_name'] = beatmap_info.get('title', 'Beatmap Desconhecido')
                data['beatmap_artist'] = beatmap_info.get('artist', 'Artista desconhecido')
                data['beatmap_difficulty'] = beatmap_info.get('version', 'Unknown')
                data['mods'] = beatmap_info.get('enabled_mods', 'None')
                
                if data.get('enabled_mods') == '0':
                    data['mods'] = ''
                elif data.get('enabled_mods') == '64':
                    data['mods'] = ' +DT'
                elif data.get('enabled_mods') == '576':
                    data['mods'] = ' +NC'
                elif data.get('enabled_mods') == '1073741824':
                    data['mods'] = ' +MR'
                elif data.get('enabled_mods') == '1073741888':
                    data['mods'] = ' +DT,MR'
                elif data.get('enabled_mods') == '1073742400':
                    data['mods'] = ' +NC,MR'
                elif data.get('enabled_mods') == '256':
                    data['mods'] = ' +HT'
                    
                    
                if data.get('rank') == 'X':
                    data['beatmap_rank'] = "SS"
                else:
                    data['beatmap_rank'] = data.get('rank', 'None')
                    
                data['ratio'] = calcular_ratio(data)
                data['username_formatado'] = data.get('username', 'None')
                
            return user_data
        else:
            return "Usuário não encontrado."
    else:
        return f"Erro ao conectar à API: {response.status_code}"
    

def get_beatmap_info(data, api_key, limit2):
    url = "https://osu.ppy.sh/api/get_beatmaps"
    beatmap_id = data.get('beatmap_id')
    params = {
        'k': api_key,
        'b': beatmap_id,
        'limit': limit2,
        'type': 'string'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        beatmap_info = json.loads(response.text)
        if beatmap_info:
            return beatmap_info[0]
    return {}  

    
def calcular_prec(data):
    countgeki = int(data.get('countgeki', 0))
    count300 = int(data.get('count300', 0))
    count100 = int(data.get('count100', 0))
    countkatu = int(data.get('countkatu', 0))
    count50 = int(data.get('count50', 0))
    countmiss = int(data.get('countmiss', 0))

    prec = ((countgeki + count300) * 300 + countkatu * 200 + count100 * 100 + count50 * 50) / (
            300 * (countmiss + count50 + count100 + countkatu + count300 + countgeki))*100
    return f"{prec:.2f}%"

def calcular_ratio(data):
    countgeki = int(data.get('countgeki', 0))
    count300 = int(data.get('count300', 0))

    ratio = (countgeki/count300)
    return f"{ratio:.2f}"

def exibir_date(data):
    date = data.get('date', 0)
    return date




@app.route('/', methods=['GET', 'POST'])
def index():
    api_key = "07e5bae41ba15ecfb3dea2020f6c726930be3b97"
    username = None
    mode = '3'
    beatmap_id = '0'
    limit = '20'

    user_data = []

    if request.method == 'POST':
        username = request.form.get('username')
        

        if username:
            user_data = fetch_osu_user_data(api_key, username, beatmap_id, mode, limit)      

    #beatmap_info = [data['beatmap_id'] for data in user_data]

    return render_template('index.html', username=username, user_data=user_data)

if __name__ == '__main__':
    
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=False)