# 📊 Gestão de Editais

Sistema desktop para gestão de editais de bolsas de estudo (CAPES, CNPq, Fundação Araucária, etc.), desenvolvido para uso na UTFPR.

![Tema Dark](https://img.shields.io/badge/Tema-Dark-2d2d2d?style=flat)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat)
![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey?style=flat)
![Versão](https://img.shields.io/badge/Versão-3.0-brightgreen?style=flat)
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

### Exportação em Excel (Novo - v3)

A aba **Acompanhamento** agora oferece exportação em **Excel com formatação profissional**.

#### Exportar Manualmente

1. Abra a aba **"Acompanhamento"**.
2. Clique no botão **"Exportar Excel"**.
3. Escolha a pasta onde salvar.
4. Arquivo `acompanhamento_YYYY-MM.xlsx` é gerado com:
   - ✅ Headers formatados (azul escuro, texto branco, negrito)
   - ✅ Valores monetários formatados (R$ X.XXX,XX)
   - ✅ Bordas e alinhamento profissional
   - ✅ Colunas ajustadas automaticamente
   - ✅ Dados do mês referência

#### Automatizar Exportação Mensal

Execute manualmente:
```powershell
python exportar_excel_mensal.py
```

Ou agende no Task Scheduler (similar ao prefill):

```powershell
$Action = New-ScheduledTaskAction -Execute "C:\...\python.exe" `
    -Argument "C:\...\exportar_excel_mensal.py" `
    -WorkingDirectory "C:\Users\higosantos\Documents\gestao_editais"

$Trigger = New-ScheduledTaskTrigger -Monthly -At 10:00 -DaysOfMonth 1

Register-ScheduledTask -TaskName "Gestão de Editais - Excel Mensal" `
    -Action $Action -Trigger $Trigger -Description "Exporta acompanhamento em Excel" `
    -RunLevel Highest
```

**Resultado:** Arquivo Excel gerado automaticamente no 1º do mês às 10:00 AM.

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

---

## 📚 Documentação Completa

Este projeto inclui documentação abrangente. Consulte os arquivos:

| Arquivo | Descrição |
|---------|-----------|
| **[DOCUMENTACAO.md](DOCUMENTACAO.md)** | 📖 Guia técnico completo (arquitetura, API, DB, troubleshooting) |
| **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** | ⚡ Quick start para usuários finais |
| **[FAQ.md](FAQ.md)** | ❓ Perguntas frequentes com respostas |
| **[DESENVOLVIMENTO.md](DESENVOLVIMENTO.md)** | 🛠️ Guia para contribuidores e desenvolvedores |
| **[GUIA_EXCEL_MENSAL.md](GUIA_EXCEL_MENSAL.md)** | 📊 Exportação Excel e automação |

### Começar Rápido

1. **Usuário iniciante?** → Leia [GUIA_RAPIDO.md](GUIA_RAPIDO.md)
2. **Dúvida?** → Procure em [FAQ.md](FAQ.md)
3. **Precisa de detalhes técnicos?** → Consulte [DOCUMENTACAO.md](DOCUMENTACAO.md)
4. **Vai contribuir com código?** → Estude [DESENVOLVIMENTO.md](DESENVOLVIMENTO.md)

---

## 🔄 Histórico de Versões

| Versão | Data | Destaques |
|--------|------|-----------|
| **3.0** | Dez 2025 | ✨ Exportação Excel com formatação profissional + Task Scheduler automático |
| **2.1** | Nov 2025 | 🐛 Correções de bugs em edição |
| **2.0** | Out 2025 | 🏗️ Refatoração para padrão MVC + módulo db.py centralizado |
| **1.0** | Set 2025 | 🎉 Lançamento inicial |

---

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature: `git checkout -b feature/AmazingFeature`
3. Commit: `git commit -m 'feat: Add AmazingFeature'`
4. Push: `git push origin feature/AmazingFeature`
5. Abra um Pull Request

Veja [DESENVOLVIMENTO.md](DESENVOLVIMENTO.md) para detalhes técnicos.

---

**Status**: ✅ Produção  
**Última atualização**: Dezembro 2025