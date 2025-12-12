# Gestão de Editais (Novo)

Aplicação web para gerenciamento de editais de bolsas, com suporte a modalidades, cadastro detalhado de bolsistas, cálculo automático de parcelas e relatórios.

## Funcionalidades

- **Dashboard**: Visão geral do sistema.
- **Editais**: Cadastro, edição e exclusão.
    - **Modalidades**: Definição de níveis (Mestrado/Doutorado), vagas e valores específicos por edital.
- **Bolsistas**: Cadastro completo com dados pessoais, acadêmicos e bancários.
    - Seleção automática de valor baseado na modalidade.
    - Cálculo de vigência.
- **Relatórios**: Geração de folha de pagamento mensal em Excel e PDF.
- **Interface**: Design moderno com Dark Mode.

## Como Rodar o Projeto

Este projeto utiliza Python e Flask. Para rodar em sua máquina:

1.  **Abra o terminal** na pasta do projeto:
    ```powershell
    cd c:\Users\higosantos\Documents\gestao_editais\gestao_editais_novo
    ```

2.  **Ative o Ambiente Virtual** (importante para carregar as bibliotecas):
    ```powershell
    .\.venv\Scripts\activate
    ```
    *(Você verá um `(.venv)` aparecer no início da linha do terminal)*

3.  **Inicie o Servidor**:
    ```powershell
    python app.py
    ```

4.  **Acesse no Navegador**:
     Abra [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Estrutura de Arquivos

- `app.py`: Arquivo principal da aplicação (Rotas e Configuração).
- `models.py`: Definição do Banco de Dados (Tabelas).
- `reports.py`: Lógica de geração de Excel e PDF.
- `utils.py`: Funções auxiliares (cálculo de datas/parcelas).
- `templates/`: Arquivos HTML (Páginas).
- `static/`: Arquivos CSS e Imagens.
- `instance/gestao_editais.db`: Banco de dados SQLite (criado automaticamente).

## Solução de Problemas

- **Erro de Banco de Dados**: Se tiver erros de "coluna não encontrada", apague o arquivo `instance/gestao_editais.db` e reinicie o programa. Ele criará um novo zerado.
- **Porta em uso**: Se a porta 5000 estiver ocupada, edite o final do `app.py` para `app.run(debug=True, port=5001)`.
