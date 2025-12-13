# Gestão de Editais (Novo)

Aplicação web para gerenciamento de editais de bolsas, com suporte a modalidades, cadastro detalhado de bolsistas, cálculo automático de parcelas e relatórios.

## Funcionalidades

- **Dashboard**: Visão geral do sistema.
- **Editais**: Cadastro, edição e exclusão.
    - **Novos Campos**: Processo SEI, Comentários.
    - **Modalidades**: Definição de níveis, vagas, valores e **Max Meses** (para cálculo de vigência).
- **Bolsistas**: Cadastro completo com dados pessoais, acadêmicos e bancários.
    - **Campos Detalhados**: Email do Orientador, Campus (Lista Dropdown), Processo SEI.
    - **Lógica Inteligente**: Cálculo automático de duração da bolsa baseado no limite da modalidade.
    - **Correções**: Sistema de desligamento (ativo/inativo) e melhorias visuais (Dark Mode).
- **Relatórios**: Geração de folha de pagamento mensal em Excel e PDF.
- **Tutorial**: Página interna com guia de uso.
- **Interface**: Design moderno com Dark Mode.

## Como Rodar o Projeto

### Modo Produção (Recomendado)
Para uma experiência estável, utilize o lançador automático:
1.  Dê dois cliques no arquivo **`Gestao_Editais.bat`** (ou use o atalho na área de trabalho).
2.  O navegador abrirá automaticamente.

### Modo Desenvolvimento
Para rodar manualmente via terminal:

1.  **Abra o terminal** na pasta do projeto:
    ```powershell
    cd c:\Users\higosantos\Documents\gestao_editais\gestao_editais_novo
    ```

2.  **Ative o Ambiente Virtual**:
    ```powershell
    .\.venv\Scripts\activate
    ```

3.  **Inicie o Servidor**:
    ```powershell
    # Servidor de Produção (Waitress)
    python serve.py
    
    # OU Servidor de Desenvolvimento (Flask)
    python app.py
    ```

4.  **Acesse no Navegador**:
     Abra [http://127.0.0.1:8080](http://127.0.0.1:8080) (Waitress) ou [http://127.0.0.1:5000](http://127.0.0.1:5000) (Flask).

## Estrutura de Arquivos

- `app.py`: Arquivo principal da aplicação (Rotas e Configuração).
- `serve.py`: Script de execução do servidor de produção (Waitress).
- `models.py`: Definição do Banco de Dados (Tabelas).
- `reports.py`: Lógica de geração de Excel e PDF.
- `utils.py`: Funções auxiliares (cálculo de datas/parcelas).
- `templates/`: Arquivos HTML (Páginas).
- `static/`: Arquivos CSS e Imagens.
- `instance/gestao_editais.db`: Banco de dados SQLite.

## Solução de Problemas

- **Erro de Banco de Dados**: Se tiver erros de "coluna não encontrada", execute o script de migração `python migrate_v2.py` ou apague o arquivo `.db` para recriar (perde dados).
