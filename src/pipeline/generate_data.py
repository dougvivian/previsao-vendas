"""Gera dados sinteticos de vendas diarias para uma loja de materiais.

Os dados sao ficticios, mas imitam padroes reais de varejo: demanda base por
produto, sazonalidade semanal e anual, tendencia de crescimento e ruido.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

# (id, nome, categoria, custo unitario, margem, demanda media diaria)
CATALOGO = [
    (1, "Cimento 50kg", "Cimento e argamassa", 32.0, 0.30, 40),
    (2, "Argamassa AC-II 20kg", "Cimento e argamassa", 14.0, 0.35, 25),
    (3, "Tijolo 6 furos (cento)", "Alvenaria", 85.0, 0.25, 15),
    (4, "Bloco de concreto", "Alvenaria", 3.2, 0.40, 60),
    (5, "Areia media (m3)", "Agregados", 90.0, 0.22, 10),
    (6, "Brita 1 (m3)", "Agregados", 105.0, 0.22, 8),
    (7, "Tinta acrilica 18L", "Tintas", 190.0, 0.32, 6),
    (8, "Massa corrida 25kg", "Tintas", 48.0, 0.38, 9),
    (9, "Rolo de pintura", "Tintas", 7.5, 0.60, 20),
    (10, "Cano PVC 100mm", "Hidraulica", 28.0, 0.45, 18),
    (11, "Joelho PVC 90 graus", "Hidraulica", 2.1, 0.70, 50),
    (12, "Torneira de jardim", "Hidraulica", 15.0, 0.65, 7),
    (13, "Fio flexivel 2,5mm (rolo)", "Eletrica", 165.0, 0.28, 8),
    (14, "Disjuntor 20A", "Eletrica", 9.5, 0.55, 14),
    (15, "Tomada 10A", "Eletrica", 6.0, 0.75, 30),
    (16, "Piso ceramico (m2)", "Acabamento", 36.0, 0.40, 22),
    (17, "Rejunte 1kg", "Acabamento", 5.0, 0.60, 26),
    (18, "Porcelanato (m2)", "Acabamento", 62.0, 0.45, 12),
    (19, "Furadeira 500W", "Ferramentas", 120.0, 0.35, 2),
    (20, "Martelo", "Ferramentas", 22.0, 0.55, 5),
]

# Vendas fortes de segunda a sabado, domingo fraco.
FATOR_SEMANAL = np.array([1.05, 1.10, 1.10, 1.05, 1.15, 1.30, 0.35])


def gerar_vendas(
    inicio: str = "2023-01-01",
    dias: int = 730,
    seed: int = 42,
) -> pd.DataFrame:
    """Retorna um DataFrame com uma linha por produto por dia.

    Colunas: data, produto_id, produto, categoria, quantidade,
    preco_unitario, custo_unitario.
    """
    rng = np.random.default_rng(seed)
    datas = pd.date_range(inicio, periods=dias, freq="D")

    dia_da_semana = datas.dayofweek.to_numpy()
    dia_do_ano = datas.dayofyear.to_numpy()

    fator_semana = FATOR_SEMANAL[dia_da_semana]
    # Pico de obras no fim do ano seco (aprox. set-nov), vale em junho-julho.
    fator_ano = 1 + 0.20 * np.sin(2 * np.pi * (dia_do_ano - 120) / 365)
    # Crescimento de 15% ao ano.
    tendencia = 1 + 0.15 * np.arange(dias) / 365

    linhas = []
    for produto_id, nome, categoria, custo, margem, demanda in CATALOGO:
        media = demanda * fator_semana * fator_ano * tendencia
        quantidade = rng.poisson(media)
        # Preco varia um pouco ao longo do tempo (inflacao de ~5% ao ano).
        inflacao = 1 + 0.05 * np.arange(dias) / 365
        custo_unitario = np.round(custo * inflacao, 2)
        preco_unitario = np.round(custo_unitario * (1 + margem), 2)

        linhas.append(
            pd.DataFrame(
                {
                    "data": datas,
                    "produto_id": produto_id,
                    "produto": nome,
                    "categoria": categoria,
                    "quantidade": quantidade,
                    "preco_unitario": preco_unitario,
                    "custo_unitario": custo_unitario,
                }
            )
        )

    return pd.concat(linhas, ignore_index=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saida", type=Path, default=Path("data/vendas.csv"))
    parser.add_argument("--inicio", default="2023-01-01")
    parser.add_argument("--dias", type=int, default=730)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    vendas = gerar_vendas(args.inicio, args.dias, args.seed)
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    vendas.to_csv(args.saida, index=False)
    print(f"{len(vendas)} linhas salvas em {args.saida}")


if __name__ == "__main__":
    main()
