import sqlite3
import os

def criar_tabela_acompanhamento():
    db_path = os.path.join(os.path.dirname(__file__), 'gestao_editais.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS acompanhamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bolsista_id INTEGER NOT NULL,
                referencia_mes TEXT NOT NULL,
                parcela INTEGER NOT NULL,
                requisicao_pagamento TEXT,
                observacoes TEXT,
                criado_em TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY(bolsista_id) REFERENCES bolsistas(id) ON DELETE CASCADE,
                UNIQUE(bolsista_id, referencia_mes)
            )
        ''')
        conn.commit()
        print("Tabela 'acompanhamento' criada/verificada com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela acompanhamento: {e}")
        return False
    finally:
        conn.close()

    return True

if __name__ == '__main__':
    if criar_tabela_acompanhamento():
        print("Banco atualizado para versão 3.")
    else:
        print("Falha na atualização do banco.")
import sqlite3
import os

def atualizar_banco_acompanhamento():
    db_path = os.path.join(os.path.dirname(__file__), 'gestao_editais.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Adicionar coluna requisicao_pagamento
        cursor.execute("ALTER TABLE bolsistas ADD COLUMN requisicao_pagamento TEXT")
        print("Coluna 'requisicao_pagamento' adicionada com sucesso.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Coluna 'requisicao_pagamento' já existe.")
        else:
            print(f"Erro ao alterar tabela: {e}")
            return False

    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    if atualizar_banco_acompanhamento():
        print("Banco atualizado para versão 3 (acompanhamento).")
    else:
        print("Falha na atualização do banco.")