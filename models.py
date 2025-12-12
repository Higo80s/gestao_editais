from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Edital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200))
    agencia = db.Column(db.String(50), nullable=False)
    codigo_projeto = db.Column(db.String(50))
    descricao_projeto = db.Column(db.Text)
    modalidades = db.relationship('Modalidade', backref='edital', cascade='all, delete-orphan', lazy=True)
    bolsistas = db.relationship('Bolsista', backref='edital', cascade='all, delete-orphan', lazy=True)

class Modalidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    edital_id = db.Column(db.Integer, db.ForeignKey('edital.id'), nullable=False)
    nivel = db.Column(db.String(50), nullable=False)
    vagas = db.Column(db.Integer, nullable=False)
    valor_mensal = db.Column(db.Float, nullable=False)
    bolsistas = db.relationship('Bolsista', backref='modalidade', lazy=True)

class Bolsista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    edital_id = db.Column(db.Integer, db.ForeignKey('edital.id'), nullable=False)
    modalidade_id = db.Column(db.Integer, db.ForeignKey('modalidade.id'), nullable=False) # Link to exact modality
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True)
    email = db.Column(db.String(100))
    
    # Academic Info
    orientador = db.Column(db.String(100))
    campus = db.Column(db.String(50))
    programa = db.Column(db.String(100))
    data_inicio_curso = db.Column(db.Date)
    previsao_defesa = db.Column(db.Date)
    
    # Bank Info
    banco = db.Column(db.String(50))
    agencia = db.Column(db.String(20))
    conta = db.Column(db.String(20))
    tipo_conta = db.Column(db.String(20)) # corrente/poupanca

    # Scholarship Info
    data_inicio_bolsa = db.Column(db.Date, nullable=False)
    meses_duracao = db.Column(db.Integer, nullable=False)
    data_fim_bolsa = db.Column(db.Date, nullable=False)
    
    # Status
    ativo = db.Column(db.Boolean, default=True)
    motivo_desligamento = db.Column(db.Text)
    data_desligamento = db.Column(db.Date)
    
    acompanhamentos = db.relationship('Acompanhamento', backref='bolsista', cascade='all, delete-orphan', lazy=True)

class Acompanhamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bolsista_id = db.Column(db.Integer, db.ForeignKey('bolsista.id'), nullable=False)
    referencia_mes = db.Column(db.String(7), nullable=False) # YYYY-MM
    parcela = db.Column(db.Integer)
    requisicao_pagamento = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('bolsista_id', 'referencia_mes', name='_bolsista_ref_uc'),)
