"""
Tratamento de dados do Inter.
"""

import pandas as pd

from ..misc import list_files, adjust_description


def to_float(num: str) -> float:
    """
    Converte string numérica no formato brasileiro para
    float.

    Args:
        num (str):
            String numérica com separador de milhar como
            ponto e decimal como vírgula (ex: '1.234,56').

    Returns:
        float: Valor numérico equivalente como float (ex: 1234.56).
    """

    clean_str = num.replace("R$ ", "").replace(".", "").replace(",", ".")

    clean_str = "".join([c for c in clean_str if c.isdigit() or c in ".-"])

    return float(clean_str)


def parse_inter_account(path: str) -> pd.DataFrame:
    """
    Lê e padroniza os dados de extratos bancários do Inter.

    Args:
        path (str):
            O caminho para o diretório contendo os arquivos de extrato.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados padronizados,
            com colunas: date_ref, description, amount, source.
    """

    rename_columns = {
        "Data Lançamento": "date_ref",
        "Descrição": "description",
        "Valor": "amount",
    }

    raw_data = pd.DataFrame()

    for file in list_files(path):
        df = pd.read_csv(file, header=4, sep=";")

        df = df[rename_columns.keys()]
        df = df.rename(columns=rename_columns)

        raw_data = pd.concat((raw_data, df))

    raw_data["description"] = raw_data["description"].apply(adjust_description)
    raw_data["date_ref"] = pd.to_datetime(raw_data["date_ref"], dayfirst=True)
    raw_data["amount"] = raw_data["amount"].apply(to_float)

    raw_data["source"] = "inter_account"

    return raw_data


def parse_inter_credit_card(path: str) -> pd.DataFrame:
    """
    Lê e padroniza os dados de faturas de cartão de crédito do Inter.

    Args:
        path (str):
            O caminho para o diretório contendo os arquivos de fatura.

    Returns:
        pd.DataFrame: Um DataFrame contendo os dados padronizados,
            com colunas: date_ref, description, amount, source.
    """

    rename_columns = {
        "Data": "date_ref",
        "Lançamento": "description",
        "Valor": "amount",
    }

    raw_data = pd.DataFrame()

    for file in list_files(path):
        df = pd.read_csv(file)

        df["Lançamento"] = df["Lançamento"] + " " + df["Categoria"]
        df = df[rename_columns.keys()]
        df = df.rename(columns=rename_columns)

        raw_data = pd.concat((raw_data, df))

    raw_data["description"] = raw_data["description"].apply(adjust_description)
    raw_data["date_ref"] = pd.to_datetime(raw_data["date_ref"], dayfirst=True)
    raw_data["amount"] = raw_data["amount"].apply(to_float) * -1

    raw_data["source"] = "inter_credit_card"

    return raw_data
