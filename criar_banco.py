import sqlite3

def criar_banco():
    conn = sqlite3.connect('gestao_editais.db')
    cursor = conn.cursor()

    # Tabela: editais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS editais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_edital TEXT NOT NULL,
            descricao TEXT,
            agencia_fomento TEXT NOT NULL,
            codigo_projeto TEXT,
            descricao_projeto TEXT
        )
    ''')

    # Tabela: modalidades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modalidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            edital_id INTEGER NOT NULL,
            nivel TEXT NOT NULL,
            vagas INTEGER NOT NULL,
            valor_mensal REAL NOT NULL,
            FOREIGN KEY(edital_id) REFERENCES editais(id) ON DELETE CASCADE
        )
    ''')

    # Tabela: bolsistas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bolsistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            edital_id INTEGER NOT NULL,
            processo_sei TEXT,
            nome TEXT NOT NULL,
            cpf TEXT,
            orientador TEXT,
            campus TEXT,
            programa TEXT,
            nivel TEXT NOT NULL,
            data_inicio_bolsa TEXT NOT NULL,
            meses_duracao INTEGER NOT NULL,
            data_fim_bolsa TEXT NOT NULL,
            previsao_defesa TEXT,
            email_bolsista TEXT,
            email_programa TEXT,
            status TEXT NOT NULL CHECK(status IN ('ativo', 'desligado', 'substituido')),
            FOREIGN KEY(edital_id) REFERENCES editais(id) ON DELETE CASCADE
        )
    ''')

    # Tabela: substituicoes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS substituicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bolsista_original_id INTEGER NOT NULL,
            novo_bolsista_id INTEGER NOT NULL,
            data_substituicao TEXT NOT NULL,
            motivo TEXT,
            FOREIGN KEY(bolsista_original_id) REFERENCES bolsistas(id) ON DELETE CASCADE,
            FOREIGN KEY(novo_bolsista_id) REFERENCES bolsistas(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados 'gestao_editais.db' criado com sucesso!")

if __name__ == "__main__":
    criar_banco()