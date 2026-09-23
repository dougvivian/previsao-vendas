# previsao-vendas

Pipeline de previsão de vendas (varejo de materiais): dados sintéticos -> SQLite -> modelo -> API -> dashboard. 100% Python.

## Comandos

- Ambiente: `python -m venv .venv` e `.venv\Scripts\activate` (Windows), depois `pip install -e ".[dev]"`
- Testes: `pytest` (ou `pytest tests/test_x.py::test_y` para um só)
- Gerar dados: `python -m src.pipeline.generate_data` (cria `data/vendas.csv`)

## Estrutura

- `src/pipeline/` geração, limpeza e carga no banco
- `src/model/` treino e previsão
- `src/api/` FastAPI
- `dashboard/` Streamlit
- `tests/` espelha a estrutura de `src/`

## Convenções

- Código e nomes de funções/variáveis em português (como já está no projeto); README em português.
- Toda funcionalidade nova vem com teste. Rode `pytest` antes de commitar.
- Dados são sempre sintéticos ou anonimizados. Nunca commitar dados reais, `.env`, chaves ou senhas.
- `data/*.csv` e bancos locais ficam fora do git.
- Ao concluir um item do roadmap, marcar no README.

## Git

- Projeto solo: commits direto na `main`, pequenos e frequentes, um por mudança lógica. Não abrir branch nem PR, salvo se o Douglas pedir.
- Só commitar com `pytest` passando.
- Mensagens de commit em português, no imperativo, primeira linha curta ("Adiciona pipeline de carga em SQLite").
