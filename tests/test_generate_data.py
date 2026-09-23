import pandas as pd

from src.pipeline.generate_data import CATALOGO, gerar_vendas

COLUNAS = [
    "data",
    "produto_id",
    "produto",
    "categoria",
    "quantidade",
    "preco_unitario",
    "custo_unitario",
]


def test_colunas_e_tamanho():
    vendas = gerar_vendas(dias=30)
    assert list(vendas.columns) == COLUNAS
    assert len(vendas) == 30 * len(CATALOGO)


def test_mesma_seed_gera_mesmos_dados():
    a = gerar_vendas(dias=30, seed=1)
    b = gerar_vendas(dias=30, seed=1)
    pd.testing.assert_frame_equal(a, b)


def test_seeds_diferentes_geram_dados_diferentes():
    a = gerar_vendas(dias=30, seed=1)
    b = gerar_vendas(dias=30, seed=2)
    assert not a["quantidade"].equals(b["quantidade"])


def test_quantidade_nao_negativa_e_preco_acima_do_custo():
    vendas = gerar_vendas(dias=90)
    assert (vendas["quantidade"] >= 0).all()
    assert (vendas["preco_unitario"] > vendas["custo_unitario"]).all()


def test_domingo_vende_menos_que_sabado():
    vendas = gerar_vendas(dias=365)
    por_dia = vendas.groupby(vendas["data"].dt.dayofweek)["quantidade"].sum()
    assert por_dia[6] < por_dia[5]
