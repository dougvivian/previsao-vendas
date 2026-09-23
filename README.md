# previsao-vendas

Pipeline de previsão de vendas para varejo: geração e limpeza de dados, banco SQL, modelo de previsão, API REST e dashboard.

> Projeto em desenvolvimento. A ideia nasceu de um problema real: prever a demanda de produtos numa loja de materiais para decidir compras e margem.

## Objetivo

Responder perguntas de negócio como:

- Quanto vou vender de cada produto nas próximas semanas?
- Quais produtos tem margem baixa e giro lento?
- Quando o estoque vai acabar?

## Arquitetura (planejada)

```
dados (CSV) -> pipeline (pandas) -> banco (SQLite) -> modelo (scikit-learn) -> API (FastAPI) -> dashboard (Streamlit)
```

## Estrutura

```
data/         dados sintéticos gerados localmente (não versionados)
src/
  pipeline/   geração, limpeza e carga no banco
  model/      treino e previsão
  api/        API REST
dashboard/    dashboard Streamlit
tests/        testes automatizados
```

## Roadmap

- [x] Estrutura do projeto
- [ ] Gerador de dados sintéticos de vendas
- [ ] Pipeline de limpeza e carga em SQLite
- [ ] Modelo base de previsão (média móvel) e modelo com scikit-learn
- [ ] API com FastAPI
- [ ] Dashboard com Streamlit
- [ ] Docker e GitHub Actions

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"
pytest
```

## Stack

Python, pandas, SQLite, scikit-learn, FastAPI, Streamlit, pytest.
