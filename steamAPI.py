import requests
import sqlite3
import random
import re
import os
from dotenv import load_dotenv
from db import inserir_jogo

load_dotenv()  # Carrega as variáveis do arquivo .env

STEAM_ID = ''
STEAM_API_KEY = os.getenv('STEAM_API_KEY')


def obter_steamID(input_usuario):
   
    if input_usuario.isdigit() and len(input_usuario) == 17: 
        # Se o input for um SteamID64 válido (17 dígitos), retorna ele
        return input_usuario

    # Se o input não for um SteamID64, verificamos se é um nome de usuário personalizado ou URL
    match = re.search(r"steamcommunity\.com/id/([\w\d_-]+)", input_usuario)
    if match:
        input_usuario = match.group(1)  # Se for uma URL, extraímos o nome do usuário

    # se for apenas o nome do usuário, monta a URL de perfil
    if not match:  # se não for uma URL, considera o input como nome de usuário
        input_usuario = f"steamcommunity.com/id/{input_usuario}"


    url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={STEAM_API_KEY}&vanityurl={input_usuario}"
    resposta = requests.get(url).json()

    if resposta["response"]["success"] == 1:
        return resposta["response"]["steamid"]  
    else:
        print("Erro ao obter STEAMID64 da conta.")
        return None

def obter_nome_jogo(appid):
    url_nome_jogo = f"https://store.steampowered.com/api/appdetails?appids={appid}" 
    # utilizamos a API de detalhes para obter o nome do jogo pelo appid

    resposta = requests.get(url_nome_jogo)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        
        if str(appid) in dados: #converte para string o appid, pois os dados provenientes da API são strings
            nome_jogo = dados[str(appid)].get("data", {}).get("name", None) 
            # converte appid para string, e usa isso para buscar os dados relacionados. dentro da chave data, busca o dado "name", que é o nome do jogo
            
            return nome_jogo
        else:
            return None
    else:
        return None

def obter_jogos_steam(STEAM_ID):
    conn = sqlite3.connect('info_jogos.db')  # conecta com o banco de dados
    cursor = conn.cursor()  # cria cursor para sql
    
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={STEAM_ID}&format=json"

    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()

        # DEBUG: exibe a estrutura completa da resposta da API
        #print("Estrutura completa da resposta da API:", dados)  

        jogos = dados.get("response", {}).get("games", [])  # usa o response (chave inicial do json de resposta), e busca os games dentro dele

        # verifica se tem jogos no perfil
        if jogos:  
            print(f"Quantidade de jogos encontrados: {len(jogos)}")
            for jogo in jogos:
                
                appid = jogo.get("appid")  # extração do appid de cada jogo
                nome_jogo = obter_nome_jogo(appid)  # chama a função para obter o nome do jogo
                horas_jogadas = jogo.get("playtime_forever") / 60  # converte minutos para horas
                
                # verifica erros ao colher o nome do jogo
                if nome_jogo is None:
                    print(f"Erro ao obter nome do jogo para AppID {appid}")
                else:
                    print(f"Nome do Jogo: {nome_jogo}, AppID: {appid}, Horas Jogadas: {horas_jogadas}")  # exibe dados coletados

                # Inserindo os dados no banco se o nome do jogo não for nulo (com erro)
                if nome_jogo is not None: 
                    inserir_jogo(nome_jogo, horas_jogadas, appid)
        else:
            print("Nenhum jogo encontrado no perfil.")
        
        conn.commit()  # Commit das alterações no banco de dados
    else:
        print("Erro ao obter dados da API")

def escolher_jogo():
    conn = sqlite3.connect('info_jogos.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM info_jogos')  # conta quantos jogos existem na tabela
    count = cursor.fetchone()[0]  # pega o resultado da contagem
    
    if count > 0:  
        cursor.execute('SELECT * FROM info_jogos')  
        jogos = cursor.fetchall()
        jogo_aleatorio = random.choice(jogos)  
        return jogo_aleatorio
    else:
        return None  

