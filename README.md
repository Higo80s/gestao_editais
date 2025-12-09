# 📊 Gestão de Editais

Sistema desktop para gestão de editais de bolsas de estudo (CAPES, CNPq, Fundação Araucária, etc.), desenvolvido para uso na UTFPR.

![Tema Dark](https://img.shields.io/badge/Tema-Dark-2d2d2d?style=flat)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat)
![Licença](https://img.shields.io/github/license/seu-usuario/gestao_editais?style=flat)

## ✨ Funcionalidades

- Cadastro e edição de **editais**
- Gestão de **modalidades** por edital (graduação, mestrado, doutorado, pós-doc)
- Controle de **bolsistas** com:
  - Datas de início no curso e início da bolsa
  - Cálculo automático da data final da bolsa
  - Status: ativo, desligado, substituído
- **Consulta integrada** com filtro por edital e busca por projeto
- **Relatórios** em:
  - TXT
  - Excel (.xlsx)
  - PDF
- **Exclusão segura** com validação de dependências
- Interface **dark theme** responsiva

## 🛠️ Requisitos

- Windows (testeado em 10/11)
- Nenhum software adicional necessário (o executável é autônomo)

## 📥 Como usar

1. Baixe o arquivo **`GestaoEditais.exe`** da seção [Releases](https://github.com/seu-usuario/gestao_editais/releases)
2. Dê dois cliques para executar
3. Use normalmente (o banco de dados `gestao_editais.db` será criado automaticamente)

> 💡 **Dica**: Mantenha o `.exe` e o `.db` na mesma pasta para preservar os dados.

## 🚀 Acompanhamento Mensal de Bolsas (Novo - v3)

### Aba Acompanhamento

Desde a v3, a aplicação inclui uma aba dedicada para **acompanhamento mensal** de requisições de pagamento:

1. Abra a aba **"Acompanhamento"**.
2. Selecione um bolsista ativo.
3. O sistema calcula automaticamente:
   - **Parcela Atual**: número do mês (baseado em data de início da bolsa).
   - **Data de Fim Bolsa**: quando a bolsa termina.
4. Preencha:
   - **Nº Requisição**: número do pagamento (SEI, fatura, etc.).
   - **Observações**: anotações adicionais (opcional).
5. Clique **"Registrar requisição"** para salvar.

Ao reabrir o bolsista, os dados preenchidos são carregados automaticamente.

### Automação: Pré-preenchimento Mensal

Para pré-criar registros de acompanhamento mensalmente **sem abrir a UI**:

#### Executar Manualmente
```powershell
python prefill_acompanhamento.py
```

#### Agendar no Windows Task Scheduler

1. Abra **Agendador de Tarefas** (`Win + R` → `taskschd.msc`).
2. Clique **"Criar Tarefa"** (no painel direito).
3. Configure conforme abaixo:

   **Aba Geral:**
   - Nome: `Gestão de Editais - Prefill Mensal`
   - Marque `Executar com privilégios mais altos`

   **Aba Gatilhos:**
   - Clique "Novo" → Tipo: Mensal
   - Dia: 1 (ou preferido)
   - Hora: 09:00 (ou preferida)

   **Aba Ações:**
   - Programa: `C:\Users\higosantos\Documents\gestao_editais\.venv\Scripts\python.exe`
   - Argumentos: `C:\Users\higosantos\Documents\gestao_editais\prefill_acompanhamento.py`
   - Iniciar em: `C:\Users\higosantos\Documents\gestao_editais`

#### Via PowerShell (alternativa)

```powershell
$Action = New-ScheduledTaskAction -Execute "C:\Users\higosantos\Documents\gestao_editais\.venv\Scripts\python.exe" `
    -Argument "C:\Users\higosantos\Documents\gestao_editais\prefill_acompanhamento.py" `
    -WorkingDirectory "C:\Users\higosantos\Documents\gestao_editais"

$Trigger = New-ScheduledTaskTrigger -Monthly -At 09:00 -DaysOfMonth 1

Register-ScheduledTask -TaskName "Gestão de Editais - Prefill Mensal" `
    -Action $Action -Trigger $Trigger -Description "Pré-cria registros de acompanhamento" `
    -RunLevel Highest
```

### Estrutura de Migrations

- **criar_banco.py**: Schema inicial.
- **atualizar_banco_v2.py**: Adiciona coluna `data_inicio_curso`.
- **atualizar_banco_v3.py**: Cria tabela `acompanhamento`.

Execute na ordem:
```powershell
python criar_banco.py
python atualizar_banco_v2.py
python atualizar_banco_v3.py
```

## 💻 Para desenvolvedores

### Pré-requisitos
- Python 3.8+
- Git

### Instalação
```bash
git clone https://github.com/seu-usuario/gestao_editais.git
cd gestao_editais
python -m venv .venv
# Ative o ambiente virtual (Windows):
.venv\Scripts\activate
pip install -r requirements.txt
```

### Gerar executável
Execute o script `build.bat` (Windows) para gerar o `.exe` atualizado.

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙌 Autor

Desenvolvido por **higosantos** para a **UTFPR**.