import db

if __name__ == '__main__':
    inserted, ref = db.prefill_mes_atual()
    print(f"Prefill completed for {ref}. Inserted: {inserted} rows.")
