"""
db.py - Módulo centralizado de acesso ao banco de dados.

Fornece funções para queries comuns e mantém a lógica SQL em um único lugar,
facilitando manutenção, testes e refatorações futuras.
"""

import sqlite3
import os
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(__file__), 'gestao_editais.db')


def get_connection():
    """Retorna uma conexão ao banco de dados."""
    return sqlite3.connect(DB_PATH)


# ===== EDITAIS =====

def obter_todos_editais():
    """Retorna lista de (id, numero_edital)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, numero_edital FROM editais ORDER BY id")
    result = cursor.fetchall()
    conn.close()
    return result


def obter_edital_por_id(edital_id):
    """Retorna dados de um edital."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, numero_edital, descricao, agencia_fomento, codigo_projeto, descricao_projeto FROM editais WHERE id = ?", (edital_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def criar_edital(numero, descricao, agencia, codigo_projeto=None, descricao_projeto=None):
    """Insere um novo edital."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO editais (numero_edital, descricao, agencia_fomento, codigo_projeto, descricao_projeto)
        VALUES (?, ?, ?, ?, ?)
    ''', (numero, descricao, agencia, codigo_projeto, descricao_projeto))
    edital_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return edital_id


# ===== BOLSISTAS =====

def obter_bolsistas_ativos():
    """Retorna lista de bolsistas com status 'ativo'."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nome, nivel, data_inicio_bolsa, meses_duracao, data_fim_bolsa
        FROM bolsistas
        WHERE status = 'ativo'
        ORDER BY nome
    ''')
    result = cursor.fetchall()
    conn.close()
    return result


def obter_bolsista_por_id(bolsista_id):
    """Retorna dados completos de um bolsista."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            bolsistas.edital_id, numero_edital, processo_sei, nome, cpf, orientador,
            campus, programa, nivel, data_inicio_curso, data_inicio_bolsa,
            meses_duracao, previsao_defesa, email_bolsista, email_programa, status
        FROM bolsistas
        JOIN editais ON bolsistas.edital_id = editais.id
        WHERE bolsistas.id = ?
    ''', (bolsista_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def criar_bolsista(edital_id, processo, nome, cpf, orientador, campus, programa,
                   nivel, data_inicio_curso_iso, data_inicio_bolsa_iso, meses, data_fim_iso,
                   defesa_iso, email_bols, email_prog):
    """Insere um novo bolsista."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bolsistas (
            edital_id, processo_sei, nome, cpf, orientador, campus, programa,
            nivel, data_inicio_curso, data_inicio_bolsa, meses_duracao, data_fim_bolsa,
            previsao_defesa, email_bolsista, email_programa, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        edital_id, processo, nome, cpf, orientador, campus, programa,
        nivel, data_inicio_curso_iso, data_inicio_bolsa_iso, meses, data_fim_iso,
        defesa_iso, email_bols, email_prog, 'ativo'
    ))
    bolsista_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return bolsista_id


def atualizar_bolsista(bolsista_id, processo, nome, cpf, orientador, campus, programa,
                       data_inicio_curso_iso, data_inicio_bolsa_iso, meses, data_fim_iso,
                       defesa_iso, email_bols, email_prog, status):
    """Atualiza dados de um bolsista."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE bolsistas SET
            processo_sei = ?, nome = ?, cpf = ?, orientador = ?, campus = ?, programa = ?,
            data_inicio_curso = ?, data_inicio_bolsa = ?, meses_duracao = ?, data_fim_bolsa = ?,
            previsao_defesa = ?, email_bolsista = ?, email_programa = ?, status = ?
        WHERE id = ?
    ''', (
        processo, nome, cpf, orientador, campus, programa,
        data_inicio_curso_iso, data_inicio_bolsa_iso, meses, data_fim_iso,
        defesa_iso, email_bols, email_prog, status, bolsista_id
    ))
    conn.commit()
    conn.close()


# ===== ACOMPANHAMENTO =====

def obter_acompanhamento_ativo(referencia=None):
    """Retorna acompanhamento para bolsistas ativos (filtro opcional por referência)."""
    conn = get_connection()
    cursor = conn.cursor()
    if referencia:
        cursor.execute('''
            SELECT a.id, b.id as bolsista_id, b.nome, b.cpf, b.nivel,
                   a.referencia_mes, a.parcela, a.requisicao_pagamento, a.observacoes
            FROM acompanhamento a
            JOIN bolsistas b ON a.bolsista_id = b.id
            WHERE b.status = 'ativo' AND a.referencia_mes = ?
            ORDER BY b.nome
        ''', (referencia,))
    else:
        cursor.execute('''
            SELECT a.id, b.id as bolsista_id, b.nome, b.cpf, b.nivel,
                   a.referencia_mes, a.parcela, a.requisicao_pagamento, a.observacoes
            FROM acompanhamento a
            JOIN bolsistas b ON a.bolsista_id = b.id
            WHERE b.status = 'ativo'
            ORDER BY a.referencia_mes DESC, b.nome
        ''')
    result = cursor.fetchall()
    conn.close()
    return result


def registrar_acompanhamento(bolsista_id, referencia_mes, parcela, requisicao, observacoes):
    """
    Insere ou atualiza acompanhamento.
    Usa ON CONFLICT com fallback para versões antigas do SQLite.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO acompanhamento (bolsista_id, referencia_mes, parcela, requisicao_pagamento, observacoes, criado_em)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT(bolsista_id, referencia_mes) DO UPDATE SET
                parcela=excluded.parcela,
                requisicao_pagamento=excluded.requisicao_pagamento,
                observacoes=excluded.observacoes,
                criado_em=datetime('now')
        ''', (bolsista_id, referencia_mes, parcela or 0, requisicao, observacoes))
    except sqlite3.OperationalError:
        # fallback
        cursor.execute('SELECT id FROM acompanhamento WHERE bolsista_id = ? AND referencia_mes = ?', (bolsista_id, referencia_mes))
        if cursor.fetchone():
            cursor.execute('''
                UPDATE acompanhamento SET parcela = ?, requisicao_pagamento = ?, observacoes = ?, criado_em = datetime('now')
                WHERE bolsista_id = ? AND referencia_mes = ?
            ''', (parcela or 0, requisicao, observacoes, bolsista_id, referencia_mes))
        else:
            cursor.execute('''
                INSERT INTO acompanhamento (bolsista_id, referencia_mes, parcela, requisicao_pagamento, observacoes, criado_em)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            ''', (bolsista_id, referencia_mes, parcela or 0, requisicao, observacoes))
    conn.commit()
    conn.close()


def obter_acompanhamento_para_csv():
    """Retorna registros de acompanhamento para exportação CSV."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.id, b.nome, b.cpf, b.nivel, a.referencia_mes, a.parcela, 
               a.requisicao_pagamento, a.observacoes, a.criado_em
        FROM acompanhamento a
        JOIN bolsistas b ON a.bolsista_id = b.id
        ORDER BY a.referencia_mes DESC, b.nome
    ''')
    result = cursor.fetchall()
    conn.close()
    return result


def prefill_mes_atual():
    """Pré-cria registros de acompanhamento para o mês atual para todos os bolsistas ativos."""
    from datetime import datetime
    ref = f"{datetime.now().year:04d}-{datetime.now().month:02d}"
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, data_inicio_bolsa FROM bolsistas WHERE status = 'ativo'")
    bolsistas = cursor.fetchall()
    
    inserted = 0
    for bolsista_id, inicio_iso in bolsistas:
        parcela = calcular_parcela(inicio_iso, ref)
        try:
            cursor.execute('''
                INSERT INTO acompanhamento (bolsista_id, referencia_mes, parcela, requisicao_pagamento, observacoes, criado_em)
                VALUES (?, ?, ?, NULL, NULL, datetime('now'))
                ON CONFLICT(bolsista_id, referencia_mes) DO NOTHING
            ''', (bolsista_id, ref, parcela))
            if cursor.rowcount == 1:
                inserted += 1
        except sqlite3.OperationalError:
            # fallback
            cursor.execute('SELECT id FROM acompanhamento WHERE bolsista_id = ? AND referencia_mes = ?', (bolsista_id, ref))
            if not cursor.fetchone():
                cursor.execute('INSERT INTO acompanhamento (bolsista_id, referencia_mes, parcela, requisicao_pagamento, observacoes, criado_em) VALUES (?, ?, ?, NULL, NULL, datetime(\'now\'))', (bolsista_id, ref, parcela))
                inserted += 1
    
    conn.commit()
    conn.close()
    return inserted, ref


def calcular_parcela(data_inicio_bolsa_iso, referencia_yyyy_mm):
    """Calcula número da parcela para uma referência (mês)."""
    try:
        inicio = datetime.strptime(data_inicio_bolsa_iso, '%Y-%m-%d')
        ref = datetime.strptime(referencia_yyyy_mm + '-01', '%Y-%m-%d')
        meses = (ref.year - inicio.year) * 12 + (ref.month - inicio.month)
        return meses + 1 if meses >= 0 else 0
    except Exception:
        return None


# ===== MODALIDADES =====

def obter_modalidades_por_edital(edital_id):
    """Retorna modalidades de um edital."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, nivel, vagas, valor_mensal FROM modalidades WHERE edital_id = ? ORDER BY nivel
    ''', (edital_id,))
    result = cursor.fetchall()
    conn.close()
    return result


def obter_edital_id_por_numero(numero_edital):
    """Retorna o ID de um edital pelo seu número."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM editais WHERE numero_edital = ?", (numero_edital,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def criar_modalidade(edital_id, nivel, vagas, valor_mensal):
    """Insere uma nova modalidade."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO modalidades (edital_id, nivel, vagas, valor_mensal)
        VALUES (?, ?, ?, ?)
    ''', (edital_id, nivel, vagas, valor_mensal))
    conn.commit()
    conn.close()
