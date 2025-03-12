import sqlite3

# conexão com o banco de dados e criação do cursor
conn = sqlite3.connect('jogos_usuario.db')
cursor = conn.cursor()

def criar_tabela_usuario():
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS jogos_usuario (  
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            horas_jogadas FLOAT,
            plataforma TEXT
        )
    ''')
    
    conn.commit()  # confirma o comando
    
def inserir_jogo(nome, horas_jogadas, plataforma):
    cursor.execute('''
        INSERT INTO jogos_usuario (nome, horas_jogadas, plataforma)
        VALUES(?, ?, ?)
    ''', (nome, horas_jogadas, plataforma))
    conn.commit()  
    

inserir_jogo('Mass Effect', 3.7, 'PC')
inserir_jogo('Max Payne 3', 30, 'PC')
inserir_jogo('Super Mario 64', 2, 'Nintendo 64')
    