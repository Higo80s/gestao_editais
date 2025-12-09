#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

def main():
    try:
        print("=" * 60)
        print("Exportando acompanhamento para Excel...")
        print("=" * 60)
        
        hoje = datetime.now()
        primeiro_dia_este_mes = datetime(hoje.year, hoje.month, 1)
        ultimo_dia_mes_passado = primeiro_dia_este_mes - timedelta(days=1)
        referencia_mes = ultimo_dia_mes_passado.strftime("%Y-%m")
        
        print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Mes de referencia: {referencia_mes}")
        
        caminho_arquivo = db.exportar_acompanhamento_mensal_automatico()
        
        if caminho_arquivo:
            print(f"SUCESSO! Arquivo salvo em:")
            print(f"  {caminho_arquivo}")
            print("=" * 60)
            return 0
        else:
            print("ERRO: Falha ao gerar arquivo Excel")
            print("=" * 60)
            return 1
            
    except Exception as e:
        print(f"ERRO: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
