"""
Realiza leitura e padronização inicial dos dados referentes
a extratos bancários e faturas de cartão de crédito.
"""

import warnings

import pandas as pd

from .inter import parse_inter_account, parse_inter_credit_card
from .btg import parse_btg_account, parse_btg_credit_card
from .nubank import parse_nubank_account, parse_nubank_credit_card

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
    elif source == "inter_credit_card":
        return parse_inter_credit_card("data/fatura_inter")
    elif source == "nubank_account":
        return parse_nubank_account("data/conta_nubank")
    elif source == "nubank_credit_card":
        return parse_nubank_credit_card("data/fatura_nubank")


def read_available_raw_data() -> pd.DataFrame:
    """
    Lê os dados brutos de todas as fontes e retorna um DataFrame consolidado.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados brutos de todas as fontes.
    """

    inter_account = parse_inter_account("data/conta_inter")
    inter_credit_card = parse_inter_credit_card("data/fatura_inter")

    btg_account = parse_btg_account("data/conta_btg")
    btg_credit_card = parse_btg_credit_card("data/fatura_btg")

    nubank_account = parse_nubank_account("data/conta_nubank")
    nubank_credit_card = parse_nubank_credit_card("data/fatura_nubank")

    all_dfs = [
        inter_account,
        inter_credit_card,
        btg_account,
        btg_credit_card,
        nubank_account,
        nubank_credit_card,
    ]

    raw_data = pd.concat(all_dfs, ignore_index=True)

    return raw_data
