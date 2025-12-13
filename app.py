from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from models import db, Edital, Modalidade, Bolsista, Acompanhamento
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gestao_editais_new.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24) # Production random key

db.init_app(app)

@app.route('/')
@app.route('/')
def index():
    active_editais = Edital.query.count()
    active_bolsistas = Bolsista.query.filter_by(ativo=True).count()
    
    # Calculate Total Monthly Investment
    # This is an approximation based on active bolsistas * their modalidade value
    # For a more accurate "Total Investido" (historical), we'd sum payments.
    # Assuming user wants "Current Monthly Investment" or "Total Allocated". 
    # Let's go with Monthly Investment for now as it's dynamic.
    
    total_investido = 0
    active_bolsistas_list = Bolsista.query.filter_by(ativo=True).all()
    for b in active_bolsistas_list:
        if b.modalidade:
            total_investido += b.modalidade.valor_mensal
            
    return render_template('index.html', 
                           active_editais=active_editais, 
                           active_bolsistas=active_bolsistas, 
                           total_investido=total_investido)

# === EDITAIS ===
@app.route('/editais')
def editais_index():
    editais = Edital.query.all()
    return render_template('editais/index.html', editais=editais)

@app.route('/editais/novo', methods=['GET', 'POST'])
def editais_novo():
    if request.method == 'POST':
        novo_edital = Edital(
            numero=request.form['numero'],
            descricao=request.form['descricao'],
            agencia=request.form['agencia'],
            codigo_projeto=request.form['codigo_projeto'],
            descricao_projeto=request.form['descricao_projeto'],
            processo_sei=request.form['processo_sei'], # [NEW] V2
            comentarios=request.form['comentarios'] # [NEW] V2
        )
        db.session.add(novo_edital)
        db.session.commit()
        flash('Edital criado com sucesso!', 'success')
        return redirect(url_for('editais_index'))
    return render_template('editais/form.html', edital=None)

@app.route('/editais/<int:id>/editar', methods=['GET', 'POST'])
def editais_editar(id):
    edital = Edital.query.get_or_404(id)
    if request.method == 'POST':
        edital.numero = request.form['numero']
        edital.descricao = request.form['descricao']
        edital.agencia = request.form['agencia']
        edital.codigo_projeto = request.form['codigo_projeto']
        edital.descricao_projeto = request.form['descricao_projeto']
        edital.processo_sei = request.form['processo_sei'] # [NEW] V2
        edital.comentarios = request.form['comentarios'] # [NEW] V2
        db.session.commit()
        flash('Edital atualizado com sucesso!', 'success')
        return redirect(url_for('editais_index'))
    return render_template('editais/form.html', edital=edital)

@app.route('/editais/<int:id>/excluir', methods=['POST'])
def editais_excluir(id):
    edital = Edital.query.get_or_404(id)
    db.session.delete(edital)
    db.session.commit()
    flash('Edital excluído com sucesso!', 'success')
    return redirect(url_for('editais_index'))

# === MODALIDADES ===
@app.route('/editais/<int:id>/modalidades', methods=['GET', 'POST'])
def modalidades_gerenciar(id):
    edital = Edital.query.get_or_404(id)
    if request.method == 'POST':
        nova_mod = Modalidade(
            edital_id=edital.id,
            nivel=request.form['nivel'],
            vagas=int(request.form['vagas']),
            valor_mensal=float(request.form['valor_mensal'].replace(',', '.')),
            max_meses=int(request.form['max_meses']) # [NEW] V2
        )
        db.session.add(nova_mod)
        db.session.commit()
        flash('Modalidade adicionada!', 'success')
        return redirect(url_for('modalidades_gerenciar', id=id))
    
    return render_template('editais/modalidades.html', edital=edital)

@app.route('/modalidades/<int:id>/excluir', methods=['POST'])
def modalidades_excluir(id):
    mod = Modalidade.query.get_or_404(id)
    edital_id = mod.edital_id
    db.session.delete(mod)
    db.session.commit()
    flash('Modalidade removida!', 'success')
    return redirect(url_for('modalidades_gerenciar', id=edital_id))

# === BOLSISTAS ===
@app.route('/bolsistas')
def bolsistas_index():
    bolsistas = Bolsista.query.all()
    return render_template('bolsistas/index.html', bolsistas=bolsistas)

@app.route('/bolsistas/novo', methods=['GET', 'POST'])
def bolsistas_novo():
    editais = Edital.query.all()
    if request.method == 'POST':
        # Get Modalidade
        modalidade_id = int(request.form['modalidade_id'])
        mod = Modalidade.query.get(modalidade_id)
        
        novo_bolsista = Bolsista(
            edital_id=mod.edital_id,
            modalidade_id=mod.id,
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            email=request.form['email'],
            orientador=request.form['orientador'],
            email_orientador=request.form['email_orientador'], # [NEW] V2
            campus=request.form['campus'],
            programa=request.form['programa'],
            data_inicio_curso=datetime.strptime(request.form['data_inicio_curso'], '%Y-%m-%d').date() if request.form['data_inicio_curso'] else None,
            previsao_defesa=datetime.strptime(request.form['previsao_defesa'], '%Y-%m-%d').date() if request.form['previsao_defesa'] else None,
            banco=request.form['banco'],
            agencia=request.form['agencia'],
            conta=request.form['conta'],
            tipo_conta=request.form['tipo_conta'],
            data_inicio_bolsa=datetime.strptime(request.form['data_inicio_bolsa'], '%Y-%m-%d').date(),
            meses_duracao=int(request.form['meses_duracao']),
            data_fim_bolsa=datetime.strptime(request.form['data_fim_bolsa'], '%Y-%m-%d').date(),
            processo_sei=request.form['processo_sei'], # [NEW] V2
            comentarios=request.form['comentarios'] # [NEW] V2
        )
        db.session.add(novo_bolsista)
        db.session.commit()
        flash('Bolsista cadastrado com sucesso!', 'success')
        return redirect(url_for('bolsistas_index'))

    return render_template('bolsistas/form.html', editais=editais)

@app.route('/bolsistas/<int:id>/editar', methods=['GET', 'POST'])
def bolsistas_editar(id):
    bolsista = Bolsista.query.get_or_404(id)
    editais = Edital.query.all()
    
    if request.method == 'POST':
        modalidade_id = int(request.form['modalidade_id'])
        mod = Modalidade.query.get(modalidade_id)
        
        bolsista.edital_id = mod.edital_id
        bolsista.modalidade_id = mod.id
        bolsista.nome = request.form['nome']
        bolsista.cpf = request.form['cpf']
        bolsista.email = request.form['email']
        bolsista.orientador = request.form['orientador']
        bolsista.email_orientador = request.form['email_orientador'] # [NEW] V2
        bolsista.campus = request.form['campus']
        bolsista.programa = request.form['programa']
        bolsista.data_inicio_curso = datetime.strptime(request.form['data_inicio_curso'], '%Y-%m-%d').date() if request.form['data_inicio_curso'] else None
        bolsista.previsao_defesa = datetime.strptime(request.form['previsao_defesa'], '%Y-%m-%d').date() if request.form['previsao_defesa'] else None
        bolsista.banco = request.form['banco']
        bolsista.agencia = request.form['agencia']
        bolsista.conta = request.form['conta']
        bolsista.tipo_conta = request.form['tipo_conta']
        bolsista.data_inicio_bolsa = datetime.strptime(request.form['data_inicio_bolsa'], '%Y-%m-%d').date()
        bolsista.meses_duracao = int(request.form['meses_duracao'])
        bolsista.data_fim_bolsa = datetime.strptime(request.form['data_fim_bolsa'], '%Y-%m-%d').date()
        bolsista.processo_sei = request.form['processo_sei'] # [NEW] V2
        bolsista.comentarios = request.form['comentarios'] # [NEW] V2
        
        # Status update (Checkbox logic: present=True, absent=False)
        bolsista.ativo = 'ativo' in request.form

        db.session.commit()
        flash('Bolsista atualizado com sucesso!', 'success')
        return redirect(url_for('bolsistas_index'))

    return render_template('bolsistas/form.html', bolsista=bolsista, editais=editais)

@app.route('/bolsistas/<int:id>/excluir', methods=['POST'])
def bolsistas_excluir(id):
    bolsista = Bolsista.query.get_or_404(id)
    db.session.delete(bolsista)
    db.session.commit()
    flash('Bolsista excluído com sucesso!', 'success')
    return redirect(url_for('bolsistas_index'))

@app.route('/api/modalidades/<int:edital_id>')
def api_modalidades(edital_id):
    modalidades = Modalidade.query.filter_by(edital_id=edital_id).all()
    return jsonify([{
        'id': m.id, 
        'nivel': m.nivel, 
        'valor': m.valor_mensal, 
        'vagas': m.vagas,
        'max_meses': m.max_meses # [NEW] V2
    } for m in modalidades])

# === RELATÓRIOS ===
from reports import gerar_relatorio_excel, gerar_relatorio_pdf

@app.route('/relatorios')
def relatorios_index():
    return render_template('relatorios/index.html')

@app.route('/tutorial') # [NEW] V2
def tutorial():
    return render_template('tutorial.html')

@app.route('/relatorios/gerar', methods=['POST'])
def relatorios_gerar():
    tipo = request.form['tipo'] # excel or pdf
    mes = request.form['mes'] # YYYY-MM
    
    if tipo == 'excel':
        output = gerar_relatorio_excel(mes)
        return send_file(output, download_name=f'pagamento_{mes}.xlsx', as_attachment=True)
    elif tipo == 'pdf':
        output = gerar_relatorio_pdf(mes)
        return send_file(output, download_name=f'pagamento_{mes}.pdf', as_attachment=True)
    
    return redirect(url_for('relatorios_index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
