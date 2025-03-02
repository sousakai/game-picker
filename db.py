import sqlite3
import random

# conn = função criada para se conectar ao banco sqlite3. Se não houver o arquivo, ele criará.
conn = sqlite3.connect('info_jogos.db')
cursor = conn.cursor()

def criar_tabela():
 
    # TODO: ADICIONAR GÊNERO DO JOGO 
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS info_jogos (  
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appid INTEGER UNIQUE,
            nome TEXT,
            horas_jogadas FLOAT
        )
    ''')
    
    conn.commit()  # confirma o comando

def inserir_jogo(nome_jogo, horas_jogadas, appid):
    cursor.execute('''SELECT * FROM info_jogos WHERE nome = ?''', (nome_jogo,))
    jogo_existente = cursor.fetchone()  # fetchone: guarda o resultado da query sql em tupla, individualmente
    
    if jogo_existente:
        print(f"O jogo {nome_jogo} já está cadastrado.")
    else:
        cursor.execute(''' 
            INSERT INTO info_jogos (nome, horas_jogadas, appid)
            VALUES(?, ?, ?)
        ''', (nome_jogo, horas_jogadas, appid))
        print("Jogo inserido com sucesso.")
        
    conn.commit()  # confirma o comando

def listar_jogos():
    cursor.execute("SELECT id, nome, horas_jogadas FROM info_jogos")  # Especificando as colunas
    jogos = cursor.fetchall()
    return jogos

def excluir_tabela():
    cursor.execute("DROP TABLE IF EXISTS info_jogos")  
    conn.commit()  # Confirma a transação
    print("Tabela excluída com sucesso.")
    
    


## TESTES / UTILIDADES PARA O BD

#def main():
    #excluir_tabela()  # Exclui a tabela para rodar o código tranquilo, sem criar várias iterações do mesmo game
    #criar_tabela()  
    #listar_jogos()  

    
    ## teste do codigo: 
    # inserir_jogo('Mass Effect', 3.7, 123)
    # inserir_jogo('Mass Effect', 5.0, 123)  # Feito para testar a verificação de jogo existente


#main()
