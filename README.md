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