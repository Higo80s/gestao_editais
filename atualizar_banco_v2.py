import sqlite3
import os

def atualizar_tabela_bolsistas():
    db_path = os.path.join(os.path.dirname(__file__), 'gestao_editais.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Adicionar coluna data_inicio_curso
    try:
        cursor.execute("ALTER TABLE bolsistas ADD COLUMN data_inicio_curso TEXT")
        print("Coluna 'data_inicio_curso' adicionada com sucesso.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Coluna 'data_inicio_curso' já existe.")
        else:
            print(f"Erro ao alterar tabela: {e}")
            return False

    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    if atualizar_tabela_bolsistas():
        print("Banco atualizado para versão 2.")
    else:
        print("Falha na atualização do banco.")