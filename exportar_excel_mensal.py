#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
exportar_excel_mensal.py - Script para exportar acompanhamento em Excel automaticamente

Este script foi criado para ser executado pelo Windows Task Scheduler mensalmente.
Gera um arquivo Excel formatado com os dados do mês atual.

Uso:
    python exportar_excel_mensal.py

Agendamento (Windows Task Scheduler):
    - Trigger: Primeiro dia do mês, 07:00 AM
    - Ação: python "C:\...\exportar_excel_mensal.py"
    - Diretório: C:\Users\higosantos\Documents\gestao_editais
    - Output: acompanhamento_YYYY-MM.xlsx (salvo na pasta do projeto)
"""

import sys
import os

# Adiciona a pasta do projeto ao path para importar db.py
sys.path.insert(0, os.path.dirname(__file__))

import db
from datetime import datetime

if __name__ == '__main__':
    print("=" * 60)
    print("EXPORTAÇÃO MENSAL DE ACOMPANHAMENTO EM EXCEL")
    print("=" * 60)
    
    try:
        # Exporta acompanhamento do mês atual
        caminho, ref, count = db.exportar_acompanhamento_mensal_automatico()
        
        if caminho:
            print(f"[OK] Exportação concluída com sucesso!")
            print(f"    Referência: {ref}")
            print(f"    Registros: {count}")
            print(f"    Arquivo: {caminho}")
        else:
            print(f"[AVISO] Nenhum registro de acompanhamento para {ref}")
        
        print("=" * 60)
        print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)
        
    except Exception as e:
        print(f"[ERRO] Falha na exportação: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
