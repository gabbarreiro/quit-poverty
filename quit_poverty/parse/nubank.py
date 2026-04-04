"""
Tratamento de dados do Nubank.
"""

import pandas as pd

from ..misc import list_files, adjust_description


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

    rename_columns = {
        "Data": "date_ref",
        "Descrição": "description",
        "Valor": "amount",
    }

    raw_data = pd.DataFrame()

    for file in list_files(path):
        df = pd.read_csv(file)

        df = df[rename_columns.keys()]
        df = df.rename(columns=rename_columns)

        raw_data = pd.concat((raw_data, df))

    raw_data["description"] = raw_data["description"].apply(adjust_description)
    raw_data["date_ref"] = pd.to_datetime(raw_data["date_ref"], dayfirst=True)
    raw_data["amount"] = raw_data["amount"].astype(float)

    raw_data["source"] = "nubank_account"

    return raw_data


def parse_nubank_credit_card(path: str) -> pd.DataFrame:
    """
    Lê e padroniza os dados de faturas de cartão de crédito do Nubank.

    Args:
        path (str):
            O caminho para o diretório contendo os arquivos de fatura.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados padronizados,
            com colunas: date_ref, description, amount, source.
    """

    rename_columns = {
        "date": "date_ref",
        "title": "description",
        "amount": "amount",
    }

    raw_data = pd.DataFrame()

    for file in list_files(path):
        df = pd.read_csv(file)

        df = df[rename_columns.keys()]
        df = df.rename(columns=rename_columns)

        raw_data = pd.concat((raw_data, df))

    raw_data["description"] = raw_data["description"].apply(adjust_description)
    raw_data["date_ref"] = pd.to_datetime(raw_data["date_ref"], yearfirst=True)
    raw_data["amount"] = raw_data["amount"].astype(float) * -1

    raw_data["source"] = "nubank_credit_card"

    return raw_data
