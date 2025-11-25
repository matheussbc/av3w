#Aluno: Matheus de Souza Barros Cerqueira

#Importa bibliotecas
import psycopg2   #biblioteca para conectar e interagir com o Postgre
import hashlib    #para gerar hash seguro das senhas
import sys        #utilitário do sistema

# Configuração de conexão com o banco de dados
DB_CONFIG = {
    "host": "localhost", # endereço do servidor PostgreSQL (localhost = máquina local)
    "port": 5432, # porta padrão do PostgreSQL
    "dbname": "cinema",  #nome do banco de dados
    "user": "postgres",  #usuário do Postgre
    "password": "Majinza.556"   #senha do usuário
}

def hash_senha(s):
    #Converte a senha em um hash SHA-256 para não armazenar texto puro no banco
    return hashlib.sha256(s.encode()).hexdigest()

def criar_conexao():
    #Cria a conexão com o banco usando psycopg2
    try:
        conn = psycopg2.connect(**DB_CONFIG)  #conecta usando os parâmetros do DB_CONFIG
        conn.autocommit = False #desativa autocommit para controlar transações manualmente
        return conn
    except Exception as e:
        print(f"Erro ao conectar: {e}") #mostra erro caso não consiga conectar
        return None

#Criação das tabelas

def criar_tabelas(conn):
    #Script para criar todas as tabelas do sistema de cinema
    sql = """
    CREATE TABLE IF NOT EXISTS Filme (
        id_filme SERIAL PRIMARY KEY,
        titulo VARCHAR(150) NOT NULL,
        genero VARCHAR(50),
        duracao INT,
        classificacao VARCHAR(20),
        sinopse TEXT
    );

    CREATE TABLE IF NOT EXISTS Sala (
        id_sala SERIAL PRIMARY KEY,
        nome_sala VARCHAR(50) NOT NULL,
        capacidade INT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Sessao (
        id_sessao SERIAL PRIMARY KEY,
        data DATE NOT NULL,
        horario TIME NOT NULL,
        id_filme INT NOT NULL REFERENCES Filme(id_filme) ON DELETE CASCADE,
        id_sala INT NOT NULL REFERENCES Sala(id_sala) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Cliente (
        id_cliente SERIAL PRIMARY KEY,
        nome VARCHAR(120) NOT NULL,
        cpf VARCHAR(20) UNIQUE,
        email VARCHAR(100),
        telefone VARCHAR(30)
    );

    CREATE TABLE IF NOT EXISTS Ingresso (
        id_ingresso SERIAL PRIMARY KEY,
        valor DECIMAL(10,2) NOT NULL,
        forma_pagamento VARCHAR(30),
        id_sessao INT NOT NULL REFERENCES Sessao(id_sessao) ON DELETE CASCADE,
        id_cliente INT NOT NULL REFERENCES Cliente(id_cliente) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Usuario (
        id_usuario SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        senha_hash VARCHAR(255),
        tipo VARCHAR(20)
    );
    """
    #Executar o script
    with conn.cursor() as c:
        c.execute(sql)
    conn.commit()  #confirma a criação das tabelas

#Garantir que exista um admin

def garantir_admin(conn):
    with conn.cursor() as c:
        #Verifica se já existe algum usuário admin
        c.execute("SELECT 1 FROM Usuario WHERE tipo='admin'")
        if not c.fetchone():
            #Se não, cria um usuário admin padrão
            c.execute(
                "INSERT INTO Usuario (username, senha_hash, tipo) VALUES (%s,%s,%s)",
                ("admin", hash_senha("admin123"), "admin")
            )
            conn.commit()
            print("Admin criado: admin / admin123")

#Crud para filme e cliente

def listar_filmes(conn):
    print("\n🎬 Filmes cadastrados:")
    with conn.cursor() as c:
        c.execute("SELECT id_filme, titulo, genero, classificacao FROM Filme")
        for f in c.fetchall():
            print(f)  #imprime cada filme encontrado

def add_filme(conn):
    #Coleta dados do usuário via input
    titulo = input("Título: ")
    genero = input("Gênero: ")
    duracao = int(input("Duração (minutos): "))
    classificacao = input("Classificação: ")
    sinopse = input("Sinopse: ")
    #Insere no banco
    with conn.cursor() as c:
        c.execute("INSERT INTO Filme (titulo,genero,duracao,classificacao,sinopse) VALUES (%s,%s,%s,%s,%s)",
                  (titulo, genero, duracao, classificacao, sinopse))
    conn.commit()
    print("✅ Filme adicionado.")

def listar_clientes(conn):
    print("\n👥 Clientes cadastrados:")
    with conn.cursor() as c:
        c.execute("SELECT id_cliente, nome, cpf, telefone FROM Cliente")
        for cte in c.fetchall():
            print(cte)  #imprime cada cliente encontrado

def add_cliente(conn):
    #Coleta dados do usuário via input
    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    telefone = input("Telefone: ")
    #Insere no banco
    with conn.cursor() as c:
        c.execute("INSERT INTO Cliente (nome,cpf,email,telefone) VALUES (%s,%s,%s,%s)",
                  (nome, cpf, email, telefone))
    conn.commit()
    print("✅ Cliente adicionado.")

#Menu admin

def menu_admin(conn):
    #Dicionário que mapeia opções do menu para funções
    opcoes = {
        "1": add_filme,
        "2": listar_filmes,
        "3": add_cliente,
        "4": listar_clientes
    }
    while True:
        print("""
--- MENU ADMIN ---
1) Adicionar Filme
2) Listar Filmes
3) Adicionar Cliente
4) Listar Clientes
0) Sair
""")
        op = input("> ")
        if op == "0":
            break  #sai do menu
        elif op in opcoes:
            try:
                opcoes[op](conn) #executa a função correspondente
            except Exception as e:
                print(f"Erro: {e}")
        else:
            print("Opção inválida.")

#menu

def menu_principal():
    conn = criar_conexao()  #cria conexão com o banco
    if not conn:
        return
    criar_tabelas(conn)     #garante que as tabelas existam
    garantir_admin(conn)    #garante que exista um admin

    while True:
        print("\n1) Login\n0) Sair")
        op = input("> ")
        if op == "1":
            #Login simplificado, entra direto como admin
            print("Login simplificado: entrando como admin...")
            menu_admin(conn)
        elif op == "0":
            break
    conn.close()  #fecha conexão ao sair

if __name__ == "__main__":
    menu_principal()  #inicia o programa