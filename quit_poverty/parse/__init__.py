"""
Realiza leitura e padronização inicial dos dados referentes
a extratos bancários e faturas de cartão de crédito.
"""

import warnings

import pandas as pd

from quit_poverty.parse.inter import parse_inter_account

from .btg import parse_btg_account, parse_btg_credit_card

warnings.simplefilter("ignore")


def read_data_source(source: str) -> pd.DataFrame:
    """
    Lê um arquivo de dados e retorna um DataFrame padronizado.

    Args:
        source (str): O caminho para o arquivo de dados.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados padronizados.
    """

    if source == "btg_account":
        return parse_btg_account("data/conta_btg")
    elif source == "btg_credit_card":
        return parse_btg_credit_card("data/fatura_btg")
    elif source == "inter_account":
        return parse_inter_account("data/conta_inter")
