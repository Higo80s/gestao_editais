
import sqlite3

def migrate():
    print("Iniciando migração V2...")
    try:
        conn = sqlite3.connect('gestao_editais_new.db')
        cursor = conn.cursor()
        
        # Edital Table
        print("Migrando Edital...")
        try:
            cursor.execute("ALTER TABLE edital ADD COLUMN processo_sei VARCHAR(50)")
            cursor.execute("ALTER TABLE edital ADD COLUMN comentarios TEXT")
            print(" - Colunas adicionadas em Edital.")
        except sqlite3.OperationalError as e:
            print(f" - Erro (provavelmente colunas já existem): {e}")

        # Modalidade Table
        print("Migrando Modalidade...")
        try:
            cursor.execute("ALTER TABLE modalidade ADD COLUMN max_meses INTEGER")
            print(" - Coluna adicionada em Modalidade.")
        except sqlite3.OperationalError as e:
            print(f" - Erro: {e}")

        # Bolsista Table
        print("Migrando Bolsista...")
        try:
            cursor.execute("ALTER TABLE bolsista ADD COLUMN email_orientador VARCHAR(100)")
            cursor.execute("ALTER TABLE bolsista ADD COLUMN processo_sei VARCHAR(50)")
            cursor.execute("ALTER TABLE bolsista ADD COLUMN comentarios TEXT")
            print(" - Colunas adicionadas em Bolsista.")
        except sqlite3.OperationalError as e:
            print(f" - Erro: {e}")

        conn.commit()
        conn.close()
        print("Migração concluída com sucesso.")

    except Exception as e:
        print(f"Erro crítico na migração: {e}")

if __name__ == "__main__":
    migrate()
