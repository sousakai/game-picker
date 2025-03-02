import requests
import sqlite3
import random
from db import inserir_jogo

STEAM_ID = ''
STEAM_API_KEY = ''

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

def obter_jogos_steam():
    conn = sqlite3.connect('info_jogos.db')  # conecta com o banco de dados
    cursor = conn.cursor()  # cria cursor para sql
    
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={STEAM_ID}&format=json"

    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()

        
        print("Estrutura completa da resposta da API:", dados)  # exibe a estrutura para debug

        jogos = dados.get("response", {}).get("games", [])  # usa o response (chave inicial do json de resposta), e busca os games dentro dele

        # verifica se tem jogos no perfil
        if jogos:  
            print(f"Quantidade de jogos encontrados: {len(jogos)}")
            for jogo in jogos:
                
                # print("Estrutura do jogo:", jogo)  # exibe a estrutura dos dados coletados por jogo para debug

                appid = jogo.get("appid")
                nome_jogo = obter_nome_jogo(appid)  # busca o nome do jogo com a função anterior
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

#obter_jogos_steam()

def escolher_jogo():
    conn = sqlite3.connect('info_jogos.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM info_jogos')
    jogos = cursor.fetchall()
    
    jogo_aleatorio = random.choice(jogos)
    return jogo_aleatorio

jogo_aleatorio = escolher_jogo()  # chama a função e guarda o return na variável



print(f"Seu jogo aleatório é: {jogo_aleatorio[2]}, com {jogo_aleatorio[3]} horas jogadas." )  # exibe o jogo na posição 1 da tupla (nome)s
