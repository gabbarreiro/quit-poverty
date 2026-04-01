"""
Tratamento de dados do Nubank.
"""

import pandas as pd

from ..misc import list_files


def parse_nubank_account(path: str) -> pd.DataFrame:
    """
    Lê e padroniza os dados de extratos bancários do Nubank.

    Args:
        path (str):
            O caminho para o diretório contendo os arquivos de extrato.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados padronizados,
            com colunas: date_ref, description, amount, source.
    """

    pass


def parse_nubank_credit_card(path: str) -> pd.DataFrame:
    """
    Lê e padroniza os dados de faturas de cartão de crédito do Nubank.

    Args:
        path (str): O caminho para o diretório contendo os arquivos de fatura.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados padronizados,
            com colunas: date_ref, description, amount, source.
    """

    pass
