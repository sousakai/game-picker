from steamAPI import * 
import sqlite3


def verificar_banco_vazio():
    conn = sqlite3.connect('info_jogos.db')  # conexão bd
    cursor = conn.cursor()  #cursor bd
    
    cursor.execute('SELECT COUNT(*) FROM info_jogos')  # Conta o número de registros na tabela
    resultado = cursor.fetchone()  # Obtém o resultado da contagem
    
    conn.close()  # Fecha a conexão com o banco
    
    if resultado[0] == 0:  # se o número de registros for 0, o banco está vazio
        return True
    else:
        return False
def main():
  
    verificar_conta = input("Você deseja verificar sua conta Steam? (s/n)\n").lower().strip()

    jogo_aleatorio = None  # inicializa como none para que ela sempre seja definida e não dê erro

    if verificar_conta == 's':  # Verifica se o usuário deseja verificar a conta Steam
        input_usuario = input("Digite seu link do perfil STEAM ou STEAMID:\n")
        STEAM_ID = obter_steamID(input_usuario)

        if STEAM_ID:  # verifica se o steamid foi obtido com sucesso
            print(f"User: {input_usuario} ID: {STEAM_ID}")
            obter_jogos_steam(STEAM_ID)  
            jogo_aleatorio = escolher_jogo() 
            
        else:  # se não conseguir obter o SteamID
            print("Não foi possível obter o SteamID. Selecionando um jogo aleatório do banco de dados...")
            jogo_aleatorio = escolher_jogo() 

    else:  # caso o usuário não queira verificar a conta Steam:
        if verificar_banco_vazio():
            print("O banco de dados está vazio. Não é possível escolher um jogo aleatório.")
            return  # Sai da função se o banco estiver vazio
        jogo_aleatorio = escolher_jogo() 

    # Exibe o jogo aleatório, caso exista
    if jogo_aleatorio:
        print(f"Seu jogo aleatório é: {jogo_aleatorio[2]}, com {jogo_aleatorio[3]} horas jogadas.")
    else:
        print("Nenhum jogo encontrado no banco de dados.")

# Chama a função main para rodar o script
main()




